from typing import List, Optional, Union, Dict
from pydantic import BaseModel, Field
import random
import string
import asyncio
import json

from deepeval.metrics import BaseMetric
from deepeval.models import GPTModel, DeepEvalBaseLLM
from deepeval.test_case import LLMTestCase
from .adversarial_template import AdversarialRobustnessTemplate
from deepeval.utils import get_or_create_event_loop

from .perturbation_result import PerturbationResult, AdversarialRobustnessScoreReason


class AdversarialRobustnessMetric(BaseMetric):
    def __init__(
        self,
        model: Optional[Union[str, DeepEvalBaseLLM]] = None,
        simulator_model: Optional[Union[str, DeepEvalBaseLLM]] = None,
        threshold: float = 0.5,
        n_perturbations: int = 3,
        enable_semantic_perturbation: bool = True,
        enable_orthographic_perturbation: bool = True,
        enable_format_perturbation: bool = True,
        verbose: bool = False,
    ):
        self.threshold = threshold
        # Use provided model if it's already a DeepEvalBaseLLM, otherwise wrap in GPTModel
        self.model = model if isinstance(model, DeepEvalBaseLLM) else GPTModel(model=model)
        # Use provided simulator_model if it's already a DeepEvalBaseLLM, otherwise wrap in GPTModel
        self.simulator_model = simulator_model if isinstance(simulator_model, DeepEvalBaseLLM) else GPTModel(model=simulator_model)
        self.n_perturbations = n_perturbations
        self.enable_semantic_perturbation = enable_semantic_perturbation
        self.enable_orthographic_perturbation = enable_orthographic_perturbation
        self.enable_format_perturbation = enable_format_perturbation
        self.verbose = verbose

        self.perturbation_functions = []
        if self.enable_semantic_perturbation:
            self.perturbation_functions.append(self.get_semantic_perturbation)
        if self.enable_orthographic_perturbation:
            self.perturbation_functions.append(
                self.get_orthographic_perturbation
            )
        if self.enable_format_perturbation:
            self.perturbation_functions.append(self.get_format_perturbation)
        if not self.perturbation_functions:
            raise ValueError(
                "At least one perturbation type must be enabled."
            )

    def measure(self, test_case: LLMTestCase) -> float:
        if test_case.input is None or test_case.actual_output is None:
            raise ValueError("Input and actual_output must not be None.")

        loop = get_or_create_event_loop()
        self.perturbation_results = loop.run_until_complete(
            self.a_measure(test_case, _is_async=False)
        )

        number_of_successful_perturbations = sum(
            1
            for result in self.perturbation_results
            if result.success is True
        )
        self.score = (
            number_of_successful_perturbations
            / len(self.perturbation_results)
            if self.perturbation_results
            else 0
        )
        self.reason = self._generate_reason()

        return self.score

    async def a_measure(
        self,
        test_case: LLMTestCase,
        _is_async: bool = True,
    ) -> float:
        if test_case.input is None or test_case.actual_output is None:
            raise ValueError("Input and actual_output must not be None.")

        if not self.perturbation_functions:
            raise ValueError(
                "No perturbation functions available. Please enable at least one perturbation type."
            )

        # Generate perturbations in parallel
        perturbations_list = await asyncio.gather(
            *[
                self.generate_perturbations(
                    test_case.input, self.n_perturbations
                )
                for _ in range(len(self.perturbation_functions))
            ]
        )
        all_perturbations = [
            item for sublist in perturbations_list for item in sublist
        ]

        if not all_perturbations:
            self.perturbation_results = []
            self.score = 0.0
            self.reason = "No perturbations were generated."
            return self.score

        # Get perturbed outputs in parallel
        perturbed_outputs = await asyncio.gather(
            *[
                self.model.a_generate(pert[0])
                for pert in all_perturbations
            ]
        )

        # Score perturbations in parallel
        tasks = []
        for i, (perturbed_input, metadata) in enumerate(all_perturbations):
            tasks.append(
                self.score_perturbation(
                    test_case.actual_output,
                    perturbed_outputs[i],
                    metadata["type"],
                    metadata["perturbation"],
                )
            )

        self.perturbation_results = await asyncio.gather(*tasks)

        number_of_successful_perturbations = sum(
            1
            for result in self.perturbation_results
            if result.success is True
        )
        self.score = (
            number_of_successful_perturbations
            / len(self.perturbation_results)
            if self.perturbation_results
            else 0
        )
        self.reason = await self._a_generate_reason()

        if self.verbose and _is_async:
            print(self.reason)

        return self.score

    async def generate_perturbations(
        self,
        text: str,
        n_perturbations: int,
    ) -> List[tuple[str, dict]]:
        perturbations = []
        for _ in range(n_perturbations):
            func = random.choice(self.perturbation_functions)
            if _is_async_func(func):
                perturbed_text, metadata = await func(text)
            else:
                perturbed_text, metadata = func(text)

            perturbations.append((perturbed_text, metadata))
        return perturbations

    async def _get_llm_semantic_perturbation(self, text: str) -> tuple[str, str]:
        prompt = f"""Given the text below, identify a non-stop word and provide a synonym.
A 'non-stop word' is a word that is not a common word like 'the', 'a', 'is', etc.
Return a JSON object with two keys: 'original_word' and 'synonym'.

Text: {text}
"""
        res = await self.simulator_model.a_generate(prompt)
        try:
            # Strip markdown fences and load JSON
            json_str = res.strip().replace("```json", "").replace("```", "")
            data = json.loads(json_str)
            original_word = data.get("original_word")
            synonym = data.get("synonym")
            if not all([original_word, synonym]):
                raise ValueError("Missing 'original_word' or 'synonym' in LLM response.")
            return original_word, synonym
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback or error handling
            print(f"Error parsing LLM response for semantic perturbation: {e} {res}")
            return None, None

    async def get_semantic_perturbation(
        self,
        text: str,
    ) -> tuple[str, dict]:
        original_word, synonym = await self._get_llm_semantic_perturbation(text)

        if original_word and synonym and original_word in text:
            perturbed_text = text.replace(original_word, synonym, 1)
            perturbation_details = {
                "original_word": original_word,
                "synonym": synonym,
            }
        else:
            # Fallback if no perturbation could be generated
            perturbed_text = text
            perturbation_details = {"original_word": "", "synonym": ""}

        return perturbed_text, {
            "type": "semantic",
            "perturbation": perturbation_details,
        }

    def get_orthographic_perturbation(
        self,
        text: str,
    ) -> tuple[str, dict]:
        words = text.split()
        if not words:
            return text, {
                "type": "orthographic",
                "perturbation": {
                    "original_word": "",
                    "perturbed_word": "",
                    "transformation": "none",
                },
            }

        word_index = random.randrange(len(words))
        original_word = words[word_index]

        if len(original_word) < 2:
            transformation_type = "none"
            perturbed_word = original_word
        else:
            transformation = random.choice(
                ["swap", "delete", "add", "substitute"]
            )
            if transformation == "swap":
                idx1, idx2 = random.sample(range(len(original_word)), 2)
                chars = list(original_word)
                chars[idx1], chars[idx2] = chars[idx2], chars[idx1]
                perturbed_word = "".join(chars)
                transformation_type = f"swapped characters at indices {idx1} and {idx2}"
            elif transformation == "delete":
                idx = random.randint(0, len(original_word) - 1)
                perturbed_word = (
                    original_word[:idx] + original_word[idx + 1 :]
                )
                transformation_type = f"deleted character at index {idx}"
            elif transformation == "add":
                idx = random.randint(0, len(original_word))
                char_to_add = random.choice(string.ascii_letters)
                perturbed_word = (
                    original_word[:idx]
                    + char_to_add
                    + original_word[idx:]
                )
                transformation_type = f"added '{char_to_add}' at index {idx}"
            else:  # substitute
                idx = random.randint(0, len(original_word) - 1)
                char_to_sub = random.choice(string.ascii_letters)
                perturbed_word = (
                    original_word[:idx]
                    + char_to_sub
                    + original_word[idx + 1 :]
                )
                transformation_type = f"substituted character at index {idx} with '{char_to_sub}'"
        
        words[word_index] = perturbed_word
        perturbed_text = " ".join(words)

        return perturbed_text, {
            "type": "orthographic",
            "perturbation": {
                "original_word": original_word,
                "perturbed_word": perturbed_word,
                "transformation": transformation_type,
            },
        }

    def get_format_perturbation(
        self,
        text: str,
    ) -> tuple[str, dict]:
        # Add random whitespace, newlines, or special characters
        mutation = random.choice(["whitespace", "newline", "special_char"])
        
        if mutation == "whitespace":
            words = text.split()
            if len(words) > 1:
                idx = random.randint(0, len(words) - 2)
                words.insert(idx + 1, " " * random.randint(1, 5))
                perturbed_text = " ".join(words)
                transformation = f"added extra whitespace at index {idx}"
            else:
                perturbed_text = text
                transformation = "none"

        elif mutation == "newline":
            words = text.split()
            if len(words) > 1:
                idx = random.randint(0, len(words) - 2)
                words.insert(idx + 1, "\n" * random.randint(1, 3))
                perturbed_text = " ".join(words)
                transformation = f"added newlines at index {idx}"
            else:
                perturbed_text = text
                transformation = "none"
        
        else:  # special_char
            idx = random.randint(0, len(text))
            char_to_add = random.choice("!@#$%^&*()_+-=[]{}|;':,./<>?")
            perturbed_text = text[:idx] + char_to_add + text[idx:]
            transformation = f"added '{char_to_add}' at index {idx}"

        return perturbed_text, {
            "type": "format",
            "perturbation": {
                "original_word": text,
                "perturbed_word": perturbed_text,
                "transformation": transformation,
            },
        }

    async def score_perturbation(
        self,
        original_output: str,
        perturbed_output: str,
        perturbation_type: str,
        perturbation: dict,
    ) -> PerturbationResult:
        
        prompt = AdversarialRobustnessTemplate.generate_robustness_score_prompt(
            original_output, perturbed_output
        )
        res = await self.model.a_generate(prompt)
        
        # Parse the score, handling "Score: " prefix
        score_str = AdversarialRobustnessTemplate.parse_robustness_score_output(res)
        if "score:" in score_str.lower():
            score_str = score_str.lower().split("score:")[1].strip()

        score = float(score_str)

        return PerturbationResult(
            original_output=original_output,
            perturbed_output=perturbed_output,
            perturbation_type=perturbation_type,
            perturbation=perturbation,
            score=score,
            reason="",  # Reason will be generated in bulk later
            success=score >= self.threshold,
        )

    def _generate_reason(self) -> str:
        loop = get_or_create_event_loop()
        return loop.run_until_complete(self._a_generate_reason())

    async def _a_generate_reason(self) -> str:
        robust_examples = [
            p for p in self.perturbation_results if p.success
        ]
        non_robust_examples = [
            p for p in self.perturbation_results if not p.success
        ]

        # Generate reasons for a few examples in parallel
        robust_reasons_tasks = [
            self._a_generate_perturbation_reason(p, is_robust=True)
            for p in robust_examples[:2]
        ]
        non_robust_reasons_tasks = [
            self._a_generate_perturbation_reason(p, is_robust=False)
            for p in non_robust_examples[:2]
        ]

        robust_reasons = await asyncio.gather(*robust_reasons_tasks)
        non_robust_reasons = await asyncio.gather(*non_robust_reasons_tasks)

        for i, reason in enumerate(robust_reasons):
            robust_examples[i].reason = reason
        for i, reason in enumerate(non_robust_reasons):
            non_robust_examples[i].reason = reason

        prompt = AdversarialRobustnessTemplate.generate_final_reason_prompt(
            self.score,
            len(robust_examples),
            len(non_robust_examples),
            robust_examples,
            non_robust_examples,
        )

        res = await self.model.a_generate(prompt)
        return res

    async def _a_generate_perturbation_reason(
        self,
        perturbation_result: PerturbationResult,
        is_robust: bool,
    ) -> str:
        prompt = (
            AdversarialRobustnessTemplate.generate_perturbation_reason_prompt(
                perturbation_result, is_robust
            )
        )
        return await self.model.a_generate(prompt)
    
    def is_successful(self) -> bool:
        return self.score >= self.threshold

    @property
    def __name__(self):
        return "Adversarial Robustness"


def _is_async_func(func):
    return asyncio.iscoroutinefunction(func)
