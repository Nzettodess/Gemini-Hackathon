#!/usr/bin/env python3

import argparse
import json
import random
import time
from datetime import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.live import Live
    from rich.layout import Layout
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    Console = None
    Panel = None
    Table = None
    RICH_AVAILABLE = False

from security_monitoring import SecurityMonitor, SecurityEvent, create_sample_event

try:
    from incident_management import IncidentManager
    INCIDENT_MGMT_AVAILABLE = True
except ImportError:
    INCIDENT_MGMT_AVAILABLE = False
    IncidentManager = None


console = Console() if RICH_AVAILABLE else None


class SecurityMonitoringDemo:
    def __init__(self, use_ai: bool = True, enable_incidents: bool = True):
        self.incident_manager = None
        if enable_incidents and INCIDENT_MGMT_AVAILABLE:
            self.incident_manager = IncidentManager(use_ai=use_ai)
        
        self.monitor = SecurityMonitor(use_ai=use_ai, incident_manager=self.incident_manager)
        self.event_count = 0
        self.threat_count = 0

    def simulate_normal_traffic(self, count: int = 10) -> None:
        endpoints = ["/api/data", "/api/users", "/api/health", "/api/metrics"]
        methods = ["GET", "POST", "PUT"]
        ips = ["192.168.1.100", "192.168.1.101", "192.168.1.102"]
        
        for i in range(count):
            event = create_sample_event(
                event_id=f"EVT-{self.event_count:06d}",
                endpoint=random.choice(endpoints),
                method=random.choice(methods),
                source_ip=random.choice(ips),
                status_code=random.choice([200, 200, 200, 201, 304]),
                response_time_ms=random.uniform(50, 300),
                metadata={"user_id": f"user_{random.randint(1, 100)}"}
            )
            self.event_count += 1
            
            threat = self.monitor.ingest_event(event)
            if threat:
                self.threat_count += 1

    def simulate_rate_limit_attack(self) -> None:
        attacker_ip = "10.0.0.666"
        
        for i in range(150):
            event = create_sample_event(
                event_id=f"EVT-{self.event_count:06d}",
                endpoint="/api/data",
                method="GET",
                source_ip=attacker_ip,
                status_code=200,
                response_time_ms=random.uniform(100, 200),
                metadata={"suspicious": True}
            )
            self.event_count += 1
            
            threat = self.monitor.ingest_event(event)
            if threat:
                self.threat_count += 1

    def simulate_sql_injection_attempt(self) -> None:
        event = create_sample_event(
            event_id=f"EVT-{self.event_count:06d}",
            endpoint="/api/users",
            method="POST",
            source_ip="203.0.113.42",
            status_code=400,
            response_time_ms=50.0,
            metadata={
                "query": "SELECT * FROM users WHERE id = '1' OR '1'='1'",
                "payload": {"username": "admin' OR '1'='1"}
            }
        )
        self.event_count += 1
        
        threat = self.monitor.ingest_event(event)
        if threat:
            self.threat_count += 1

    def simulate_xss_attempt(self) -> None:
        event = create_sample_event(
            event_id=f"EVT-{self.event_count:06d}",
            endpoint="/api/comments",
            method="POST",
            source_ip="198.51.100.23",
            status_code=400,
            response_time_ms=75.0,
            metadata={
                "comment": "<script>alert('XSS')</script>",
                "user_agent": "Mozilla/5.0 <script>malicious</script>"
            }
        )
        self.event_count += 1
        
        threat = self.monitor.ingest_event(event)
        if threat:
            self.threat_count += 1

    def simulate_error_spike(self) -> None:
        for i in range(15):
            event = create_sample_event(
                event_id=f"EVT-{self.event_count:06d}",
                endpoint="/api/process",
                method="POST",
                source_ip="192.168.1.100",
                status_code=500,
                response_time_ms=random.uniform(2000, 5000),
                metadata={"error": "Internal server error"}
            )
            self.event_count += 1
            
            threat = self.monitor.ingest_event(event)
            if threat:
                self.threat_count += 1

    def run_full_demo(self) -> None:
        if RICH_AVAILABLE:
            console.print(Panel.fit(
                "[bold cyan]Security Monitoring & Alerting Demo[/bold cyan]\n"
                "[dim]Real-time threat detection with EU AI Act Article 15 & 73 compliance[/dim]",
                border_style="cyan"
            ))
        else:
            print("=" * 60)
            print("Security Monitoring & Alerting Demo")
            print("Real-time threat detection with EU AI Act Article 15 & 73 compliance")
            print("=" * 60)

        scenarios = [
            ("Normal Traffic", self.simulate_normal_traffic, 20),
            ("SQL Injection Attack", self.simulate_sql_injection_attempt, None),
            ("XSS Attack Attempt", self.simulate_xss_attempt, None),
            ("Rate Limit Attack", self.simulate_rate_limit_attack, None),
            ("Error Spike", self.simulate_error_spike, None),
            ("More Normal Traffic", self.simulate_normal_traffic, 30),
        ]

        for scenario_name, scenario_func, arg in scenarios:
            if RICH_AVAILABLE:
                console.print(f"\n[yellow]→ Simulating: {scenario_name}[/yellow]")
            else:
                print(f"\n→ Simulating: {scenario_name}")
            
            if arg is not None:
                scenario_func(arg)
            else:
                scenario_func()
            
            time.sleep(0.5)

        self._display_results()

    def _display_results(self) -> None:
        summary = self.monitor.get_threat_summary(hours=24)
        
        if RICH_AVAILABLE:
            console.print("\n")
            console.print(Panel.fit(
                "[bold green]Security Monitoring Summary[/bold green]",
                border_style="green"
            ))
            
            stats_table = Table(title="Detection Statistics", box=box.ROUNDED, border_style="cyan")
            stats_table.add_column("Metric", style="cyan")
            stats_table.add_column("Value", style="yellow", justify="right")
            
            stats_table.add_row("Total Events Processed", str(self.event_count))
            stats_table.add_row("Threats Detected", str(summary["total_threats"]))
            stats_table.add_row("Detection Rate", f"{(summary['total_threats'] / max(self.event_count, 1)) * 100:.2f}%")
            
            console.print(stats_table)
            
            threat_table = Table(title="Threats by Level", box=box.ROUNDED, border_style="red")
            threat_table.add_column("Threat Level", style="cyan")
            threat_table.add_column("Count", style="yellow", justify="right")
            
            for level in ["critical", "high", "medium", "low"]:
                count = summary["by_threat_level"].get(level, 0)
                if count > 0:
                    color = {"critical": "bold red", "high": "red", "medium": "yellow", "low": "green"}.get(level, "white")
                    threat_table.add_row(f"[{color}]{level.upper()}[/{color}]", str(count))
            
            console.print(threat_table)
            
            if summary["critical_threats"] or summary["high_threats"]:
                console.print("\n[bold red]Critical/High Severity Threats:[/bold red]")
                
                for threat in summary["critical_threats"][:3]:
                    console.print(Panel(
                        f"[bold]ID:[/bold] {threat['detection_id']}\n"
                        f"[bold]Category:[/bold] {threat['category']}\n"
                        f"[bold]Description:[/bold] {threat['description'][:200]}...\n"
                        f"[bold]Confidence:[/bold] {threat['confidence_score']:.2%}\n"
                        f"[bold]EU AI Act:[/bold] {threat['eu_ai_act_article']}",
                        title=f"[red]CRITICAL: {threat['title']}[/red]",
                        border_style="red"
                    ))
                
                for threat in summary["high_threats"][:2]:
                    console.print(Panel(
                        f"[bold]ID:[/bold] {threat['detection_id']}\n"
                        f"[bold]Category:[/bold] {threat['category']}\n"
                        f"[bold]Description:[/bold] {threat['description'][:200]}...\n"
                        f"[bold]Confidence:[/bold] {threat['confidence_score']:.2%}",
                        title=f"[yellow]HIGH: {threat['title']}[/yellow]",
                        border_style="yellow"
                    ))
            
            if self.incident_manager and INCIDENT_MGMT_AVAILABLE:
                console.print("\n[bold cyan]EU AI Act Article 73 Incidents Created:[/bold cyan]")
                incidents_dir = Path("incidents")
                if incidents_dir.exists():
                    incident_files = list(incidents_dir.glob("*.json"))
                    console.print(f"Total incidents: {len(incident_files)}")
                    
                    for inc_file in sorted(incident_files, reverse=True)[:3]:
                        with open(inc_file) as f:
                            inc_data = json.load(f)
                        console.print(f"  • {inc_data['id']}: {inc_data['title']}")
        else:
            print("\n" + "=" * 60)
            print("Security Monitoring Summary")
            print("=" * 60)
            print(f"Total Events Processed: {self.event_count}")
            print(f"Threats Detected: {summary['total_threats']}")
            print(f"Detection Rate: {(summary['total_threats'] / max(self.event_count, 1)) * 100:.2f}%")
            print("\nThreats by Level:")
            for level, count in summary["by_threat_level"].items():
                print(f"  {level.upper()}: {count}")
            
            print(f"\nCritical Threats: {len(summary['critical_threats'])}")
            print(f"High Threats: {len(summary['high_threats'])}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-ai", action="store_true", help="Disable AI-powered threat analysis")
    parser.add_argument("--no-incidents", action="store_true", help="Disable incident creation")
    args = parser.parse_args()

    demo = SecurityMonitoringDemo(
        use_ai=not args.no_ai,
        enable_incidents=not args.no_incidents
    )
    
    try:
        demo.run_full_demo()
    except KeyboardInterrupt:
        if RICH_AVAILABLE:
            console.print("\n[yellow]Demo interrupted[/yellow]")
        else:
            print("\nDemo interrupted")


if __name__ == "__main__":
    main()
