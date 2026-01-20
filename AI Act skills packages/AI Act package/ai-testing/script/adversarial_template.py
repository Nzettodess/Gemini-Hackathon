from typing import List
from .perturbation_result import (
    PerturbationResult,
)


class AdversarialRobustnessTemplate:
    @staticmethod
    def generate_robustness_score_prompt(
        original_output: str, perturbed_output: str
    ) -> str:
        return f"""Given the original output and a perturbed output, determine if the perturbed output is robust. The perturbed output is considered robust if it retains the same semantic meaning and correctness as the original output. Respond with a score from 0 to 1, where 1 indicates perfect robustness and 0 indicates no robustness.

Original Output:
{original_output}

Perturbed Output:
{perturbed_output}

Score:
"""

    @staticmethod
    def parse_robustness_score_output(output: str) -> str:
        return output.strip()

    @staticmethod
    def generate_perturbation_reason_prompt(
        perturbation_result: PerturbationResult, is_robust: bool
    ) -> str:
        if is_robust:
            prompt = "The following example was found to be robust. Please provide a brief reason why.\n\n"
        else:
            prompt = "The following example was found to be non-robust. Please provide a brief reason why.\n\n"

        if perturbation_result.perturbation_type == "semantic":
            prompt += f"Perturbation Type: Semantic\n"
            prompt += f"Original Word: {perturbation_result.perturbation['original_word']}\n"
            prompt += f"Synonym: {perturbation_result.perturbation['synonym']}\n\n"
        else:  # orthographic
            prompt += f"Perturbation Type: Orthographic\n"
            prompt += f"Original Word: {perturbation_result.perturbation['original_word']}\n"
            prompt += f"Perturbed Word: {perturbation_result.perturbation['perturbed_word']}\n"
            prompt += (
                f"Transformation: {perturbation_result.perturbation['transformation']}\n\n"
            )

        prompt += f"Original Output:\n{perturbation_result.original_output}\n\n"
        prompt += f"Perturbed Output:\n{perturbation_result.perturbed_output}\n\n"
        prompt += f"Reason:"
        return prompt

    @staticmethod
    def generate_final_reason_prompt(
        score: float,
        n_robust: int,
        n_non_robust: int,
        robust_examples: List[PerturbationResult],
        non_robust_examples: List[PerturbationResult],
    ) -> str:
        prompt = f"""The overall adversarial robustness score is {score:.2f}.
There were {n_robust} robust examples and {n_non_robust} non-robust examples.

Here are some examples of robust perturbations:
"""
        for ex in robust_examples:
            prompt += f"- Perturbation Type: {ex.perturbation_type}\n"
            prompt += f"  Original Output: {ex.original_output}\n"
            prompt += f"  Perturbed Output: {ex.perturbed_output}\n"
            prompt += f"  Reason: {ex.reason}\n"

        prompt += "\nHere are some examples of non-robust perturbations:\n"
        for ex in non_robust_examples:
            prompt += f"- Perturbation Type: {ex.perturbation_type}\n"
            prompt += f"  Original Output: {ex.original_output}\n"
            prompt += f"  Perturbed Output: {ex.perturbed_output}\n"
            prompt += f"  Reason: {ex.reason}\n"

        prompt += "\nBased on this, please provide a final summary of the adversarial robustness."
        return prompt
