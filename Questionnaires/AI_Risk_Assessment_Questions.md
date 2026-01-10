# AI Risk Assessment Questionnaire

**Based on EU AI Act and NIST AI RMF**

---

## Section 1: Initial Classification Questions

### 1.1 AI System Use Case

**Q1. What is the primary use case of your AI system?**

Select one:
- [ ] Social Scoring (evaluating individuals based on social behavior)
- [ ] Subliminal Manipulation (techniques beyond user awareness)
- [ ] Vulnerability Exploitation (targeting age, disability, social situation)
- [ ] Facial Recognition Scraping (building databases from internet/CCTV)
- [ ] Predictive Policing (crime prediction for individuals)
- [ ] Emotion Recognition
- [ ] Biometric Identification
- [ ] Credit Scoring
- [ ] Recruitment Screening
- [ ] Performance Monitoring
- [ ] Chatbot / Conversational AI
- [ ] Deepfake / Synthetic Content Generation
- [ ] Content Generation (text, image, audio)
- [ ] Recommendation System
- [ ] Game AI
- [ ] Spam Filter
- [ ] Other: _________________________

---

### 1.2 Deployment Context

**Q2. Who is deploying this AI system?**

- [ ] Public Authority (government, public institution)
- [ ] Private Sector Organization
- [ ] Other: _________________________

**Q3. In what context will this AI system be deployed?**

- [ ] Workplace (employee-facing)
- [ ] Educational Institution
- [ ] Healthcare Setting
- [ ] Law Enforcement
- [ ] General/Consumer-facing
- [ ] Other: _________________________

---

### 1.3 AI System Category

**Q4. What category does your AI system fall under?**

- [ ] Biometrics (identification, categorization, emotion recognition)
- [ ] Critical Infrastructure (transport, water, gas, electricity, digital)
- [ ] Education (access decisions, exam evaluation, behavior assessment)
- [ ] Employment (recruitment, job ads, performance, promotion/termination)
- [ ] Essential Services (credit, insurance, emergency services)
- [ ] Law Enforcement (risk assessment, evidence evaluation, profiling)
- [ ] Migration/Asylum (border control, visa/asylum processing)
- [ ] Justice/Democracy (judicial assistance, election influence)
- [ ] General Purpose (no specific high-risk category)

---

## Section 2: Prohibited Practices Screening

### 2.1 Social Scoring Check

**Q5. Does your AI system evaluate or score natural persons based on their social behavior or personal characteristics for general purposes by public authorities?**

- [ ] Yes → **PROHIBITED: System cannot be deployed**
- [ ] No → Continue to next question

---

### 2.2 Manipulation Check

**Q6. Does your AI system use subliminal techniques beyond a person's consciousness to materially distort behavior in a manner that causes harm?**

- [ ] Yes → **PROHIBITED: System cannot be deployed**
- [ ] No → Continue to next question

---

### 2.3 Vulnerability Exploitation Check

**Q7. Does your AI system exploit vulnerabilities of specific groups (age, disability, social/economic situation) to materially distort behavior?**

- [ ] Yes → **PROHIBITED: System cannot be deployed**
- [ ] No → Continue to next question

---

### 2.4 Facial Recognition Database Check

**Q8. Does your AI system involve untargeted scraping of facial images from the internet or CCTV to build facial recognition databases?**

- [ ] Yes → **PROHIBITED: System cannot be deployed**
- [ ] No → Continue to next question

---

### 2.5 Predictive Policing Check

**Q9. Does your AI system predict crime risk for individuals based SOLELY on profiling or personality traits?**

- [ ] Yes → **PROHIBITED: System cannot be deployed**
- [ ] No → Continue to next question

---

### 2.6 Emotion Recognition in Workplace/Education

**Q10. If your system uses emotion recognition in workplace or educational settings, is it for medical or safety purposes?**

- [ ] Not applicable (no emotion recognition in workplace/education)
- [ ] Yes, for medical or safety purposes → **PERMITTED with conditions**
- [ ] No, for other purposes → **PROHIBITED: System cannot be deployed in this context**

---

## Section 3: High-Risk Classification

*Answer these questions if your system passed the prohibited practices screening.*

### 3.1 Biometrics Category

**Q11. Does your AI system involve:**

- [ ] Remote biometric identification systems
- [ ] Biometric categorization (inferring race, political opinions, religion)
- [ ] Emotion recognition systems
- [ ] None of the above

*If any selected (except "None") → Classified as HIGH-RISK*

---

### 3.2 Critical Infrastructure Category

**Q12. Is your AI system a safety component in:**

- [ ] Road traffic management
- [ ] Water, gas, heating, or electricity supply
- [ ] Digital infrastructure
- [ ] None of the above

*If any selected (except "None") → Classified as HIGH-RISK*

---

### 3.3 Education Category

**Q13. Does your AI system make decisions regarding:**

- [ ] Access to educational or vocational institutions
- [ ] Evaluation of learning outcomes (exams)
- [ ] Behavior assessment in educational institutions
- [ ] None of the above

*If any selected (except "None") → Classified as HIGH-RISK*

---

### 3.4 Employment Category

**Q14. Does your AI system involve:**

- [ ] Recruitment or candidate filtering
- [ ] Job advertisement targeting
- [ ] Application evaluation
- [ ] Promotion or termination decisions
- [ ] Task allocation based on behavior/traits
- [ ] Employee performance monitoring
- [ ] None of the above

*If any selected (except "None") → Classified as HIGH-RISK*

---

### 3.5 Essential Services Category

**Q15. Does your AI system involve:**

- [ ] Credit scoring or creditworthiness assessment
- [ ] Risk assessment for life or health insurance
- [ ] Emergency services dispatch prioritization
- [ ] None of the above

*If any selected (except "None") → Classified as HIGH-RISK*

---

### 3.6 Law Enforcement Category

**Q16. Does your AI system assist with:**

- [ ] Individual risk assessment (re-offending probability)
- [ ] Polygraph or similar detection tools
- [ ] Evidence reliability assessment
- [ ] Crime prediction for individuals or groups
- [ ] Profiling during criminal investigations
- [ ] None of the above

*If any selected (except "None") → Classified as HIGH-RISK*

---

### 3.7 Migration/Asylum Category

**Q17. Does your AI system involve:**

- [ ] Polygraph or similar tools at borders
- [ ] Risk assessment for security, health, or irregular entry
- [ ] Travel document authenticity verification
- [ ] Asylum, visa, or residence application processing
- [ ] None of the above

*If any selected (except "None") → Classified as HIGH-RISK*

---

### 3.8 Justice/Democracy Category

**Q18. Does your AI system:**

- [ ] Assist judicial research or interpretation of law
- [ ] Apply law to facts in legal cases
- [ ] Facilitate alternative dispute resolution
- [ ] Influence elections or referendums
- [ ] None of the above

*If any selected (except "None") → Classified as HIGH-RISK*

---

## Section 4: Limited Risk (Transparency) Check

*Answer if NOT classified as High-Risk*

### 4.1 Transparency Obligations

**Q19. Does your AI system involve:**

- [ ] Chatbot interactions where users might not know they're interacting with AI
- [ ] Emotion recognition (not in workplace/education)
- [ ] Deepfake or synthetic content generation
- [ ] AI-generated content (text, image, audio, video)
- [ ] None of the above

*If any selected (except "None") → Classified as LIMITED RISK*

---

## Section 5: Risk Classification Result

Based on your answers:

| Classification | Result |
|----------------|--------|
| **UNACCEPTABLE** | If any "PROHIBITED" answer in Section 2 |
| **HIGH-RISK** | If any high-risk category in Section 3 |
| **LIMITED RISK** | If any transparency obligation in Section 4 |
| **MINIMAL RISK** | If none of the above apply |

---

## Section 6: High-Risk Compliance Requirements

*Complete only if classified as HIGH-RISK*

### 6.1 Risk Management System (Article 9)

- [ ] Continuous risk management process established
- [ ] Known and foreseeable risks identified
- [ ] Risk levels estimated
- [ ] Emerging risks evaluated
- [ ] Mitigation measures adopted
- [ ] Decisions documented
- [ ] Testing conducted against defined metrics
- [ ] Testing with representative data
- [ ] Testing for foreseeable misuse
- [ ] Independent party testing (where appropriate)

### 6.2 Data Governance (Article 10)

- [ ] Training data documented
- [ ] Data quality management implemented
- [ ] Bias examination conducted
- [ ] Data relevance verified
- [ ] Data representativeness checked
- [ ] Special category data handling compliant

### 6.3 Technical Documentation (Article 11)

- [ ] General description documented
- [ ] Intended purpose specified
- [ ] Design specifications created
- [ ] System architecture documented
- [ ] Data requirements specified
- [ ] Training methodologies documented
- [ ] Validation procedures defined
- [ ] Performance metrics recorded
- [ ] Risk management system documented
- [ ] Cybersecurity measures documented
- [ ] Modification log maintained

### 6.4 Record Keeping (Article 12)

- [ ] Automatic logging implemented
- [ ] Operational logs captured
- [ ] User identity recorded
- [ ] Date/time of use logged
- [ ] Reference input data stored
- [ ] Output data retained
- [ ] Appropriate retention period defined

### 6.5 Transparency (Article 13)

- [ ] Clear instructions for use created
- [ ] Provider identity disclosed
- [ ] System capabilities documented
- [ ] System limitations disclosed
- [ ] Accuracy levels specified
- [ ] Foreseeable risks documented
- [ ] Human oversight measures described
- [ ] Maintenance requirements specified

### 6.6 Human Oversight (Article 14)

- [ ] System designed for human oversight
- [ ] Operators can understand capabilities and limitations
- [ ] Operators can monitor operation correctly
- [ ] Measures to detect automation bias
- [ ] Operators can interpret outputs correctly
- [ ] Override/interrupt capability provided
- [ ] Option to disregard AI output available

---

## Section 7: Additional Requirements for Biometrics

*Complete only if system involves biometrics*

- [ ] Fundamental rights impact assessment conducted
- [ ] System registered in EU AI database

---

## Appendix: Risk Level Summary

| Risk Level | Requirements |
|------------|--------------|
| **Unacceptable** | System BANNED - Discontinue development |
| **High-Risk** | Full compliance with Articles 9-15 required |
| **Limited Risk** | Disclosure and transparency mechanisms required |
| **Minimal Risk** | Voluntary codes of conduct recommended |

---

*Document generated based on EU AI Act requirements and NIST AI RMF guidance*

*Date: _______________*

*Assessed by: _______________*

*Signature: _______________*
