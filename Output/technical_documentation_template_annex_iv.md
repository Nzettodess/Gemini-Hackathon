# Technical Documentation for High-Risk AI Systems
## EU AI Act Annex IV Compliance Template

> **Regulation Reference:** Regulation (EU) 2024/1689 - Annex IV
> **Last Updated:** [Date]
> **Document Version:** [Version]
> **System Name:** [AI System Name]
> **System Version:** [Version]
> **Provider:** [Organization Name]

---

## Document Control

| Field | Value |
|-------|-------|
| Document ID | [Unique identifier] |
| Prepared By | [Name, Role] |
| Reviewed By | [Name, Role] |
| Approved By | [Name, Role] |
| Approval Date | [Date] |
| Next Review Date | [Date] |
| Classification | [Confidential/Internal/Public] |
| Retention Period | 10 years after market placement |

---

## Executive Summary

**Purpose of this Document:**
This technical documentation demonstrates compliance of [AI System Name] with the requirements of the EU AI Act for high-risk AI systems as specified in Annex IV.

**AI System Classification:**
- **Risk Level:** High-Risk
- **Annex III Category:** [Specify category, e.g., "Employment - Recruitment and selection"]
- **Article 6 Classification:** [Specify basis for high-risk classification]

**Conformity Status:**
- **Conformity Assessment Procedure:** [Annex VI / Annex VII]
- **Conformity Status:** [Not Started / In Progress / Completed]
- **CE Marking:** [Yes / No / Not Yet Applied]
- **EU Database Registration:** [Completed / Pending]

---

## Table of Contents

1. [General Description](#1-general-description)
2. [Detailed System Description](#2-detailed-system-description)
3. [Intended Purpose and Specifications](#3-intended-purpose-and-specifications)
4. [System Architecture](#4-system-architecture)
5. [Development and Training](#5-development-and-training)
6. [Data Governance](#6-data-governance)
7. [Risk Management](#7-risk-management)
8. [Performance and Validation](#8-performance-and-validation)
9. [Accuracy, Robustness, and Cybersecurity](#9-accuracy-robustness-and-cybersecurity)
10. [Human Oversight](#10-human-oversight)
11. [Transparency and Instructions for Use](#11-transparency-and-instructions-for-use)
12. [Logging and Record-Keeping](#12-logging-and-record-keeping)
13. [Conformity Assessment](#13-conformity-assessment)
14. [Post-Market Monitoring](#14-post-market-monitoring)
15. [Lifecycle Management](#15-lifecycle-management)

---

## 1. General Description

### 1.1 AI System Overview

**System Name:** [Full name of AI system]

**Provider Information:**
- **Organization:** [Legal entity name]
- **Address:** [Complete address]
- **Registration Number:** [Company registration number]
- **Contact Person:** [Name, role, email, phone]

**System Purpose in Brief:**
[2-3 sentences describing what the system does and its primary function]

**Version History:**

| Version | Release Date | Major Changes | Status |
|---------|--------------|---------------|--------|
| 1.0 | [Date] | Initial release | Current |
| | | | |

### 1.2 Regulatory Classification

**High-Risk Classification Basis:**
- **Annex III Reference:** [Specific category and subcategory]
- **Justification:** [Explain why system falls under this category]

**Applicable Harmonized Standards:**
- [List any harmonized standards followed]
- [Standard reference numbers and versions]

**Applicable Common Specifications:**
- [If applicable, list common specifications per Article 41]

---

## 2. Detailed System Description

### 2.1 System Components

**Core AI Components:**

| Component | Description | Technology | Version | Purpose |
|-----------|-------------|------------|---------|---------|
| [Component 1] | [Description] | [ML model type] | [Version] | [Purpose] |
| [Component 2] | [Description] | [Technology] | [Version] | [Purpose] |
| | | | | |

**Supporting Infrastructure:**
- **Compute Resources:** [CPU/GPU specs, cloud services, etc.]
- **Storage Systems:** [Database types, data lakes, etc.]
- **Integration Points:** [APIs, data feeds, external systems]

### 2.2 AI Methods and Techniques

**Model Type:** [e.g., Deep Neural Network, Random Forest, Transformer, etc.]

**Learning Approach:** [Supervised / Unsupervised / Reinforcement / Semi-supervised]

**Algorithm Details:**
- **Primary Algorithm:** [Detailed description]
- **Architecture:** [e.g., ResNet-50, BERT, GPT-based, etc.]
- **Key Hyperparameters:** [List critical hyperparameters]

**Input/Output Specifications:**

| Aspect | Specification |
|--------|---------------|
| Input Format | [Format, dimensions, data types] |
| Input Features | [List and describe key features] |
| Output Format | [Format, dimensions, data types] |
| Output Interpretation | [How outputs should be interpreted] |
| Decision Threshold(s) | [If applicable, decision boundaries] |

### 2.3 Design Specifications

**Design Principles:**
- [List key design principles, e.g., "Privacy by design"]
- [Security principles]
- [Fairness considerations in design]

**Design Choices and Rationale:**

| Design Choice | Rationale | Alternatives Considered |
|---------------|-----------|------------------------|
| [Choice 1] | [Why chosen] | [Alternatives and why not chosen] |
| [Choice 2] | [Why chosen] | [Alternatives and why not chosen] |

**Data Processing Pipeline:**
```
[Raw Input] → [Preprocessing] → [Feature Engineering] → [Model Inference] → [Post-processing] → [Output]
```

[Provide detailed description of each stage]

---

## 3. Intended Purpose and Specifications

### 3.1 Intended Purpose

**Primary Use Case:** [Detailed description of intended use]

**Intended Users:**
- **User Type:** [e.g., HR professionals, loan officers, medical staff]
- **Required Competence:** [Skills, training, certifications needed]
- **Geographic Scope:** [EU countries, specific regions]
- **Deployment Context:** [Workplace, healthcare facility, educational institution, etc.]

**Intended Benefits:**
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

### 3.2 Contraindications and Out-of-Scope Use

**The AI system is NOT intended for:**
- [Prohibited use case 1]
- [Prohibited use case 2]
- [Context where system should not be used]

**Known Limitations:**
- [Limitation 1 - e.g., "Not validated for use with population group X"]
- [Limitation 2 - e.g., "Performance degrades in condition Y"]
- [Limitation 3]

### 3.3 Foreseeable Misuse

**Reasonably Foreseeable Misuse Scenarios:**

| Misuse Scenario | Potential Harm | Mitigation Measures |
|----------------|----------------|---------------------|
| [Scenario 1] | [Harm description] | [How prevented/mitigated] |
| [Scenario 2] | [Harm description] | [How prevented/mitigated] |
| [Scenario 3] | [Harm description] | [How prevented/mitigated] |

---

## 4. System Architecture

### 4.1 Technical Architecture

**System Architecture Diagram:**
```
[Insert architecture diagram showing data flow, components, integrations]
```

**Component Descriptions:**

#### 4.1.1 Data Ingestion Layer
- [Description of how data enters the system]
- [Data sources]
- [Data validation and quality checks]

#### 4.1.2 Processing Layer
- [Description of data processing and transformation]
- [Feature engineering components]
- [Real-time vs batch processing]

#### 4.1.3 Model Inference Layer
- [Description of model serving infrastructure]
- [Scalability approach]
- [Response time requirements and actual performance]

#### 4.1.4 Output Layer
- [Description of how outputs are delivered]
- [Integration with downstream systems]
- [User interface components]

### 4.2 Computational Resources

**Training Infrastructure:**
- **Hardware:** [GPU/TPU types, quantities]
- **Training Time:** [Typical training duration]
- **Energy Consumption:** [Estimated energy use during training]

**Inference Infrastructure:**
- **Deployment Environment:** [Cloud/On-premise/Edge/Hybrid]
- **Hardware Requirements:** [Minimum and recommended specs]
- **Scalability:** [Concurrent requests handled, latency requirements]
- **Energy Consumption:** [Estimated per-inference energy use]

**Third-Party Dependencies:**

| Dependency | Purpose | Version | License | Provider |
|------------|---------|---------|---------|----------|
| [Library/Service] | [Purpose] | [Version] | [License] | [Provider] |
| | | | | |

---

## 5. Development and Training

### 5.1 Development Methodology

**Development Process:** [Agile / Waterfall / Hybrid]

**Development Timeline:**

| Phase | Start Date | End Date | Key Deliverables |
|-------|------------|----------|------------------|
| Requirements | [Date] | [Date] | [Deliverables] |
| Design | [Date] | [Date] | [Deliverables] |
| Development | [Date] | [Date] | [Deliverables] |
| Testing | [Date] | [Date] | [Deliverables] |
| Deployment | [Date] | [Date] | [Deliverables] |

**Development Team:**

| Role | Responsibilities | Qualifications |
|------|------------------|----------------|
| [Role 1] | [Responsibilities] | [Required qualifications] |
| [Role 2] | [Responsibilities] | [Required qualifications] |

### 5.2 Training Methodology

**Training Approach:** [Description of training methodology]

**Training Process:**
1. **Data Preparation:** [Description]
2. **Feature Engineering:** [Description]
3. **Model Selection:** [Description]
4. **Hyperparameter Tuning:** [Method used, parameters tuned]
5. **Model Training:** [Details of training process]
6. **Validation:** [Validation approach]

**Training Configuration:**

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Learning Rate | [Value] | [Why chosen] |
| Batch Size | [Value] | [Why chosen] |
| Epochs | [Value] | [Why chosen] |
| Optimizer | [Type] | [Why chosen] |
| Loss Function | [Function] | [Why chosen] |
| Regularization | [Method] | [Why chosen] |

**Training Metrics Tracked:**
- [Metric 1 - e.g., Loss]
- [Metric 2 - e.g., Accuracy]
- [Metric 3 - e.g., F1-score]

**Training Results:**
- **Final Training Loss:** [Value]
- **Training Duration:** [Hours/days]
- **Convergence:** [Description of convergence behavior]

### 5.3 Testing and Validation Methodology

**Validation Strategy:** [k-fold cross-validation / holdout / time-based split / etc.]

**Test Data Split:**
- **Training Set:** [Percentage/number of samples]
- **Validation Set:** [Percentage/number of samples]
- **Test Set:** [Percentage/number of samples]

**Testing Procedures:**

| Test Type | Purpose | Methodology | Frequency |
|-----------|---------|-------------|-----------|
| Unit Testing | [Purpose] | [Method] | [Frequency] |
| Integration Testing | [Purpose] | [Method] | [Frequency] |
| Performance Testing | [Purpose] | [Method] | [Frequency] |
| Fairness Testing | [Purpose] | [Method] | [Frequency] |
| Adversarial Testing | [Purpose] | [Method] | [Frequency] |

---

## 6. Data Governance

### 6.1 Training Data

**Training Dataset Overview:**

| Attribute | Details |
|-----------|---------|
| Dataset Name | [Name/identifier] |
| Source | [Origin of data] |
| Size | [Number of samples/records] |
| Time Period | [Data collection period] |
| Geographic Coverage | [Geographic scope] |
| Update Frequency | [How often updated] |

**Data Collection Methodology:**
- **Collection Method:** [How data was collected]
- **Collection Period:** [Time period]
- **Consent Mechanism:** [If applicable, how consent obtained]
- **Legal Basis (GDPR):** [Article 6(1) basis]

**Data Characteristics:**

| Feature | Data Type | Range/Categories | Missing Data % | Source |
|---------|-----------|------------------|----------------|--------|
| [Feature 1] | [Type] | [Range] | [%] | [Source] |
| [Feature 2] | [Type] | [Range] | [%] | [Source] |
| | | | | |

### 6.2 Data Quality Management

**Data Quality Metrics:**

| Quality Dimension | Metric | Target | Actual | Verification Method |
|-------------------|--------|--------|--------|---------------------|
| Accuracy | [Metric] | [Target] | [Actual] | [Method] |
| Completeness | [Metric] | [Target] | [Actual] | [Method] |
| Consistency | [Metric] | [Target] | [Actual] | [Method] |
| Timeliness | [Metric] | [Target] | [Actual] | [Method] |
| Relevance | [Metric] | [Target] | [Actual] | [Method] |

**Data Cleaning Procedures:**
1. [Procedure 1 - e.g., "Outlier detection and handling"]
2. [Procedure 2 - e.g., "Missing data imputation"]
3. [Procedure 3 - e.g., "Duplicate removal"]

**Data Preprocessing Steps:**
- [Step 1 - e.g., "Normalization/scaling"]
- [Step 2 - e.g., "Encoding categorical variables"]
- [Step 3 - e.g., "Feature selection"]

### 6.3 Data Representativeness

**Target Population:** [Describe the population the AI system is intended to serve]

**Dataset Representativeness Analysis:**

| Demographic Factor | Population % | Training Data % | Assessment |
|--------------------|--------------|-----------------|------------|
| [Factor 1 - e.g., Age groups] | [%] | [%] | [Representative / Underrepresented / Overrepresented] |
| [Factor 2 - e.g., Gender] | [%] | [%] | [Assessment] |
| [Factor 3 - e.g., Geography] | [%] | [%] | [Assessment] |

**Identified Representativeness Gaps:**
- [Gap 1 and mitigation strategy]
- [Gap 2 and mitigation strategy]

### 6.4 Bias Examination and Mitigation

**Bias Assessment Conducted:**

| Bias Type | Assessment Method | Findings | Mitigation Actions |
|-----------|-------------------|----------|-------------------|
| Selection Bias | [Method] | [Findings] | [Actions taken] |
| Measurement Bias | [Method] | [Findings] | [Actions taken] |
| Label Bias | [Method] | [Findings] | [Actions taken] |
| Algorithmic Bias | [Method] | [Findings] | [Actions taken] |

**Fairness Metrics Computed:**

| Metric | Definition | Value | Acceptable Range | Status |
|--------|------------|-------|------------------|--------|
| [Metric 1 - e.g., Demographic Parity] | [Definition] | [Value] | [Range] | [Pass/Fail] |
| [Metric 2 - e.g., Equal Opportunity] | [Definition] | [Value] | [Range] | [Pass/Fail] |
| [Metric 3] | [Definition] | [Value] | [Range] | [Pass/Fail] |

**Bias Mitigation Techniques Applied:**
- [Technique 1 - e.g., "Resampling of underrepresented groups"]
- [Technique 2 - e.g., "Fairness constraints in training"]
- [Technique 3 - e.g., "Post-processing calibration"]

### 6.5 Personal and Special Category Data

**Personal Data Processing:**
- **Personal Data Processed:** [Yes / No]
- **If Yes, Types:** [List types of personal data]
- **GDPR Compliance Measures:** [List measures]
- **Data Protection Impact Assessment (DPIA):** [Completed / Not Required]
- **DPIA Reference:** [Document reference if completed]

**Special Categories of Personal Data (GDPR Article 9):**
- **Special Category Data Used:** [Yes / No]
- **If Yes, Categories:** [e.g., health data, biometric data]
- **Necessity Justification:** [Why strictly necessary for bias detection/correction]
- **Safeguards Implemented:** [List technical and organizational safeguards]

---

## 7. Risk Management

### 7.1 Risk Management System

**Risk Management Framework:** [Framework/standard used, e.g., ISO 31000]

**Risk Management Process:**
```
Risk Identification → Risk Analysis → Risk Evaluation → Risk Treatment → Monitoring & Review
```

**Risk Management Lifecycle:**
- **Established:** [Date]
- **Review Frequency:** [Quarterly / Bi-annually / Annually]
- **Last Review Date:** [Date]
- **Next Review Date:** [Date]

**Responsible Parties:**

| Role | Name | Responsibilities |
|------|------|------------------|
| Risk Owner | [Name] | [Overall accountability] |
| Risk Manager | [Name] | [Day-to-day management] |
| Risk Assessors | [Names] | [Risk assessment activities] |

### 7.2 Risk Identification and Analysis

**Identified Risks:**

| Risk ID | Risk Description | Risk Category | Likelihood | Impact | Risk Level | Article 9 Reference |
|---------|------------------|---------------|------------|--------|------------|---------------------|
| RISK-001 | [Description] | [Health/Safety/Fundamental Rights/Environment] | [L/M/H] | [L/M/H] | [L/M/H/Critical] | [Relevant provision] |
| RISK-002 | [Description] | [Category] | [L/M/H] | [L/M/H] | [Level] | [Reference] |
| | | | | | | |

**Risk Assessment Criteria:**

| Likelihood | Probability | Description |
|------------|-------------|-------------|
| Low | < 10% | [Description] |
| Medium | 10-50% | [Description] |
| High | > 50% | [Description] |

| Impact | Severity | Description |
|--------|----------|-------------|
| Low | Minor | [Description] |
| Medium | Moderate | [Description] |
| High | Severe | [Description] |
| Critical | Catastrophic | [Description] |

### 7.3 Risk Treatment and Mitigation

**Risk Mitigation Measures:**

| Risk ID | Mitigation Strategy | Implementation Status | Verification Method | Residual Risk |
|---------|-------------------|----------------------|---------------------|---------------|
| RISK-001 | [Strategy] | [Completed/In Progress/Planned] | [How verified] | [L/M/H] |
| RISK-002 | [Strategy] | [Status] | [Method] | [Level] |
| | | | | |

**Residual Risk Acceptance:**
- **Residual Risk Level:** [Overall level after mitigations]
- **Accepted By:** [Name, role, date]
- **Acceptance Rationale:** [Why residual risks are acceptable]

### 7.4 Risk Testing and Validation

**Risk Testing Conducted:**

| Test ID | Test Purpose | Test Method | Test Data | Results | Date |
|---------|-------------|-------------|-----------|---------|------|
| TEST-001 | [Purpose] | [Method] | [Data used] | [Results summary] | [Date] |
| TEST-002 | [Purpose] | [Method] | [Data used] | [Results summary] | [Date] |
| | | | | | |

**Testing Against Foreseeable Misuse:**
- [Misuse scenario tested]
- [Test method]
- [Results and mitigations]

---

## 8. Performance and Validation

### 8.1 Performance Metrics

**Primary Performance Metrics:**

| Metric | Definition | Target | Validation Result | Test Result | Production (if deployed) |
|--------|------------|--------|-------------------|-------------|--------------------------|
| Accuracy | [Definition] | [Target] | [Result] | [Result] | [Result] |
| Precision | [Definition] | [Target] | [Result] | [Result] | [Result] |
| Recall | [Definition] | [Target] | [Result] | [Result] | [Result] |
| F1-Score | [Definition] | [Target] | [Result] | [Result] | [Result] |
| AUC-ROC | [Definition] | [Target] | [Result] | [Result] | [Result] |
| [Custom metric] | [Definition] | [Target] | [Result] | [Result] | [Result] |

**Performance by Subgroup:**

| Subgroup | Metric | Value | Comparison to Overall | Acceptable? |
|----------|--------|-------|----------------------|-------------|
| [Subgroup 1] | [Metric] | [Value] | [Higher/Lower/Equal] | [Yes/No] |
| [Subgroup 2] | [Metric] | [Value] | [Comparison] | [Yes/No] |
| | | | | |

**Performance Variability Analysis:**
- **Standard Deviation:** [Value]
- **Confidence Intervals:** [95% CI]
- **Performance Stability:** [Assessment]

### 8.2 Validation Results

**Validation Dataset Details:**
- **Size:** [Number of samples]
- **Source:** [Origin, different from training]
- **Representativeness:** [How representative of target population]

**Cross-Validation Results:**
- **Method:** [k-fold, leave-one-out, etc.]
- **Folds:** [Number]
- **Mean Performance:** [Metrics]
- **Variability:** [Standard deviation across folds]

**Independent Validation:**
- **Conducted By:** [Internal team / External organization]
- **Date:** [Date]
- **Results:** [Summary]
- **Report Reference:** [Document reference]

### 8.3 Error Analysis

**Error Distribution:**

| Error Type | Frequency | Percentage | Severity | Root Cause Analysis |
|------------|-----------|------------|----------|---------------------|
| False Positive | [Count] | [%] | [L/M/H] | [Analysis] |
| False Negative | [Count] | [%] | [L/M/H] | [Analysis] |
| [Other error type] | [Count] | [%] | [L/M/H] | [Analysis] |

**Failure Mode Analysis:**
- [Failure mode 1]: [Frequency, impact, mitigation]
- [Failure mode 2]: [Frequency, impact, mitigation]

**Edge Cases and Limitations:**
- [Edge case 1]: [Description and handling]
- [Edge case 2]: [Description and handling]

---

## 9. Accuracy, Robustness, and Cybersecurity

### 9.1 Accuracy Requirements (Article 15)

**Declared Accuracy Levels:**
- **Overall Accuracy:** [Percentage/metric value]
- **Accuracy by Subgroup:** [See section 8.1]
- **Accuracy Thresholds:** [Minimum acceptable levels]

**Accuracy Monitoring:**
- **Monitoring Method:** [How accuracy is tracked in production]
- **Monitoring Frequency:** [Real-time / Daily / Weekly]
- **Alert Thresholds:** [When alerts are triggered]
- **Degradation Response:** [Actions taken if accuracy degrades]

### 9.2 Robustness (Article 15)

**Robustness Testing Conducted:**

| Test Type | Purpose | Method | Results | Date |
|-----------|---------|--------|---------|------|
| Noise Injection | Test resilience to noisy inputs | [Method] | [Pass/Fail, details] | [Date] |
| Input Perturbation | Test sensitivity to small changes | [Method] | [Results] | [Date] |
| Out-of-Distribution Detection | Test behavior on unexpected inputs | [Method] | [Results] | [Date] |
| Stress Testing | Test under high load/edge conditions | [Method] | [Results] | [Date] |

**Error Handling Mechanisms:**
- [Mechanism 1 - e.g., "Input validation and rejection of invalid inputs"]
- [Mechanism 2 - e.g., "Graceful degradation under system failures"]
- [Mechanism 3 - e.g., "Uncertainty quantification for low-confidence predictions"]

**Resilience Measures:**
- **Fault Tolerance:** [Description of fault tolerance mechanisms]
- **Redundancy:** [Backup systems, failover procedures]
- **Recovery Procedures:** [How system recovers from failures]

### 9.3 Cybersecurity (Article 15)

**Security Threat Model:**

| Threat | Likelihood | Impact | Mitigation | Status |
|--------|------------|--------|------------|--------|
| Data Poisoning | [L/M/H] | [L/M/H] | [Mitigation measures] | [Implemented/Planned] |
| Model Evasion (Adversarial Attacks) | [L/M/H] | [L/M/H] | [Mitigation measures] | [Status] |
| Model Inversion | [L/M/H] | [L/M/H] | [Mitigation measures] | [Status] |
| Membership Inference | [L/M/H] | [L/M/H] | [Mitigation measures] | [Status] |
| Model Theft | [L/M/H] | [L/M/H] | [Mitigation measures] | [Status] |
| Unauthorized Access | [L/M/H] | [L/M/H] | [Mitigation measures] | [Status] |
| Data Breach | [L/M/H] | [L/M/H] | [Mitigation measures] | [Status] |

**Adversarial Robustness:**
- **Adversarial Testing Conducted:** [Yes/No]
- **Attack Methods Tested:** [List attack methods, e.g., FGSM, PGD]
- **Robustness Metrics:** [Accuracy under attack, etc.]
- **Defenses Implemented:** [Adversarial training, input preprocessing, etc.]

**Security Controls Implemented:**

| Control Category | Specific Controls | Implementation Status |
|-----------------|-------------------|----------------------|
| Access Control | [List controls] | [Implemented] |
| Data Protection | [List controls] | [Implemented] |
| Model Protection | [List controls] | [Implemented] |
| Infrastructure Security | [List controls] | [Implemented] |
| Monitoring & Logging | [List controls] | [Implemented] |

**Security Testing:**
- **Penetration Testing:** [Conducted by, date, results]
- **Vulnerability Scanning:** [Frequency, last scan date, findings]
- **Security Audits:** [Date, auditor, summary]

**Incident Response:**
- **Incident Response Plan:** [Reference to plan document]
- **Security Incidents (if any):** [Log of past incidents and resolutions]

---

## 10. Human Oversight

### 10.1 Human Oversight Design (Article 14)

**Oversight Model:**
- **Type:** [Human-in-the-loop / Human-on-the-loop / Human-in-command]
- **Rationale:** [Why this model is appropriate for the risk level]

**Oversight Mechanisms:**

| Mechanism | Description | Implementation | Effectiveness Validation |
|-----------|-------------|----------------|-------------------------|
| [Mechanism 1] | [Description] | [How implemented] | [How validated] |
| [Mechanism 2] | [Description] | [How implemented] | [How validated] |
| | | | |

### 10.2 Human Oversight Capabilities (Article 14(4))

**Capabilities Provided to Oversight Personnel:**

| Capability | Implementation | Training Required |
|------------|----------------|-------------------|
| Understand system capabilities and limitations | [How provided - e.g., documentation, training] | [Training requirements] |
| Monitor system operation | [Monitoring tools/interfaces provided] | [Training requirements] |
| Detect anomalies, dysfunctions, unexpected performance | [Alert systems, dashboards] | [Training requirements] |
| Interpret system outputs correctly | [Explanation tools, documentation] | [Training requirements] |
| Decide not to use or disregard output | [Process/authority granted] | [Training requirements] |
| Intervene or interrupt system (stop button) | [Stop mechanisms implemented] | [Training requirements] |

**Override Mechanisms:**
- **Override Method:** [How humans can override system decisions]
- **Override Authority:** [Who has authority to override]
- **Override Logging:** [How overrides are logged and reviewed]

### 10.3 Competence Requirements

**Required Competencies for Oversight Personnel:**

| Competency Area | Required Level | Verification Method |
|----------------|----------------|---------------------|
| [Area 1 - e.g., Domain expertise] | [Level] | [Certification, experience, etc.] |
| [Area 2 - e.g., AI/ML understanding] | [Level] | [Training completion, assessment] |
| [Area 3 - e.g., Risk assessment] | [Level] | [Method] |

**Training Program:**
- **Training Curriculum:** [Reference to training materials]
- **Training Duration:** [Hours/days]
- **Assessment Method:** [How competence is verified]
- **Refresher Training:** [Frequency]

---

## 11. Transparency and Instructions for Use

### 11.1 Transparency Requirements (Article 13)

**System Transparency Features:**

| Feature | Implementation | User Accessibility |
|---------|----------------|-------------------|
| Output interpretability | [How outputs are made interpretable] | [How users access this] |
| Confidence scores | [If provided, how calculated and displayed] | [Accessibility] |
| Explanation of decisions | [Explainability methods used] | [How provided to users] |
| Limitations disclosure | [Where and how communicated] | [Accessibility] |

**Explainability Methods:**
- **Method Used:** [e.g., LIME, SHAP, attention mechanisms, rule extraction]
- **Explanation Type:** [Local / Global / Both]
- **Explanation Format:** [Text / Visual / Both]
- **Validation:** [How explanation accuracy/fidelity is validated]

### 11.2 Instructions for Use

**Instructions for Use Document:** [Reference to separate IFU document]

**Key Elements Included in Instructions:**

| Element | Article 13(3)(b) Reference | Included | Location in IFU |
|---------|---------------------------|----------|----------------|
| Provider identity and contact | (i) | [Yes/No] | [Section] |
| System characteristics, capabilities, performance | (ii) | [Yes/No] | [Section] |
| Limitations, error rates, circumstances of risks | (iii) | [Yes/No] | [Section] |
| Performance related to specific persons/groups | (iii) | [Yes/No] | [Section] |
| Intended purpose and misuse | (iv) | [Yes/No] | [Section] |
| Expected lifetime and maintenance | (v) | [Yes/No] | [Section] |
| Human oversight measures | (vi) | [Yes/No] | [Section] |
| Cybersecurity measures | (vii) | [Yes/No] | [Section] |

**User Documentation Suite:**
- [ ] Instructions for Use (IFU) document
- [ ] Quick Start Guide
- [ ] User Manual
- [ ] Technical Reference
- [ ] Training Materials
- [ ] Troubleshooting Guide

---

## 12. Logging and Record-Keeping

### 12.1 Logging Capabilities (Article 12)

**Automatic Logging System:**
- **Logging Infrastructure:** [Technology/system used]
- **Log Storage:** [Where logs are stored]
- **Log Retention Period:** [Duration, justification]
- **Log Security:** [Access controls, encryption]

**Events Logged:**

| Event Type | Data Captured | Retention | Purpose |
|------------|---------------|-----------|---------|
| System use | Date, time, user ID | [Duration] | [Purpose] |
| Input data | [Reference or actual input] | [Duration] | [Purpose] |
| Output data | [Output/decision] | [Duration] | [Purpose] |
| User interactions | [Type of interaction] | [Duration] | [Purpose] |
| System errors | [Error type, context] | [Duration] | [Purpose] |
| Human overrides | [Override details] | [Duration] | [Purpose] |

**Traceability:**
- **End-to-End Traceability:** [How individual decisions can be traced]
- **Audit Trail:** [How complete audit trail is maintained]
- **Log Analysis:** [Tools and processes for log analysis]

### 12.2 Record-Keeping Procedures

**Record Types Maintained:**
- [ ] Technical documentation (this document)
- [ ] Training records
- [ ] Validation reports
- [ ] Risk assessments
- [ ] Conformity assessment records
- [ ] Modification logs
- [ ] Incident reports
- [ ] Operational logs
- [ ] User feedback

**Record Storage and Access:**
- **Storage System:** [Document management system used]
- **Access Controls:** [Who can access which records]
- **Backup Procedures:** [How records are backed up]
- **Retention Schedule:** [Retention periods by record type]

---

## 13. Conformity Assessment

### 13.1 Conformity Assessment Procedure

**Applicable Procedure:**
- [ ] Annex VI - Internal Control (for most high-risk systems)
- [ ] Annex VII - Quality Management System + Assessment by Notified Body

**Assessment Status:**
- **Status:** [Not Started / In Progress / Completed]
- **Start Date:** [Date]
- **Completion Date:** [Date or Target Date]
- **Assessor:** [Internal / Notified Body Name]

### 13.2 Conformity Assessment Activities

**Activities Completed:**

| Activity | Annex Reference | Status | Evidence | Date |
|----------|----------------|--------|----------|------|
| Technical documentation prepared | Annex VI/VII | [Status] | [This document] | [Date] |
| Conformity verification | Annex VI, § 3 | [Status] | [Evidence] | [Date] |
| Internal controls established | Annex VI, § 4 | [Status] | [Evidence] | [Date] |
| EU Declaration of Conformity drawn up | Article 47 | [Status] | [Document ref] | [Date] |
| CE marking affixed | Article 48 | [Status] | [Evidence] | [Date] |
| Registration in EU database | Article 49 | [Status] | [Registration ID] | [Date] |

**Quality Management System (if Annex VII):**
- **QMS Standard:** [e.g., ISO 9001]
- **Certification:** [Certification body, certificate number]
- **Notified Body:** [Name, identification number]
- **Assessment Report:** [Reference]

### 13.3 EU Declaration of Conformity

**Declaration Status:** [Draft / Signed / Not Yet Prepared]

**Declaration Details:**
- **Document Reference:** [Reference number]
- **Signatory:** [Name, role]
- **Date of Issue:** [Date]
- **Applicable Directives/Regulations:** EU AI Act (Regulation 2024/1689)
- **Harmonized Standards Applied:** [List]

### 13.4 CE Marking

**CE Marking Application:**
- **Applied:** [Yes / No / Planned]
- **Location:** [On product / In documentation / Both]
- **Format:** [Physical label / Digital / Both]
- **Compliance:** [Meets Regulation (EC) No 765/2008 requirements]

---

## 14. Post-Market Monitoring

### 14.1 Post-Market Monitoring System (Article 72)

**Monitoring Plan:** [Reference to separate post-market monitoring plan]

**Monitoring Objectives:**
- [Objective 1 - e.g., "Monitor performance in real-world use"]
- [Objective 2 - e.g., "Detect emerging risks"]
- [Objective 3 - e.g., "Collect user feedback"]

**Data Collection Methods:**

| Method | Frequency | Data Collected | Responsible Party |
|--------|-----------|----------------|-------------------|
| [Method 1] | [Frequency] | [Data types] | [Name/role] |
| [Method 2] | [Frequency] | [Data types] | [Name/role] |
| | | | |

### 14.2 Performance Monitoring

**Performance Metrics Tracked:**

| Metric | Target | Monitoring Frequency | Alert Threshold | Current Value |
|--------|--------|---------------------|-----------------|---------------|
| [Metric 1] | [Target] | [Frequency] | [Threshold] | [If deployed] |
| [Metric 2] | [Target] | [Frequency] | [Threshold] | [If deployed] |
| | | | | |

**Monitoring Dashboard:** [Reference to monitoring system/dashboard]

**Performance Reviews:**
- **Review Frequency:** [Monthly / Quarterly / Annually]
- **Review Team:** [Names/roles]
- **Last Review Date:** [Date]
- **Findings:** [Summary]

### 14.3 Incident Management (Article 73)

**Serious Incident Definition:** [How serious incidents are defined for this system]

**Incident Reporting Process:**
1. [Step 1 - e.g., "Detection and initial assessment"]
2. [Step 2 - e.g., "Notification to relevant authorities"]
3. [Step 3 - e.g., "Investigation and root cause analysis"]
4. [Step 4 - e.g., "Corrective and preventive actions"]
5. [Step 5 - e.g., "Follow-up and closure"]

**Incident Log:**

| Incident ID | Date | Description | Severity | Actions Taken | Status |
|-------------|------|-------------|----------|---------------|--------|
| [ID] | [Date] | [Description] | [L/M/H/Critical] | [Actions] | [Open/Closed] |
| | | | | | |

**Competent Authority Contact:**
- **Authority Name:** [National competent authority]
- **Contact:** [Email, phone]

### 14.4 Corrective Actions

**Corrective Action Process:**

| Action Type | Trigger | Process | Responsible Party |
|-------------|---------|---------|-------------------|
| Software Update | [Trigger condition] | [Process] | [Name/role] |
| Recall | [Trigger condition] | [Process] | [Name/role] |
| Market Withdrawal | [Trigger condition] | [Process] | [Name/role] |
| User Notification | [Trigger condition] | [Process] | [Name/role] |

**Corrective Actions Taken:**

| Date | Issue | Action | Effectiveness | Status |
|------|-------|--------|---------------|--------|
| [Date] | [Description] | [Action taken] | [Assessment] | [Complete/Ongoing] |
| | | | | |

---

## 15. Lifecycle Management

### 15.1 Modification Management

**Modification Log:**

| Version | Date | Type of Change | Rationale | Impact Assessment | Re-assessment Required |
|---------|------|----------------|-----------|-------------------|----------------------|
| [Version] | [Date] | [Substantial/Non-substantial] | [Reason] | [Impact] | [Yes/No] |
| | | | | | |

**Substantial Modification Criteria:** [Define what constitutes substantial modification requiring re-assessment]

**Change Control Process:**
1. [Step 1 - e.g., "Change request and justification"]
2. [Step 2 - e.g., "Impact assessment"]
3. [Step 3 - e.g., "Testing and validation"]
4. [Step 4 - e.g., "Documentation update"]
5. [Step 5 - e.g., "Deployment"]

### 15.2 Maintenance and Updates

**Maintenance Schedule:**

| Maintenance Type | Frequency | Last Performed | Next Scheduled | Responsible Party |
|-----------------|-----------|----------------|----------------|-------------------|
| Model Retraining | [Frequency] | [Date] | [Date] | [Name/role] |
| Software Updates | [Frequency] | [Date] | [Date] | [Name/role] |
| Security Patches | [As needed] | [Date] | [Continuous] | [Name/role] |
| Performance Tuning | [Frequency] | [Date] | [Date] | [Name/role] |

**Update Deployment Process:**
- **Testing Requirements:** [Testing before deployment]
- **Rollback Procedure:** [How to rollback if issues arise]
- **User Notification:** [How users are notified of updates]

### 15.3 Decommissioning

**Decommissioning Plan:** [Reference to decommissioning plan]

**Decommissioning Considerations:**
- **Data Disposal:** [How data will be securely deleted]
- **User Notification:** [How users/deployers will be notified]
- **Record Retention:** [Which records must be retained and for how long]
- **Alternative Arrangements:** [Plans for users transitioning away from system]

**End-of-Life Date:** [If known/planned]

---

## Appendices

### Appendix A: References

**Regulatory References:**
- Regulation (EU) 2024/1689 (EU AI Act)
- Regulation (EU) 2016/679 (GDPR)
- [Other applicable regulations]

**Standards and Guidelines:**
- [ISO/IEC standards referenced]
- [Industry guidelines]
- [Technical specifications]

**Internal Documents:**
- [Reference to related internal documents]

### Appendix B: Glossary

| Term | Definition |
|------|------------|
| [Term 1] | [Definition] |
| [Term 2] | [Definition] |
| | |

### Appendix C: Supporting Documentation Index

| Document Title | Document ID | Version | Location |
|---------------|-------------|---------|----------|
| Risk Assessment Report | [ID] | [Version] | [Location] |
| Validation Report | [ID] | [Version] | [Location] |
| Instructions for Use | [ID] | [Version] | [Location] |
| Training Data Documentation | [ID] | [Version] | [Location] |
| Conformity Assessment Report | [ID] | [Version] | [Location] |
| Post-Market Monitoring Plan | [ID] | [Version] | [Location] |
| | | | |

### Appendix D: Contact Information

**Provider Contact:**
- **Organization:** [Name]
- **Address:** [Full address]
- **Phone:** [Number]
- **Email:** [Email]
- **Website:** [URL]

**Technical Support:**
- **Contact:** [Name/department]
- **Email:** [Email]
- **Phone:** [Number]
- **Hours:** [Support hours]

**Compliance Contact:**
- **Contact:** [Name/role]
- **Email:** [Email]
- **Phone:** [Number]

---

## Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Technical Lead | [Name] | | |
| Compliance Officer | [Name] | | |
| Legal Counsel | [Name] | | |
| Authorized Representative | [Name] | | |

---

**End of Technical Documentation**

*This document must be kept up to date throughout the AI system's lifecycle and retained for 10 years after the system is placed on the market or put into service.*

*Document Version: [Version] | Last Updated: [Date]*
