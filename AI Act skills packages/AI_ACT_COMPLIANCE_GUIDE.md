# EU AI Act Compliance Artifacts Guide
## Complete Toolkit for AI System Compliance

**Generated:** 2025-01-07
**EU AI Act Reference:** Regulation (EU) 2024/1689
**Purpose:** Practical tools and templates for achieving EU AI Act compliance

---

## Overview

This toolkit provides comprehensive artifacts to help organizations achieve compliance with the EU AI Act. The artifacts cover the entire compliance lifecycle from initial risk classification through ongoing monitoring.

### What's Included

1. **Interactive Risk Classifier** - Python tool for classifying AI systems
2. **Compliance Checklist** - Comprehensive YAML checklist with 91+ tasks
3. **Technical Documentation Template** - Annex IV compliant documentation
4. **Model Card Template** - Transparency and documentation template
5. **Supporting Tools** - Your existing Python scripts for querying AI Act text

---

## Quick Start Guide

### Step 1: Classify Your AI System

**Tool:** `ai_risk_classifier.py`

Run the interactive classifier to determine your AI system's risk level:

```bash
python ai_risk_classifier.py
```

**What it does:**
- Asks questions about your AI system
- Checks for prohibited practices (Article 5)
- Identifies high-risk categories (Annex III)
- Determines transparency obligations
- Generates detailed assessment report

**Output:**
- Risk classification (Unacceptable/High/Limited/Minimal)
- Applicable requirements
- Recommended compliance actions
- Markdown assessment report

**Timeline:** 15-30 minutes

---

### Step 2: Review Compliance Requirements

**Tool:** `compliance_checklist_high_risk.yaml`

If your system is HIGH-RISK, use the comprehensive checklist:

**What's included:**
- 91 compliance tasks across 11 categories
- Article references for each requirement
- Priority levels (Critical/High/Medium)
- Status tracking fields
- Evidence documentation fields

**Key sections:**
1. Risk Management (Article 9) - 8 tasks
2. Data Governance (Article 10) - 8 tasks
3. Technical Documentation (Article 11) - 10 tasks
4. Record-Keeping (Article 12) - 8 tasks
5. Transparency (Article 13) - 8 tasks
6. Human Oversight (Article 14) - 9 tasks
7. Accuracy/Robustness/Security (Article 15) - 7 tasks
8. Conformity Assessment - 5 tasks
9. Registration - 3 tasks
10. Post-Market Monitoring - 4 tasks
11. Additional requirements

**How to use:**
1. Open YAML file in text editor
2. Fill in metadata (system name, dates, etc.)
3. Set applicable: true/false for special categories
4. Track status for each task
5. Document evidence locations
6. Update regularly

**Timeline:** Ongoing throughout implementation

---

### Step 3: Create Technical Documentation

**Tool:** `technical_documentation_template_annex_iv.md`

This is your primary compliance document (required by Article 11):

**Structure:**
- 15 main sections covering all Annex IV requirements
- Document control and approval tracking
- Comprehensive system description
- Risk management documentation
- Data governance records
- Performance validation results
- Human oversight design
- Post-market monitoring plans

**How to complete:**
1. Copy template for your system
2. Fill in bracketed placeholders [like this]
3. Complete tables with actual data
4. Add supporting evidence and references
5. Review and approve with stakeholders
6. Keep updated throughout lifecycle
7. Retain for 10 years after market placement

**Key sections to prioritize:**
- Section 1-4: System description and architecture
- Section 6-7: Data and risk management
- Section 9: Accuracy, robustness, cybersecurity
- Section 10: Human oversight
- Section 11: Transparency

**Timeline:** 2-6 months to complete initially

---

### Step 4: Create Model Card

**Tool:** `model_card_template.md`

Required for transparency (Article 13) and good practice:

**What it includes:**
- Model details and specifications
- Intended use and limitations
- Training and evaluation data
- Performance metrics overall and by subgroup
- Fairness analysis
- Ethical considerations
- Maintenance and monitoring plans
- Regulatory compliance status

**How to use:**
1. Fill in during model development
2. Update with evaluation results
3. Include disaggregated performance metrics
4. Document bias testing and mitigation
5. Publish with model or in instructions for use

**Timeline:** 1-2 weeks

---

### Step 5: Query AI Act Requirements

**Tools:** Your existing Python scripts

Use these to look up specific AI Act articles and requirements:

#### Interactive AI Act Agent (`ai_act_cli.py`)

```bash
python ai_act_cli.py
```

**Use for:**
- Asking questions about AI Act requirements
- Getting specific article explanations
- Understanding legal definitions
- Clarifying compliance requirements

**Example queries:**
- "What are the prohibited AI practices under Article 5?"
- "What documentation is required for high-risk systems?"
- "Explain human oversight requirements in Article 14"

#### Programmatic Queries (`query_ai_act.py`)

```bash
python query_ai_act.py "What are high-risk AI categories?"
```

**Use for:**
- Quick lookups
- Scripting and automation
- Batch queries
- Integration with compliance tools

---

## Compliance Workflow

### For HIGH-RISK AI Systems

```
┌─────────────────────────────────────┐
│ 1. Classify System                  │
│    └─> ai_risk_classifier.py        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. Review Requirements              │
│    └─> compliance_checklist.yaml    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 3. Implement Requirements           │
│    Articles 9-15                    │
│    ├─> Risk Management              │
│    ├─> Data Governance              │
│    ├─> Technical Documentation      │
│    ├─> Logging                      │
│    ├─> Transparency                 │
│    ├─> Human Oversight              │
│    └─> Accuracy/Robustness/Security │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 4. Document Everything              │
│    └─> Annex IV template            │
│    └─> Model card                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 5. Conformity Assessment            │
│    └─> Internal (Annex VI) or       │
│    └─> Third-party (Annex VII)      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 6. CE Marking & Registration        │
│    └─> EU Declaration of Conformity │
│    └─> EU Database Registration     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 7. Market Placement                 │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 8. Post-Market Monitoring           │
│    └─> Ongoing performance tracking │
│    └─> Incident reporting           │
│    └─> Periodic reviews             │
└─────────────────────────────────────┘
```

### Timeline Estimates

| Phase | Duration | Effort Level |
|-------|----------|--------------|
| Classification | 1 day | Low |
| Gap Analysis | 1-2 weeks | Medium |
| Requirements Implementation | 6-18 months | High |
| Documentation | 2-6 months | High |
| Conformity Assessment | 1-3 months | Medium-High |
| Registration & Marking | 2-4 weeks | Low-Medium |
| **Total (minimum)** | **9-24 months** | **High** |

---

## Article-by-Article Guidance

### Article 5: Prohibited AI Practices

**Status:** Effective from 2 February 2025

**Prohibited practices:**
- Social scoring by public authorities
- Subliminal manipulation causing harm
- Exploitation of vulnerabilities
- Real-time biometric identification in public (with exceptions)
- Emotion recognition in workplace/education (with exceptions)
- Predictive policing based solely on profiling
- Facial recognition scraping

**Action:** Use `ai_risk_classifier.py` to check if your system is prohibited

---

### Article 9: Risk Management

**Requirements:**
- Continuous risk management system
- Identify known and foreseeable risks
- Evaluate emerging risks during use
- Adopt appropriate mitigation measures
- Test risk management measures
- Document all decisions

**Tools:**
- `compliance_checklist.yaml` - Section: risk_management
- `technical_documentation_template.md` - Section 7

**Key Deliverables:**
- Risk register
- Risk assessment reports
- Testing results
- Mitigation documentation

---

### Article 10: Data Governance

**Requirements:**
- Relevant, representative, error-free data
- Examine for biases
- Implement bias mitigation
- Document data design choices
- Manage data quality throughout lifecycle

**Tools:**
- `compliance_checklist.yaml` - Section: data_governance
- `technical_documentation_template.md` - Section 6
- `model_card_template.md` - Sections: Training Data, Evaluation Data

**Key Deliverables:**
- Data quality reports
- Bias assessment
- Representativeness analysis
- Data governance procedures

---

### Article 11: Technical Documentation

**Requirements:**
- Prepare before market placement
- Demonstrate conformity with all requirements
- Keep up to date
- Retain for 10 years

**Tools:**
- `technical_documentation_template_annex_iv.md` (PRIMARY TOOL)

**Annex IV Sections Required:**
1. General description
2. Detailed system description
3. Development and training methodology
4. Validation and testing
5. Risk management
6. Changes made throughout lifecycle
7. Conformity assessment procedures

---

### Article 12: Record-Keeping

**Requirements:**
- Automatic logging capability
- Log time/date of use
- Log input data
- Log output decisions
- Enable traceability
- Appropriate retention period

**Tools:**
- `compliance_checklist.yaml` - Section: record_keeping
- `technical_documentation_template.md` - Section 12

**Key Deliverables:**
- Logging system design
- Log retention policy
- Traceability procedures

---

### Article 13: Transparency

**Requirements:**
- Instructions for use
- Provider identity and contact
- System capabilities and limitations
- Accuracy levels
- Human oversight measures
- Maintenance requirements

**Tools:**
- `compliance_checklist.yaml` - Section: transparency
- `technical_documentation_template.md` - Section 11
- `model_card_template.md` (can serve as basis for instructions)

**Key Deliverables:**
- Instructions for use document
- User documentation
- Transparency disclosures

---

### Article 14: Human Oversight

**Requirements:**
- Design for effective oversight
- Enable understanding of capabilities/limitations
- Enable monitoring
- Enable detection of anomalies
- Enable interpretation of outputs
- Enable override/intervention
- Assign to competent individuals

**Tools:**
- `compliance_checklist.yaml` - Section: human_oversight
- `technical_documentation_template.md` - Section 10

**Key Deliverables:**
- Human oversight design
- Override mechanisms
- Operator training program
- Competence requirements

---

### Article 15: Accuracy, Robustness, Cybersecurity

**Requirements:**
- Appropriate accuracy levels
- Robustness to errors and inconsistencies
- Resilience against attacks
- Address AI-specific vulnerabilities
- Security testing

**Tools:**
- `compliance_checklist.yaml` - Section: accuracy_robustness_security
- `technical_documentation_template.md` - Section 9
- `model_card_template.md` - Metrics section

**Key Deliverables:**
- Performance validation reports
- Robustness testing results
- Security assessment
- Adversarial testing results

---

## Risk Category Mapping

### High-Risk Categories (Annex III)

Use `ai_risk_classifier.py` to determine if your system falls under these:

| Category | Examples | Special Requirements |
|----------|----------|---------------------|
| **Biometrics** | Facial recognition, emotion recognition | Fundamental rights impact assessment |
| **Critical Infrastructure** | Traffic management, utility safety | Enhanced safety testing |
| **Education** | Exam scoring, access decisions | Performance monitoring by subgroup |
| **Employment** | Hiring, performance evaluation | Bias testing, discrimination checks |
| **Essential Services** | Credit scoring, insurance risk | Fairness analysis |
| **Law Enforcement** | Risk assessment, evidence evaluation | Strict human oversight |
| **Migration** | Visa processing, border control | Human rights safeguards |
| **Justice** | Judicial assistance, ADR | Due process protections |

---

## Conformity Assessment Options

### Annex VI: Internal Control

**When to use:** Most high-risk AI systems

**Process:**
1. Prepare technical documentation (use template)
2. Implement internal control procedures
3. Verify conformity with requirements
4. Draw up EU declaration of conformity
5. Affix CE marking
6. Register in EU database

**Responsible party:** Provider (you)

**External involvement:** None required (but recommended)

**Timeline:** 2-4 months

---

### Annex VII: Quality Management + Assessment

**When to use:**
- Biometric systems
- Critical infrastructure
- When specified in harmonized standards
- Voluntary choice for credibility

**Process:**
1. Establish quality management system
2. Prepare technical documentation
3. Engage notified body
4. Undergo QMS assessment
5. Technical documentation review by notified body
6. Draw up EU declaration of conformity
7. Affix CE marking
8. Register in EU database

**Responsible party:** Provider + Notified Body

**External involvement:** Notified body assessment required

**Timeline:** 4-8 months (includes notified body engagement)

---

## Common Pitfalls to Avoid

### 1. Underestimating Timeline
**Problem:** Assuming compliance can be achieved in weeks
**Reality:** High-risk compliance typically takes 9-24 months
**Solution:** Start early, plan realistic timeline

### 2. Treating as Checkbox Exercise
**Problem:** Filling templates without substance
**Reality:** Regulators expect genuine implementation
**Solution:** Build real processes, systems, and capabilities

### 3. Ignoring Data Quality
**Problem:** Assuming existing data is "good enough"
**Reality:** Data governance is critical compliance requirement
**Solution:** Invest in data quality, bias assessment, documentation

### 4. Weak Human Oversight
**Problem:** Token override buttons without real effectiveness
**Reality:** Human oversight must be genuine and effective
**Solution:** Design meaningful oversight mechanisms with trained operators

### 5. Missing Documentation
**Problem:** Building system without documenting decisions
**Reality:** Documentation must be contemporaneous
**Solution:** Document as you build, not after the fact

### 6. Insufficient Testing
**Problem:** Basic accuracy testing only
**Reality:** Must test across subgroups, for biases, robustness, security
**Solution:** Comprehensive testing program with disaggregated results

### 7. Ignoring Post-Market Monitoring
**Problem:** "Set and forget" after deployment
**Reality:** Ongoing monitoring is mandatory
**Solution:** Build monitoring systems before deployment

---

## FAQ

### Q: Do I need to use all these templates?

**A:** For HIGH-RISK systems: Yes, you need technical documentation (Annex IV template), compliance evidence (checklist), and transparency docs (model card or instructions for use).

For LIMITED RISK: Model card and transparency disclosures.

For MINIMAL RISK: No mandatory requirements, but model card is good practice.

### Q: Can I use these templates as-is?

**A:** These are templates to be completed with your system-specific information. Every bracket [like this] needs to be filled in with actual data about your AI system.

### Q: How long does it take to complete the Annex IV documentation?

**A:** Typically 2-6 months for the first version, depending on:
- System complexity
- Availability of existing documentation
- Testing and validation needed
- Team capacity

### Q: Who should complete these documents?

**A:** Cross-functional team including:
- AI/ML engineers (technical sections)
- Data scientists (data sections, performance)
- Compliance/legal (regulatory sections)
- Product managers (intended use, limitations)
- Security team (cybersecurity section)

### Q: Can I get help from external consultants?

**A:** Yes, recommended for:
- Legal interpretation
- Gap analysis
- Conformity assessment
- Technical documentation review

### Q: What if my system changes after compliance?

**A:** Depends on change magnitude:
- **Minor changes:** Update documentation
- **Substantial modifications:** May require new conformity assessment
- Use modification log in technical documentation template

### Q: Do I need a notified body?

**A:** Required for Annex VII procedure (certain biometric systems, critical infrastructure).

Optional but beneficial for other high-risk systems for credibility.

---

## Resources and Support

### EU AI Act Text Queries

Use your Python scripts:
- `ai_act_cli.py` - Interactive Q&A
- `query_ai_act.py` - Programmatic queries

### Official EU Resources

- **EU AI Act Text:** Regulation (EU) 2024/1689
- **European Commission:** https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
- **AI Office:** https://digital-strategy.ec.europa.eu/en/policies/ai-office

### Standards and Guidelines

- **NIST AI RMF:** https://airc.nist.gov/AI_RMF_Knowledge_Base
- **ISO/IEC 42001:** AI Management System
- **ISO/IEC 23894:** Risk management
- **IEEE 7000 series:** Ethics and AI standards

### Notified Bodies

- **NANDO Database:** https://ec.europa.eu/growth/tools-databases/nando/
- (Will be populated as bodies are designated for AI Act)

---

## Getting Started Checklist

- [ ] Run `ai_risk_classifier.py` to classify your AI system
- [ ] Review the generated risk assessment report
- [ ] If HIGH-RISK: Open `compliance_checklist_high_risk.yaml`
- [ ] Identify which requirements apply to your system
- [ ] Form compliance team with necessary expertise
- [ ] Create project plan with realistic timeline (9-24 months)
- [ ] Begin with critical requirements (Articles 9-15)
- [ ] Start completing `technical_documentation_template_annex_iv.md`
- [ ] Establish data governance processes
- [ ] Implement risk management system
- [ ] Design human oversight mechanisms
- [ ] Conduct comprehensive testing (performance, fairness, robustness)
- [ ] Complete model card for transparency
- [ ] Plan conformity assessment approach
- [ ] Budget for ongoing compliance and monitoring

---

## Document Inventory

| Document | File Name | Purpose | Priority |
|----------|-----------|---------|----------|
| Risk Classifier | `ai_risk_classifier.py` | Classify AI system risk level | ⭐⭐⭐ Critical |
| Compliance Checklist | `compliance_checklist_high_risk.yaml` | Track 91 compliance tasks | ⭐⭐⭐ Critical |
| Technical Documentation | `technical_documentation_template_annex_iv.md` | Primary compliance document (Article 11) | ⭐⭐⭐ Critical |
| Model Card | `model_card_template.md` | Transparency and documentation | ⭐⭐ High |
| AI Act CLI | `ai_act_cli.py` | Query regulation text | ⭐⭐ High |
| Query Tool | `query_ai_act.py` | Programmatic queries | ⭐ Medium |
| Setup Tool | `setup_ai_act_store.py` | Knowledge base setup | ⭐ Medium |
| This Guide | `AI_ACT_COMPLIANCE_GUIDE.md` | Overview and instructions | ⭐⭐ High |

---

## Next Steps

1. **Immediate (Today):**
   - Run risk classifier on your AI system
   - Read generated assessment report
   - Share with stakeholders

2. **This Week:**
   - Form compliance team
   - Review compliance checklist
   - Identify major gaps
   - Create high-level project plan

3. **This Month:**
   - Start technical documentation
   - Begin risk assessment
   - Assess data governance current state
   - Define human oversight approach

4. **Next 3 Months:**
   - Implement critical requirements (Articles 9-15)
   - Conduct comprehensive testing
   - Document everything
   - Engage legal counsel

5. **Months 3-12:**
   - Complete technical documentation
   - Conduct conformity assessment
   - Prepare EU declaration of conformity
   - Plan market placement

6. **Ongoing:**
   - Post-market monitoring
   - Performance tracking
   - Incident management
   - Periodic reviews

---

## Support and Feedback

**Questions?** Use your AI Act query tools:
```bash
python ai_act_cli.py
# Ask: "What are the penalties for non-compliance?"
```

**Need Help?**
- Engage legal counsel with EU AI Act expertise
- Consider AI compliance consultants
- Join AI Act implementation communities
- Attend EU AI Office webinars and guidance sessions

**Keep Learning:**
- Monitor EU AI Office guidance documents
- Track harmonized standards development
- Follow notified body designations
- Watch for implementing acts and delegated acts

---

**Document Version:** 1.0
**Last Updated:** 2025-01-07
**Compliance Status:** Toolkit Complete ✓

**Remember:** EU AI Act compliance is not a one-time project but an ongoing commitment. These tools are designed to support you throughout the entire lifecycle of your AI system.

Good luck with your compliance journey! 🇪🇺 🤖
