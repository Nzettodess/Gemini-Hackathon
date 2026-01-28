#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


_REPO_ROOT = Path(__file__).resolve().parent

_DEFAULT_EXCLUDES = {
    ".git",
    ".venv",
    "__pycache__",
    "Output",
    "incidents",
    "change_management",
    "AI Act skills packages",
    "Risks packages",
}


@dataclass
class ToolResult:
    name: str
    status: str
    details: str
    stdout: str = ""
    stderr: str = ""


@dataclass
class Finding:
    category: str
    severity: str
    title: str
    evidence: str
    recommendation: str


@dataclass
class CybersecurityAssessmentReport:
    generated_at: str
    scope_root: str
    eu_ai_act_alignment: Dict[str, Any]
    tool_results: List[Dict[str, Any]]
    findings: List[Dict[str, Any]]
    summary: Dict[str, Any]


_SECRET_PATTERNS: List[Tuple[str, re.Pattern[str]]] = [
    ("Private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b")),
    ("Generic API key", re.compile(r"(?i)\b(api[_-]?key|secret|token)\b\s*[:=]\s*['\"]?[0-9a-zA-Z_\-]{16,}['\"]?")),
]


def _iter_text_files(root: Path, excludes: set[str]) -> List[Path]:
    paths: List[Path] = []
    for p in root.rglob("*"):
        rel_parts = set(p.relative_to(root).parts)
        if rel_parts & excludes:
            continue
        if not p.is_file():
            continue
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".mov", ".xlsx"}:
            continue
        if p.stat().st_size > 2_000_000:
            continue
        paths.append(p)
    return paths


def _scan_secrets(root: Path, excludes: set[str]) -> List[Finding]:
    findings: List[Finding] = []
    for path in _iter_text_files(root, excludes):
        try:
            content = path.read_text(errors="ignore")
        except Exception:
            continue

        for label, pat in _SECRET_PATTERNS:
            if pat.search(content):
                findings.append(
                    Finding(
                        category="secrets_management",
                        severity="high",
                        title=f"Potential secret detected: {label}",
                        evidence=str(path.relative_to(root)),
                        recommendation="Rotate impacted credentials, remove secrets from repo history, and enforce secret scanning in CI.",
                    )
                )
    return findings


def _scan_code_patterns(root: Path, excludes: set[str]) -> List[Finding]:
    checks: List[Tuple[str, str, str, re.Pattern[str], str]] = [
        (
            "security_code_review",
            "medium",
            "Use of eval/exec",
            re.compile(r"\b(eval|exec)\s*\("),
            "Avoid dynamic code execution. If unavoidable, strictly constrain inputs and use safe parsers.",
        ),
        (
            "security_code_review",
            "medium",
            "subprocess with shell=True",
            re.compile(r"subprocess\.(?:Popen|run|call|check_call|check_output)\([^\n]*shell\s*=\s*True"),
            "Avoid shell=True. Prefer argv lists and validate inputs. If required, hardcode commands and escape arguments.",
        ),
        (
            "security_code_review",
            "low",
            "Potential insecure YAML load",
            re.compile(r"yaml\.load\("),
            "Use yaml.safe_load for untrusted YAML.",
        ),
    ]

    findings: List[Finding] = []
    for path in _iter_text_files(root, excludes):
        if path.suffix.lower() not in {".py", ".js", ".ts", ".tsx", ".sh", ".yaml", ".yml"}:
            continue
        try:
            content = path.read_text(errors="ignore")
        except Exception:
            continue

        for category, severity, title, pat, rec in checks:
            if pat.search(content):
                findings.append(
                    Finding(
                        category=category,
                        severity=severity,
                        title=title,
                        evidence=str(path.relative_to(root)),
                        recommendation=rec,
                    )
                )

    return findings


def _run_optional_tool(name: str, args: List[str], cwd: Path) -> ToolResult:
    exe = shutil.which(args[0])
    if not exe:
        return ToolResult(name=name, status="skipped", details=f"'{args[0]}' not found in PATH")

    try:
        proc = subprocess.run(
            args,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
            timeout=300,
        )
        status = "passed" if proc.returncode == 0 else "failed"
        return ToolResult(
            name=name,
            status=status,
            details=f"Exit code {proc.returncode}",
            stdout=(proc.stdout or "")[:50_000],
            stderr=(proc.stderr or "")[:50_000],
        )
    except subprocess.TimeoutExpired:
        return ToolResult(name=name, status="failed", details="Timed out")
    except Exception as e:
        return ToolResult(name=name, status="failed", details=f"Error: {e}")


def _threat_model_with_llm(system_description: str) -> Optional[str]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        from google import genai
    except Exception:
        return None

    try:
        client = genai.Client(api_key=api_key)
        prompt = (
            "You are a cybersecurity architect. Produce a concise threat model for the described system. "
            "Use STRIDE categories. Provide: assets, trust boundaries, entry points, threats, mitigations, and validation checks.\n\n"
            f"SYSTEM DESCRIPTION:\n{system_description}\n"
        )
        resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return (resp.text or "").strip()[:30_000]
    except Exception:
        return None


def _summarize(findings: List[Finding], tool_results: List[ToolResult]) -> Dict[str, Any]:
    sev_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1

    top = sorted(findings, key=lambda f: sev_order.get(f.severity, 0), reverse=True)[:10]
    tools_failed = [t.name for t in tool_results if t.status == "failed"]

    return {
        "finding_counts": counts,
        "top_findings": [asdict(f) for f in top],
        "tools_failed": tools_failed,
    }


def run_assessment(scope_root: Path, system_description: str, excludes: Optional[List[str]] = None) -> CybersecurityAssessmentReport:
    exclude_set = set(excludes or []) | _DEFAULT_EXCLUDES

    findings: List[Finding] = []
    findings.extend(_scan_secrets(scope_root, exclude_set))
    findings.extend(_scan_code_patterns(scope_root, exclude_set))

    tool_results = [
        _run_optional_tool("Bandit (Python SAST)", ["bandit", "-q", "-r", str(scope_root)], cwd=scope_root),
        _run_optional_tool("pip-audit (deps)", ["pip-audit"], cwd=scope_root),
        _run_optional_tool("gitleaks (secrets)", ["gitleaks", "detect", "--no-git"], cwd=scope_root),
    ]

    threat_model = _threat_model_with_llm(system_description)
    if threat_model:
        findings.append(
            Finding(
                category="threat_modeling",
                severity="low",
                title="LLM-generated threat model (review required)",
                evidence=threat_model,
                recommendation="Have a security engineer validate and refine; convert mitigations into backlog items and tests.",
            )
        )
    else:
        findings.append(
            Finding(
                category="threat_modeling",
                severity="low",
                title="Threat modeling not generated (missing GEMINI_API_KEY or google-genai)",
                evidence="N/A",
                recommendation="Provide GEMINI_API_KEY and ensure google-genai is installed to generate a draft threat model, then validate with experts.",
            )
        )

    summary = _summarize(findings, tool_results)

    eu_ai_act_alignment = {
        "article_15_1": {
            "keywords": ["system security", "data protection", "attack prevention"],
            "controls_covered": ["threat_modeling", "security_code_review", "vulnerability_assessment", "secrets_management"],
        },
        "article_15_4": {
            "keywords": ["system integrity", "injection attack prevention", "attack prevention"],
            "controls_covered": ["input_validation", "rate_limiting", "sanitization"],
        },
    }

    return CybersecurityAssessmentReport(
        generated_at=datetime.now().isoformat(),
        scope_root=str(scope_root),
        eu_ai_act_alignment=eu_ai_act_alignment,
        tool_results=[asdict(t) for t in tool_results],
        findings=[asdict(f) for f in findings],
        summary=summary,
    )


def _to_markdown(report: CybersecurityAssessmentReport) -> str:
    lines: List[str] = []
    lines.append(f"# Cybersecurity Assessment Report")
    lines.append("")
    lines.append(f"Generated at: `{report.generated_at}`")
    lines.append(f"Scope: `{report.scope_root}`")
    lines.append("")

    lines.append("## EU AI Act Alignment")
    lines.append("")
    lines.append("- Article 15(1): system security, data protection, attack prevention")
    lines.append("- Article 15(4): resilience against attacks / integrity controls")
    lines.append("")

    lines.append("## Automated Tool Results")
    lines.append("")
    for t in report.tool_results:
        lines.append(f"- **{t['name']}**: `{t['status']}` ({t['details']})")
    lines.append("")

    lines.append("## Findings")
    lines.append("")
    for f in report.findings:
        lines.append(f"### {f['severity'].upper()}: {f['title']}")
        lines.append("")
        lines.append(f"- Category: `{f['category']}`")
        lines.append(f"- Evidence: {f['evidence'] if f['category'] == 'threat_modeling' else '`' + f['evidence'] + '`'}")
        lines.append(f"- Recommendation: {f['recommendation']}")
        lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(report.summary, indent=2))
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", default=str(_REPO_ROOT), help="Root directory to assess")
    parser.add_argument("--output", default=str(_REPO_ROOT / "Output" / "CYBERSECURITY_ASSESSMENT.md"))
    parser.add_argument("--json-output", default=str(_REPO_ROOT / "Output" / "CYBERSECURITY_ASSESSMENT.json"))
    parser.add_argument(
        "--system-description",
        default="Python-based EU AI Act compliance tooling including metrics, incident management, and webhooks.",
    )
    parser.add_argument("--exclude", action="append", default=[], help="Additional directory/file names to exclude")
    args = parser.parse_args()

    scope = Path(args.scope).resolve()
    report = run_assessment(scope, args.system_description, excludes=args.exclude)

    out_md = Path(args.output)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(_to_markdown(report))

    out_json = Path(args.json_output)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(asdict(report), indent=2))

    print(str(out_md))


if __name__ == "__main__":
    main()
