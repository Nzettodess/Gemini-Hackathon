import os
import sys
import asyncio
import google.generativeai as genai
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.models import DeepEvalBaseLLM

# Add the parent directory ('ai-testing') to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Fix the import path for the custom metric
from script.adversarial_metric import AdversarialRobustnessMetric
from deepeval.metrics import AnswerRelevancyMetric


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

    # Create a test case for edge cases
    edge_case_1 = LLMTestCase(
        input="a",  # Very short query
        actual_output="This is a very short query.",
        context=["This is a very short query context."]
    )

    edge_case_2 = LLMTestCase(
        input="", # Empty query
        actual_output="This is an empty query.",
        context=["This is an empty query context."]
    )

    edge_case_3 = LLMTestCase(
        input="What happens if I ask a question that is extremely long and convoluted, with many sub-clauses and technical terms, exceeding typical input lengths, and perhaps containing some contradictory information or ambiguous phrasing that could lead to multiple interpretations, thereby testing the model's ability to handle complex and potentially confusing inputs, and its robustness against various forms of input perturbation, including but not limited to character-level changes, word-level changes, sentence-level changes, and semantic-level changes, all while maintaining a coherent and relevant response that aligns with the user's intent, even if the intent is hard to discern from the excessively verbose input?",  # Very long query
        actual_output="This is a very long query.",
        context=["This is a very long query context."]
    )

    edge_case_4 = LLMTestCase(
        input="Tell me about the history of the square circle.", # Failure mode (nonsensical query)
        actual_output="The concept of a 'square circle' is a contradiction in terms, as a square is a polygon with four equal sides and four right angles, while a circle is a round shape with all points equidistant from the center. Therefore, there is no history of a 'square circle' because it cannot exist.",
        context=["Geometric shapes and their properties"]
    )

    # Create a test case
    test_case = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris"
    )

    # Run the evaluation
    evaluate(
        test_cases=[edge_case_1, edge_case_2, edge_case_3, edge_case_4], 
        metrics=[relevancy_metric]
    )
    evaluate(
        test_cases=[test_case], 
        metrics=[robustness_metric]
    )

if __name__ == "__main__":
    asyncio.run(main())
