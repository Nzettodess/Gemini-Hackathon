# Downstream Notifier: AI Act Article 13 Compliance

## Overview

The **Downstream Notifier** is an automated compliance tool designed to help high-risk AI providers fulfill their transparency obligations under **Article 13** and **Annex XII** of the EU AI Act.

It automatically analyzes code changes in your AI system, generates human-readable compliance summaries using **Gemini**, and populates official regulatory templates (Excel/PDF) for distribution to downstream providers (deployers).

## Features

- **Code-to-Compliance**: Scans your Git repo or a specific directory for technical changes.
- **Multi-Standards Support**:
  - **Article 13 (Instructions for Use)**: Generates user manuals, capability descriptions, and maintenance instructions.
  - **Annex XII (GPAI)**: Autofills documentation for General Purpose AI models (tasks, modalities, compute resources).
- **Automated Excel Injection**:
  - Intelligence mapping to fill "Instructions for Use", "Compliance Checklist", and "Document Metadata" sheets.
  - Handles "Yes/No" checklist indicators automatically.
- **Personalized Branding**: Injects your Provider Name, ID, Contacts, and System Version into the headers of every document.
- **Dual Output**: Prodces both an edited **Excel (.xlsx)** for official records and a **PDF Summary** for quick reading.

## Setup & Installation

1. **Prerequisites**:
   - Python 3.10+
   - A Google Cloud Project with Gemini API access.

2. **Installation**:

   ```bash
   cd downstream-notifier
   pip install -r requirements.txt
   ```

3. **Configuration**:
   - Create a `.env` file in the root directory (or ensure one exists in your project root).
   - Add your Gemini API key:

     ```ini
     GEMINI_API_KEY=your_api_key_here
     ```

## Usage

### Basic Run

To scan the current repository and generate a notification package:

```bash
python scripts/notifier.py
```

### Advanced Options

- **Scan a specific repository**:

  ```bash
  python scripts/notifier.py --repo path/to/your/code
  ```

- **Use custom provider profiles** (for testing/multi-tenant):

  ```bash
  python scripts/notifier.py --examples path/to/provider_excels
  ```

- **Manual Input** (skip code scan):

  ```bash
  python scripts/notifier.py --manual "Refactored the safety filter to increase strictness by 20%."
  ```

## Output

All generated documents are stored in the `Output/Batch_{TIMESTAMP}` directory:

- `Article_13_Compliance_{ProviderID}.xlsx`: The requested regulatory file.
- `Annex_XII_Provider_{ProviderID}.xlsx`: GPAI documentation.
- `Summary_{ProviderID}.pdf`: Detailed change summary.
- `run_manifest.json`: Machine-readable log of the generation event.

## Troubleshooting

- **Unicode Errors**: Ensure your terminal supports UTF-8. The script has been hardened to strip emojis for compatibility.
- **Missing API Key**: The script looks for `.env` in the current and parent directories. Verify your key is robust.
