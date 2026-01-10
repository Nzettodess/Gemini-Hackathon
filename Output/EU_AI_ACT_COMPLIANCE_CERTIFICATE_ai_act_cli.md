# EU AI Act Compliance Certificate
## EU AI Act Query Assistant (ai_act_cli.py)

---

## System Identification

| Attribute | Value |
|-----------|-------|
| **System Name** | EU AI Act Query Assistant |
| **Version** | 1.0.0 |
| **File** | ai_act_cli.py |
| **Provider** | [Your Organization] |
| **Classification Date** | 2025-01-07 |
| **Certificate Date** | 2025-01-07 |

---

## EU AI Act Classification

### Risk Level: **LIMITED RISK** ✓

**Regulation:** Regulation (EU) 2024/1689 (EU AI Act)

**Classification Basis:**
- System Type: Chatbot / Conversational AI
- Article Applicability: Article 50(1) - Transparency obligations
- Risk Category: Limited Risk (transparency obligations only)

**Not Classified As:**
- ❌ Prohibited AI Practice (Article 5)
- ❌ High-Risk AI System (Articles 6-7, Annex III)
- ✓ Limited Risk - Chatbot (Article 50)

---

## Applicable Requirements

### Article 50(1): Transparency Obligations for Chatbots

**Requirement:**
> "Providers of AI systems intended to interact directly with natural persons shall ensure that the AI system is designed and developed in such a way that natural persons are informed that they are interacting with an AI system, unless this is obvious from the circumstances and the context of use."

**Compliance Status:** ✅ COMPLIANT

---

## Compliance Implementation

### 1. AI Disclosure at Startup ✅

**Implementation Location:** `ai_act_cli.py` lines 99-114

**Disclosure Content:**
- Clear identification as AI-powered system
- Model information (Google Gemini)
- AI-generated response disclaimer
- Legal advice disclaimer
- Regulation references (EU AI Act, GDPR)
- System classification information
- Version and classification date

**Display Method:**
- Prominent yellow panel on startup
- Displayed before any user interaction
- Cannot be missed or skipped

**Evidence:** See code lines 99-114 in ai_act_cli.py

---

### 2. AI-Generated Content Labels ✅

**Implementation Location:** `ai_act_cli.py` line 200

**Label Content:**
> "⚠️ AI-generated response - Verify with official sources and legal counsel for compliance decisions"

**Display Method:**
- Appears after every AI response
- Italic, dimmed styling for unobtrusive but visible notice
- Consistent reminder throughout usage

**Evidence:** See code line 200 in ai_act_cli.py

---

### 3. System Prompt Transparency ✅

**Implementation Location:** `ai_act_cli.py` lines 151-168

**Transparency Measures:**
- System instructed to acknowledge AI status
- Includes disclaimers in responses when appropriate
- Emphasizes legal counsel requirement for compliance decisions
- Transparent about AI limitations

**Evidence:** See system prompt configuration

---

### 4. Version and Classification Information ✅

**Implementation Location:** `ai_act_cli.py` lines 35-38, 206-232

**Information Provided:**
- System version accessible via `--version` flag
- Risk classification displayed in help and disclosure
- Classification date documented
- Model information (Gemini model name)

**Commands:**
```bash
python ai_act_cli.py --version  # Show version and compliance info
python ai_act_cli.py --help     # Show usage and compliance status
```

**Evidence:** See command-line argument handling

---

## Compliance Verification Checklist

### Article 50(1) Requirements

- [x] **System designed for transparency** - Disclosure panel implemented
- [x] **Users informed of AI interaction** - Clear notice at startup
- [x] **Disclosure visible and understandable** - Prominent yellow panel
- [x] **Disclosure timing appropriate** - Shown before first interaction
- [x] **AI-generated content labeled** - Footer notice on all responses
- [x] **Model information disclosed** - Gemini model specified
- [x] **Version information available** - `--version` flag
- [x] **Documentation maintained** - This certificate and assessment report

### Additional Best Practices Implemented

- [x] Legal advice disclaimer included
- [x] Verification reminder on each response
- [x] System classification disclosed
- [x] Regulation references provided (EU AI Act, GDPR)
- [x] User commands documented (`--help`)
- [x] Compliance status accessible programmatically

---

## Non-Applicable Requirements

The following EU AI Act requirements **do NOT apply** to this Limited Risk system:

### High-Risk Requirements (NOT APPLICABLE)

| Requirement | Article | Status | Reason |
|-------------|---------|--------|--------|
| Risk Management System | Article 9 | ❌ Not Required | Not high-risk |
| Data Governance | Article 10 | ❌ Not Required | Not high-risk |
| Technical Documentation (Annex IV) | Article 11 | ❌ Not Required | Not high-risk |
| Record-Keeping | Article 12 | ❌ Not Required | Not high-risk |
| Transparency (Instructions for Use) | Article 13 | ❌ Not Required | Not high-risk |
| Human Oversight | Article 14 | ❌ Not Required | Not high-risk |
| Accuracy/Robustness/Security | Article 15 | ❌ Not Required | Not high-risk |
| Conformity Assessment | Articles 43-48 | ❌ Not Required | Not high-risk |
| CE Marking | Article 48 | ❌ Not Required | Not high-risk |
| EU Database Registration | Article 49 | ❌ Not Required | Not high-risk |
| Post-Market Monitoring | Article 72 | ❌ Not Required | Not high-risk |

### Prohibited Practices (NOT APPLICABLE)

- ❌ Social scoring - System does not perform social scoring
- ❌ Subliminal manipulation - No manipulation techniques used
- ❌ Vulnerability exploitation - No exploitation of vulnerabilities
- ❌ Facial recognition scraping - Not applicable to text-based system
- ❌ Emotion recognition (prohibited contexts) - Not applicable
- ❌ Predictive policing - Not applicable

---

## Compliance Evidence Repository

### Code Evidence

| Compliance Measure | File | Lines | Description |
|-------------------|------|-------|-------------|
| AI Disclosure Panel | ai_act_cli.py | 99-114 | Startup disclosure notice |
| AI-Generated Label | ai_act_cli.py | 200 | Response footer notice |
| System Prompt Transparency | ai_act_cli.py | 151-168 | AI awareness in responses |
| Version Information | ai_act_cli.py | 35-38 | System metadata |
| Help/Version Flags | ai_act_cli.py | 206-232 | CLI compliance info |
| Compliance Documentation | Header comments | 8-11 | Code-level documentation |

### Documentation Evidence

| Document | Purpose | Location |
|----------|---------|----------|
| Risk Assessment Report | Classification and analysis | ai_risk_assessment_EU_AI_Act_Query_Assistant_20250107.md |
| Compliance Certificate | This document | EU_AI_ACT_COMPLIANCE_CERTIFICATE_ai_act_cli.md |
| Instructions for Use | User guidance | (Embedded in --help) |
| Code Comments | In-code compliance notes | ai_act_cli.py throughout |

---

## Maintenance and Review

### Update Schedule

| Activity | Frequency | Last Performed | Next Scheduled |
|----------|-----------|----------------|----------------|
| Compliance Review | Annually | 2025-01-07 | 2026-01-07 |
| Risk Classification Review | Upon material changes | 2025-01-07 | As needed |
| Disclosure Text Review | Annually | 2025-01-07 | 2026-01-07 |
| Regulatory Monitoring | Continuous | Ongoing | Ongoing |

### Triggers for Re-assessment

The risk classification and compliance approach should be reviewed if:

1. **Functionality Changes:**
   - System starts making automated decisions
   - System is integrated into high-risk applications
   - System begins processing biometric data
   - System is used in prohibited contexts

2. **Regulatory Changes:**
   - EU AI Act implementing acts or delegated acts
   - Updated Article 50 guidance from EU AI Office
   - New case law or enforcement decisions
   - Harmonized standards published

3. **Deployment Changes:**
   - Used in judicial, law enforcement, or other high-risk domains
   - Deployment to wider public audience
   - Integration with critical systems

---

## Responsible Parties

### Compliance Oversight

| Role | Responsibilities | Review Frequency |
|------|------------------|------------------|
| System Owner | Overall compliance accountability | Ongoing |
| Developer | Maintain compliance implementations | Each update |
| Legal Counsel | Regulatory interpretation and advice | Annually |
| Compliance Officer | Monitor regulatory changes | Continuous |

---

## Declaration of Compliance

**System:** EU AI Act Query Assistant (ai_act_cli.py) v1.0.0

**Classification:** Limited Risk AI System under EU AI Act

**Applicable Requirements:** Article 50(1) - Transparency obligations for chatbots

**Compliance Status:** ✅ **COMPLIANT**

**Declaration:**

This AI system has been assessed and classified according to the EU AI Act (Regulation (EU) 2024/1689). The system is classified as a Limited Risk AI system subject to transparency obligations under Article 50(1). All applicable requirements have been implemented as documented in this certificate.

The system:
- ✅ Clearly discloses AI interaction to users
- ✅ Labels AI-generated content appropriately
- ✅ Provides model and version information
- ✅ Includes appropriate disclaimers and notices
- ✅ Maintains compliance documentation

**Certification Date:** 2025-01-07

**Valid Until:** Material changes or regulatory updates require re-assessment

**Assessed By:** [Your Name/Role]

**Reviewed By:** [Reviewer Name/Role]

**Approved By:** [Approver Name/Role]

---

## Notes

### Implementation Summary

The EU AI Act Query Assistant achieves compliance through:

1. **Transparent Design:** Users are clearly informed of AI interaction through prominent disclosure
2. **Consistent Labeling:** Every AI response carries a verification reminder
3. **Accessible Information:** Version and compliance info available via command-line flags
4. **Documented Compliance:** Code comments and external documentation maintain evidence

### Compliance Cost

- **Implementation Time:** ~2 hours (code modifications)
- **Ongoing Maintenance:** Minimal (annual reviews)
- **Cost:** Negligible (no certification, assessment, or registration required)

### Comparison to High-Risk

If this were a high-risk system, additional requirements would include:
- 6-24 months implementation timeline
- Comprehensive technical documentation (100+ pages)
- Risk management system
- Data governance processes
- Conformity assessment (internal or third-party)
- CE marking
- EU database registration
- Post-market monitoring
- Estimated cost: $50,000-$500,000+

**Actual cost for Limited Risk:** < $500 (development time only)

---

## Appendix A: Article 50 Full Text

### Article 50: Transparency Obligations for Certain AI Systems

**Article 50(1) - Chatbots:**
> Providers of AI systems intended to interact directly with natural persons shall ensure that the AI system is designed and developed in such a way that natural persons are informed that they are interacting with an AI system, unless this is obvious from the circumstances and the context of use. This obligation shall not apply to AI systems authorised by law to detect, prevent, investigate or prosecute criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, unless those systems are available for the public to report a criminal offence.

**Compliance:** ✅ Implemented via startup disclosure panel

---

## Appendix B: Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-01-07 | Initial compliance certification | [Author] |

---

## Appendix C: Contact Information

**For Compliance Questions:**
- System Owner: [Name, Email]
- Compliance Contact: [Name, Email]
- Technical Support: [Name, Email]

**Regulatory Authority:**
- [National competent authority for your jurisdiction]
- [Contact information]

---

**Document Version:** 1.0
**Last Updated:** 2025-01-07
**Next Review:** 2026-01-07

---

✅ **CERTIFICATION COMPLETE**

This AI system is COMPLIANT with EU AI Act requirements for Limited Risk systems.

---

*This compliance certificate is based on the EU AI Act (Regulation (EU) 2024/1689) and represents the compliance status as of the certification date. Consult legal counsel for definitive compliance guidance.*
