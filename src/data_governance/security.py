
import re
from typing import Dict, Any, List

class SecurityScanner:
    def __init__(self):
        # Heuristic patterns for common injection attacks
        self.injection_patterns = [
            (r"ignore previous instructions", "Prompt Injection (Instruction Override)"),
            (r"ignore all prior instructions", "Prompt Injection (Instruction Override)"),
            (r"delete all files", "Malicious Action (System Command)"),
            (r"drop table", "SQL Injection Attempt"),
            (r"system prompt", "System Prompt Leakage Attempt"),
            (r"your core directives", "System Prompt Leakage Attempt"),
            (r"DAN mode", "Jailbreak (DAN Mode)"),
            (r"do anything now", "Jailbreak (DAN Mode)"),
            (r"act as a", "Persona Adoption (Potential Jailbreak)"),
        ]

    def scan_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Scans a prompt for potential security risks using heuristic analysis.
        In a real industrial setting, this would call a model like Llama Guard or Rebuff.
        """
        detected_risks = []
        
        for pattern, risk_type in self.injection_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                detected_risks.append({
                    "type": risk_type,
                    "pattern_matched": pattern,
                    "severity": "HIGH"
                })
        
        # Check for length anomalies (buffer overflow attempts in older systems, or DoS)
        if len(prompt) > 10000:
            detected_risks.append({
                "type": "Denial of Service (DoS)",
                "details": "Prompt length exceeds safety threshold (10k chars)",
                "severity": "MEDIUM"
            })

        return {
            "safe": len(detected_risks) == 0,
            "risk_score": len(detected_risks) * 10,  # Simple scoring
            "detected_risks": detected_risks
        }

def scan_prompt_for_risk(prompt: str) -> Dict[str, Any]:
    scanner = SecurityScanner()
    return scanner.scan_prompt(prompt)
