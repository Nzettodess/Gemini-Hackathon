"""
Interactive CLI for Change Management System
EU AI Act compliant change request workflow with Rich terminal UI
"""

import sys
from datetime import datetime
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich import box
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
import json

from change_management import (
    ChangeManagementSystem,
    ChangeType,
    ChangePriority,
    ChangeStatus
)

console = Console()


class ChangeManagementCLI:
    def __init__(self):
        self.cms = ChangeManagementSystem()
        self.current_change_id = None
    
    def run(self):
        """Main CLI loop"""
        console.print(Panel.fit(
            "[bold cyan]EU AI Act Change Management System[/bold cyan]\n"
            "[dim]Article 17 & 43 Compliance - Systematic Change Control[/dim]",
            border_style="cyan"
        ))
        
        while True:
            console.print()
            choice = self._show_main_menu()
            
            if choice == "1":
                self._create_change_request()
            elif choice == "2":
                self._view_change_requests()
            elif choice == "3":
                self._manage_change()
            elif choice == "4":
                self._run_impact_assessment()
            elif choice == "5":
                self._run_tests()
            elif choice == "6":
                self._approve_reject_change()
            elif choice == "7":
                self._deploy_change()
            elif choice == "8":
                self._rollback_change()
            elif choice == "9":
                self._view_statistics()
            elif choice == "0":
                console.print("[yellow]Exiting Change Management System[/yellow]")
                break
            else:
                console.print("[red]Invalid choice[/red]")
    
    def _show_main_menu(self) -> str:
        """Display main menu and get user choice"""
        menu = Table(show_header=False, box=box.ROUNDED, border_style="blue")
        menu.add_column("Option", style="cyan", width=4)
        menu.add_column("Action", style="white")
        
        menu.add_row("1", "Create New Change Request")
        menu.add_row("2", "View All Change Requests")
        menu.add_row("3", "Manage Specific Change")
        menu.add_row("4", "Run Impact Assessment")
        menu.add_row("5", "Run Automated Tests")
        menu.add_row("6", "Approve/Reject Change")
        menu.add_row("7", "Deploy Change")
        menu.add_row("8", "Rollback Change")
        menu.add_row("9", "View Statistics")
        menu.add_row("0", "Exit")
        
        console.print(menu)
        return Prompt.ask("[bold cyan]Select option[/bold cyan]", default="1")
    
    def _create_change_request(self):
        """Create a new change request"""
        console.print(Panel("[bold]Create New Change Request[/bold]", style="green"))
        
        title = Prompt.ask("[cyan]Change Title[/cyan]")
        description = Prompt.ask("[cyan]Description[/cyan]")
        
        console.print("\n[bold]Change Type:[/bold]")
        for i, ct in enumerate(ChangeType, 1):
            console.print(f"  {i}. {ct.value}")
        
        type_choice = int(Prompt.ask("[cyan]Select type[/cyan]", default="1")) - 1
        change_type = list(ChangeType)[type_choice]
        
        console.print("\n[bold]Priority:[/bold]")
        for i, cp in enumerate(ChangePriority, 1):
            console.print(f"  {i}. {cp.value}")
        
        priority_choice = int(Prompt.ask("[cyan]Select priority[/cyan]", default="2")) - 1
        priority = list(ChangePriority)[priority_choice]
        
        requester = Prompt.ask("[cyan]Requester email[/cyan]")
        
        affected_systems_input = Prompt.ask("[cyan]Affected systems (comma-separated)[/cyan]")
        affected_systems = [s.strip() for s in affected_systems_input.split(",")]
        
        business_justification = Prompt.ask("[cyan]Business justification[/cyan]")
        technical_details = Prompt.ask("[cyan]Technical details[/cyan]")
        
        target_date = Prompt.ask("[cyan]Target deployment date (YYYY-MM-DD)[/cyan]", default="")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Creating change request...", total=None)
            
            change = self.cms.create_change_request(
                title=title,
                description=description,
                change_type=change_type,
                priority=priority,
                requester=requester,
                affected_systems=affected_systems,
                business_justification=business_justification,
                technical_details=technical_details,
                target_deployment_date=target_date if target_date else None
            )
            
            progress.update(task, completed=True)
        
        console.print(Panel(
            f"[green]✓ Change Request Created[/green]\n\n"
            f"[bold]Change ID:[/bold] {change.change_id}\n"
            f"[bold]Title:[/bold] {change.title}\n"
            f"[bold]Status:[/bold] {change.status}\n"
            f"[bold]Priority:[/bold] {change.priority}",
            border_style="green"
        ))
        
        self.current_change_id = change.change_id
    
    def _view_change_requests(self):
        """View all change requests"""
        console.print(Panel("[bold]All Change Requests[/bold]", style="blue"))
        
        status_filter = Prompt.ask(
            "[cyan]Filter by status (leave empty for all)[/cyan]",
            default=""
        )
        
        changes = self.cms.list_changes(
            status_filter=status_filter if status_filter else None
        )
        
        if not changes:
            console.print("[yellow]No change requests found[/yellow]")
            return
        
        table = Table(title=f"Change Requests ({len(changes)} total)", box=box.ROUNDED)
        table.add_column("Change ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="white")
        table.add_column("Type", style="magenta")
        table.add_column("Priority", style="yellow")
        table.add_column("Status", style="green")
        table.add_column("Requester", style="blue")
        table.add_column("Created", style="dim")
        
        for change in changes:
            status_color = {
                "draft": "dim",
                "pending_approval": "yellow",
                "approved": "green",
                "deployed": "bold green",
                "rejected": "red",
                "rolled_back": "red"
            }.get(change["status"], "white")
            
            priority_color = {
                "critical": "bold red",
                "high": "red",
                "medium": "yellow",
                "low": "green"
            }.get(change["priority"], "white")
            
            table.add_row(
                change["change_id"],
                change["title"][:40] + "..." if len(change["title"]) > 40 else change["title"],
                change["change_type"],
                f"[{priority_color}]{change['priority']}[/{priority_color}]",
                f"[{status_color}]{change['status']}[/{status_color}]",
                change["requester"],
                change["created_at"][:10]
            )
        
        console.print(table)
    
    def _manage_change(self):
        """Manage a specific change request"""
        change_id = Prompt.ask("[cyan]Enter Change ID[/cyan]")
        
        try:
            status = self.cms.get_change_status(change_id)
            
            table = Table(title=f"Change Status: {change_id}", box=box.DOUBLE)
            table.add_column("Property", style="cyan", no_wrap=True)
            table.add_column("Value", style="white")
            
            for key, value in status.items():
                table.add_row(key.replace("_", " ").title(), str(value))
            
            console.print(table)
            self.current_change_id = change_id
            
        except FileNotFoundError:
            console.print(f"[red]Change request {change_id} not found[/red]")
    
    def _run_impact_assessment(self):
        """Run AI-powered impact assessment"""
        if not self.current_change_id:
            self.current_change_id = Prompt.ask("[cyan]Enter Change ID[/cyan]")
        
        console.print(Panel(
            f"[bold]Running Impact Assessment[/bold]\n"
            f"Change ID: {self.current_change_id}",
            style="yellow"
        ))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Analyzing impact with AI...", total=None)
            
            try:
                assessment = self.cms.assess_impact(self.current_change_id)
                progress.update(task, completed=True)
                
                console.print(Panel(
                    f"[bold green]✓ Impact Assessment Complete[/bold green]\n\n"
                    f"[bold]Risk Level:[/bold] {assessment.risk_level.upper()}\n"
                    f"[bold]Affected Components:[/bold] {', '.join(assessment.affected_components)}\n"
                    f"[bold]Affected Users:[/bold] {assessment.affected_users}\n"
                    f"[bold]Performance Impact:[/bold] {assessment.performance_impact}\n"
                    f"[bold]Compliance Impact:[/bold] {assessment.compliance_impact}\n"
                    f"[bold]Rollback Complexity:[/bold] {assessment.rollback_complexity}\n"
                    f"[bold]AI Confidence:[/bold] {assessment.confidence_score:.1%}\n\n"
                    f"[bold]Testing Requirements:[/bold]\n" +
                    "\n".join(f"  • {req}" for req in assessment.testing_requirements) +
                    f"\n\n[bold]AI Analysis:[/bold]\n{assessment.ai_analysis[:300]}...",
                    border_style="green",
                    title="Impact Assessment Results"
                ))
                
            except Exception as e:
                progress.update(task, completed=True)
                console.print(f"[red]Assessment failed: {e}[/red]")
    
    def _run_tests(self):
        """Run automated test suite"""
        if not self.current_change_id:
            self.current_change_id = Prompt.ask("[cyan]Enter Change ID[/cyan]")
        
        console.print("\n[bold]Test Suite:[/bold]")
        console.print("  1. Quick (unit + smoke)")
        console.print("  2. Standard (unit + integration + regression)")
        console.print("  3. Comprehensive (all tests)")
        console.print("  4. Compliance (EU AI Act compliance tests)")
        
        suite_choice = Prompt.ask("[cyan]Select test suite[/cyan]", default="2")
        suite_map = {
            "1": "quick",
            "2": "standard",
            "3": "comprehensive",
            "4": "compliance"
        }
        suite = suite_map.get(suite_choice, "standard")
        
        console.print(Panel(
            f"[bold]Running Automated Tests[/bold]\n"
            f"Change ID: {self.current_change_id}\n"
            f"Suite: {suite}",
            style="blue"
        ))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Executing test suite...", total=None)
            
            try:
                results = self.cms.run_automated_tests(self.current_change_id, suite)
                progress.update(task, completed=True)
                
                table = Table(title="Test Results", box=box.ROUNDED)
                table.add_column("Test", style="cyan")
                table.add_column("Status", style="white")
                table.add_column("Duration", style="yellow")
                table.add_column("Details", style="dim")
                
                for result in results:
                    status_icon = "✓" if result.passed else "✗"
                    status_color = "green" if result.passed else "red"
                    
                    table.add_row(
                        result.test_name,
                        f"[{status_color}]{status_icon} {result.status}[/{status_color}]",
                        f"{result.duration_seconds:.1f}s",
                        result.details[:50] + "..." if len(result.details) > 50 else result.details
                    )
                
                console.print(table)
                
                passed = sum(1 for r in results if r.passed)
                total = len(results)
                
                if passed == total:
                    console.print(Panel(
                        f"[bold green]✓ All Tests Passed ({passed}/{total})[/bold green]",
                        border_style="green"
                    ))
                else:
                    console.print(Panel(
                        f"[bold red]✗ Some Tests Failed ({passed}/{total} passed)[/bold red]",
                        border_style="red"
                    ))
                
            except Exception as e:
                progress.update(task, completed=True)
                console.print(f"[red]Test execution failed: {e}[/red]")
    
    def _approve_reject_change(self):
        """Approve or reject a change request"""
        if not self.current_change_id:
            self.current_change_id = Prompt.ask("[cyan]Enter Change ID[/cyan]")
        
        approver = Prompt.ask("[cyan]Approver email[/cyan]")
        
        action = Prompt.ask(
            "[cyan]Action[/cyan]",
            choices=["approve", "reject", "request"],
            default="request"
        )
        
        if action == "request":
            notes = Prompt.ask("[cyan]Request notes[/cyan]", default="")
            self.cms.request_approval(self.current_change_id, approver, notes)
            console.print(f"[green]✓ Approval requested from {approver}[/green]")
            
        elif action == "approve":
            notes = Prompt.ask("[cyan]Approval notes[/cyan]", default="")
            success = self.cms.approve_change(self.current_change_id, approver, notes)
            if success:
                console.print(Panel(
                    f"[bold green]✓ Change Approved[/bold green]\n"
                    f"Approver: {approver}\n"
                    f"Change ID: {self.current_change_id}",
                    border_style="green"
                ))
            else:
                console.print("[red]Approval failed - no pending approval found[/red]")
                
        elif action == "reject":
            reason = Prompt.ask("[cyan]Rejection reason[/cyan]")
            success = self.cms.reject_change(self.current_change_id, approver, reason)
            if success:
                console.print(Panel(
                    f"[bold red]✗ Change Rejected[/bold red]\n"
                    f"Approver: {approver}\n"
                    f"Reason: {reason}",
                    border_style="red"
                ))
            else:
                console.print("[red]Rejection failed - no pending approval found[/red]")
    
    def _deploy_change(self):
        """Deploy an approved change"""
        if not self.current_change_id:
            self.current_change_id = Prompt.ask("[cyan]Enter Change ID[/cyan]")
        
        deployed_by = Prompt.ask("[cyan]Deployed by (email)[/cyan]")
        
        if not Confirm.ask(f"[yellow]Deploy change {self.current_change_id}?[/yellow]"):
            console.print("[dim]Deployment cancelled[/dim]")
            return
        
        try:
            console.print(Panel(
                f"[bold]Deploying Change[/bold]\n"
                f"Change ID: {self.current_change_id}\n"
                f"Deployed by: {deployed_by}",
                style="cyan"
            ))
            
            deployment = self.cms.deploy_change(self.current_change_id, deployed_by)
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Deploying...", total=None)
                import time
                time.sleep(2)
                progress.update(task, completed=True)
            
            success = Confirm.ask("[cyan]Deployment successful?[/cyan]", default=True)
            notes = Prompt.ask("[cyan]Deployment notes[/cyan]", default="")
            
            self.cms.complete_deployment(self.current_change_id, success, notes)
            
            if success:
                console.print(Panel(
                    f"[bold green]✓ Deployment Complete[/bold green]\n"
                    f"Change ID: {self.current_change_id}\n"
                    f"Status: Deployed",
                    border_style="green"
                ))
            else:
                console.print(Panel(
                    f"[bold red]✗ Deployment Failed[/bold red]\n"
                    f"Change ID: {self.current_change_id}\n"
                    f"Notes: {notes}",
                    border_style="red"
                ))
                
        except ValueError as e:
            console.print(f"[red]Deployment failed: {e}[/red]")
    
    def _rollback_change(self):
        """Rollback a deployed change"""
        if not self.current_change_id:
            self.current_change_id = Prompt.ask("[cyan]Enter Change ID[/cyan]")
        
        rolled_back_by = Prompt.ask("[cyan]Rolled back by (email)[/cyan]")
        reason = Prompt.ask("[cyan]Rollback reason[/cyan]")
        
        if not Confirm.ask(f"[bold red]Rollback change {self.current_change_id}?[/bold red]"):
            console.print("[dim]Rollback cancelled[/dim]")
            return
        
        try:
            console.print(Panel(
                f"[bold yellow]Executing Rollback[/bold yellow]\n"
                f"Change ID: {self.current_change_id}\n"
                f"Reason: {reason}",
                style="yellow"
            ))
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Rolling back...", total=None)
                
                rollback_result = self.cms.rollback_change(
                    self.current_change_id,
                    rolled_back_by,
                    reason
                )
                
                progress.update(task, completed=True)
            
            console.print(Panel(
                f"[bold green]✓ Rollback Complete[/bold green]\n"
                f"Change ID: {self.current_change_id}\n"
                f"Steps completed: {len(rollback_result['steps_completed'])}\n"
                f"Status: {rollback_result['status']}",
                border_style="green"
            ))
            
        except Exception as e:
            console.print(f"[red]Rollback failed: {e}[/red]")
    
    def _view_statistics(self):
        """View change management statistics"""
        all_changes = self.cms.list_changes()
        
        if not all_changes:
            console.print("[yellow]No change requests found[/yellow]")
            return
        
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
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body")
        )
        
        layout["header"].update(Panel(
            f"[bold cyan]Change Management Statistics[/bold cyan]\n"
            f"Total Changes: {stats['total']}",
            border_style="cyan"
        ))
        
        body_layout = Layout()
        body_layout.split_row(
            Layout(name="status"),
            Layout(name="priority"),
            Layout(name="type")
        )
        
        status_table = Table(title="By Status", box=box.SIMPLE)
        status_table.add_column("Status", style="cyan")
        status_table.add_column("Count", style="white", justify="right")
        for status, count in sorted(stats["by_status"].items()):
            status_table.add_row(status, str(count))
        
        priority_table = Table(title="By Priority", box=box.SIMPLE)
        priority_table.add_column("Priority", style="yellow")
        priority_table.add_column("Count", style="white", justify="right")
        for priority, count in sorted(stats["by_priority"].items()):
            priority_table.add_row(priority, str(count))
        
        type_table = Table(title="By Type", box=box.SIMPLE)
        type_table.add_column("Type", style="magenta")
        type_table.add_column("Count", style="white", justify="right")
        for change_type, count in sorted(stats["by_type"].items()):
            type_table.add_row(change_type, str(count))
        
        body_layout["status"].update(Panel(status_table, border_style="blue"))
        body_layout["priority"].update(Panel(priority_table, border_style="yellow"))
        body_layout["type"].update(Panel(type_table, border_style="magenta"))
        
        layout["body"].update(body_layout)
        
        console.print(layout)


def main():
    try:
        cli = ChangeManagementCLI()
        cli.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
