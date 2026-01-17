#!/usr/bin/env python3
"""
EU AI Act Article 73 - Incident Management CLI
===============================================
Command-line interface for managing incidents and ensuring Article 73 compliance.

Usage:
    python incident_cli.py create --title "..." --description "..." --ai-system-id "..." --member-state "..."
    python incident_cli.py classify <incident_id>
    python incident_cli.py timeline <incident_id>
    python incident_cli.py list [--status <status>]
    python incident_cli.py show <incident_id>
"""

import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from datetime import datetime

from incident_management import IncidentManager, Incident, SeriousIncidentType, IncidentStatus


def format_incident_table(incidents: list) -> Table:
    """Format incidents as a Rich table."""
    table = Table(title="Incidents", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim")
    table.add_column("Title", style="bold")
    table.add_column("AI System", style="cyan")
    table.add_column("Severity", justify="center")
    table.add_column("Serious", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Detected", style="dim")
    
    for inc in incidents:
        serious = "✓" if inc.is_serious else "✗"
        severity = inc.severity or "N/A"
        detected = datetime.fromisoformat(inc.detected_at.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
        
        table.add_row(
            inc.id,
            inc.title[:40] + "..." if len(inc.title) > 40 else inc.title,
            inc.ai_system_name[:30] + "..." if len(inc.ai_system_name) > 30 else inc.ai_system_name,
            severity,
            serious,
            inc.status,
            detected
        )
    
    return table


def format_incident_detail(incident: Incident, manager: IncidentManager) -> str:
    """Format detailed incident information."""
    lines = []
    lines.append(f"# {incident.title}\n")
    lines.append(f"**ID:** {incident.id}  \n")
    lines.append(f"**Status:** {incident.status}  \n")
    lines.append(f"**Detected:** {incident.detected_at} ({incident.detected_by})  \n")
    lines.append(f"**AI System:** {incident.ai_system_name} ({incident.ai_system_id})  \n")
    lines.append(f"**Member State:** {incident.member_state}  \n")
    lines.append(f"\n## Description\n{incident.description}\n")
    
    lines.append(f"\n## Classification\n")
    lines.append(f"- **Severity:** {incident.severity or 'Not classified'}  \n")
    lines.append(f"- **Incident Type:** {incident.incident_type or 'Not classified'}  \n")
    lines.append(f"- **Is Serious:** {'Yes' if incident.is_serious else 'No'}  \n")
    if incident.serious_incident_type:
        lines.append(f"- **Serious Incident Type:** {incident.serious_incident_type}  \n")
    
    if incident.causal_link_established:
        lines.append(f"\n## Causal Link (Article 73(2))\n")
        lines.append(f"- **Established:** Yes  \n")
        lines.append(f"- **Established At:** {incident.causal_link_established_at}  \n")
        if incident.causal_link_evidence:
            lines.append(f"- **Evidence:** {incident.causal_link_evidence}  \n")
    else:
        lines.append(f"\n## Causal Link (Article 73(2))\n")
        lines.append(f"- **Established:** No  \n")
    
    if incident.is_serious:
        timeline = manager.track_reporting_timeline(incident)
        lines.append(f"\n## Reporting Timeline (Article 73)\n")
        lines.append(f"- **Deadline:** {incident.reporting_deadline}  \n")
        lines.append(f"- **Timeline:** {incident.reporting_timeline_days} days  \n")
        lines.append(f"- **Status:** {timeline['status']} ({timeline.get('days_remaining', 'N/A')} days remaining)  \n")
        lines.append(f"- **Initial Report:** {'Submitted' if incident.initial_report_submitted else 'Not submitted'}  \n")
        lines.append(f"- **Complete Report:** {'Submitted' if incident.complete_report_submitted else 'Not submitted'}  \n")
    
    if incident.remediation_actions:
        lines.append(f"\n## Remediation Actions\n")
        for action in incident.remediation_actions:
            lines.append(f"- {action}  \n")
        lines.append(f"- **Status:** {incident.remediation_status}  \n")
    
    if incident.authority_notified:
        lines.append(f"\n## Regulatory Notification (Article 73(1))\n")
        lines.append(f"- **Notified:** Yes  \n")
        lines.append(f"- **Notified At:** {incident.authority_notified_at}  \n")
        if incident.authority_contact:
            lines.append(f"- **Authority Contact:** {incident.authority_contact}  \n")
    else:
        lines.append(f"\n## Regulatory Notification (Article 73(1))\n")
        lines.append(f"- **Notified:** No  \n")
    
    if incident.investigation_notes:
        lines.append(f"\n## Investigation Notes\n")
        for note in incident.investigation_notes:
            lines.append(f"- {note}  \n")
    
    if incident.risk_assessment:
        lines.append(f"\n## Risk Assessment (Article 73(6))\n")
        lines.append(f"{incident.risk_assessment}\n")
    
    return "\n".join(lines)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="EU AI Act Article 73 Incident Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new incident
  python incident_cli.py create --title "AI System Error" --description "..." \\
    --ai-system-id "AI-001" --ai-system-name "Medical AI" --member-state "Germany"
  
  # Classify an incident
  python incident_cli.py classify INC-20260117-102838-0
  
  # Check reporting timeline
  python incident_cli.py timeline INC-20260117-102838-0
  
  # List all incidents
  python incident_cli.py list
  
  # Show incident details
  python incident_cli.py show INC-20260117-102838-0
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new incident')
    create_parser.add_argument('--title', required=True, help='Incident title')
    create_parser.add_argument('--description', required=True, help='Incident description')
    create_parser.add_argument('--ai-system-id', required=True, help='AI system identifier')
    create_parser.add_argument('--ai-system-name', required=True, help='AI system name')
    create_parser.add_argument('--member-state', required=True, help='EU Member State where incident occurred')
    create_parser.add_argument('--detected-by', default='human', choices=['human', 'automated'], help='Detection method')
    
    # Classify command
    classify_parser = subparsers.add_parser('classify', help='Classify incident severity')
    classify_parser.add_argument('incident_id', help='Incident ID')
    classify_parser.add_argument('--override', choices=['a', 'b', 'c', 'd', 'not_serious'],
                               help='Human override for serious incident type')
    
    # Establish causal link
    causal_parser = subparsers.add_parser('causal-link', help='Establish causal link')
    causal_parser.add_argument('incident_id', help='Incident ID')
    causal_parser.add_argument('--established', action='store_true', help='Causal link established')
    causal_parser.add_argument('--evidence', help='Evidence for causal link')
    
    # Timeline command
    timeline_parser = subparsers.add_parser('timeline', help='Check reporting timeline')
    timeline_parser.add_argument('incident_id', help='Incident ID')
    
    # Suggest remediation
    suggest_parser = subparsers.add_parser('suggest-remediation', help='Suggest remediation actions')
    suggest_parser.add_argument('incident_id', help='Incident ID')
    
    # Notify authority
    notify_parser = subparsers.add_parser('notify-authority', help='Record authority notification')
    notify_parser.add_argument('incident_id', help='Incident ID')
    notify_parser.add_argument('--authority-contact', required=True, help='Authority contact information')
    notify_parser.add_argument('--notification-content', help='Notification content')
    
    # Submit report
    report_parser = subparsers.add_parser('submit-report', help='Submit incident report')
    report_parser.add_argument('incident_id', help='Incident ID')
    report_parser.add_argument('--type', choices=['initial', 'complete'], default='complete', help='Report type')
    report_parser.add_argument('--content', help='Report content')
    
    # Risk assessment
    risk_parser = subparsers.add_parser('risk-assessment', help='Record risk assessment')
    risk_parser.add_argument('incident_id', help='Incident ID')
    risk_parser.add_argument('--assessment', required=True, help='Risk assessment content')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List incidents')
    list_parser.add_argument('--status', help='Filter by status')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show incident details')
    show_parser.add_argument('incident_id', help='Incident ID')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    console = Console()
    manager = IncidentManager(use_ai=True)
    
    try:
        if args.command == 'create':
            incident = manager.create_incident(
                title=args.title,
                description=args.description,
                ai_system_id=args.ai_system_id,
                ai_system_name=args.ai_system_name,
                member_state=args.member_state,
                detected_by=args.detected_by
            )
            console.print(f"\n[green]✓[/green] Created incident: {incident.id}")
            console.print(f"  Title: {incident.title}")
            console.print(f"  Status: {incident.status}")
        
        elif args.command == 'classify':
            incident = manager.load_incident(args.incident_id)
            if not incident:
                console.print(f"[red]Error:[/red] Incident {args.incident_id} not found")
                sys.exit(1)
            
            incident = manager.classify_severity(incident, human_override=args.override)
            console.print(f"\n[green]✓[/green] Classified incident: {incident.id}")
            console.print(f"  Severity: {incident.severity}")
            console.print(f"  Is Serious: {incident.is_serious}")
            if incident.serious_incident_type:
                console.print(f"  Serious Type: {incident.serious_incident_type}")
            if incident.reporting_deadline:
                console.print(f"  Reporting Deadline: {incident.reporting_deadline}")
        
        elif args.command == 'causal-link':
            incident = manager.load_incident(args.incident_id)
            if not incident:
                console.print(f"[red]Error:[/red] Incident {args.incident_id} not found")
                sys.exit(1)
            
            incident = manager.establish_causal_link(
                incident,
                established=args.established,
                evidence=args.evidence
            )
            console.print(f"\n[green]✓[/green] Updated causal link for: {incident.id}")
            console.print(f"  Causal Link Established: {incident.causal_link_established}")
            if incident.reporting_deadline:
                console.print(f"  Reporting Deadline: {incident.reporting_deadline}")
        
        elif args.command == 'timeline':
            incident = manager.load_incident(args.incident_id)
            if not incident:
                console.print(f"[red]Error:[/red] Incident {args.incident_id} not found")
                sys.exit(1)
            
            timeline = manager.track_reporting_timeline(incident)
            console.print(f"\n[bold]Reporting Timeline for {args.incident_id}[/bold]")
            console.print(f"  Status: {timeline['status']}")
            if 'days_remaining' in timeline:
                console.print(f"  Days Remaining: {timeline['days_remaining']}")
                console.print(f"  Hours Remaining: {timeline['hours_remaining']:.1f}")
            if timeline.get('deadline'):
                console.print(f"  Deadline: {timeline['deadline']}")
            console.print(f"  Reported: {timeline.get('reported', False)}")
        
        elif args.command == 'suggest-remediation':
            incident = manager.load_incident(args.incident_id)
            if not incident:
                console.print(f"[red]Error:[/red] Incident {args.incident_id} not found")
                sys.exit(1)
            
            suggestions = manager.suggest_remediation(incident)
            console.print(f"\n[bold]Remediation Suggestions for {args.incident_id}[/bold]")
            for i, suggestion in enumerate(suggestions, 1):
                console.print(f"  {i}. {suggestion}")
        
        elif args.command == 'notify-authority':
            incident = manager.load_incident(args.incident_id)
            if not incident:
                console.print(f"[red]Error:[/red] Incident {args.incident_id} not found")
                sys.exit(1)
            
            incident = manager.notify_authority(
                incident,
                authority_contact=args.authority_contact,
                notification_content=args.notification_content
            )
            console.print(f"\n[green]✓[/green] Recorded authority notification for: {incident.id}")
            console.print(f"  Authority Contact: {incident.authority_contact}")
            console.print(f"  Notified At: {incident.authority_notified_at}")
        
        elif args.command == 'submit-report':
            incident = manager.load_incident(args.incident_id)
            if not incident:
                console.print(f"[red]Error:[/red] Incident {args.incident_id} not found")
                sys.exit(1)
            
            incident = manager.submit_report(
                incident,
                report_type=args.type,
                report_content=args.content
            )
            console.print(f"\n[green]✓[/green] Submitted {args.type} report for: {incident.id}")
            if args.type == 'initial':
                console.print(f"  Initial Report At: {incident.initial_report_submitted_at}")
            else:
                console.print(f"  Complete Report At: {incident.complete_report_submitted_at}")
        
        elif args.command == 'risk-assessment':
            incident = manager.load_incident(args.incident_id)
            if not incident:
                console.print(f"[red]Error:[/red] Incident {args.incident_id} not found")
                sys.exit(1)
            
            incident = manager.perform_risk_assessment(incident, args.assessment)
            console.print(f"\n[green]✓[/green] Recorded risk assessment for: {incident.id}")
        
        elif args.command == 'list':
            incidents = manager.list_incidents(status=args.status)
            if not incidents:
                console.print("[yellow]No incidents found[/yellow]")
            else:
                table = format_incident_table(incidents)
                console.print(table)
        
        elif args.command == 'show':
            incident = manager.load_incident(args.incident_id)
            if not incident:
                console.print(f"[red]Error:[/red] Incident {args.incident_id} not found")
                sys.exit(1)
            
            detail = format_incident_detail(incident, manager)
            md = Markdown(detail)
            console.print(md)
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
