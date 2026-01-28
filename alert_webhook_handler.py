"""
Webhook handler for Grafana alerts
Integrates with EU AI Act Article 73 incident management system
REFACTORED: Now uses unified incident_management.py for compliance
"""

from flask import Flask, request, jsonify
from datetime import datetime
from typing import Dict, Any
import json
from rich.console import Console

from security_input import InMemoryRateLimiter, InputValidationError, validate_grafana_alert_payload

console = Console()

app = Flask(__name__)

rate_limiter = InMemoryRateLimiter()


class AlertWebhookHandler:
    """
    Handles incoming Grafana alerts and creates EU AI Act compliant incidents
    
    Integration: Uses incident_management.py for Article 73 compliance
    """
    
    def __init__(self):
        self.incident_manager = None
        self._load_incident_manager()
    
    def _load_incident_manager(self):
        """Load EU AI Act incident manager"""
        try:
            from incident_management import IncidentManager
            self.incident_manager = IncidentManager(use_ai=True)
            console.print("[green]✓ EU AI Act Article 73 incident management loaded[/green]")
        except ImportError:
            console.print("[yellow]Warning: incident_management module not available[/yellow]")
    
    def process_alert(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming Grafana alert"""
        
        if alert_data.get('status') == 'firing':
            return self._handle_firing_alert(alert_data)
        elif alert_data.get('status') == 'resolved':
            return self._handle_resolved_alert(alert_data)
        
        return {'status': 'ignored', 'reason': 'unknown alert status'}
    
    def _handle_firing_alert(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a firing alert - creates EU AI Act compliant incidents"""
        
        alerts = alert_data.get('alerts', [])
        results = []
        
        for alert in alerts:
            labels = alert.get('labels', {})
            annotations = alert.get('annotations', {})
            
            risk_id = labels.get('risk_id', 'unknown')
            severity = labels.get('severity', 'medium')
            
            console.print(f"\n[bold red]🚨 ALERT FIRING[/bold red]")
            console.print(f"Risk ID: {risk_id}")
            console.print(f"Severity: {severity}")
            console.print(f"Description: {annotations.get('description', 'N/A')}")
            
            if self.incident_manager and risk_id.startswith('safety-'):
                # Create EU AI Act Article 73 compliant incident
                try:
                    incident = self.incident_manager.create_incident(
                        title=annotations.get('summary', labels.get('alertname', 'Grafana Alert')),
                        description=f"{annotations.get('description', '')}\n\n"
                                   f"Alert Details:\n"
                                   f"Risk ID: {risk_id}\n"
                                   f"Severity: {severity}\n"
                                   f"Article Reference: {annotations.get('article_reference', 'N/A')}\n"
                                   f"Alert Fingerprint: {alert.get('fingerprint', 'N/A')}",
                        ai_system_id=labels.get('ai_system_id', 'GRAFANA-MONITORED-SYSTEM'),
                        ai_system_name=labels.get('ai_system', 'AI System'),
                        member_state=labels.get('member_state', 'EU'),
                        detected_by='grafana_alert',
                        metadata={
                            'grafana_alert': True,
                            'alert_fingerprint': alert.get('fingerprint', ''),
                            'risk_id': risk_id,
                            'severity_label': severity,
                            'article_reference': annotations.get('article_reference', ''),
                            'reporting_deadline': annotations.get('reporting_deadline', ''),
                            'alert_labels': labels,
                            'alert_annotations': annotations
                        }
                    )
                    
                    # AI classification happens automatically in create_incident if AI is available
                    result = {
                        'status': 'eu_ai_act_incident_created',
                        'incident_id': incident.id,
                        'risk_id': risk_id,
                        'is_serious': incident.is_serious,
                        'severity': incident.severity.value if incident.severity else 'unclassified',
                        'article_73_compliant': True
                    }
                    
                    if incident.is_serious:
                        result['reporting_deadline_days'] = incident.reporting_timeline_days
                        result['incident_type'] = incident.incident_type.value if incident.incident_type else None
                        console.print(f"[yellow]⚠️  SERIOUS INCIDENT - {incident.reporting_timeline_days} days reporting deadline[/yellow]")
                    
                    results.append(result)
                    console.print(f"[green]✓ EU AI Act incident created: {incident.id}[/green]")
                    
                except Exception as e:
                    console.print(f"[red]Error creating incident: {e}[/red]")
                    import traceback
                    console.print(f"[dim]{traceback.format_exc()}[/dim]")
                    results.append({
                        'status': 'error',
                        'error': str(e),
                        'risk_id': risk_id
                    })
            else:
                results.append({
                    'status': 'logged',
                    'risk_id': risk_id,
                    'note': 'No incident manager available or non-safety alert'
                })
        
        return {
            'status': 'processed',
            'alerts_processed': len(alerts),
            'results': results
        }
    
    def _handle_resolved_alert(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a resolved alert"""
        
        alerts = alert_data.get('alerts', [])
        
        for alert in alerts:
            labels = alert.get('labels', {})
            risk_id = labels.get('risk_id', 'unknown')
            
            console.print(f"\n[bold green]✓ ALERT RESOLVED[/bold green]")
            console.print(f"Risk ID: {risk_id}")
        
        return {
            'status': 'resolved',
            'alerts_resolved': len(alerts)
        }
    


webhook_handler = AlertWebhookHandler()


@app.route('/api/alerts/webhook', methods=['POST'])
def handle_webhook():
    """Webhook endpoint for Grafana alerts"""
    
    try:
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
        if not rate_limiter.allow(f"grafana_webhook:{client_ip}"):
            return jsonify({'error': 'Rate limit exceeded'}), 429

        alert_data = request.get_json(silent=True)
        
        if not alert_data:
            return jsonify({'error': 'No data received'}), 400

        alert_data, _ = validate_grafana_alert_payload(alert_data)
        
        result = webhook_handler.process_alert(alert_data)
        
        return jsonify(result), 200

    except InputValidationError as e:
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        console.print(f"[red]Webhook error: {e}[/red]")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'eu-ai-act-alert-webhook',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/alerts/test', methods=['POST'])
def test_alert():
    """Test endpoint to simulate an alert"""
    
    test_alert = {
        'status': 'firing',
        'alerts': [
            {
                'labels': {
                    'alertname': 'Test Alert',
                    'severity': 'critical',
                    'risk_id': 'safety-001',
                    'ai_system': 'test_system'
                },
                'annotations': {
                    'summary': 'Test critical safety alert',
                    'description': 'This is a test alert for safety-001',
                    'article_reference': 'Article 3(49)(a), Article 73(4)',
                    'reporting_deadline': '10 days'
                },
                'fingerprint': 'test123456',
                'startsAt': datetime.now().isoformat()
            }
        ]
    }
    
    result = webhook_handler.process_alert(test_alert)
    return jsonify(result), 200


if __name__ == '__main__':
    console.print("[bold cyan]Starting Alert Webhook Handler[/bold cyan]")
    console.print("Listening on http://localhost:8002")
    app.run(host='0.0.0.0', port=8002, debug=True)
