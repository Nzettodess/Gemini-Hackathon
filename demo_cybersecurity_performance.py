#!/usr/bin/env python3

import argparse
import time
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    Console = None
    Panel = None
    Table = None
    RICH_AVAILABLE = False

from cybersecurity_assessment import run_assessment
from security_input import InMemoryRateLimiter, InputValidationError, validate_grafana_alert_payload


console = Console() if RICH_AVAILABLE else None


def _sample_grafana_payload(alert_count: int = 1):
    alerts = []
    for i in range(alert_count):
        alerts.append(
            {
                "labels": {
                    "alertname": f"Test Alert {i}",
                    "severity": "critical",
                    "risk_id": "safety-001",
                    "ai_system": "test_system",
                    "ai_system_id": "TEST-001",
                    "member_state": "EU",
                },
                "annotations": {
                    "summary": "Test critical safety alert",
                    "description": "This is a test alert for safety-001",
                    "article_reference": "Article 3(49)(a), Article 73(4)",
                    "reporting_deadline": "10 days",
                },
                "fingerprint": "test123456",
                "startsAt": "2026-01-01T00:00:00",
            }
        )

    return {"status": "firing", "alerts": alerts}


def benchmark_input_validation(iterations: int, alerts_per_payload: int) -> dict:
    payload = _sample_grafana_payload(alert_count=alerts_per_payload)

    start = time.perf_counter()
    ok = 0
    failed = 0
    for _ in range(iterations):
        try:
            validate_grafana_alert_payload(payload)
            ok += 1
        except InputValidationError:
            failed += 1
    elapsed = time.perf_counter() - start

    return {
        "iterations": iterations,
        "alerts_per_payload": alerts_per_payload,
        "elapsed_s": elapsed,
        "per_op_ms": (elapsed / max(iterations, 1)) * 1000.0,
        "ok": ok,
        "failed": failed,
    }


def benchmark_rate_limiter(iterations: int) -> dict:
    limiter = InMemoryRateLimiter()
    key = "demo:127.0.0.1"

    start = time.perf_counter()
    allowed = 0
    denied = 0
    for _ in range(iterations):
        if limiter.allow(key):
            allowed += 1
        else:
            denied += 1
    elapsed = time.perf_counter() - start

    return {
        "iterations": iterations,
        "elapsed_s": elapsed,
        "per_op_ms": (elapsed / max(iterations, 1)) * 1000.0,
        "allowed": allowed,
        "denied": denied,
    }


def benchmark_cybersecurity_assessment(scope: Path, system_description: str) -> dict:
    start = time.perf_counter()
    report = run_assessment(scope, system_description=system_description, excludes=None)
    elapsed = time.perf_counter() - start

    findings_count = len(report.findings)
    tools = report.tool_results
    skipped_tools = sum(1 for t in tools if t.get("status") == "skipped")
    failed_tools = sum(1 for t in tools if t.get("status") == "failed")

    return {
        "scope": str(scope),
        "elapsed_s": elapsed,
        "findings": findings_count,
        "tools_total": len(tools),
        "tools_skipped": skipped_tools,
        "tools_failed": failed_tools,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", default=".", help="Repository path to scan")
    parser.add_argument("--iterations", type=int, default=5000, help="Iterations for micro-benchmarks")
    parser.add_argument("--alerts-per-payload", type=int, default=3, help="Alerts per payload for validation benchmark")
    parser.add_argument(
        "--system-description",
        default="Python-based EU AI Act compliance tooling including metrics, incident management, and webhooks.",
    )
    args = parser.parse_args()

    scope = Path(args.scope).resolve()

    header = "Cybersecurity Performance Demo\nBenchmarks assessment runtime and input-validation throughput"
    if RICH_AVAILABLE:
        console.print(
            Panel.fit(
                "[bold cyan]Cybersecurity Performance Demo[/bold cyan]\n"
                "[dim]Benchmarks assessment runtime and input-validation throughput[/dim]",
                border_style="cyan",
            )
        )
    else:
        print("=" * 60)
        print(header)
        print("=" * 60)

    iv = benchmark_input_validation(iterations=args.iterations, alerts_per_payload=args.alerts_per_payload)
    rl = benchmark_rate_limiter(iterations=args.iterations)
    ca = benchmark_cybersecurity_assessment(scope=scope, system_description=args.system_description)

    rows = [
        ("Input validation", "iterations", str(iv["iterations"])),
        ("Input validation", "alerts/payload", str(iv["alerts_per_payload"])),
        ("Input validation", "elapsed (s)", f"{iv['elapsed_s']:.4f}"),
        ("Input validation", "per-op (ms)", f"{iv['per_op_ms']:.4f}"),
        ("Rate limiter", "iterations", str(rl["iterations"])),
        ("Rate limiter", "elapsed (s)", f"{rl['elapsed_s']:.4f}"),
        ("Rate limiter", "per-op (ms)", f"{rl['per_op_ms']:.4f}"),
        ("Rate limiter", "allowed/denied", f"{rl['allowed']}/{rl['denied']}"),
        ("Assessment", "scope", ca["scope"]),
        ("Assessment", "elapsed (s)", f"{ca['elapsed_s']:.2f}"),
        ("Assessment", "findings", str(ca["findings"])),
        ("Assessment", "tools skipped", str(ca["tools_skipped"])),
        ("Assessment", "tools failed", str(ca["tools_failed"])),
    ]

    if RICH_AVAILABLE:
        table = Table(title="Benchmarks", border_style="green")
        table.add_column("Benchmark", style="cyan", no_wrap=True)
        table.add_column("Metric", style="white")
        table.add_column("Value", style="yellow")
        for b, m, v in rows:
            table.add_row(b, m, v)
        console.print(table)
    else:
        for b, m, v in rows:
            print(f"{b:16} | {m:14} | {v}")


if __name__ == "__main__":
    main()
