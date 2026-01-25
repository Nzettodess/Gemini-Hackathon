"""
Dashboard Core - AI-powered signal detection and monitoring
EU AI Act Post-Market Surveillance Dashboard
"""
import random
import statistics
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

from ..data.models import (
    Signal, SignalType, SignalStatus, AlertSeverity,
    Complaint, ComplaintStatus, ComplaintPriority,
    RegulatoryReport, ReportType, ReportStatus,
    PerformanceSnapshot
)
from ..data.storage import storage


class SignalDetector:
    """
    AI-powered signal detection engine

    Detects anomalies, trends, and patterns in monitoring data
    """

    def __init__(self):
        self.signal_counter = 0
        # Configuration for detection
        self.anomaly_threshold = 2.0  # Standard deviations
        self.trend_window = 10  # Data points for trend analysis
        self.min_confidence = 0.7

    def detect_signals(self, metric_name: str, values: List[float]) -> List[Signal]:
        """
        Run all signal detection algorithms on metric data

        Args:
            metric_name: Name of the metric
            values: Recent metric values

        Returns:
            List of detected signals
        """
        signals = []

        if len(values) < 3:
            return signals

        # 1. Anomaly detection (Z-score based)
        anomaly_signal = self._detect_anomaly(metric_name, values)
        if anomaly_signal:
            signals.append(anomaly_signal)

        # 2. Trend change detection
        if len(values) >= self.trend_window:
            trend_signal = self._detect_trend_change(metric_name, values)
            if trend_signal:
                signals.append(trend_signal)

        # 3. Pattern detection (simple patterns)
        pattern_signal = self._detect_patterns(metric_name, values)
        if pattern_signal:
            signals.append(pattern_signal)

        return signals

    def _detect_anomaly(self, metric_name: str, values: List[float]) -> Optional[Signal]:
        """Detect anomalies using Z-score method"""
        if len(values) < 5:
            return None

        current_value = values[-1]
        historical = values[:-1]

        mean = statistics.mean(historical)
        std = statistics.stdev(historical) if len(historical) > 1 else 0.1

        if std == 0:
            return None

        z_score = abs(current_value - mean) / std

        if z_score > self.anomaly_threshold:
            self.signal_counter += 1
            deviation = (current_value - mean) / mean * 100 if mean != 0 else 0

            severity = AlertSeverity.CRITICAL if z_score > 3 else AlertSeverity.HIGH
            confidence = min(0.99, 0.7 + (z_score - self.anomaly_threshold) * 0.1)

            return Signal(
                signal_id=f"SIG-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{self.signal_counter:04d}",
                timestamp=datetime.now(timezone.utc),
                signal_type=SignalType.ANOMALY,
                severity=severity,
                metric_name=metric_name,
                detected_value=current_value,
                expected_value=mean,
                deviation=deviation,
                confidence=confidence,
                description=f"Anomaly detected: {metric_name} = {current_value:.4f} "
                           f"(expected ~{mean:.4f}, z-score: {z_score:.2f})"
            )

        return None

    def _detect_trend_change(self, metric_name: str, values: List[float]) -> Optional[Signal]:
        """Detect significant trend changes"""
        if len(values) < self.trend_window:
            return None

        recent = values[-self.trend_window // 2:]
        earlier = values[-self.trend_window:-self.trend_window // 2]

        recent_avg = statistics.mean(recent)
        earlier_avg = statistics.mean(earlier)

        if earlier_avg == 0:
            return None

        change_pct = (recent_avg - earlier_avg) / earlier_avg * 100

        # Significant change threshold: 15%
        if abs(change_pct) > 15:
            self.signal_counter += 1
            direction = "increasing" if change_pct > 0 else "decreasing"

            severity = AlertSeverity.HIGH if abs(change_pct) > 25 else AlertSeverity.MEDIUM

            return Signal(
                signal_id=f"SIG-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{self.signal_counter:04d}",
                timestamp=datetime.now(timezone.utc),
                signal_type=SignalType.TREND_CHANGE,
                severity=severity,
                metric_name=metric_name,
                detected_value=recent_avg,
                expected_value=earlier_avg,
                deviation=change_pct,
                confidence=min(0.95, 0.6 + abs(change_pct) / 100),
                description=f"Trend change detected: {metric_name} is {direction} "
                           f"({change_pct:+.1f}% change)"
            )

        return None

    def _detect_patterns(self, metric_name: str, values: List[float]) -> Optional[Signal]:
        """Detect specific patterns (consecutive drops, oscillations, etc.)"""
        if len(values) < 5:
            return None

        # Check for consecutive drops
        recent = values[-5:]
        drops = sum(1 for i in range(1, len(recent)) if recent[i] < recent[i-1])

        if drops >= 4:  # 4 or more consecutive drops
            self.signal_counter += 1
            return Signal(
                signal_id=f"SIG-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{self.signal_counter:04d}",
                timestamp=datetime.now(timezone.utc),
                signal_type=SignalType.PATTERN_DETECTED,
                severity=AlertSeverity.MEDIUM,
                metric_name=metric_name,
                detected_value=recent[-1],
                expected_value=recent[0],
                deviation=(recent[-1] - recent[0]) / recent[0] * 100 if recent[0] != 0 else 0,
                confidence=0.8,
                description=f"Pattern detected: {metric_name} showing consecutive decline "
                           f"({drops} drops in last 5 readings)"
            )

        return None


class TrendAnalyzer:
    """
    Trend analysis and forecasting
    """

    def analyze_trends(self, metric_name: str,
                      values: List[float],
                      timestamps: List[datetime]) -> Dict:
        """
        Analyze metric trends

        Returns trend analysis including direction, strength, and forecast
        """
        if len(values) < 2:
            return {
                "metric_name": metric_name,
                "trend": "insufficient_data",
                "data_points": len(values)
            }

        # Calculate basic statistics
        current = values[-1]
        mean = statistics.mean(values)
        std = statistics.stdev(values) if len(values) > 1 else 0

        # Determine trend direction
        if len(values) >= 5:
            first_half = statistics.mean(values[:len(values)//2])
            second_half = statistics.mean(values[len(values)//2:])

            if second_half > first_half * 1.05:
                direction = "increasing"
                strength = min(1.0, (second_half - first_half) / first_half)
            elif second_half < first_half * 0.95:
                direction = "decreasing"
                strength = min(1.0, (first_half - second_half) / first_half)
            else:
                direction = "stable"
                strength = 0.0
        else:
            direction = "stable"
            strength = 0.0

        # Simple forecast (linear extrapolation)
        if len(values) >= 3:
            # Calculate average change
            changes = [values[i] - values[i-1] for i in range(1, len(values))]
            avg_change = statistics.mean(changes)

            forecast = {
                "next_value": current + avg_change,
                "next_3": current + avg_change * 3,
                "confidence": 0.7 if abs(avg_change) < std else 0.5
            }
        else:
            forecast = None

        return {
            "metric_name": metric_name,
            "current_value": current,
            "mean": mean,
            "std": std,
            "min": min(values),
            "max": max(values),
            "trend_direction": direction,
            "trend_strength": strength,
            "data_points": len(values),
            "forecast": forecast,
            "analysis_time": datetime.now(timezone.utc).isoformat()
        }

    def get_all_trends(self, hours: int = 24) -> Dict[str, Dict]:
        """Get trend analysis for all metrics"""
        start_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        trends = {}

        for metric_name in storage.metrics.keys():
            records = storage.get_metrics(metric_name, start_time=start_time)
            if records:
                values = [r.value for r in records]
                timestamps = [r.timestamp for r in records]
                trends[metric_name] = self.analyze_trends(metric_name, values, timestamps)

        return trends


class ComplaintManager:
    """
    Complaint tracking and management
    """

    def __init__(self):
        self.complaint_counter = 0

    def create_complaint(self,
                        user_id: Optional[str],
                        category: str,
                        subject: str,
                        description: str,
                        priority: str = "medium",
                        related_interaction_id: Optional[str] = None,
                        tags: List[str] = None) -> Complaint:
        """Create a new complaint"""
        self.complaint_counter += 1

        complaint = Complaint(
            complaint_id=f"CMP-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{self.complaint_counter:04d}",
            created_at=datetime.now(timezone.utc),
            user_id=user_id,
            category=category,
            subject=subject,
            description=description,
            priority=ComplaintPriority(priority),
            status=ComplaintStatus.OPEN,
            related_interaction_id=related_interaction_id,
            tags=tags or []
        )

        storage.store_complaint(complaint)
        return complaint

    def update_complaint(self, complaint_id: str, updates: Dict) -> bool:
        """Update a complaint"""
        complaint = storage.get_complaint(complaint_id)
        if not complaint:
            return False

        # Add update to history
        update_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "changes": updates
        }
        complaint.updates.append(update_record)

        # Apply updates
        for key, value in updates.items():
            if key == "status":
                complaint.status = ComplaintStatus(value)
            elif key == "priority":
                complaint.priority = ComplaintPriority(value)
            elif key == "resolution" and value:
                complaint.resolution = value
                complaint.resolved_at = datetime.now(timezone.utc)
            elif hasattr(complaint, key):
                setattr(complaint, key, value)

        storage._persist_to_file("complaints")
        return True

    def get_analytics(self, days: int = 30) -> Dict:
        """Get complaint analytics"""
        start_time = datetime.now(timezone.utc) - timedelta(days=days)
        complaints = storage.get_complaints(start_time=start_time)

        if not complaints:
            return {
                "total": 0,
                "period_days": days
            }

        # Status distribution
        status_dist = defaultdict(int)
        priority_dist = defaultdict(int)
        category_dist = defaultdict(int)

        resolution_times = []

        for c in complaints:
            status_dist[c.status.value] += 1
            priority_dist[c.priority.value] += 1
            category_dist[c.category] += 1

            if c.resolved_at:
                resolution_time = (c.resolved_at - c.created_at).total_seconds() / 3600
                resolution_times.append(resolution_time)

        return {
            "total": len(complaints),
            "period_days": days,
            "by_status": dict(status_dist),
            "by_priority": dict(priority_dist),
            "by_category": dict(category_dist),
            "resolution_stats": {
                "resolved_count": len(resolution_times),
                "avg_resolution_hours": statistics.mean(resolution_times) if resolution_times else None,
                "min_resolution_hours": min(resolution_times) if resolution_times else None,
                "max_resolution_hours": max(resolution_times) if resolution_times else None
            },
            "open_count": status_dist.get("open", 0) + status_dist.get("in_progress", 0)
        }


class PerformanceMonitor:
    """
    Real-time performance monitoring
    """

    def __init__(self):
        self.sla_targets = {
            "response_time_avg": 200,  # ms
            "response_time_p95": 500,  # ms
            "availability": 99.9,  # %
            "error_rate": 1.0,  # %
            "throughput": 100  # requests/sec
        }

    def capture_snapshot(self) -> PerformanceSnapshot:
        """Capture current performance snapshot"""
        # In production, this would collect real metrics
        # For demo, we simulate realistic values
        snapshot = PerformanceSnapshot(
            timestamp=datetime.now(timezone.utc),
            response_time_avg=random.uniform(150, 250),
            response_time_p95=random.uniform(400, 600),
            throughput=random.uniform(80, 120),
            error_rate=random.uniform(0.1, 1.5),
            availability=random.uniform(99.5, 99.99),
            active_users=random.randint(50, 200),
            metrics={
                "cpu_usage": random.uniform(30, 70),
                "memory_usage": random.uniform(40, 80),
                "request_queue": random.randint(0, 50)
            }
        )

        storage.store_performance_snapshot(snapshot)
        return snapshot

    def get_realtime_metrics(self) -> Dict:
        """Get real-time performance metrics"""
        snapshot = self.capture_snapshot()

        return {
            "timestamp": snapshot.timestamp.isoformat(),
            "response_time": {
                "avg_ms": round(snapshot.response_time_avg, 2),
                "p95_ms": round(snapshot.response_time_p95, 2),
                "sla_status": "ok" if snapshot.response_time_avg < self.sla_targets["response_time_avg"] else "breach"
            },
            "throughput": {
                "requests_per_sec": round(snapshot.throughput, 2),
                "sla_status": "ok" if snapshot.throughput >= self.sla_targets["throughput"] else "breach"
            },
            "availability": {
                "percentage": round(snapshot.availability, 3),
                "sla_status": "ok" if snapshot.availability >= self.sla_targets["availability"] else "breach"
            },
            "error_rate": {
                "percentage": round(snapshot.error_rate, 3),
                "sla_status": "ok" if snapshot.error_rate <= self.sla_targets["error_rate"] else "breach"
            },
            "active_users": snapshot.active_users,
            "system": snapshot.metrics
        }

    def get_sla_status(self) -> Dict:
        """Get SLA compliance status"""
        # Get recent snapshots
        start_time = datetime.now(timezone.utc) - timedelta(hours=24)
        snapshots = storage.get_performance_snapshots(start_time=start_time)

        if not snapshots:
            return {"status": "no_data", "period": "24h"}

        # Calculate SLA metrics
        avg_response = statistics.mean([s.response_time_avg for s in snapshots])
        avg_availability = statistics.mean([s.availability for s in snapshots])
        avg_error_rate = statistics.mean([s.error_rate for s in snapshots])

        breaches = []
        if avg_response > self.sla_targets["response_time_avg"]:
            breaches.append("response_time")
        if avg_availability < self.sla_targets["availability"]:
            breaches.append("availability")
        if avg_error_rate > self.sla_targets["error_rate"]:
            breaches.append("error_rate")

        return {
            "status": "compliant" if not breaches else "breach",
            "period": "24h",
            "metrics": {
                "response_time_avg": {
                    "value": round(avg_response, 2),
                    "target": self.sla_targets["response_time_avg"],
                    "compliant": avg_response <= self.sla_targets["response_time_avg"]
                },
                "availability": {
                    "value": round(avg_availability, 3),
                    "target": self.sla_targets["availability"],
                    "compliant": avg_availability >= self.sla_targets["availability"]
                },
                "error_rate": {
                    "value": round(avg_error_rate, 3),
                    "target": self.sla_targets["error_rate"],
                    "compliant": avg_error_rate <= self.sla_targets["error_rate"]
                }
            },
            "breaches": breaches,
            "samples": len(snapshots)
        }


class RegulatoryReporter:
    """
    EU AI Act regulatory reporting
    """

    def __init__(self):
        self.report_counter = 0

        # EU AI Act Article 72 requirements
        self.compliance_requirements = {
            "article_72_1": "Post-market monitoring system established",
            "article_72_2": "Data collection and analysis procedures defined",
            "article_72_3": "Serious incident reporting mechanism in place",
            "article_72_4": "Corrective action procedures established",
            "article_72_5": "Documentation maintained and updated"
        }

    def generate_report(self,
                       report_type: str = "periodic",
                       period_days: int = 30) -> RegulatoryReport:
        """Generate a regulatory report"""
        self.report_counter += 1

        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=period_days)

        # Gather metrics
        metrics_summary = self._gather_metrics_summary(start_time, end_time)
        incidents_summary = self._gather_incidents_summary(start_time, end_time)
        compliance_status = self._check_compliance()

        report = RegulatoryReport(
            report_id=f"REG-{end_time.strftime('%Y%m%d')}-{self.report_counter:04d}",
            created_at=datetime.now(timezone.utc),
            report_type=ReportType(report_type),
            period_start=start_time,
            period_end=end_time,
            status=ReportStatus.DRAFT,
            title=f"EU AI Act Article 72 Compliance Report - {end_time.strftime('%B %Y')}",
            summary=self._generate_summary(metrics_summary, incidents_summary),
            metrics_summary=metrics_summary,
            incidents_summary=incidents_summary,
            compliance_status=compliance_status,
            recommendations=self._generate_recommendations(metrics_summary, incidents_summary)
        )

        storage.store_regulatory_report(report)
        return report

    def _gather_metrics_summary(self, start: datetime, end: datetime) -> Dict:
        """Gather metrics summary for report"""
        summary = {}

        for metric_name in storage.metrics.keys():
            records = storage.get_metrics(metric_name, start_time=start, end_time=end)
            if records:
                values = [r.value for r in records]
                summary[metric_name] = {
                    "count": len(values),
                    "avg": round(statistics.mean(values), 4),
                    "min": round(min(values), 4),
                    "max": round(max(values), 4),
                    "std": round(statistics.stdev(values), 4) if len(values) > 1 else 0
                }

        return summary

    def _gather_incidents_summary(self, start: datetime, end: datetime) -> Dict:
        """Gather incidents summary for report"""
        alerts = [a for a in storage.alerts if start <= a.timestamp <= end]

        severity_dist = defaultdict(int)
        type_dist = defaultdict(int)

        for alert in alerts:
            severity_dist[alert.severity.value] += 1
            type_dist[alert.alert_type] += 1

        return {
            "total_alerts": len(alerts),
            "by_severity": dict(severity_dist),
            "by_type": dict(type_dist),
            "critical_count": severity_dist.get("critical", 0),
            "high_count": severity_dist.get("high", 0)
        }

    def _check_compliance(self) -> Dict:
        """Check EU AI Act compliance status"""
        compliance = {}

        for article, requirement in self.compliance_requirements.items():
            # In production, this would check actual compliance
            # For demo, we simulate compliance status
            compliance[article] = {
                "requirement": requirement,
                "status": "compliant",
                "last_verified": datetime.now(timezone.utc).isoformat()
            }

        return {
            "overall_status": "compliant",
            "articles": compliance,
            "next_audit_due": (datetime.now(timezone.utc) + timedelta(days=90)).isoformat()
        }

    def _generate_summary(self, metrics: Dict, incidents: Dict) -> str:
        """Generate executive summary"""
        lines = [
            "This report summarizes post-market monitoring activities ",
            "in accordance with EU AI Act Article 72 requirements.",
            "",
            f"Metrics tracked: {len(metrics)}",
            f"Total alerts: {incidents.get('total_alerts', 0)}",
            f"Critical incidents: {incidents.get('critical_count', 0)}",
            "",
            "The AI system continues to operate within defined safety parameters."
        ]
        return "\n".join(lines)

    def _generate_recommendations(self, metrics: Dict, incidents: Dict) -> List[str]:
        """Generate recommendations based on findings"""
        recommendations = []

        if incidents.get("critical_count", 0) > 0:
            recommendations.append(
                "Review and address root causes of critical incidents"
            )

        if incidents.get("total_alerts", 0) > 10:
            recommendations.append(
                "Consider adjusting alert thresholds to reduce alert fatigue"
            )

        recommendations.append(
            "Continue regular monitoring and documentation updates"
        )

        return recommendations

    def get_compliance_status(self) -> Dict:
        """Get current EU AI Act compliance status"""
        return {
            "framework": "EU AI Act",
            "articles_covered": ["Article 72"],
            "status": self._check_compliance(),
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "system_classification": "High-Risk AI System",
            "monitoring_status": "Active"
        }


class DashboardCore:
    """
    Main Dashboard coordinator

    Integrates all monitoring components for EU AI Act compliance
    """

    def __init__(self):
        self.signal_detector = SignalDetector()
        self.trend_analyzer = TrendAnalyzer()
        self.complaint_manager = ComplaintManager()
        self.performance_monitor = PerformanceMonitor()
        self.regulatory_reporter = RegulatoryReporter()

        print("Dashboard Core initialized")

    def get_overview(self) -> Dict:
        """Get dashboard overview"""
        now = datetime.now(timezone.utc)
        last_24h = now - timedelta(hours=24)

        # Gather overview data
        active_signals = storage.get_active_signals()
        active_alerts = storage.get_active_alerts()
        open_complaints = storage.get_complaints(status=ComplaintStatus.OPEN)
        recent_feedback = storage.get_recent_feedback(days=1)

        # Get trends
        trends = self.trend_analyzer.get_all_trends(hours=24)

        # Calculate health score (0-100)
        health_score = self._calculate_health_score(active_signals, active_alerts)

        return {
            "timestamp": now.isoformat(),
            "health_score": health_score,
            "health_status": self._get_health_status(health_score),
            "active_signals": len(active_signals),
            "active_alerts": len(active_alerts),
            "open_complaints": len(open_complaints),
            "feedback_today": len(recent_feedback),
            "metrics_tracked": len(storage.metrics),
            "trends_summary": {
                name: {
                    "direction": data.get("trend_direction"),
                    "current": data.get("current_value")
                }
                for name, data in trends.items()
            },
            "compliance_status": "compliant",
            "last_report": storage.regulatory_reports[-1].report_id if storage.regulatory_reports else None
        }

    def get_kpis(self) -> Dict:
        """Get key performance indicators"""
        now = datetime.now(timezone.utc)
        last_24h = now - timedelta(hours=24)
        last_7d = now - timedelta(days=7)

        # Interaction KPIs
        interactions_24h = storage.get_interactions(start_time=last_24h)
        interactions_7d = storage.get_interactions(start_time=last_7d)

        # Feedback KPIs
        feedback_7d = storage.get_recent_feedback(days=7)
        avg_rating = statistics.mean([f.rating for f in feedback_7d]) if feedback_7d else 0

        # Metric KPIs
        metric_kpis = {}
        for metric_name in ['response_accuracy', 'hallucination_rate', 'user_satisfaction']:
            records = storage.get_metrics(metric_name, start_time=last_24h)
            if records:
                values = [r.value for r in records]
                metric_kpis[metric_name] = round(statistics.mean(values), 4)

        return {
            "timestamp": now.isoformat(),
            "interactions": {
                "last_24h": len(interactions_24h),
                "last_7d": len(interactions_7d),
                "avg_per_day": len(interactions_7d) / 7 if interactions_7d else 0
            },
            "feedback": {
                "count_7d": len(feedback_7d),
                "avg_rating": round(avg_rating, 2),
                "satisfaction_rate": round(sum(1 for f in feedback_7d if f.rating >= 4) / len(feedback_7d) * 100, 1) if feedback_7d else 0
            },
            "metrics": metric_kpis,
            "alerts": {
                "active": len(storage.get_active_alerts()),
                "last_24h": len([a for a in storage.alerts if a.timestamp >= last_24h])
            },
            "signals": {
                "active": len(storage.get_active_signals()),
                "detected_7d": len([s for s in storage.signals if s.timestamp >= last_7d])
            }
        }

    def run_signal_detection(self) -> List[Dict]:
        """Run signal detection on all metrics"""
        detected_signals = []

        for metric_name, records in storage.metrics.items():
            if len(records) >= 5:
                values = [r.value for r in records[-50:]]  # Last 50 values
                signals = self.signal_detector.detect_signals(metric_name, values)

                for signal in signals:
                    storage.store_signal(signal)
                    detected_signals.append({
                        "signal_id": signal.signal_id,
                        "type": signal.signal_type.value,
                        "severity": signal.severity.value,
                        "metric": signal.metric_name,
                        "description": signal.description
                    })

        return detected_signals

    def _calculate_health_score(self, signals: List, alerts: List) -> int:
        """Calculate system health score (0-100)"""
        score = 100

        # Deduct for signals
        for signal in signals:
            if signal.severity == AlertSeverity.CRITICAL:
                score -= 15
            elif signal.severity == AlertSeverity.HIGH:
                score -= 10
            elif signal.severity == AlertSeverity.MEDIUM:
                score -= 5

        # Deduct for alerts
        for alert in alerts:
            if alert.severity == AlertSeverity.CRITICAL:
                score -= 20
            elif alert.severity == AlertSeverity.HIGH:
                score -= 10

        return max(0, min(100, score))

    def _get_health_status(self, score: int) -> str:
        """Get health status from score"""
        if score >= 90:
            return "healthy"
        elif score >= 70:
            return "warning"
        elif score >= 50:
            return "degraded"
        else:
            return "critical"


# Global dashboard instance
dashboard = DashboardCore()
