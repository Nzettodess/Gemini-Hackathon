# Regulatory Compliance Notification
**Provider:** Alpha Medical AI Solutions (AI-MED-2026-X1)
**Date:** 2026-01-17

## Newest Changes
- Added 'safety_score' float field to the State TypedDict.
- Updated 'model_node' to return a generated safety score.
- Implemented 'safety_moderator' function to filter outputs scoring < 0.8.
- Restructured LangGraph workflow to include the moderator node between model and END.
- Noted latency impact in codebase comments.

## Article 13 Perspective
The implementation of the 'safety_moderator' node significantly alters the transparency and robustness characteristics of the system, directly impacting Article 13.3(b)(ii) and (iii). The documentation has been updated to reflect the new deterministic blocking mechanism where a safety score below 0.8 results in a suppressed output ('Blocked: Security Risk'). This introduces a trade-off between safety and availability that must be communicated to deployers. Additionally, the change increases the computational latency (Article 13.3(e)) and necessitates new log interpretation guidance (Article 13.3(f)) to monitor the rate of blocked requests.

---
*Please refer to the attached Excel documentation for full Article 13 and Annex XII compliance details.*