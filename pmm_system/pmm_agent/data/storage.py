"""Data storage layer - simplified in-memory implementation"""
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
import json
from pathlib import Path

from .models import (
    AIInteraction, MonitoringAlert, UserFeedback, MetricRecord,
    Signal, Complaint, RegulatoryReport, PerformanceSnapshot,
    SignalStatus, ComplaintStatus
)


class InMemoryStorage:
    """In-memory storage for development/testing"""

    def __init__(self):
        self.interactions: List[AIInteraction] = []
        self.alerts: List[MonitoringAlert] = []
        self.feedback: List[UserFeedback] = []
        self.metrics: Dict[str, List[MetricRecord]] = defaultdict(list)
        # Dashboard data
        self.signals: List[Signal] = []
        self.complaints: List[Complaint] = []
        self.regulatory_reports: List[RegulatoryReport] = []
        self.performance_snapshots: List[PerformanceSnapshot] = []
        self.storage_path = Path("pmm_data")
        self.storage_path.mkdir(exist_ok=True)

    def store_interaction(self, interaction: AIInteraction):
        """Store an interaction"""
        self.interactions.append(interaction)
        self._persist_to_file("interactions")

    def store_alert(self, alert: MonitoringAlert):
        """Store an alert"""
        self.alerts.append(alert)
        self._persist_to_file("alerts")

    def store_feedback(self, feedback: UserFeedback):
        """Store user feedback"""
        self.feedback.append(feedback)
        self._persist_to_file("feedback")

    def store_metric(self, metric: MetricRecord):
        """Store a metric"""
        self.metrics[metric.metric_name].append(metric)
        self._persist_to_file(f"metrics_{metric.metric_name}")

    def get_interactions(self,
                         start_time: Optional[datetime] = None,
                         end_time: Optional[datetime] = None) -> List[AIInteraction]:
        """Get interactions in time range"""
        if not start_time:
            start_time = datetime.min
        if not end_time:
            end_time = datetime.now(timezone.utc)

        return [i for i in self.interactions
                if start_time <= i.timestamp <= end_time]

    def get_metrics(self,
                   metric_name: str,
                   start_time: Optional[datetime] = None,
                   end_time: Optional[datetime] = None) -> List[MetricRecord]:
        """Get metrics in time range"""
        if not start_time:
            start_time = datetime.min
        if not end_time:
            end_time = datetime.now(timezone.utc)

        metrics = self.metrics.get(metric_name, [])
        return [m for m in metrics
                if start_time <= m.timestamp <= end_time]

    def get_active_alerts(self) -> List[MonitoringAlert]:
        """Get active alerts (last 24 hours)"""
        threshold = datetime.now(timezone.utc) - timedelta(hours=24)
        return [a for a in self.alerts if a.timestamp >= threshold]

    def get_recent_feedback(self, days: int = 7) -> List[UserFeedback]:
        """Get recent feedback"""
        threshold = datetime.now(timezone.utc) - timedelta(days=days)
        return [f for f in self.feedback if f.timestamp >= threshold]

    # ========================================================================
    # Signal Storage
    # ========================================================================

    def store_signal(self, signal: Signal):
        """Store a detected signal"""
        self.signals.append(signal)
        self._persist_to_file("signals")

    def get_signals(self,
                   status: Optional[SignalStatus] = None,
                   start_time: Optional[datetime] = None,
                   end_time: Optional[datetime] = None) -> List[Signal]:
        """Get signals with optional filters"""
        result = self.signals

        if status:
            result = [s for s in result if s.status == status]

        if start_time:
            result = [s for s in result if s.timestamp >= start_time]

        if end_time:
            result = [s for s in result if s.timestamp <= end_time]

        return result

    def get_active_signals(self) -> List[Signal]:
        """Get active signals"""
        return [s for s in self.signals if s.status == SignalStatus.ACTIVE]

    def update_signal(self, signal_id: str, updates: Dict):
        """Update a signal"""
        for signal in self.signals:
            if signal.signal_id == signal_id:
                for key, value in updates.items():
                    if hasattr(signal, key):
                        setattr(signal, key, value)
                self._persist_to_file("signals")
                return True
        return False

    # ========================================================================
    # Complaint Storage
    # ========================================================================

    def store_complaint(self, complaint: Complaint):
        """Store a complaint"""
        self.complaints.append(complaint)
        self._persist_to_file("complaints")

    def get_complaints(self,
                      status: Optional[ComplaintStatus] = None,
                      priority: Optional[str] = None,
                      start_time: Optional[datetime] = None) -> List[Complaint]:
        """Get complaints with optional filters"""
        result = self.complaints

        if status:
            result = [c for c in result if c.status == status]

        if priority:
            result = [c for c in result if c.priority.value == priority]

        if start_time:
            result = [c for c in result if c.created_at >= start_time]

        return result

    def get_complaint(self, complaint_id: str) -> Optional[Complaint]:
        """Get a specific complaint"""
        for complaint in self.complaints:
            if complaint.complaint_id == complaint_id:
                return complaint
        return None

    def update_complaint(self, complaint_id: str, updates: Dict):
        """Update a complaint"""
        for complaint in self.complaints:
            if complaint.complaint_id == complaint_id:
                for key, value in updates.items():
                    if hasattr(complaint, key):
                        setattr(complaint, key, value)
                self._persist_to_file("complaints")
                return True
        return False

    # ========================================================================
    # Regulatory Report Storage
    # ========================================================================

    def store_regulatory_report(self, report: RegulatoryReport):
        """Store a regulatory report"""
        self.regulatory_reports.append(report)
        self._persist_to_file("regulatory_reports")

    def get_regulatory_reports(self,
                              report_type: Optional[str] = None,
                              status: Optional[str] = None) -> List[RegulatoryReport]:
        """Get regulatory reports with optional filters"""
        result = self.regulatory_reports

        if report_type:
            result = [r for r in result if r.report_type.value == report_type]

        if status:
            result = [r for r in result if r.status.value == status]

        return result

    def get_regulatory_report(self, report_id: str) -> Optional[RegulatoryReport]:
        """Get a specific regulatory report"""
        for report in self.regulatory_reports:
            if report.report_id == report_id:
                return report
        return None

    # ========================================================================
    # Performance Snapshot Storage
    # ========================================================================

    def store_performance_snapshot(self, snapshot: PerformanceSnapshot):
        """Store a performance snapshot"""
        self.performance_snapshots.append(snapshot)
        # Keep only last 1000 snapshots
        if len(self.performance_snapshots) > 1000:
            self.performance_snapshots = self.performance_snapshots[-1000:]
        self._persist_to_file("performance")

    def get_performance_snapshots(self,
                                  start_time: Optional[datetime] = None,
                                  end_time: Optional[datetime] = None) -> List[PerformanceSnapshot]:
        """Get performance snapshots in time range"""
        result = self.performance_snapshots

        if start_time:
            result = [p for p in result if p.timestamp >= start_time]

        if end_time:
            result = [p for p in result if p.timestamp <= end_time]

        return result

    def _persist_to_file(self, data_type: str):
        """Persist data to JSON file"""
        try:
            file_path = self.storage_path / f"{data_type}.json"

            if data_type == "interactions":
                data = [self._serialize_interaction(i) for i in self.interactions[-100:]]
            elif data_type == "alerts":
                data = [self._serialize_alert(a) for a in self.alerts[-100:]]
            elif data_type == "feedback":
                data = [self._serialize_feedback(f) for f in self.feedback[-100:]]
            elif data_type == "signals":
                data = [self._serialize_signal(s) for s in self.signals[-100:]]
            elif data_type == "complaints":
                data = [self._serialize_complaint(c) for c in self.complaints[-100:]]
            elif data_type == "regulatory_reports":
                data = [self._serialize_report(r) for r in self.regulatory_reports[-50:]]
            elif data_type == "performance":
                data = [self._serialize_performance(p) for p in self.performance_snapshots[-500:]]
            elif data_type.startswith("metrics_"):
                metric_name = data_type.replace("metrics_", "")
                data = [self._serialize_metric(m) for m in self.metrics[metric_name][-100:]]
            else:
                return

            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Warning: Failed to persist {data_type}: {e}")

    @staticmethod
    def _serialize_interaction(interaction: AIInteraction) -> dict:
        return {
            "interaction_id": interaction.interaction_id,
            "timestamp": interaction.timestamp.isoformat(),
            "user_id": interaction.user_id,
            "prompt": interaction.prompt[:100],  # Truncate for storage
            "response": interaction.response[:200],
            "response_time": interaction.response_time,
            "model_version": interaction.model_version
        }

    @staticmethod
    def _serialize_alert(alert: MonitoringAlert) -> dict:
        return {
            "alert_id": alert.alert_id,
            "timestamp": alert.timestamp.isoformat(),
            "alert_type": alert.alert_type,
            "severity": alert.severity.value,
            "metric_name": alert.metric_name,
            "current_value": alert.current_value,
            "threshold": alert.threshold
        }

    @staticmethod
    def _serialize_feedback(feedback: UserFeedback) -> dict:
        return {
            "feedback_id": feedback.feedback_id,
            "interaction_id": feedback.interaction_id,
            "timestamp": feedback.timestamp.isoformat(),
            "rating": feedback.rating,
            "sentiment": feedback.sentiment,
            "categories": feedback.categories
        }

    @staticmethod
    def _serialize_metric(metric: MetricRecord) -> dict:
        return {
            "metric_name": metric.metric_name,
            "value": metric.value,
            "timestamp": metric.timestamp.isoformat(),
            "tags": metric.tags
        }

    @staticmethod
    def _serialize_signal(signal: Signal) -> dict:
        return {
            "signal_id": signal.signal_id,
            "timestamp": signal.timestamp.isoformat(),
            "signal_type": signal.signal_type.value,
            "severity": signal.severity.value,
            "metric_name": signal.metric_name,
            "detected_value": signal.detected_value,
            "expected_value": signal.expected_value,
            "deviation": signal.deviation,
            "confidence": signal.confidence,
            "description": signal.description,
            "status": signal.status.value
        }

    @staticmethod
    def _serialize_complaint(complaint: Complaint) -> dict:
        return {
            "complaint_id": complaint.complaint_id,
            "created_at": complaint.created_at.isoformat(),
            "user_id": complaint.user_id,
            "category": complaint.category,
            "subject": complaint.subject,
            "priority": complaint.priority.value,
            "status": complaint.status.value,
            "assigned_to": complaint.assigned_to,
            "tags": complaint.tags
        }

    @staticmethod
    def _serialize_report(report: RegulatoryReport) -> dict:
        return {
            "report_id": report.report_id,
            "created_at": report.created_at.isoformat(),
            "report_type": report.report_type.value,
            "period_start": report.period_start.isoformat(),
            "period_end": report.period_end.isoformat(),
            "status": report.status.value,
            "title": report.title,
            "summary": report.summary
        }

    @staticmethod
    def _serialize_performance(snapshot: PerformanceSnapshot) -> dict:
        return {
            "timestamp": snapshot.timestamp.isoformat(),
            "response_time_avg": snapshot.response_time_avg,
            "response_time_p95": snapshot.response_time_p95,
            "throughput": snapshot.throughput,
            "error_rate": snapshot.error_rate,
            "availability": snapshot.availability,
            "active_users": snapshot.active_users
        }


# Global storage instance
storage = InMemoryStorage()
