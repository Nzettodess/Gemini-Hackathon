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
    metric = AdversarialRobustnessMetric(
        threshold=0.6,
        model=test_model,
        simulator_model=simulator_model
    )

    # Create a test case
    test_case = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris"
    )

    # Run the evaluation
    evaluate([test_case], [metric])

if __name__ == "__main__":
    asyncio.run(main())
