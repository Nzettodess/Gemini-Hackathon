#!/usr/bin/env python3
"""
EU AI Act Article 73 - Incident Management System
==================================================
Comprehensive incident management for high-risk AI systems with:
- Incident detection (automated and manual)
- Severity classification (Article 3(49))
- Timeline tracking (2/10/15 day reporting deadlines)
- Remediation workflow with AI assistance
- Regulatory notification
- Investigation and risk assessment

EU AI Act Compliance: Article 73 - Reporting of serious incidents
"""

import json
import os
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
import uuid

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class IncidentSeverity(str, Enum):
    """Incident severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SeriousIncidentType(str, Enum):
    """Serious incident types per EU AI Act Article 3(49)."""
    TYPE_A = "a"  # Death or serious harm to person's health → 10 days
    TYPE_B = "b"  # Serious disruption of critical infrastructure → 2 days
    TYPE_C = "c"  # Infringement of fundamental rights → 15 days
    TYPE_D = "d"  # Serious harm to property/environment → 15 days
    NOT_SERIOUS = "not_serious"  # Not a serious incident


class IncidentStatus(str, Enum):
    """Incident lifecycle status."""
    DETECTED = "detected"
    CLASSIFYING = "classifying"
    INVESTIGATING = "investigating"
    REMEDIATING = "remediating"
    REPORTING = "reporting"
    RESOLVED = "resolved"
    CLOSED = "closed"


@dataclass
class Incident:
    """Incident record for EU AI Act Article 73 compliance."""
    id: str
    title: str
    description: str
    detected_at: str
    detected_by: str  # "automated" or "human"
    ai_system_id: str
    ai_system_name: str
    member_state: str
    
    # Classification
    severity: Optional[str] = None
    incident_type: Optional[str] = None
    is_serious: bool = False
    serious_incident_type: Optional[str] = None
    
    # Causal link (Article 73(2))
    causal_link_established: bool = False
    causal_link_established_at: Optional[str] = None
    causal_link_evidence: Optional[str] = None
    
    # Reporting timeline (Article 73)
    reporting_deadline: Optional[str] = None
    reporting_timeline_days: Optional[int] = None
    initial_report_submitted: bool = False
    initial_report_submitted_at: Optional[str] = None
    complete_report_submitted: bool = False
    complete_report_submitted_at: Optional[str] = None
    
    # Status and workflow
    status: str = "detected"
    remediation_actions: List[str] = field(default_factory=list)
    remediation_status: str = "pending"
    corrective_actions: List[str] = field(default_factory=list)
    
    # Regulatory notification (Article 73(1))
    authority_notified: bool = False
    authority_notified_at: Optional[str] = None
    authority_contact: Optional[str] = None
    
    # Investigation (Article 73(6))
    investigation_notes: List[str] = field(default_factory=list)
    risk_assessment: Optional[str] = None
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert incident to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Incident':
        """Create incident from dictionary."""
        return cls(**data)


class IncidentManager:
    """Manages incidents for EU AI Act Article 73 compliance."""
    
    def __init__(self, incidents_dir: Optional[Path] = None, use_ai: bool = True):
        """
        Initialize incident manager.
        
        Args:
            incidents_dir: Directory to store incident JSON files
            use_ai: Whether to use AI for classification and remediation suggestions
        """
        self.use_ai = use_ai and GEMINI_AVAILABLE
        self.incidents_dir = incidents_dir or Path(__file__).parent / "incidents"
        self.incidents_dir.mkdir(exist_ok=True)
        
        if self.use_ai:
            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key:
                api_key = api_key.strip().split('\n')[0].split('\r')[0]
                try:
                    self.client = genai.Client(api_key=api_key)
                except Exception:
                    self.use_ai = False
            else:
                self.use_ai = False
    
    def create_incident(
        self,
        title: str,
        description: str,
        ai_system_id: str,
        ai_system_name: str,
        member_state: str,
        detected_by: str = "human",
        **kwargs
    ) -> Incident:
        """
        Create a new incident record.
        
        Args:
            title: Incident title
            description: Detailed description
            ai_system_id: Identifier of the AI system
            ai_system_name: Name of the AI system
            member_state: EU Member State where incident occurred
            detected_by: "automated" or "human"
            **kwargs: Additional fields
        
        Returns:
            Created incident
        """
        incident_id = f"INC-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:1]}"
        
        incident = Incident(
            id=incident_id,
            title=title,
            description=description,
            detected_at=datetime.utcnow().isoformat(),
            detected_by=detected_by,
            ai_system_id=ai_system_id,
            ai_system_name=ai_system_name,
            member_state=member_state,
            status=IncidentStatus.DETECTED.value,
            **kwargs
        )
        
        self._save_incident(incident)
        return incident
    
    def classify_severity(self, incident: Incident, human_override: Optional[str] = None) -> Incident:
        """
        Classify incident severity and determine if it's a serious incident (Article 3(49)).
        Uses AI assistance but requires human judgment for serious incidents.
        
        Args:
            incident: Incident to classify
            human_override: Optional human override for serious incident type
        
        Returns:
            Updated incident
        """
        if human_override:
            # Human has already classified
            incident.serious_incident_type = human_override
            incident.is_serious = human_override != SeriousIncidentType.NOT_SERIOUS.value
            self._calculate_reporting_timeline(incident)
            incident.status = IncidentStatus.INVESTIGATING.value
            self._save_incident(incident)
            return incident
        
        # AI-assisted classification
        if self.use_ai:
            classification = self._ai_classify_severity(incident)
            incident.severity = classification.get("severity", "medium")
            incident.incident_type = classification.get("incident_type")
            incident.is_serious = classification.get("is_serious", False)
            incident.serious_incident_type = classification.get("serious_incident_type")
        else:
            # Basic classification without AI
            incident.severity = "medium"
            incident.is_serious = False
        
        if incident.is_serious:
            self._calculate_reporting_timeline(incident)
            incident.status = IncidentStatus.INVESTIGATING.value
        else:
            incident.status = IncidentStatus.REMEDIATING.value
        
        self._save_incident(incident)
        return incident
    
    def establish_causal_link(
        self,
        incident: Incident,
        established: bool,
        evidence: Optional[str] = None
    ) -> Incident:
        """
        Establish causal link between AI system and incident (Article 73(2)).
        
        Args:
            incident: Incident to update
            established: Whether causal link is established
            evidence: Evidence supporting the determination
        
        Returns:
            Updated incident
        """
        incident.causal_link_established = established
        incident.causal_link_established_at = datetime.utcnow().isoformat()
        if evidence:
            incident.causal_link_evidence = evidence
            incident.investigation_notes.append(
                f"Causal link {'established' if established else 'not established'}: {evidence}"
            )
        
        # Recalculate deadline based on causal link establishment
        if established and incident.is_serious:
            self._calculate_reporting_timeline(incident)
        
        incident.updated_at = datetime.utcnow().isoformat()
        self._save_incident(incident)
        return incident
    
    def track_reporting_timeline(self, incident: Incident) -> Dict:
        """
        Track reporting timeline and return status.
        
        Args:
            incident: Incident to track
        
        Returns:
            Timeline status
        """
        if not incident.is_serious:
            return {"status": "not_serious", "message": "No reporting required"}
        
        if not incident.reporting_deadline:
            return {"status": "no_deadline", "message": "Deadline not calculated"}
        
        deadline = datetime.fromisoformat(incident.reporting_deadline.replace('Z', '+00:00'))
        now = datetime.utcnow()
        
        if deadline.tzinfo:
            now = now.replace(tzinfo=deadline.tzinfo)
        
        days_remaining = (deadline - now).days
        hours_remaining = (deadline - now).total_seconds() / 3600
        
        status = "on_track"
        if days_remaining < 0:
            status = "overdue"
        elif days_remaining <= 1:
            status = "urgent"
        elif days_remaining <= 3:
            status = "approaching"
        
        return {
            "status": status,
            "days_remaining": days_remaining,
            "hours_remaining": hours_remaining,
            "deadline": incident.reporting_deadline,
            "reported": incident.complete_report_submitted,
            "initial_reported": incident.initial_report_submitted
        }
    
    def suggest_remediation(self, incident: Incident) -> List[str]:
        """
        Suggest remediation actions using AI assistance.
        Human approval required before implementation.
        
        Args:
            incident: Incident to suggest remediation for
        
        Returns:
            List of suggested remediation actions
        """
        if self.use_ai:
            suggestions = self._ai_suggest_remediation(incident)
        else:
            # Basic suggestions without AI
            suggestions = [
                "Conduct root cause analysis",
                "Implement immediate containment measures",
                "Review and update risk management system (Article 9)",
                "Update technical documentation",
                "Notify affected users if required"
            ]
        
        incident.remediation_actions.extend([f"[AI Suggested] {s}" for s in suggestions])
        incident.updated_at = datetime.utcnow().isoformat()
        self._save_incident(incident)
        return suggestions
    
    def notify_authority(
        self,
        incident: Incident,
        authority_contact: str,
        notification_content: Optional[str] = None
    ) -> Incident:
        """
        Record authority notification (Article 73(1)).
        Note: This records the notification; actual submission should be done separately.
        
        Args:
            incident: Incident to notify about
            authority_contact: Contact information for market surveillance authority
            notification_content: Content of the notification
        
        Returns:
            Updated incident
        """
        incident.authority_notified = True
        incident.authority_notified_at = datetime.utcnow().isoformat()
        incident.authority_contact = authority_contact
        
        if notification_content:
            incident.investigation_notes.append(
                f"Authority notified: {notification_content}"
            )
        
        incident.updated_at = datetime.utcnow().isoformat()
        self._save_incident(incident)
        return incident
    
    def submit_report(
        self,
        incident: Incident,
        report_type: str = "complete",
        report_content: Optional[str] = None
    ) -> Incident:
        """
        Submit incident report (initial or complete) per Article 73(5).
        
        Args:
            incident: Incident to report
            report_type: "initial" or "complete"
            report_content: Content of the report
        
        Returns:
            Updated incident
        """
        if report_type == "initial":
            incident.initial_report_submitted = True
            incident.initial_report_submitted_at = datetime.utcnow().isoformat()
        else:
            incident.complete_report_submitted = True
            incident.complete_report_submitted_at = datetime.utcnow().isoformat()
            incident.status = IncidentStatus.REPORTING.value
        
        if report_content:
            incident.investigation_notes.append(
                f"{report_type.capitalize()} report submitted: {report_content[:200]}"
            )
        
        incident.updated_at = datetime.utcnow().isoformat()
        self._save_incident(incident)
        return incident
    
    def perform_risk_assessment(self, incident: Incident, assessment: str) -> Incident:
        """
        Record risk assessment per Article 73(6).
        
        Args:
            incident: Incident to assess
            assessment: Risk assessment content
        
        Returns:
            Updated incident
        """
        incident.risk_assessment = assessment
        incident.investigation_notes.append(f"Risk assessment: {assessment}")
        incident.updated_at = datetime.utcnow().isoformat()
        self._save_incident(incident)
        return incident
    
    def load_incident(self, incident_id: str) -> Optional[Incident]:
        """Load incident from file."""
        incident_path = self.incidents_dir / f"{incident_id}.json"
        if not incident_path.exists():
            return None
        
        try:
            with incident_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
            return Incident.from_dict(data)
        except Exception:
            return None
    
    def list_incidents(self, status: Optional[str] = None) -> List[Incident]:
        """List all incidents, optionally filtered by status."""
        incidents = []
        for path in self.incidents_dir.glob("*.json"):
            try:
                with path.open('r', encoding='utf-8') as f:
                    data = json.load(f)
                incident = Incident.from_dict(data)
                if status is None or incident.status == status:
                    incidents.append(incident)
            except Exception:
                continue
        
        return sorted(incidents, key=lambda x: x.detected_at, reverse=True)
    
    def _calculate_reporting_timeline(self, incident: Incident):
        """Calculate reporting deadline based on serious incident type."""
        if not incident.is_serious or not incident.serious_incident_type:
            return
        
        # Determine timeline based on Article 73
        if incident.serious_incident_type == SeriousIncidentType.TYPE_B.value:
            # Critical infrastructure → 2 days (Article 73(3))
            days = 2
        elif incident.serious_incident_type == SeriousIncidentType.TYPE_A.value:
            # Death → 10 days (Article 73(4))
            days = 10
        else:
            # Other serious incidents → 15 days (Article 73(2))
            days = 15
        
        # Timeline starts from causal link establishment or detection
        if incident.causal_link_established_at:
            start_time = datetime.fromisoformat(incident.causal_link_established_at.replace('Z', '+00:00'))
        else:
            start_time = datetime.fromisoformat(incident.detected_at.replace('Z', '+00:00'))
        
        deadline = start_time + timedelta(days=days)
        incident.reporting_deadline = deadline.isoformat()
        incident.reporting_timeline_days = days
    
    def _ai_classify_severity(self, incident: Incident) -> Dict:
        """Use AI to classify incident severity."""
        prompt = f"""You are an expert on EU AI Act Article 3(49) serious incident classification.

Analyze this incident and classify it according to EU AI Act Article 3(49):

Incident Title: {incident.title}
Description: {incident.description}
AI System: {incident.ai_system_name}
Member State: {incident.member_state}

Serious incident types per Article 3(49):
(a) Death of a person, or serious harm to a person's health → 10 days reporting
(b) Serious and irreversible disruption of critical infrastructure → 2 days reporting
(c) Infringement of obligations under Union law protecting fundamental rights → 15 days reporting
(d) Serious harm to property or the environment → 15 days reporting

Provide your analysis in JSON format:
{{
    "severity": "low|medium|high|critical",
    "incident_type": "brief description",
    "is_serious": true/false,
    "serious_incident_type": "a|b|c|d|not_serious",
    "reasoning": "brief explanation"
}}

IMPORTANT: Only classify as serious if it clearly matches one of the Article 3(49) definitions.
Human judgment will be required for final confirmation of serious incidents."""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.3)
            )
            
            # Parse JSON from response
            text = response.text.strip()
            # Extract JSON if wrapped in markdown
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(text)
            return result
        except Exception as e:
            # Fallback to non-serious
            return {
                "severity": "medium",
                "is_serious": False,
                "serious_incident_type": SeriousIncidentType.NOT_SERIOUS.value
            }
    
    def _ai_suggest_remediation(self, incident: Incident) -> List[str]:
        """Use AI to suggest remediation actions."""
        prompt = f"""You are an expert on EU AI Act compliance and incident remediation.

Incident: {incident.title}
Description: {incident.description}
AI System: {incident.ai_system_name}
Severity: {incident.severity}
Is Serious: {incident.is_serious}

Suggest 3-5 specific remediation actions that comply with EU AI Act requirements.
Focus on:
- Immediate containment
- Root cause analysis
- Risk management system updates (Article 9)
- Technical documentation updates
- Corrective actions

Provide a JSON array of action strings:
["action 1", "action 2", "action 3"]"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.3)
            )
            
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            actions = json.loads(text)
            if isinstance(actions, list):
                return actions
            return []
        except Exception:
            return [
                "Conduct root cause analysis",
                "Implement immediate containment measures",
                "Review and update risk management system (Article 9)"
            ]
    
    def _save_incident(self, incident: Incident):
        """Save incident to JSON file."""
        incident.updated_at = datetime.utcnow().isoformat()
        incident_path = self.incidents_dir / f"{incident.id}.json"
        
        with incident_path.open('w', encoding='utf-8') as f:
            json.dump(incident.to_dict(), f, indent=2, ensure_ascii=False)
