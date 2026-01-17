# Downstream Provider Notification Plugin (EU AI Act)

This plugin automates the generation of **Article 13 (Transparency)** and **Annex XII (GPAI)** compliance notices for downstream providers. It analyzes code changes in an AI system's repository and intelligently populates an official Excel compliance template with technical details.

## Features

- **Code-to-Compliance**: Scans git diffs to detect architectural changes (e.g., new models, API layers).
- **Rich Template Filling**: Populates complex Excel templates including "Instructions for Use", "Risk Classification", and "Log Retention" policies.
- **Dynamic Reasoning**: Uses Gemini to infer compliance status (Yes/No) and generate specific, context-aware technical descriptions (e.g., "Accuracy metrics methodology validated" instead of generic placeholders).
- **Annex XII Integration**: Merges upstream GPAI model data (from JSON input) into the downstream provider's documentation.

---

## Integration Guide

### 1. Backend Connection

The backend should trigger the `notifier.py` script as a subprocess or job step whenever a new release is cut or a significant change is detected in the AI system's repository.

**CLI Command:**

```bash
python scripts/notifier.py --repo /path/to/target/repo --examples examples/ --templates templates/
```

### 2. Input Data Structure

The plugin expects two types of inputs in the `examples/` directory (or directory specified by `--examples`):

**A. Provider Metadata (JSON)**
Each downstream provider to be notified must have a corresponding `*_AnnexXII.json` file. This file contains their specific details and the GPAI model info they are using.
*File Naming:* `[ProviderName]_AnnexXII.json`
*Format:*

```json
{
  "provider_name": "Alpha Medical AI Solutions",
  "provider_id": "AI-MED-2026-X1",
  "contact_email": "compliance@alphamed.ai",
  "intended_tasks": "Medical summarization",
  ...
}
```

**B. Rich Context (Excel)**
For high-fidelity filling of technical fields (e.g., exact accuracy numbers, hardware specs), provide a `Fake_Annex_XII_Input.xlsx` (or similarly named context file). The script reads filled cells from this "Input" sheet to overwrite generic AI logic with ground-truth data.

### 3. Output

The plugin generates a timestamped batch folder in `Output/`.
**Example Output Location:** `Output/Batch_20260117_033655/` (Contains verified Alpha Medical Notice).

Inside, you will find:

1. **Compliance Notice (Excel)**: `Article_13_Compliance_[ProviderID].xlsx` - The fully filled legal document.
2. **Manifest (JSON)**: `Notice_[ProviderID].json` - A machine-readable summary of the generation run, including file paths and status.

### 4. Automated Emailing

The generate JSON manifest (`Notice_[ProviderID].json`) is designed to trigger automated notifications.
- **Field**: `contact_email` (from the input JSON) is preserved in the output manifest.
- **Action**: Your backend can parse this JSON, extract the email, and send the generated `Article_13_Compliance_*.xlsx` as an attachment to the downstream provider.

### 5. Configuration

- **API Key**: Ensure `GEMINI_API_KEY` is set in the environment variables (or `.env` file).
- **Templates**: Place the official `Article_13_Compliance_Template.xlsx` in the `templates/` directory.

---

## Example Workflow

1. **Dev Team** pushes code to `repo/`.
2. **CI/CD Pipeline** runs `notifier.py`.
3. **Plugin** extracts diffs, reads `Alpha_Medical_AnnexXII.json`.
4. **Plugin** fills `Article_13_Compliance_Template.xlsx` with:
    - Code analysis from Gemini.
    - Static data from JSON.
    - Rich details from `Fake_Annex_XII_Input.xlsx`.
5. **Output** Excel file is emailed to the Compliance Officer.
