"""
Unified EU AI Act Metrics Definitions
======================================
Single source of truth for all EU AI Act Article 73 safety metrics.
Used by: metrics_exporter.py, critical_alert_detector.py, PMM system

Article 3(49) - Serious Incident Types:
- safety-001: Death or serious harm to health (Article 3(49)(a))
- safety-002: Critical infrastructure disruption (Article 3(49)(b))
- safety-003: Fundamental rights violations (Article 3(49)(c))
- safety-005: Serious harm to property/environment (Article 3(49)(d))
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any


class RiskCategory(str, Enum):
    """EU AI Act Article 3(49) serious incident risk categories"""
    SAFETY_001 = "safety-001"  # Death or serious harm to health
    SAFETY_002 = "safety-002"  # Critical infrastructure disruption
    SAFETY_003 = "safety-003"  # Fundamental rights violation
    SAFETY_005 = "safety-005"  # Property/environmental harm


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class EUAIActRiskMapping:
    """Risk mapping for EU AI Act compliance"""
    risk_id: str
    article_reference: str
    incident_type: str
    reporting_deadline_days: int
    severity: AlertSeverity
    description: str
    threshold_config: Dict[str, Any]


# Unified risk mappings - single source of truth
EU_AI_ACT_RISK_MAPPINGS = {
    RiskCategory.SAFETY_001: EUAIActRiskMapping(
        risk_id="safety-001",
        article_reference="Article 3(49)(a), Article 73(4)",
        incident_type="Death or serious harm to health",
        reporting_deadline_days=10,
        severity=AlertSeverity.CRITICAL,
        description="Death of a person or serious harm to a person's health",
        threshold_config={
            "health_impact_score": 9.0,
            "fatality_detected": True,
            "immediate_notification": True
        }
    ),
    RiskCategory.SAFETY_002: EUAIActRiskMapping(
        risk_id="safety-002",
        article_reference="Article 3(49)(b), Article 73(3)",
        incident_type="Critical infrastructure disruption",
        reporting_deadline_days=2,
        severity=AlertSeverity.CRITICAL,
        description="Serious and irreversible disruption of critical infrastructure",
        threshold_config={
            "infrastructure_impact_score": 8.5,
            "disruption_duration_minutes": 15,
            "affected_services": 1
        }
    ),
    RiskCategory.SAFETY_003: EUAIActRiskMapping(
        risk_id="safety-003",
        article_reference="Article 3(49)(c), Article 73(2)",
        incident_type="Fundamental rights violation",
        reporting_deadline_days=15,
        severity=AlertSeverity.HIGH,
        description="Infringement of Union law protecting fundamental rights",
        threshold_config={
            "rights_violation_score": 7.0,
            "affected_individuals": 1,
            "bias_detection_threshold": 0.15
        }
    ),
    RiskCategory.SAFETY_005: EUAIActRiskMapping(
        risk_id="safety-005",
        article_reference="Article 3(49)(d), Article 73(2)",
        incident_type="Property/environmental harm",
        reporting_deadline_days=15,
        severity=AlertSeverity.HIGH,
        description="Serious harm to property or the environment",
        threshold_config={
            "damage_value_eur": 50000,
            "environmental_impact_score": 7.5,
            "affected_area_km2": 0.1
        }
    )
}


# Metric name constants
class MetricNames:
    """Standard metric names for EU AI Act monitoring"""
    # Safety-001 metrics
    HEALTH_IMPACT_SCORE = "ai_system_health_impact_score"
    FATALITY_DETECTED = "ai_system_fatality_detected"
    
    # Safety-002 metrics
    INFRASTRUCTURE_IMPACT_SCORE = "ai_system_infrastructure_impact_score"
    DISRUPTION_DURATION_MINUTES = "ai_system_disruption_duration_minutes"
    
    # Safety-003 metrics
    RIGHTS_VIOLATION_SCORE = "ai_system_rights_violation_score"
    BIAS_SCORE = "ai_system_bias_score"
    
    # Safety-005 metrics
    DAMAGE_VALUE_EUR = "ai_system_damage_value_eur"
    ENVIRONMENTAL_IMPACT_SCORE = "ai_system_environmental_impact_score"
    
    # General metrics
    ERROR_RATE = "ai_system_error_rate"
    PREDICTION_LATENCY = "ai_system_prediction_latency_seconds"
    PREDICTIONS_TOTAL = "ai_system_predictions_total"
    SERIOUS_INCIDENTS_TOTAL = "ai_system_serious_incidents_total"
    COMPLIANCE_STATUS = "ai_system_compliance_status"


def get_risk_mapping(risk_category: RiskCategory) -> EUAIActRiskMapping:
    """Get risk mapping for a specific category"""
    return EU_AI_ACT_RISK_MAPPINGS[risk_category]


def get_reporting_deadline(risk_category: RiskCategory) -> int:
    """Get reporting deadline in days for a risk category"""
    return EU_AI_ACT_RISK_MAPPINGS[risk_category].reporting_deadline_days


def get_threshold_config(risk_category: RiskCategory) -> Dict[str, Any]:
    """Get threshold configuration for a risk category"""
    return EU_AI_ACT_RISK_MAPPINGS[risk_category].threshold_config


def is_critical_risk(risk_category: RiskCategory) -> bool:
    """Check if risk category is critical severity"""
    return EU_AI_ACT_RISK_MAPPINGS[risk_category].severity == AlertSeverity.CRITICAL
