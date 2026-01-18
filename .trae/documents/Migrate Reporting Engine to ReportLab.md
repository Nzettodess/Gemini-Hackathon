# Migration to ReportLab for PDF Generation

To resolve the `WeasyPrint` dependency issues on Windows (GTK libraries) and ensure reliable PDF generation, we will migrate the reporting engine to `ReportLab`.

## 1. Dependency Management
*   **Remove**: `weasyprint` (causes GTK errors).
*   **Add**: `reportlab` (Pure Python, no external DLLs required).

## 2. Code Refactoring (`reporting.py`)
*   Rewrite `ReportGenerator` to use `reportlab.platypus`.
*   Implement a standard layout:
    *   **Header**: Title, Date, System ID.
    *   **Summary Table**: Quality, Privacy, Bias status (with color coding).
    *   **Details Section**: Iterative lists for detected risks.
    *   **Footer**: Page numbers.

## 3. Implementation Steps
1.  Update `pyproject.toml` dependencies.
2.  Install `reportlab`.
3.  Rewrite `src/data_governance/reporting.py`.
4.  Verify with `try.py`.

This change is transparent to the MCP Server interface; `generate_conformity_report` will still work exactly the same way, just with a more robust backend.