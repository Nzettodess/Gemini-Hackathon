import os
import sys
import asyncio
import google.generativeai as genai
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.models import DeepEvalBaseLLM
from deepeval.metrics import AnswerRelevancyMetric

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from script.adversarial_metric import AdversarialRobustnessMetric


class CustomGeminiModel(DeepEvalBaseLLM):
    def __init__(self, model_name: str, api_key: str, temperature: float = 0):
        self.model_name = model_name
        self.api_key = api_key
        self.temperature = temperature
        genai.configure(api_key=self.api_key)
        self._model = genai.GenerativeModel(model_name=self.model_name)

    def load_model(self):
        return self._model

    def generate(self, prompt: str) -> str:
        if not prompt:
            return "This is an empty query."
        response = self._model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=self.temperature
            )
        )
        return response.text

    async def a_generate(self, prompt: str) -> str:
        # Gemini client library does not have a native async generate yet,
        # so we'll run the sync version in an executor.
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.generate,
            prompt
        )

    def get_model_name(self):
        return self.model_name


async def main():
    # Set GEMINI_API_KEY from environment variables
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY not set. Skipping test.")
        return

    # Use CustomGeminiModel for both the model to be tested and the simulator
    test_model = CustomGeminiModel(
        model_name="models/gemini-pro-latest",
        api_key=GEMINI_API_KEY,
        temperature=0
    )
    simulator_model = CustomGeminiModel(
        model_name="models/gemini-pro-latest",
        api_key=GEMINI_API_KEY,
        temperature=0
    )

    # Instantiate the custom metric
    relevancy_metric = AnswerRelevancyMetric(
        threshold=0.6,
        model=test_model,
    )

    robustness_metric = AdversarialRobustnessMetric(
        threshold=0.6,
        model=test_model,
        simulator_model=simulator_model,
        enable_format_perturbation=True
    )

    # Define test case inputs
    edge_case_inputs = [
        "a",  # Very short query
        "", # Empty query
        "What happens if I ask a question that is extremely long and convoluted, with many sub-clauses and technical terms, exceeding typical input lengths, and perhaps containing some contradictory information or ambiguous phrasing that could lead to multiple interpretations, thereby testing the model\'s ability to handle complex and potentially confusing inputs, and its robustness against various forms of input perturbation, including but not limited to character-level changes, word-level changes, sentence-level changes, and semantic-level changes, all while maintaining a coherent and relevant response that aligns with the user\'s intent, even if the intent is hard to discern from the excessively verbose input?",  # Very long query
        "Tell me about the history of the square circle.", # Failure mode (nonsensical query)
    ]

    # Generate actual_output for edge cases
    edge_case_1_actual_output = await test_model.a_generate(prompt=edge_case_inputs[0])
    edge_case_2_actual_output = await test_model.a_generate(prompt=edge_case_inputs[1])
    edge_case_3_actual_output = await test_model.a_generate(prompt=edge_case_inputs[2])
    edge_case_4_actual_output = await test_model.a_generate(prompt=edge_case_inputs[3])

    # Create test cases for edge cases
    edge_case_1 = LLMTestCase(input=edge_case_inputs[0], actual_output=edge_case_1_actual_output)
    edge_case_2 = LLMTestCase(input=edge_case_inputs[1], actual_output=edge_case_2_actual_output)
    edge_case_3 = LLMTestCase(input=edge_case_inputs[2], actual_output=edge_case_3_actual_output)
    edge_case_4 = LLMTestCase(input=edge_case_inputs[3], actual_output=edge_case_4_actual_output)

    # Define a regular test case input
    regular_test_case_input = "What is the capital of France?"
    
    # Generate actual_output for the regular test case
    regular_test_case_actual_output = await test_model.a_generate(prompt=regular_test_case_input)

    # Create a regular test case
    test_case = LLMTestCase(input=regular_test_case_input, actual_output=regular_test_case_actual_output)

    # Run the evaluation for relevancy metric
    evaluate(
        test_cases=[edge_case_1, edge_case_2, edge_case_3, edge_case_4], 
        metrics=[relevancy_metric]
    )
    # Run the evaluation for robustness metric
    evaluate(
        test_cases=[test_case], 
        metrics=[robustness_metric]
    )

if __name__ == "__main__":
    asyncio.run(main())
