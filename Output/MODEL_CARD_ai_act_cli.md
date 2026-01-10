# Model Card: EU AI Act Query Assistant

**System Version:** 1.0.0
**Date:** 2025-01-07
**Model:** Google Gemini-3-pro-preview
**License:** Proprietary
**EU AI Act Classification:** Limited Risk (Article 50 - Chatbot)

---

## Model Details

### Basic Information

| Attribute | Value |
|-----------|-------|
| **System Name** | EU AI Act Query Assistant |
| **Version** | 1.0.0 |
| **System Type** | Conversational AI / Chatbot |
| **Primary Function** | Legal research assistant for EU AI Act and GDPR |
| **Model** | Google Gemini-3-pro-preview |
| **Framework** | Google GenAI SDK |
| **Interface** | Command-line interface (CLI) |
| **Programming Language** | Python 3.x |
| **Release Date** | 2025-01-07 |

### Developers

**Provider:** [Your Organization]
**Development Team:** [Team name]
**Contact:** [Email address]

### Purpose

This system provides an AI-powered conversational interface to query the EU AI Act (Regulation 2024/1689) and GDPR regulations. It uses Google's Gemini large language model with long context capabilities to analyze the full text of the regulations and provide cited answers to user questions.

---

## Intended Use

### Primary Use Cases

**Intended Users:**
- Legal professionals researching EU AI Act requirements
- Compliance officers assessing AI system requirements
- Developers understanding AI regulations
- Business analysts evaluating regulatory implications
- Students and researchers studying AI law

**Primary Applications:**
1. **Compliance Research:** Understanding specific articles and requirements
2. **Risk Assessment Support:** Researching risk classifications and obligations
3. **Educational Use:** Learning about EU AI Act provisions
4. **Quick Reference:** Looking up specific regulatory definitions and requirements

**Geographic Scope:** European Union (EU AI Act focus) + Global (GDPR focus)

**Deployment Context:** Desktop/terminal environment, individual user research

### Out-of-Scope Uses

**This system should NOT be used for:**

❌ **Providing Legal Advice** - Not a substitute for qualified legal counsel
❌ **Making Compliance Decisions** - Decisions require human legal expertise
❌ **Formal Legal Proceedings** - Not appropriate for court or official submissions
❌ **Automated Compliance Assessment** - Cannot replace comprehensive assessment
❌ **Regulatory Filings** - Should not generate official regulatory documents
❌ **Sole Source of Truth** - Must be verified against official regulation text

**Important Limitations:**
- Responses are AI-generated and may contain errors
- Interpretations should be verified with legal counsel
- Not updated in real-time with regulatory changes
- Cannot account for jurisdiction-specific interpretations
- Does not replace reading official regulation text

---

## System Architecture

### Technical Components

**Core Components:**
1. **Input Interface:** Rich console-based CLI
2. **Query Processing:** Natural language understanding via Gemini
3. **Context Retrieval:** Full-text injection of EU AI Act and GDPR
4. **Response Generation:** Gemini-3-pro-preview with long context window
5. **Output Formatting:** Markdown rendering with Rich library

**Data Flow:**
```
User Query → Gemini (with full regulation text in context) → AI Response → Rich Formatting → User
```

**Processing Approach:**
- **Long Context RAG:** Entire regulation text (~500k+ characters) injected into model context
- **Temperature:** 0.3 (conservative, factual responses)
- **Citation Enforcement:** System prompt requires article citations
- **Conversation Memory:** Maintains chat history within session

---

## Training Data

### Source Documents

**Primary Knowledge Sources:**
1. **EU AI Act Full Text** (Regulation (EU) 2024/1689)
   - Source: Official EU regulation
   - Loaded at runtime from `EU_AI_Act_Full_Text.txt`
   - Comprehensive coverage of all articles and annexes

2. **GDPR Text** (Regulation (EU) 2016/679)
   - Source: Official EU regulation
   - Loaded from `GDPR_Full_Text.txt`
   - Referenced for data protection questions

### Model Training

**Note:** This system uses Google's Gemini-3-pro-preview model, which was trained by Google. The system itself does not perform training; it uses the pre-trained model for inference only.

**Google Gemini:**
- Pre-trained large language model
- Long context window capability (handles 500k+ characters)
- General purpose language understanding and generation

**System-Specific Configuration:**
- Temperature: 0.3 (prioritizes accuracy over creativity)
- System prompt: Instructs model to cite articles and be precise
- Context injection: Full regulation text provided in each query

---

## Performance and Limitations

### Capabilities

**What the system CAN do:**
- ✅ Answer questions about EU AI Act provisions
- ✅ Cite specific articles and paragraphs
- ✅ Explain regulatory requirements and definitions
- ✅ Compare different articles or provisions
- ✅ Provide structured summaries of requirements
- ✅ Answer GDPR-related questions
- ✅ Maintain conversation context for follow-up questions

**Accuracy Characteristics:**
- Responses based on official regulation text
- Article citations enforced via system prompt
- Conservative temperature setting for factual accuracy
- Long context window reduces information retrieval errors

### Known Limitations

**What the system CANNOT do:**
- ❌ Provide legal opinions or advice
- ❌ Guarantee 100% accuracy (AI-generated responses)
- ❌ Account for implementing acts or delegated acts not in training data
- ❌ Provide jurisdiction-specific interpretations
- ❌ Stay automatically updated with regulation changes
- ❌ Replace comprehensive legal analysis
- ❌ Access external resources or case law

**Technical Limitations:**
- Responses limited by model's context window
- May occasionally misinterpret complex legal language
- Cannot verify against most recent regulatory updates
- No real-time access to amendments or guidance documents

**Reliability Factors:**
- **Strengths:** Full regulation text in context, citation requirements, conservative temperature
- **Weaknesses:** AI hallucination risk, no external verification, static knowledge base

---

## Ethical Considerations

### Transparency

**AI Disclosure:** ✅ COMPLIANT with EU AI Act Article 50
- Clear disclosure at startup that system uses AI
- Every response labeled as AI-generated
- Model information provided (Gemini-3-pro-preview)
- Version and classification information accessible

**Disclaimers:**
- Not legal advice disclaimer prominently displayed
- Verification reminder on every response
- Encourages consultation with legal counsel

### Risks and Mitigations

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Over-Reliance** | Users may trust AI responses without verification | Prominent disclaimers, verification reminders |
| **Inaccurate Advice** | AI may generate incorrect interpretations | "Not legal advice" notice, encourage legal counsel |
| **Outdated Information** | Regulations may change | Display classification date, recommend verification |
| **Misinterpretation** | Complex legal language may be misunderstood | Conservative temperature, citation requirements |
| **Unauthorized Use** | Use in formal legal proceedings | Clear out-of-scope warnings in documentation |

### Privacy Considerations

**Data Processing:**
- User queries processed by Google Gemini API
- No persistent storage of user queries (beyond session)
- Regulation text loaded from local files (no external requests for content)
- No personal data collected or stored by system

**User Privacy:**
- Users should avoid including sensitive information in queries
- System does not require user authentication or identification
- No telemetry or usage tracking implemented
- API key hardcoded (development use; should use environment variable in production)

**GDPR Compliance:**
- Minimal data processing (queries sent to API, not stored)
- No personal data collection by the system itself
- Users responsible for avoiding PII in queries

---

## Regulatory Compliance

### EU AI Act Compliance

**Classification:** Limited Risk AI System

**Applicable Requirements:**
- ✅ **Article 50(1):** Transparency obligations for chatbots
  - Implementation: Startup disclosure panel
  - AI-generated content labels
  - Model information disclosure

**Non-Applicable Requirements:**
- ❌ High-Risk Requirements (Articles 9-15): System is not high-risk
- ❌ Prohibited Practices (Article 5): System does not engage in prohibited practices
- ❌ Conformity Assessment: Not required for limited-risk systems
- ❌ CE Marking: Not applicable
- ❌ EU Database Registration: Not required

**Compliance Documentation:**
- Risk Assessment: `ai_risk_assessment_EU_AI_Act_Query_Assistant_20250107.md`
- Compliance Certificate: `EU_AI_ACT_COMPLIANCE_CERTIFICATE_ai_act_cli.md`
- This Model Card: `MODEL_CARD_ai_act_cli.md`

### GDPR Compliance

**Personal Data Processing:** Minimal
- System processes user queries (may incidentally contain personal data)
- No data storage beyond session
- No profiling or automated decision-making
- Users advised not to include PII in queries

**Legal Basis:** Legitimate interest (providing information tool)

**User Rights:** Not applicable (no persistent data storage)

---

## Usage Recommendations

### Best Practices

**For Users:**
1. **Verify All Responses:** Cross-check AI responses against official regulation text
2. **Consult Legal Counsel:** For compliance decisions, engage qualified lawyers
3. **Use as Research Tool:** Treat as starting point, not final authority
4. **Check Date:** Ensure regulation version is current (check classification date)
5. **Avoid PII:** Do not include personal data in queries

**For Organizations:**
1. **Training:** Ensure users understand system limitations
2. **Disclaimers:** Reinforce that responses are not legal advice
3. **Verification:** Require human review of AI-generated information
4. **Updates:** Monitor for regulation changes and update knowledge base
5. **API Security:** Use environment variables for API keys (not hardcoded)

### Deployment Recommendations

**Production Deployment Considerations:**
- [ ] Move API key to environment variable
- [ ] Implement usage logging (with privacy safeguards)
- [ ] Add rate limiting for API calls
- [ ] Regular updates to regulation text
- [ ] Monitor for Google Gemini API changes
- [ ] Consider caching for common queries
- [ ] Add error handling for API failures

**Human Oversight:**
- System designed for human-in-command use
- All outputs reviewed by user before use
- No automated actions based on responses
- Users retain full decision-making authority

---

## Maintenance and Updates

### Update Schedule

| Component | Update Frequency | Responsibility |
|-----------|------------------|----------------|
| Regulation Text | Quarterly or upon changes | Content maintainer |
| System Code | As needed for bugs/features | Developer |
| Compliance Documentation | Annually or upon material changes | Compliance officer |
| Risk Classification | Upon material changes | Compliance officer |
| Dependencies | Monthly (security patches) | Developer |

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-07 | Initial release with EU AI Act Article 50 compliance |

### Monitoring

**System Monitoring:**
- User feedback collection (manual)
- Error rate tracking (if implemented)
- API response time monitoring (if implemented)

**Regulatory Monitoring:**
- Watch for EU AI Act implementing acts
- Monitor Article 50 guidance from EU AI Office
- Track case law and enforcement actions
- Review harmonized standards when published

**Performance Monitoring:**
- No automated metrics (simple CLI tool)
- Recommended: Collect user feedback on accuracy
- Recommended: Track common query patterns

---

## Technical Specifications

### Requirements

**System Requirements:**
- Python 3.7+
- `google-genai` package
- `rich` package for console formatting
- Internet connection (for Gemini API)
- Terminal/command-line interface

**Dependencies:**
```
google-genai
rich
pathlib (built-in)
```

**Environment:**
- Operating System: Cross-platform (Windows, macOS, Linux)
- Terminal: Any terminal supporting Rich library
- Network: HTTPS access to Google APIs

### Configuration

**Key Settings:**
- `MODEL_NAME`: "gemini-3-pro-preview"
- `TEMPERATURE`: 0.3
- `VERSION`: "1.0.0"
- `EU_AI_ACT_RISK_LEVEL`: "Limited Risk"

**File Paths:**
- `EU_AI_Act_Full_Text.txt`: Full regulation text
- `GDPR_Full_Text.txt`: GDPR regulation text
- `articles/`: Directory containing individual article files

---

## Contact and Support

### Primary Contact

**System Owner:** [Name, Email]
**Technical Support:** [Name, Email]
**Compliance Questions:** [Name, Email]

### Feedback

**How to Provide Feedback:**
- Email: [feedback@example.com]
- Issues: [GitHub/GitLab repository if applicable]

**What to Report:**
- Inaccurate responses (with query and response)
- Technical bugs or errors
- Compliance concerns
- Suggestions for improvements

---

## Acknowledgments

**Data Sources:**
- EU AI Act (Regulation (EU) 2024/1689) - European Union
- GDPR (Regulation (EU) 2016/679) - European Union

**Technologies:**
- Google Gemini AI - Google LLC
- Rich library - Will McGugan
- Python - Python Software Foundation

---

## Appendix: Sample Queries

### Example Queries

**Good Queries:**
- "What are the prohibited AI practices under Article 5?"
- "Explain the requirements for high-risk AI systems"
- "What is the definition of 'AI system' in the EU AI Act?"
- "What are the transparency obligations under Article 50?"

**Queries to Avoid:**
- "Is my specific AI system compliant?" (requires legal assessment)
- "What should I do to comply?" (requires legal advice)
- "Can I use facial recognition in my workplace?" (legal advice needed)

---

**Model Card Version:** 1.0
**Last Updated:** 2025-01-07
**Based on:** Model Cards for Model Reporting (Mitchell et al., 2019) + EU AI Act Requirements

**Note:** This model card is a living document and should be updated when the system or its regulatory environment changes.

---

✅ **EU AI Act Article 50 Compliant**
⚖️ **Not Legal Advice - Consult Qualified Counsel**
🔄 **Verify All AI-Generated Responses**
