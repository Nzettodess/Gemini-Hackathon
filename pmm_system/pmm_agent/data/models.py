"""Data models for PMM system"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class MetricType(str, Enum):
    """Metric types"""
    RESPONSE_ACCURACY = "response_accuracy"
    HALLUCINATION_RATE = "hallucination_rate"
    PRIVACY_INCIDENTS = "privacy_incidents"
    USER_SATISFACTION = "user_satisfaction"
    PROMPT_INJECTION_ATTEMPTS = "prompt_injection_attempts"
    CITATION_ACCURACY = "citation_accuracy"


@dataclass
class AIInteraction:
    """AI system interaction record"""
    interaction_id: str
    timestamp: datetime
    user_id: Optional[str]
    prompt: str
    response: str
    response_time: float
    model_version: str
    metadata: Dict = field(default_factory=dict)
    demographics: Optional[Dict] = None


@dataclass
class SafetyThreshold:
    """Safety threshold configuration"""
    metric_name: str
    target: float
    alert_threshold: float
    critical_threshold: float


@dataclass
class MonitoringAlert:
    """Monitoring alert"""
    alert_id: str
    timestamp: datetime
    alert_type: str
    severity: AlertSeverity
    metric_name: str
    current_value: float
    threshold: float
    details: Dict = field(default_factory=dict)


@dataclass
class UserFeedback:
    """User feedback record"""
    feedback_id: str
    interaction_id: str
    user_id: Optional[str]
    timestamp: datetime
    rating: int  # 1-5
    comment: Optional[str]
    issues: List[str] = field(default_factory=list)
    sentiment: Optional[str] = None
    categories: List[str] = field(default_factory=list)


@dataclass
class MetricRecord:
    """Metric record for time series"""
    metric_name: str
    value: float
    timestamp: datetime
    tags: Dict = field(default_factory=dict)


@dataclass
class MonitoringPlan:
    """Monitoring plan configuration"""
    system_name: str
    metrics: Dict[str, SafetyThreshold]
    collection_methods: Dict
    reporting_cadence: str
    alert_thresholds: Dict
    created_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# Dashboard Models
# ============================================================================

class SignalType(str, Enum):
    """Signal detection types"""
    ANOMALY = "anomaly"
    TREND_CHANGE = "trend_change"
    THRESHOLD_BREACH = "threshold_breach"
    PATTERN_DETECTED = "pattern_detected"
    DRIFT_DETECTED = "drift_detected"


class SignalStatus(str, Enum):
    """Signal status"""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


class ComplaintStatus(str, Enum):
    """Complaint status"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    CLOSED = "closed"


class ComplaintPriority(str, Enum):
    """Complaint priority"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ReportType(str, Enum):
    """Regulatory report types"""
    PERIODIC = "periodic"
    INCIDENT = "incident"
    COMPLIANCE = "compliance"
    AUDIT = "audit"


class ReportStatus(str, Enum):
    """Report status"""
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    SUBMITTED = "submitted"


@dataclass
class Signal:
    """AI-detected signal/anomaly"""
    signal_id: str
    timestamp: datetime
    signal_type: SignalType
    severity: AlertSeverity
    metric_name: str
    detected_value: float
    expected_value: float
    deviation: float
    confidence: float
    description: str
    status: SignalStatus = SignalStatus.ACTIVE
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    context: Dict = field(default_factory=dict)


@dataclass
class Complaint:
    """User complaint record"""
    complaint_id: str
    created_at: datetime
    user_id: Optional[str]
    category: str
    subject: str
    description: str
    priority: ComplaintPriority
    status: ComplaintStatus = ComplaintStatus.OPEN
    assigned_to: Optional[str] = None
    related_interaction_id: Optional[str] = None
    resolution: Optional[str] = None
    resolved_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    updates: List[Dict] = field(default_factory=list)


@dataclass
class RegulatoryReport:
    """EU AI Act regulatory report"""
    report_id: str
    created_at: datetime
    report_type: ReportType
    period_start: datetime
    period_end: datetime
    status: ReportStatus
    title: str
    summary: str
    metrics_summary: Dict = field(default_factory=dict)
    incidents_summary: Dict = field(default_factory=dict)
    compliance_status: Dict = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    submitted_at: Optional[datetime] = None
    submitted_to: Optional[str] = None


@dataclass
class PerformanceSnapshot:
    """Performance monitoring snapshot"""
    timestamp: datetime
    response_time_avg: float
    response_time_p95: float
    throughput: float
    error_rate: float
    availability: float
    active_users: int
    metrics: Dict[str, float] = field(default_factory=dict)
