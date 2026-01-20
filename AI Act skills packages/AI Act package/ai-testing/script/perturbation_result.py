from typing import List, Dict
from pydantic import BaseModel

class PerturbationResult(BaseModel):
    original_output: str
    perturbed_output: str
    perturbation_type: str
    perturbation: Dict[str, str]
    score: float
    reason: str
    success: bool


class AdversarialRobustnessScoreReason(BaseModel):
    robust_reason: str
    non_robust_reason: str
    robust_examples: List[PerturbationResult]
    non_robust_examples: List[PerturbationResult]
    score: float
