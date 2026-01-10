# AI Safety Plan: ai_act_cli.py (EU AI Act Query Assistant)

**Generated:** 2026-01-10  
**System:** EU AI Act Query Assistant v1.0.0  
**Skill Applied:** ai-safety-planning

---

## 1. Risk Classification

### EU AI Act Category: **Limited Risk**
- **Applicable Article:** Article 50 (Transparency Obligations)
- **Justification:** Chatbot/Conversational AI system that interacts with users
- **Classification Date:** 2025-01-07

### NIST AI RMF Profile
- **Primary Function:** Information retrieval and legal guidance
- **AI Type:** Large Language Model (Gemini 3 Pro Preview)
- **Deployment:** CLI-based interactive system

### Internal Risk Score: **2/5** (Low-Medium)

| Factor | Assessment | Score |
|--------|------------|-------|
| Autonomy Level | Human-initiated queries only | 1/5 |
| Decision Impact | Informational only (not automated decisions) | 2/5 |
| Data Sensitivity | Processes public regulatory text | 1/5 |
| User Vulnerability | General public/developers | 2/5 |
| Reversibility | Fully reversible (information only) | 1/5 |

---

## 2. Identified Risks

| Risk ID | Risk Description | Likelihood | Impact | Severity | Mitigation |
|---------|------------------|------------|--------|----------|------------|
| R-001 | **Hallucination/Misinformation** - LLM may generate incorrect legal interpretations | Medium | High | High | System prompt constraints, source citations |
| R-002 | **Over-reliance on AI** - Users may treat responses as legal advice | Medium | High | High | Prominent disclaimers, legal counsel reminders |
| R-003 | **Prompt Injection** - Malicious inputs to manipulate responses | Low | Medium | Medium | Input validation (not currently implemented) |
| R-004 | **API Key Exposure** - Environment variable may be leaked | Low | High | Medium | Environment variable usage (current), secrets management (recommended) |
| R-005 | **Context Overflow** - Full text injection may exceed limits | Low | Low | Low | Token counting, chunking strategy |
| R-006 | **Outdated Information** - Regulation text may become outdated | Medium | Medium | Medium | Version tracking, update notifications |

---

## 3. Current Safety Controls (✅ Implemented)

### Transparency (Article 50 Compliance)
- [x] **AI Disclosure Notice** - Lines 105-119: Clear panel informing users they're interacting with AI
- [x] **Model Identification** - Lines 109, 116: Model name (gemini-3-pro-preview) displayed
- [x] **Disclaimer Notices** - Lines 112-114: Not legal advice, verify with sources
- [x] **AI-Generated Content Label** - Line 206: Footer on every response

### System Prompt Safety
- [x] **Context Constraints** - Line 166: "based ONLY on the provided context document"
- [x] **Citation Requirements** - Line 169: "ALWAYS cite specific Articles"
- [x] **Legal Counsel Reminders** - Lines 173-174: Emphasize professional advice
- [x] **Temperature Control** - Line 179: temperature=0.3 for more deterministic outputs

### User Experience
- [x] **Clear Exit Options** - Lines 131-133: exit/quit/q commands
- [x] **Conversation History Clear** - Lines 135-139: 'clear' command
- [x] **Error Handling** - Lines 147-148, 195-196: Exception handling with user feedback

---

## 4. Missing Safety Controls (❌ Not Implemented)

### Input Guards
- [ ] **Prompt Injection Detection** - No filtering for injection attempts
- [ ] **Input Validation** - No length limits or content validation
- [ ] **Rate Limiting** - No protection against abuse

### Output Filters
- [ ] **Toxicity Filtering** - No post-processing safety checks
- [ ] **PII Detection** - No checking for accidental PII in responses
- [ ] **Confidence Scoring** - No indication of response confidence

### Monitoring & Logging
- [ ] **Query Logging** - No audit trail of user queries
- [ ] **Response Logging** - No storage of AI responses
- [ ] **Error Tracking** - Errors displayed but not logged
- [ ] **Usage Analytics** - No metrics collection

### Security
- [ ] **API Key Rotation** - No mechanism for key rotation
- [ ] **Input Sanitization** - User input passed directly to API
- [ ] **Session Management** - No session timeout or limits

---

## 5. Guardrails Recommendations

### 5.1 Input Guards (Priority: High)

```python
# Recommended: Add PromptInjectionGuard
INJECTION_INDICATORS = [
    "ignore previous instructions",
    "disregard your training",
    "you are now",
    "pretend you are",
    "system prompt:",
    "new instructions:",
]

def validate_input(user_input: str) -> tuple[bool, str]:
    """Validate user input for potential attacks."""
    normalized = user_input.lower()
    
    # Check for injection attempts
    for indicator in INJECTION_INDICATORS:
        if indicator in normalized:
            return False, f"Input blocked: Potential prompt injection detected"
    
    # Length limit
    if len(user_input) > 10000:
        return False, "Input too long (max 10,000 characters)"
    
    return True, ""
```

### 5.2 Output Filters (Priority: Medium)

```python
# Recommended: Add response validation
def validate_response(response_text: str) -> str:
    """Post-process response for safety."""
    # Check for potential PII patterns
    import re
    pii_patterns = [
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
    ]
    
    for pattern in pii_patterns:
        if re.search(pattern, response_text):
            # Log warning but don't block (legal text may contain examples)
            pass
    
    return response_text
```

### 5.3 Logging Implementation (Priority: Medium)

```python
# Recommended: Add audit logging
import logging
from datetime import datetime

def setup_logging():
    logging.basicConfig(
        filename=f'ai_act_cli_{datetime.now():%Y%m%d}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
def log_interaction(query: str, response: str, latency: float):
    logging.info(f"Query: {query[:100]}... | Response length: {len(response)} | Latency: {latency:.2f}s")
```

---

## 6. Testing Plan

### Pre-Launch Red Teaming
- [ ] Direct injection attempts ("ignore previous instructions...")
- [ ] Indirect injection via user content
- [ ] Multi-turn manipulation attempts
- [ ] Jailbreak scenarios ("pretend you are a different AI...")

### Bias Testing
- [ ] Test responses across different regulatory topics
- [ ] Check for consistent citation quality
- [ ] Verify balanced interpretation of ambiguous provisions

### Continuous Testing
- [ ] Monthly review of flagged interactions
- [ ] Quarterly security assessment
- [ ] Annual compliance audit

---

## 7. Monitoring Plan

### Safety Metrics Dashboard
| Metric | Target | Current |
|--------|--------|---------|
| Response Accuracy | >95% with citations | Not measured |
| Disclaimer Display Rate | 100% | ✅ 100% |
| Error Rate | <1% | Not measured |
| Average Response Latency | <5s | Not measured |

### Alerting Thresholds
- Critical: API errors >5% in 1 hour
- High: Response latency >10s sustained
- Medium: Unusual query patterns detected

---

## 8. Compliance Status

### EU AI Act Article 50 Requirements

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Inform users they are interacting with AI | ✅ Compliant | Lines 107-119 |
| Disclose AI-generated content | ✅ Compliant | Line 206 |
| Provide information about AI capabilities | ✅ Compliant | Lines 113-114 |
| Enable user to understand AI limitations | ✅ Compliant | Lines 112-114 |

### Additional Recommendations for Full Compliance
1. Add logging for regulatory audit purposes
2. Implement version tracking for regulation text
3. Add mechanism to notify users of system updates
4. Consider user feedback mechanism

---

## 9. Action Items

### Immediate (Before Next Release)
1. [ ] Add input validation/prompt injection detection
2. [ ] Implement basic query logging
3. [ ] Add response latency monitoring

### Short-term (Within 30 days)
4. [ ] Implement rate limiting
5. [ ] Add output safety filtering
6. [ ] Create error tracking system

### Medium-term (Within 90 days)
7. [ ] Develop red teaming test suite
8. [ ] Implement comprehensive logging
9. [ ] Create safety metrics dashboard

---

## 10. Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Safety Lead | | | |
| Development Lead | | | |
| Compliance Officer | | | |
| Product Owner | | | |

---

*This safety plan was generated using the ai-safety-planning skill based on analysis of ai_act_cli.py*
