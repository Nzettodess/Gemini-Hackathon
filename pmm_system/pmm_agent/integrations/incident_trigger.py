"""
Integration with incident-responder skill and EU AI Act Article 73 incident management
REFACTORED: Now uses the main incident_management.py system for EU AI Act compliance
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional
import sys
from pathlib import Path

from ..data.models import MonitoringAlert, AlertSeverity

# Import main incident management system
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
try:
    from incident_management import IncidentManager, IncidentSeverity, SeriousIncidentType
    INCIDENT_MANAGEMENT_AVAILABLE = True
except ImportError:
    INCIDENT_MANAGEMENT_AVAILABLE = False
    IncidentManager = None


class IncidentTrigger:
    """
    Trigger incident response - Integrated with EU AI Act Article 73 compliance
    
    This class now acts as a bridge between PMM monitoring alerts and the 
    comprehensive EU AI Act incident management system.

    Based on: skills/health-safety/skills/incident-responder/SKILL.md
    Enhanced with: EU AI Act Article 73 compliance via incident_management.py
    """

    # Severity mapping based on incident-responder SKILL
    SEVERITY_MAPPING = {
        AlertSeverity.CRITICAL: {
            'priority': 'P1',
            'response_time': '< 5 minutes',
            'classification': 'security_breach',
            'incident_severity': IncidentSeverity.CRITICAL if INCIDENT_MANAGEMENT_AVAILABLE else None
        },
        AlertSeverity.HIGH: {
            'priority': 'P2',
            'response_time': '< 1 hour',
            'classification': 'compliance_violation',
            'incident_severity': IncidentSeverity.HIGH if INCIDENT_MANAGEMENT_AVAILABLE else None
        },
        AlertSeverity.MEDIUM: {
            'priority': 'P3',
            'response_time': '< 24 hours',
            'classification': 'service_outage',
            'incident_severity': IncidentSeverity.MEDIUM if INCIDENT_MANAGEMENT_AVAILABLE else None
        },
        AlertSeverity.LOW: {
            'priority': 'P4',
            'response_time': '< 1 week',
            'classification': 'data_incident',
            'incident_severity': IncidentSeverity.LOW if INCIDENT_MANAGEMENT_AVAILABLE else None
        }
    }

    def __init__(self):
        self.incident_counter = 0
        self.active_incidents = []
        self.incident_history = []
        
        # Initialize EU AI Act incident manager if available
        if INCIDENT_MANAGEMENT_AVAILABLE:
            self.incident_manager = IncidentManager(use_ai=True)
            print("✓ EU AI Act Article 73 incident management enabled")
        else:
            self.incident_manager = None
            print("⚠️  EU AI Act incident management not available - using fallback mode")

    def create_incident(self,
                       alert: MonitoringAlert,
                       context: Dict = None) -> str:
        """
        Create incident and trigger response
        
        ENHANCED: Now creates EU AI Act Article 73 compliant incidents when available,
        with fallback to original PMM incident tracking.

        Based on incident-responder First response procedures:
        - Initial assessment
        - Severity determination
        - Team mobilization
        - Containment actions
        - Evidence preservation

        Args:
            alert: Monitoring alert
            context: Additional context

        Returns:
            incident_id
        """
        severity_config = self.SEVERITY_MAPPING.get(
            alert.severity,
            self.SEVERITY_MAPPING[AlertSeverity.MEDIUM]
        )
        
        # Use EU AI Act incident management if available
        if self.incident_manager and INCIDENT_MANAGEMENT_AVAILABLE:
            # Create EU AI Act compliant incident
            eu_incident = self.incident_manager.create_incident(
                title=f"PMM Alert: {alert.alert_type}",
                description=f"Monitoring alert triggered:\n"
                           f"Metric: {alert.metric_name}\n"
                           f"Current Value: {alert.current_value:.3f}\n"
                           f"Threshold: {alert.threshold:.3f}\n"
                           f"Alert Type: {alert.alert_type}\n"
                           f"Context: {context or {}}",
                ai_system_id=context.get('ai_system_id', 'PMM-MONITORED-SYSTEM') if context else 'PMM-MONITORED-SYSTEM',
                ai_system_name=context.get('ai_system_name', 'AI System under PMM') if context else 'AI System under PMM',
                member_state=context.get('member_state', 'EU') if context else 'EU',
                detected_by="automated_pmm",
                metadata={
                    'pmm_alert_id': alert.alert_id,
                    'pmm_priority': severity_config['priority'],
                    'pmm_classification': severity_config['classification'],
                    'response_time_sla': severity_config['response_time'],
                    'alert_severity': alert.severity.value,
                    'context': context or {}
                }
            )
            
            incident_id = eu_incident.id
            
            # Add AI-suggested remediation actions
            if self.incident_manager.use_ai:
                remediation_actions = self.incident_manager.suggest_remediation(eu_incident)
                for action in remediation_actions[:5]:  # Add top 5 suggestions
                    self.incident_manager.add_remediation_action(eu_incident, action, ai_suggested=True)
            
            # Also maintain PMM-specific tracking
            pmm_incident = {
                'incident_id': incident_id,
                'eu_ai_act_incident': True,
                'created_at': datetime.now(timezone.utc),
                'alert': alert,
                'priority': severity_config['priority'],
                'classification': severity_config['classification'],
                'response_time_sla': severity_config['response_time'],
                'status': 'open',
                'context': context or {},
                'actions_taken': [],
                'response_plan': self._generate_response_plan(alert),
                'eu_incident_object': eu_incident
            }
            
            self.active_incidents.append(pmm_incident)
            self.incident_history.append(pmm_incident)
            
            print(f"\n{'='*60}")
            print(f"🚨 EU AI ACT INCIDENT CREATED: {incident_id}")
            print(f"{'='*60}")
            print(f"Priority: {severity_config['priority']}")
            print(f"Classification: {severity_config['classification']}")
            print(f"Response Time SLA: {severity_config['response_time']}")
            print(f"EU AI Act Compliance: Article 73")
            if eu_incident.is_serious:
                print(f"⚠️  SERIOUS INCIDENT - Reporting deadline: {eu_incident.reporting_timeline_days} days")
            print(f"Alert Type: {alert.alert_type}")
            print(f"Severity: {alert.severity.value}")
            print(f"Metric: {alert.metric_name} = {alert.current_value:.3f}")
            print(f"Threshold: {alert.threshold:.3f}")
            print(f"\nRecommended Actions (PMM + EU AI Act):")
            for i, action in enumerate(pmm_incident['response_plan'], 1):
                print(f"  {i}. {action}")
            print(f"{'='*60}\n")
            
        else:
            # Fallback to original PMM incident tracking
            self.incident_counter += 1
            incident_id = f"INC-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{self.incident_counter:04d}"

            incident = {
                'incident_id': incident_id,
                'eu_ai_act_incident': False,
                'created_at': datetime.now(timezone.utc),
                'alert': alert,
                'priority': severity_config['priority'],
                'classification': severity_config['classification'],
                'response_time_sla': severity_config['response_time'],
                'status': 'open',
                'context': context or {},
                'actions_taken': [],
                'response_plan': self._generate_response_plan(alert)
            }

            self.active_incidents.append(incident)
            self.incident_history.append(incident)

            print(f"\n{'='*60}")
            print(f"🚨 INCIDENT CREATED: {incident_id}")
            print(f"{'='*60}")
            print(f"Priority: {severity_config['priority']}")
            print(f"Classification: {severity_config['classification']}")
            print(f"Response Time SLA: {severity_config['response_time']}")
            print(f"Alert Type: {alert.alert_type}")
            print(f"Severity: {alert.severity.value}")
            print(f"Metric: {alert.metric_name} = {alert.current_value:.3f}")
            print(f"Threshold: {alert.threshold:.3f}")
            print(f"\nRecommended Actions:")
            for i, action in enumerate(incident['response_plan'], 1):
                print(f"  {i}. {action}")
            print(f"{'='*60}\n")

        return incident_id

    def _generate_response_plan(self, alert: MonitoringAlert) -> List[str]:
        """Generate response plan based on alert type"""
        base_actions = [
            "Initial assessment of impact scope",
            "Preserve evidence and logs",
            "Notify response team"
        ]

        # Add specific actions based on alert type
        if 'bias' in alert.alert_type.lower():
            base_actions.extend([
                "Review model outputs for affected demographic groups",
                "Analyze training data for bias",
                "Implement temporary output filtering if needed",
                "Prepare user communication"
            ])
        elif 'privacy' in alert.alert_type.lower():
            base_actions.extend([
                "Identify exposed data",
                "Contain data exposure",
                "Assess regulatory notification requirements",
                "Prepare incident disclosure"
            ])
        elif 'performance' in alert.alert_type.lower() or 'accuracy' in alert.alert_type.lower():
            base_actions.extend([
                "Analyze recent model changes",
                "Review input data quality",
                "Check for data drift",
                "Consider model rollback"
            ])
        else:
            base_actions.extend([
                "Investigate root cause",
                "Implement temporary mitigation",
                "Plan permanent fix"
            ])

        base_actions.append("Document findings and actions")

        return base_actions

    def get_active_incidents(self) -> List[Dict]:
        """Get list of active (open) incidents"""
        return [inc for inc in self.active_incidents if inc['status'] == 'open']

    def get_incident(self, incident_id: str) -> Optional[Dict]:
        """Get specific incident by ID"""
        for incident in self.incident_history:
            if incident['incident_id'] == incident_id:
                return incident
        return None

    def update_incident(self, incident_id: str, update: Dict):
        """Update incident with new information"""
        for incident in self.active_incidents:
            if incident['incident_id'] == incident_id:
                incident.update(update)
                if 'action' in update:
                    incident['actions_taken'].append({
                        'timestamp': datetime.now(timezone.utc),
                        'action': update['action']
                    })
                break

    def close_incident(self, incident_id: str, resolution: str):
        """Close an incident"""
        for incident in self.active_incidents:
            if incident['incident_id'] == incident_id:
                incident['status'] = 'closed'
                incident['closed_at'] = datetime.now(timezone.utc)
                incident['resolution'] = resolution
                print(f"✓ Incident {incident_id} closed: {resolution}")
                break

    def get_incident_stats(self) -> Dict:
        """Get incident statistics"""
        return {
            'total_incidents': len(self.incident_history),
            'active_incidents': len(self.get_active_incidents()),
            'closed_incidents': len([i for i in self.incident_history if i['status'] == 'closed']),
            'by_priority': self._count_by_field('priority'),
            'by_classification': self._count_by_field('classification')
        }

    def _count_by_field(self, field: str) -> Dict[str, int]:
        """Count incidents by a specific field"""
        from collections import Counter
        return dict(Counter(inc[field] for inc in self.incident_history if field in inc))
