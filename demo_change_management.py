"""
Comprehensive Demo/Test for Change Management System
Demonstrates all features: workflow, AI assessment, testing, approvals, deployment, rollback
"""

import os
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box
from rich.layout import Layout
from rich.live import Live

from change_management import (
    ChangeManagementSystem,
    ChangeType,
    ChangePriority,
    ChangeStatus
)

console = Console()


class ChangeManagementDemo:
    def __init__(self):
        self.cms = ChangeManagementSystem()
        self.demo_changes = []
    
    def run_full_demo(self):
        """Run complete demonstration of all features"""
        console.print(Panel.fit(
            "[bold cyan]Change Management System - Full Feature Demo[/bold cyan]\n"
            "[dim]Testing all workflows, AI assessment, testing, approvals, deployment, and rollback[/dim]",
            border_style="cyan"
        ))
        
        console.print("\n[bold yellow]═══ DEMO SEQUENCE ═══[/bold yellow]\n")
        
        # Demo 1: Create multiple change requests
        self.demo_create_changes()
        time.sleep(1)
        
        # Demo 2: AI Impact Assessment
        self.demo_impact_assessment()
        time.sleep(1)
        
        # Demo 3: Rollback Plan Generation
        self.demo_rollback_plans()
        time.sleep(1)
        
        # Demo 4: Automated Testing
        self.demo_automated_testing()
        time.sleep(1)
        
        # Demo 5: Approval Workflow
        self.demo_approval_workflow()
        time.sleep(1)
        
        # Demo 6: Deployment
        self.demo_deployment()
        time.sleep(1)
        
        # Demo 7: Rollback
        self.demo_rollback()
        time.sleep(1)
        
        # Demo 8: Statistics and Reporting
        self.demo_statistics()
        time.sleep(1)
        
        # Demo 9: Change Status Tracking
        self.demo_status_tracking()
        
        console.print("\n[bold green]✓ Demo Complete![/bold green]")
        console.print("[dim]All change management features demonstrated successfully[/dim]\n")
    
    def demo_create_changes(self):
        """Demo: Create various types of change requests"""
        console.print(Panel(
            "[bold]Demo 1: Creating Change Requests[/bold]\n"
            "Testing different change types and priorities",
            style="blue",
            border_style="blue"
        ))
        
        change_configs = [
            {
                "title": "Update AI Risk Classification Model to v2.1",
                "description": "Deploy improved risk classification model with 5% accuracy increase",
                "change_type": ChangeType.MODEL_UPDATE,
                "priority": ChangePriority.HIGH,
                "systems": ["risk-classifier", "api-gateway", "monitoring"],
                "justification": "Improve accuracy and reduce false positives per Article 17 requirements",
                "technical": "New attention mechanism, trained on 2M samples, optimized inference"
            },
            {
                "title": "Security Patch: Update Authentication Library",
                "description": "Critical security update for OAuth2 library",
                "change_type": ChangeType.SECURITY_PATCH,
                "priority": ChangePriority.CRITICAL,
                "systems": ["auth-service", "api-gateway"],
                "justification": "Address CVE-2026-1234 vulnerability",
                "technical": "Update oauth2-lib from v3.2 to v3.3.1"
            },
            {
                "title": "Add Explainability Dashboard Feature",
                "description": "New dashboard for AI decision explanations per Article 13",
                "change_type": ChangeType.FEATURE_ADDITION,
                "priority": ChangePriority.MEDIUM,
                "systems": ["frontend", "explainability-service", "database"],
                "justification": "EU AI Act Article 13 transparency requirements",
                "technical": "React dashboard with SHAP value visualizations"
            },
            {
                "title": "Fix Data Pipeline Memory Leak",
                "description": "Resolve memory leak in data preprocessing pipeline",
                "change_type": ChangeType.BUG_FIX,
                "priority": ChangePriority.HIGH,
                "systems": ["data-pipeline", "preprocessing"],
                "justification": "Prevent system crashes and data loss",
                "technical": "Fix buffer overflow in streaming processor"
            },
            {
                "title": "Update Monitoring Configuration",
                "description": "Add new metrics for Article 17 compliance monitoring",
                "change_type": ChangeType.CONFIGURATION,
                "priority": ChangePriority.LOW,
                "systems": ["prometheus", "grafana"],
                "justification": "Enhanced compliance monitoring capabilities",
                "technical": "Add custom metrics for quality management tracking"
            }
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Creating change requests...", total=len(change_configs))
            
            for config in change_configs:
                change = self.cms.create_change_request(
                    title=config["title"],
                    description=config["description"],
                    change_type=config["change_type"],
                    priority=config["priority"],
                    requester="demo-user@company.com",
                    affected_systems=config["systems"],
                    business_justification=config["justification"],
                    technical_details=config["technical"],
                    target_deployment_date="2026-02-15"
                )
                self.demo_changes.append(change.change_id)
                progress.advance(task)
                time.sleep(0.3)
        
        table = Table(title="Created Change Requests", box=box.ROUNDED, border_style="green")
        table.add_column("Change ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="white")
        table.add_column("Type", style="magenta")
        table.add_column("Priority", style="yellow")
        
        for change_id in self.demo_changes:
            status = self.cms.get_change_status(change_id)
            priority_color = {
                "critical": "bold red",
                "high": "red",
                "medium": "yellow",
                "low": "green"
            }.get(status["priority"], "white")
            
            table.add_row(
                change_id,
                status["title"][:50] + "..." if len(status["title"]) > 50 else status["title"],
                status["status"].replace("_", " ").title(),
                f"[{priority_color}]{status['priority'].upper()}[/{priority_color}]"
            )
        
        console.print(table)
        console.print(f"\n[green]✓ Created {len(self.demo_changes)} change requests[/green]\n")
    
    def demo_impact_assessment(self):
        """Demo: AI-powered impact assessment"""
        console.print(Panel(
            "[bold]Demo 2: AI-Powered Impact Assessment[/bold]\n"
            "Running Gemini AI analysis on change requests",
            style="yellow",
            border_style="yellow"
        ))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Running AI impact assessments...", total=len(self.demo_changes))
            
            assessments = []
            for change_id in self.demo_changes:
                assessment = self.cms.assess_impact(change_id)
                assessments.append((change_id, assessment))
                progress.advance(task)
                time.sleep(0.5)
        
        table = Table(title="Impact Assessment Results", box=box.ROUNDED, border_style="yellow")
        table.add_column("Change ID", style="cyan", no_wrap=True)
        table.add_column("Risk Level", style="white")
        table.add_column("Components", style="magenta")
        table.add_column("Rollback", style="blue")
        table.add_column("AI Confidence", style="green")
        
        for change_id, assessment in assessments:
            risk_color = {
                "critical": "bold red",
                "high": "red",
                "medium": "yellow",
                "low": "green",
                "minimal": "dim green"
            }.get(assessment.risk_level, "white")
            
            table.add_row(
                change_id[-12:],
                f"[{risk_color}]{assessment.risk_level.upper()}[/{risk_color}]",
                str(len(assessment.affected_components)),
                assessment.rollback_complexity,
                f"{assessment.confidence_score:.0%}"
            )
        
        console.print(table)
        
        console.print("\n[bold]Sample Detailed Assessment:[/bold]")
        sample_assessment = assessments[0][1]
        detail_panel = Panel(
            f"[bold]Risk Level:[/bold] {sample_assessment.risk_level}\n"
            f"[bold]Affected Components:[/bold] {', '.join(sample_assessment.affected_components)}\n"
            f"[bold]Performance Impact:[/bold] {sample_assessment.performance_impact}\n"
            f"[bold]Compliance Impact:[/bold] {sample_assessment.compliance_impact}\n"
            f"[bold]Testing Requirements:[/bold]\n" +
            "\n".join(f"  • {req}" for req in sample_assessment.testing_requirements[:3]) +
            f"\n[bold]AI Confidence:[/bold] {sample_assessment.confidence_score:.1%}",
            title=f"Assessment: {assessments[0][0][-12:]}",
            border_style="yellow"
        )
        console.print(detail_panel)
        console.print(f"\n[green]✓ Completed {len(assessments)} impact assessments[/green]\n")
    
    def demo_rollback_plans(self):
        """Demo: Automated rollback plan generation"""
        console.print(Panel(
            "[bold]Demo 3: Automated Rollback Plan Generation[/bold]\n"
            "Creating change-type specific rollback procedures",
            style="magenta",
            border_style="magenta"
        ))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating rollback plans...", total=len(self.demo_changes))
            
            rollback_plans = []
            for change_id in self.demo_changes:
                plan = self.cms.create_rollback_plan(change_id)
                rollback_plans.append((change_id, plan))
                progress.advance(task)
                time.sleep(0.3)
        
        table = Table(title="Rollback Plans", box=box.ROUNDED, border_style="magenta")
        table.add_column("Change ID", style="cyan", no_wrap=True)
        table.add_column("Steps", style="white", justify="right")
        table.add_column("Duration (min)", style="yellow", justify="right")
        table.add_column("Automated", style="green")
        
        for change_id, plan in rollback_plans:
            table.add_row(
                change_id[-12:],
                str(len(plan["rollback_steps"])),
                str(plan["estimated_duration_minutes"]),
                "✓" if plan["automated"] else "✗"
            )
        
        console.print(table)
        
        console.print("\n[bold]Sample Rollback Plan:[/bold]")
        sample_plan = rollback_plans[0][1]
        steps_text = "\n".join(f"  {i+1}. {step}" for i, step in enumerate(sample_plan["rollback_steps"]))
        plan_panel = Panel(
            f"[bold]Rollback Steps:[/bold]\n{steps_text}\n\n"
            f"[bold]Estimated Duration:[/bold] {sample_plan['estimated_duration_minutes']} minutes\n"
            f"[bold]Automated:[/bold] {'Yes' if sample_plan['automated'] else 'No'}",
            title=f"Rollback Plan: {rollback_plans[0][0][-12:]}",
            border_style="magenta"
        )
        console.print(plan_panel)
        console.print(f"\n[green]✓ Generated {len(rollback_plans)} rollback plans[/green]\n")
    
    def demo_automated_testing(self):
        """Demo: Automated test suite execution"""
        console.print(Panel(
            "[bold]Demo 4: Automated Testing[/bold]\n"
            "Running different test suites on change requests",
            style="blue",
            border_style="blue"
        ))
        
        test_suites = ["quick", "standard", "comprehensive", "compliance"]
        
        for i, change_id in enumerate(self.demo_changes[:4]):
            suite = test_suites[i]
            
            console.print(f"\n[cyan]Testing {change_id[-12:]} with '{suite}' suite...[/cyan]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task(f"Running {suite} tests...", total=None)
                results = self.cms.run_automated_tests(change_id, suite)
                progress.update(task, completed=True)
            
            table = Table(box=box.SIMPLE, show_header=True, border_style="blue")
            table.add_column("Test", style="cyan")
            table.add_column("Status", style="white")
            table.add_column("Duration", style="yellow")
            
            for result in results:
                status_icon = "✓" if result.passed else "✗"
                status_color = "green" if result.passed else "red"
                
                table.add_row(
                    result.test_name,
                    f"[{status_color}]{status_icon} {result.status}[/{status_color}]",
                    f"{result.duration_seconds:.1f}s"
                )
            
            console.print(table)
            
            passed = sum(1 for r in results if r.passed)
            total = len(results)
            if passed == total:
                console.print(f"[green]✓ All {total} tests passed[/green]")
            else:
                console.print(f"[yellow]⚠ {passed}/{total} tests passed[/yellow]")
        
        console.print(f"\n[green]✓ Completed automated testing on 4 changes[/green]\n")
    
    def demo_approval_workflow(self):
        """Demo: Multi-approver workflow"""
        console.print(Panel(
            "[bold]Demo 5: Approval Workflow[/bold]\n"
            "Testing approval request, approval, and rejection flows",
            style="green",
            border_style="green"
        ))
        
        approvers = [
            ("compliance-officer@company.com", "Article 17 compliance review"),
            ("security-team@company.com", "Security impact assessment"),
            ("tech-lead@company.com", "Technical review"),
            ("product-manager@company.com", "Business alignment check")
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Processing approvals...", total=len(self.demo_changes))
            
            for i, change_id in enumerate(self.demo_changes):
                approver, notes = approvers[i % len(approvers)]
                
                self.cms.request_approval(change_id, approver, notes)
                time.sleep(0.2)
                
                if i < 3:
                    self.cms.approve_change(
                        change_id,
                        approver,
                        f"Approved - meets EU AI Act requirements. {notes} complete."
                    )
                elif i == 3:
                    self.cms.reject_change(
                        change_id,
                        approver,
                        "Insufficient testing coverage - requires additional security tests"
                    )
                else:
                    pass
                
                progress.advance(task)
                time.sleep(0.3)
        
        table = Table(title="Approval Status", box=box.ROUNDED, border_style="green")
        table.add_column("Change ID", style="cyan", no_wrap=True)
        table.add_column("Approver", style="white")
        table.add_column("Status", style="white")
        table.add_column("Decision", style="dim")
        
        for change_id in self.demo_changes:
            change = self.cms._load_change(change_id)
            if change.approvals:
                approval = change.approvals[0]
                status_color = {
                    "pending": "yellow",
                    "approved": "green",
                    "rejected": "red"
                }.get(approval["status"], "white")
                
                decision_text = approval.get("decision_notes") or approval.get("notes") or ""
                decision_display = (decision_text[:40] + "...") if decision_text else "N/A"
                
                table.add_row(
                    change_id[-12:],
                    approval["approver"].split("@")[0],
                    f"[{status_color}]{approval['status'].upper()}[/{status_color}]",
                    decision_display
                )
        
        console.print(table)
        console.print(f"\n[green]✓ Processed approvals for {len(self.demo_changes)} changes[/green]\n")
    
    def demo_deployment(self):
        """Demo: Change deployment"""
        console.print(Panel(
            "[bold]Demo 6: Deployment[/bold]\n"
            "Deploying approved changes",
            style="cyan",
            border_style="cyan"
        ))
        
        approved_changes = []
        for change_id in self.demo_changes:
            status = self.cms.get_change_status(change_id)
            if status["status"] == "approved":
                approved_changes.append(change_id)
        
        if not approved_changes:
            console.print("[yellow]No approved changes to deploy[/yellow]\n")
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Deploying changes...", total=len(approved_changes))
            
            for change_id in approved_changes:
                deployment = self.cms.deploy_change(change_id, "ops-team@company.com")
                time.sleep(0.5)
                
                success = True
                self.cms.complete_deployment(
                    change_id,
                    success=success,
                    notes="Deployment completed successfully. All health checks passed."
                )
                
                progress.advance(task)
                time.sleep(0.3)
        
        table = Table(title="Deployment Results", box=box.ROUNDED, border_style="cyan")
        table.add_column("Change ID", style="cyan", no_wrap=True)
        table.add_column("Status", style="white")
        table.add_column("Deployed By", style="blue")
        table.add_column("Result", style="green")
        
        for change_id in approved_changes:
            change = self.cms._load_change(change_id)
            if change.deployment_log:
                deployment = change.deployment_log[-1]
                status_color = "green" if deployment["status"] == "completed" else "red"
                
                table.add_row(
                    change_id[-12:],
                    f"[{status_color}]{deployment['status'].upper()}[/{status_color}]",
                    deployment["deployed_by"].split("@")[0],
                    "✓ Success" if deployment["status"] == "completed" else "✗ Failed"
                )
        
        console.print(table)
        console.print(f"\n[green]✓ Deployed {len(approved_changes)} changes[/green]\n")
    
    def demo_rollback(self):
        """Demo: Change rollback"""
        console.print(Panel(
            "[bold]Demo 7: Rollback Execution[/bold]\n"
            "Demonstrating rollback of a deployed change",
            style="red",
            border_style="red"
        ))
        
        deployed_changes = []
        for change_id in self.demo_changes:
            status = self.cms.get_change_status(change_id)
            if status["status"] == "deployed":
                deployed_changes.append(change_id)
        
        if not deployed_changes:
            console.print("[yellow]No deployed changes to rollback[/yellow]\n")
            return
        
        rollback_change_id = deployed_changes[0]
        
        console.print(f"[yellow]Simulating issue with {rollback_change_id[-12:]}...[/yellow]")
        console.print("[red]⚠ Performance degradation detected - initiating rollback[/red]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Executing rollback...", total=None)
            
            rollback_result = self.cms.rollback_change(
                rollback_change_id,
                "ops-team@company.com",
                "Performance degradation: 95th percentile latency increased by 200ms"
            )
            
            progress.update(task, completed=True)
        
        console.print(Panel(
            f"[bold green]✓ Rollback Complete[/bold green]\n\n"
            f"[bold]Change ID:[/bold] {rollback_change_id}\n"
            f"[bold]Rolled Back By:[/bold] {rollback_result['rolled_back_by']}\n"
            f"[bold]Reason:[/bold] {rollback_result['reason']}\n"
            f"[bold]Steps Completed:[/bold] {len(rollback_result['steps_completed'])}\n"
            f"[bold]Status:[/bold] {rollback_result['status']}\n"
            f"[bold]Duration:[/bold] {rollback_result['started_at']} to {rollback_result['completed_at']}",
            border_style="green",
            title="Rollback Execution Report"
        ))
        
        console.print(f"\n[green]✓ Successfully rolled back change {rollback_change_id[-12:]}[/green]\n")
    
    def demo_statistics(self):
        """Demo: Statistics and reporting"""
        console.print(Panel(
            "[bold]Demo 8: Statistics and Reporting[/bold]\n"
            "Analyzing change management metrics",
            style="yellow",
            border_style="yellow"
        ))
        
        all_changes = self.cms.list_changes()
        
        stats = {
            "total": len(all_changes),
            "by_status": {},
            "by_priority": {},
            "by_type": {}
        }
        
        for change in all_changes:
            status = change["status"]
            priority = change["priority"]
            change_type = change["change_type"]
            
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
            stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
            stats["by_type"][change_type] = stats["by_type"].get(change_type, 0) + 1
        
        layout = Layout()
        layout.split_row(
            Layout(name="status"),
            Layout(name="priority"),
            Layout(name="type")
        )
        
        status_table = Table(title="By Status", box=box.SIMPLE, border_style="blue")
        status_table.add_column("Status", style="cyan")
        status_table.add_column("Count", style="white", justify="right")
        for status, count in sorted(stats["by_status"].items()):
            status_table.add_row(status.replace("_", " ").title(), str(count))
        
        priority_table = Table(title="By Priority", box=box.SIMPLE, border_style="yellow")
        priority_table.add_column("Priority", style="yellow")
        priority_table.add_column("Count", style="white", justify="right")
        for priority, count in sorted(stats["by_priority"].items()):
            priority_table.add_row(priority.upper(), str(count))
        
        type_table = Table(title="By Type", box=box.SIMPLE, border_style="magenta")
        type_table.add_column("Type", style="magenta")
        type_table.add_column("Count", style="white", justify="right")
        for change_type, count in sorted(stats["by_type"].items()):
            type_table.add_row(change_type.replace("_", " ").title(), str(count))
        
        layout["status"].update(Panel(status_table, border_style="blue"))
        layout["priority"].update(Panel(priority_table, border_style="yellow"))
        layout["type"].update(Panel(type_table, border_style="magenta"))
        
        console.print(layout)
        
        console.print(f"\n[bold]Summary Statistics:[/bold]")
        console.print(f"  • Total Changes: {stats['total']}")
        console.print(f"  • Deployed: {stats['by_status'].get('deployed', 0)}")
        console.print(f"  • Rolled Back: {stats['by_status'].get('rolled_back', 0)}")
        console.print(f"  • Rejected: {stats['by_status'].get('rejected', 0)}")
        console.print(f"  • Success Rate: {(stats['by_status'].get('deployed', 0) / stats['total'] * 100):.1f}%")
        
        console.print(f"\n[green]✓ Statistics generated for {stats['total']} changes[/green]\n")
    
    def demo_status_tracking(self):
        """Demo: Detailed status tracking"""
        console.print(Panel(
            "[bold]Demo 9: Change Status Tracking[/bold]\n"
            "Detailed status information for all changes",
            style="cyan",
            border_style="cyan"
        ))
        
        table = Table(title="Complete Change Status Overview", box=box.ROUNDED, border_style="cyan")
        table.add_column("Change ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="white")
        table.add_column("Status", style="green")
        table.add_column("Tests", style="yellow")
        table.add_column("Approvals", style="blue")
        table.add_column("Rollback Ready", style="magenta")
        
        for change_id in self.demo_changes:
            status = self.cms.get_change_status(change_id)
            
            status_color = {
                "draft": "dim",
                "pending_approval": "yellow",
                "approved": "green",
                "deployed": "bold green",
                "rejected": "red",
                "rolled_back": "red"
            }.get(status["status"], "white")
            
            table.add_row(
                change_id[-12:],
                status["title"][:30] + "..." if len(status["title"]) > 30 else status["title"],
                f"[{status_color}]{status['status'].replace('_', ' ').title()}[/{status_color}]",
                f"{status['tests_passed']}/{status['tests_run']}",
                f"✓ {status['approvals_granted']}" if status['approvals_granted'] > 0 else f"⧗ {status['approvals_pending']}",
                "✓" if status["rollback_plan_ready"] else "✗"
            )
        
        console.print(table)
        
        console.print("\n[bold]Sample Detailed Status:[/bold]")
        sample_status = self.cms.get_change_status(self.demo_changes[0])
        detail_text = "\n".join(f"  • {key.replace('_', ' ').title()}: {value}" 
                                for key, value in sample_status.items())
        console.print(Panel(detail_text, border_style="cyan", title=f"Status: {self.demo_changes[0][-12:]}"))
        
        console.print(f"\n[green]✓ Status tracking complete for {len(self.demo_changes)} changes[/green]\n")


def main():
    """Run the comprehensive demo"""
    console.print("\n")
    
    demo = ChangeManagementDemo()
    
    try:
        demo.run_full_demo()
        
        console.print(Panel.fit(
            "[bold green]✓ All Demos Completed Successfully[/bold green]\n\n"
            "[bold]Features Demonstrated:[/bold]\n"
            "  ✓ Change request creation (5 types)\n"
            "  ✓ AI-powered impact assessment\n"
            "  ✓ Automated rollback plan generation\n"
            "  ✓ Automated testing (4 test suites)\n"
            "  ✓ Multi-approver workflow\n"
            "  ✓ Change deployment\n"
            "  ✓ Rollback execution\n"
            "  ✓ Statistics and reporting\n"
            "  ✓ Status tracking\n\n"
            "[bold]EU AI Act Compliance:[/bold]\n"
            "  ✓ Article 17: Quality Management System\n"
            "  ✓ Article 43: Conformity Assessment\n\n"
            "[dim]Check the 'change_management/' directory for all generated data[/dim]",
            border_style="green"
        ))
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Demo error: {e}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")


if __name__ == "__main__":
    main()
