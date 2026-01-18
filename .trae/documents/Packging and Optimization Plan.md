# MCP Packaging and Optimization Plan

## 1. MCP Packaging and Distribution
To allow others to use your Data Governance MCP, we need to package it properly.

### Packaging Strategy
*   **Standard Python Package**: Use `pyproject.toml` (already exists) to define dependencies and entry points.
*   **Entry Points**: Add `[project.scripts]` to allow running `data-gov-server` directly from the command line after installation.
*   **Dockerization**: Create a `Dockerfile` so users can run the server in an isolated container without managing Python environments manually.

### Usage Instructions for End Users
Once packaged, users will typically follow these steps:
1.  **Installation**: `pip install data-governance` (or pull Docker image).
2.  **Configuration**: Add the server to their AI Client config (e.g., `claude_desktop_config.json` or `cursor.json`).
    *   *Example Config*:
        ```json
        "mcpServers": {
          "data-governance": {
            "command": "data-gov-server",
            "args": []
          }
        }
        ```
3.  **Interaction**: Users open their AI Chat (Claude/Cursor) and say: "Scan this dataset for privacy risks" or "Analyze the bias in this CSV". The AI will automatically call your tools.

## 2. Industrial-Grade Optimization Roadmap
Based on your "Avis de groupe" and high-risk AI requirements, here is the gap analysis and optimization plan.

### A. Functional Expansion (New Modules)
*   **🌍 Environmental Risk (New)**:
    *   **Goal**: Measure the carbon footprint of AI inference/training.
    *   **Tool**: Integrate `codecarbon`.
    *   **Implementation**: Add a decorator or context manager to measure energy usage during model execution tasks.
*   **🛡️ Cybersecurity Risk (New)**:
    *   **Goal**: Detect prompt injections and jailbreaks.
    *   **Tool**: Integrate `rebuff` or `llm-guard` (or simple keyword/heuristic blocking as a start).
    *   **Implementation**: Add a `scan_prompt_security` tool.
*   **⚖️ Human Rights/Fairness (Enhance)**:
    *   **Current**: Basic bias detection (Fairlearn).
    *   **Upgrade**: Add "Disparate Impact" thresholds compliant with EU AI Act (e.g., 80% rule) and generate a formal "Conformity Assessment" report.

### B. Technical Architecture (Industrial Scale)
*   **Performance**:
    *   *Current*: Pandas (in-memory). Fails on large files (>1GB).
    *   *Upgrade*: Switch to `Polars` or `DuckDB` for streaming large datasets without OOM errors.
*   **Security & Isolation**:
    *   *Risk*: Running arbitrary analysis code is dangerous.
    *   *Upgrade*: Run the actual analysis workers in isolated Docker containers or sandboxes, separate from the MCP server handling the requests.
*   **API & Integration**:
    *   *Current*: Local MCP.
    *   *Upgrade*: Expose a REST API alongside MCP so standard CI/CD pipelines (GitHub Actions/GitLab CI) can call it without an LLM.

## 3. Implementation Plan (Next Steps)
I will implement the following immediately to demonstrate the "Industrial" upgrade:

1.  **Package**: Update `pyproject.toml` with entry points and add `Dockerfile`.
2.  **Environment Module**: Add `codecarbon` dependency and a basic `track_energy` tool.
3.  **Security Module**: Add a basic `scan_prompt` tool using regex/heuristics (mocking a heavy security scanner).
4.  **Refactor**: Update `server.py` to include these new tools.

Shall I proceed with this plan?