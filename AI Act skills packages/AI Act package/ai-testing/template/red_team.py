from deepteam import red_team
from deepteam.vulnerabilities import Bias, PIILeakage, RecursiveHijacking, IndirectInstruction
from deepteam.attacks.single_turn import PromptInjection
from deepteam.frameworks import OWASPTop10

from deepeval.models import GeminiModel
import os
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

model = GeminiModel(
    model="gemini-2.5-flash",
    api_key=GEMINI_API_KEY,
    temperature=0,
)

async def model_callback(input: str, turns=None):
    # Call your LLM app here
    return f"I'm sorry, but I can't answer {input}"

# EU AI Act Compliance Checks

# Article 10: Data and data governance
# Recital 450: addresses the mitigation of possible biases in data sets, which are likely to have a negative impact on fundamental rights.
# This test checks for biases in the model's responses.
bias = Bias()

# Article 10: Data and data governance
# Recital 69: "The right to privacy and to protection of personal data must be guaranteed throughout the entire lifecycle of the AI system."
# This checks for potential leaks of personally identifiable information.
pii_leakage = PIILeakage()

# * Article 5 (Prohibited AI practices): Prohibits AI systems that use "purposefully
#     manipulative or deceptive techniques" to distort behavior.
# * Article 15 (Cybersecurity): Requires that high-risk AI systems "shall be resilient
#     against attempts by unauthorised third parties to alter their use, outputs or
#     performance.
recursive_hijacking = RecursiveHijacking()
indirect_instruction = IndirectInstruction()

# * Article 15 (Cybersecurity): Requires measures to prevent "attacks trying to manipulate
#     the training data set (data poisoning)."
# * Recital 76: Explicitly names "data poisoning" as a key risk.
owasp = OWASPTop10(categories=["LLM_04"])
attacks_owasp = owasp.attacks
vulnerabilities_owasp = owasp.vulnerabilities

# Recital 75: "Technical robustness is a key requirement for high-risk AI systems. They should be resilient in relation to harmful or otherwise undesirable behaviour that may result from limitations within the systems or the environment in which the systems operate (e.g. errors, faults, inconsistencies, unexpected situations)."
# Recital 494 (from previous search): Mentions data poisoning and adversarial attacks.

# This PromptInjection instance is used to simulate various attack vectors,
# including general prompt injection, adversarial attacks (inputs designed to misguide the model),
# data poisoning (attempts to make the model output harmful/biased info as if training data was compromised),
# and robustness challenges (unusual or ambiguous phrasing).
# Devising specific test cases within the 'deepteam' framework for these nuanced attacks
# will require generating prompts that target these specific scenarios.
prompt_injection_attack = PromptInjection()

red_team(
    model_callback=model_callback,
    vulnerabilities=[bias, pii_leakage, recursive_hijacking, indirect_instruction],
    attacks=[prompt_injection_attack],
    simulator_model=model, evaluation_model=model
)

red_team(
    model_callback=model_callback,
    attacks=attacks_owasp,
    vulnerabilities=vulnerabilities_owasp,
    simulator_model=model, evaluation_model=model
)
