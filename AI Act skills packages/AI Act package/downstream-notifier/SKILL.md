---
name: downstream-notifier
description: Automated email notification system for EU AI Act Article 13 compliance, featuring codebase change summarization and documentation distribution.
---

# Downstream Provider Notifier

Automate the provision of information (Article 13) to downstream deployers when an AI system is updated.

## When to use

Trigger when:

- "Notify our downstream providers about the latest code changes"
- "Send the Article 13 compliance package to deployers"
- "Summarize what changed in the system for our partners"

## Workflow

```
Downstream Notification Progress:
- [ ] Step 1: Detect changes (Git Diff or SQLite Snapshot)
- [ ] Step 2: Generate AI summary using Gemini (Article 13.3.c focus)
- [ ] Step 3: Identify recipients from examples/ directory
- [ ] Step 4: Generate compliance packages (JSON Manifest + Excel + PDF)
- [ ] Step 5: Log transaction
```

### Modes

- **Git Mode**: Automatic `git diff` detection for repositories.
- **Snapshot Mode**: SQLite-based file hashing (`examples/notices.db`) for tracking changes in local directories without git.

## Usage

### 1. Preparation

Place master templates in the `templates/` folder:

- `templates/Article_13_Compliance_Template.xlsx`
- `templates/Annex_XII_Provider_Template.xlsx`

Add provider-specific info as `*_Provider.xlsx` files in the `examples/` directory.

### 2. Execution

Run the notifier against your codebase:

```powershell
# Against a git repo
python scripts/notifier.py --repo "path/to/repo"

# Against a non-git directory (SQLite diffing)
python scripts/notifier.py --repo "path/to/folder"
```

### 3. Output

Each run creates a batch in `Output/Batch_[TIMESTAMP]/`:

- `Notice_[ID].json`: SMTP-ready manifest with To, Subject, and Attachment paths.
- `Article_13_[ID].xlsx`: Populated compliance template.
- `Summary_[ID].pdf`: AI-generated summary PDF.

## Testing

Unit tests are in `examples/tests/`. Run them with:

```powershell
python -m pytest examples/tests/test_notifier.py
```

## Quality Checklist

- [ ] Code changes correctly identified
- [ ] AI Summary is accurate and non-technical
- [ ] All 3+ providers from registry are processed
- [ ] Article 13 template is correctly attached
- [ ] Audit log is updated with timestamps and recipient IDs
