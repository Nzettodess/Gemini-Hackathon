"""
PMM Agent FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime, timedelta, timezone
import asyncio

from .core.pmm_core import PMMCoreAgent
from .core.dashboard import dashboard
from .data.models import AIInteraction, UserFeedback, SignalStatus, ComplaintStatus

# Initialize FastAPI app
app = FastAPI(
    title="Post-Market Monitoring Agent",
    description="EU AI Act Article 72 Compliance Monitoring System",
    version="1.0.0"
)

# Global PMM agent instance
pmm_agent = PMMCoreAgent()


# ============================================================================
# Pydantic Models for API
# ============================================================================

class InteractionRequest(BaseModel):
    """Request model for logging interaction"""
    interaction_id: str
    user_id: Optional[str] = None
    prompt: str
    response: str
    response_time: float
    model_version: str = "default"
    metadata: Dict = Field(default_factory=dict)
    demographics: Optional[Dict] = None


class FeedbackRequest(BaseModel):
    """Request model for submitting feedback"""
    interaction_id: str
    user_id: Optional[str] = None
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    issues: List[str] = Field(default_factory=list)


class MetricsQuery(BaseModel):
    """Request model for querying metrics"""
    metric_names: Optional[List[str]] = None
    hours: int = 24


class ComplaintRequest(BaseModel):
    """Request model for creating a complaint"""
    user_id: Optional[str] = None
    category: str
    subject: str
    description: str
    priority: str = "medium"
    related_interaction_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class ComplaintUpdateRequest(BaseModel):
    """Request model for updating a complaint"""
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    resolution: Optional[str] = None


class SignalAcknowledgeRequest(BaseModel):
    """Request model for acknowledging a signal"""
    acknowledged_by: str


class ReportGenerateRequest(BaseModel):
    """Request model for generating a report"""
    report_type: str = "periodic"
    period_days: int = 30


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Post-Market Monitoring Agent",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "integrations": {
            "safety_provider": "connected",
            "ethics_bridge": "connected",
            "incident_trigger": "connected"
        }
    }


@app.post("/api/v1/interactions/log")
async def log_interaction(request: InteractionRequest):
    """
    Log an AI interaction for monitoring

    This endpoint records AI system interactions and automatically:
    - Extracts performance metrics
    - Checks safety thresholds
    - Monitors for bias (if demographics provided)
    - Triggers alerts and incidents if needed
    """
    try:
        # Create interaction object
        interaction = AIInteraction(
            interaction_id=request.interaction_id,
            timestamp=datetime.now(timezone.utc),
            user_id=request.user_id,
            prompt=request.prompt,
            response=request.response,
            response_time=request.response_time,
            model_version=request.model_version,
            metadata=request.metadata,
            demographics=request.demographics
        )

        # Process interaction
        result = await pmm_agent.process_interaction(interaction)

        return {
            "status": "logged",
            "interaction_id": request.interaction_id,
            "summary": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/feedback/submit")
async def submit_feedback(request: FeedbackRequest):
    """
    Submit user feedback

    Collects and analyzes user feedback including:
    - Sentiment analysis
    - Auto-categorization
    - Issue tracking
    """
    try:
        # Create feedback object
        feedback = UserFeedback(
            feedback_id=f"FB-{datetime.now(timezone.utc).timestamp()}",
            interaction_id=request.interaction_id,
            user_id=request.user_id,
            timestamp=datetime.now(timezone.utc),
            rating=request.rating,
            comment=request.comment,
            issues=request.issues
        )

        # Process feedback
        result = await pmm_agent.process_feedback(feedback)

        return {
            "status": "received",
            "feedback_id": feedback.feedback_id,
            "analysis": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/metrics/query")
async def query_metrics(request: MetricsQuery):
    """
    Query metrics

    Get summary of performance metrics over specified time period
    """
    try:
        summary = pmm_agent.get_metrics_summary(hours=request.hours)

        if request.metric_names:
            # Filter to requested metrics
            summary = {k: v for k, v in summary.items() if k in request.metric_names}

        return {
            "metrics": summary,
            "period_hours": request.hours,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/metrics/current")
async def get_current_metrics():
    """
    Get current metrics snapshot

    Returns latest metrics from buffer
    """
    try:
        current_metrics = {}
        for metric_name, values in pmm_agent.metrics_buffer.items():
            if values:
                current_metrics[metric_name] = {
                    'current_value': values[-1],
                    'recent_average': sum(values) / len(values),
                    'samples': len(values)
                }

        return {
            "metrics": current_metrics,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/alerts/active")
async def get_active_alerts():
    """Get active alerts"""
    try:
        from .data.storage import storage
        alerts = storage.get_active_alerts()

        return {
            "alerts": [
                {
                    "alert_id": a.alert_id,
                    "timestamp": a.timestamp.isoformat(),
                    "severity": a.severity.value,
                    "alert_type": a.alert_type,
                    "metric_name": a.metric_name,
                    "current_value": a.current_value,
                    "threshold": a.threshold
                }
                for a in alerts
            ],
            "count": len(alerts)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/incidents/active")
async def get_active_incidents():
    """Get active incidents"""
    try:
        incidents = pmm_agent.incident_trigger.get_active_incidents()

        return {
            "incidents": [
                {
                    "incident_id": inc['incident_id'],
                    "created_at": inc['created_at'].isoformat(),
                    "priority": inc['priority'],
                    "classification": inc['classification'],
                    "alert_type": inc['alert'].alert_type,
                    "severity": inc['alert'].severity.value
                }
                for inc in incidents
            ],
            "count": len(incidents)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/reports/summary")
async def get_summary_report(days: int = 7):
    """
    Generate summary report

    Creates comprehensive monitoring report for specified period
    """
    try:
        report = pmm_agent.generate_report(days=days)

        return {
            "report": report,
            "period_days": days,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/reports/bias")
async def get_bias_report():
    """Get bias monitoring report"""
    try:
        report = pmm_agent.ethics_bridge.get_bias_report()

        return {
            "report": report,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/stats")
async def get_statistics():
    """Get system statistics"""
    try:
        from .data.storage import storage

        stats = {
            "interactions": {
                "total": len(storage.interactions),
                "last_24h": len(storage.get_interactions(
                    start_time=datetime.now(timezone.utc) - timedelta(hours=24)
                ))
            },
            "alerts": {
                "total": len(storage.alerts),
                "active": len(storage.get_active_alerts())
            },
            "feedback": {
                "total": len(storage.feedback),
                "last_7d": len(storage.get_recent_feedback(days=7))
            },
            "incidents": pmm_agent.incident_trigger.get_incident_stats()
        }

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Dashboard API Endpoints
# ============================================================================

@app.get("/api/v1/dashboard/overview")
async def get_dashboard_overview():
    """
    Get dashboard overview

    Returns comprehensive monitoring dashboard data including:
    - System health score
    - Active signals and alerts
    - Key metrics summary
    - Compliance status
    """
    try:
        overview = dashboard.get_overview()
        return overview

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/dashboard/kpis")
async def get_dashboard_kpis():
    """
    Get key performance indicators

    Returns KPIs for monitoring dashboard
    """
    try:
        kpis = dashboard.get_kpis()
        return kpis

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Signal Detection API Endpoints
# ============================================================================

@app.get("/api/v1/signals/detect")
async def detect_signals():
    """
    Run AI-powered signal detection

    Analyzes metrics to detect:
    - Anomalies
    - Trend changes
    - Patterns
    """
    try:
        detected = dashboard.run_signal_detection()
        return {
            "status": "completed",
            "signals_detected": len(detected),
            "signals": detected,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/signals/history")
async def get_signals_history(
    status: Optional[str] = None,
    hours: int = 24
):
    """
    Get signal history

    Returns detected signals with optional filtering
    """
    try:
        from .data.storage import storage

        start_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        signal_status = SignalStatus(status) if status else None

        signals = storage.get_signals(status=signal_status, start_time=start_time)

        return {
            "signals": [
                {
                    "signal_id": s.signal_id,
                    "timestamp": s.timestamp.isoformat(),
                    "type": s.signal_type.value,
                    "severity": s.severity.value,
                    "metric_name": s.metric_name,
                    "detected_value": s.detected_value,
                    "expected_value": s.expected_value,
                    "deviation": s.deviation,
                    "confidence": s.confidence,
                    "description": s.description,
                    "status": s.status.value
                }
                for s in signals
            ],
            "count": len(signals),
            "period_hours": hours
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/signals/{signal_id}/acknowledge")
async def acknowledge_signal(signal_id: str, request: SignalAcknowledgeRequest):
    """
    Acknowledge a detected signal
    """
    try:
        from .data.storage import storage

        success = storage.update_signal(signal_id, {
            "status": SignalStatus.ACKNOWLEDGED,
            "acknowledged_by": request.acknowledged_by,
            "acknowledged_at": datetime.now(timezone.utc)
        })

        if not success:
            raise HTTPException(status_code=404, detail="Signal not found")

        return {
            "status": "acknowledged",
            "signal_id": signal_id,
            "acknowledged_by": request.acknowledged_by,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Trend Analysis API Endpoints
# ============================================================================

@app.get("/api/v1/trends/metrics")
async def get_metric_trends(hours: int = 24):
    """
    Get metric trends

    Returns trend analysis for all tracked metrics
    """
    try:
        trends = dashboard.trend_analyzer.get_all_trends(hours=hours)
        return {
            "trends": trends,
            "period_hours": hours,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/trends/forecast")
async def get_forecast(metric_name: str, hours: int = 24):
    """
    Get metric forecast

    Returns trend analysis with forecast for specific metric
    """
    try:
        from .data.storage import storage

        start_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        records = storage.get_metrics(metric_name, start_time=start_time)

        if not records:
            raise HTTPException(status_code=404, detail=f"No data for metric: {metric_name}")

        values = [r.value for r in records]
        timestamps = [r.timestamp for r in records]

        analysis = dashboard.trend_analyzer.analyze_trends(metric_name, values, timestamps)

        return {
            "metric_name": metric_name,
            "analysis": analysis,
            "period_hours": hours,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Complaint Tracking API Endpoints
# ============================================================================

@app.get("/api/v1/complaints")
async def get_complaints(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    days: int = 30
):
    """
    Get complaints list

    Returns complaints with optional filtering
    """
    try:
        from .data.storage import storage

        start_time = datetime.now(timezone.utc) - timedelta(days=days)
        complaint_status = ComplaintStatus(status) if status else None

        complaints = storage.get_complaints(
            status=complaint_status,
            priority=priority,
            start_time=start_time
        )

        return {
            "complaints": [
                {
                    "complaint_id": c.complaint_id,
                    "created_at": c.created_at.isoformat(),
                    "user_id": c.user_id,
                    "category": c.category,
                    "subject": c.subject,
                    "priority": c.priority.value,
                    "status": c.status.value,
                    "assigned_to": c.assigned_to,
                    "tags": c.tags
                }
                for c in complaints
            ],
            "count": len(complaints),
            "period_days": days
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/complaints")
async def create_complaint(request: ComplaintRequest):
    """
    Create a new complaint
    """
    try:
        complaint = dashboard.complaint_manager.create_complaint(
            user_id=request.user_id,
            category=request.category,
            subject=request.subject,
            description=request.description,
            priority=request.priority,
            related_interaction_id=request.related_interaction_id,
            tags=request.tags
        )

        return {
            "status": "created",
            "complaint_id": complaint.complaint_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/complaints/{complaint_id}")
async def get_complaint(complaint_id: str):
    """
    Get complaint details
    """
    try:
        from .data.storage import storage

        complaint = storage.get_complaint(complaint_id)
        if not complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")

        return {
            "complaint_id": complaint.complaint_id,
            "created_at": complaint.created_at.isoformat(),
            "user_id": complaint.user_id,
            "category": complaint.category,
            "subject": complaint.subject,
            "description": complaint.description,
            "priority": complaint.priority.value,
            "status": complaint.status.value,
            "assigned_to": complaint.assigned_to,
            "related_interaction_id": complaint.related_interaction_id,
            "resolution": complaint.resolution,
            "resolved_at": complaint.resolved_at.isoformat() if complaint.resolved_at else None,
            "tags": complaint.tags,
            "updates": complaint.updates
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/v1/complaints/{complaint_id}")
async def update_complaint(complaint_id: str, request: ComplaintUpdateRequest):
    """
    Update a complaint
    """
    try:
        updates = {k: v for k, v in request.model_dump().items() if v is not None}

        success = dashboard.complaint_manager.update_complaint(complaint_id, updates)
        if not success:
            raise HTTPException(status_code=404, detail="Complaint not found")

        return {
            "status": "updated",
            "complaint_id": complaint_id,
            "updates": updates,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/complaints/analytics")
async def get_complaints_analytics(days: int = 30):
    """
    Get complaint analytics
    """
    try:
        analytics = dashboard.complaint_manager.get_analytics(days=days)
        return {
            "analytics": analytics,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Performance Monitoring API Endpoints
# ============================================================================

@app.get("/api/v1/performance/realtime")
async def get_realtime_performance():
    """
    Get real-time performance metrics

    Returns current system performance snapshot
    """
    try:
        metrics = dashboard.performance_monitor.get_realtime_metrics()
        return metrics

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/performance/history")
async def get_performance_history(hours: int = 24):
    """
    Get performance history

    Returns performance snapshots over time
    """
    try:
        from .data.storage import storage

        start_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        snapshots = storage.get_performance_snapshots(start_time=start_time)

        return {
            "snapshots": [
                {
                    "timestamp": s.timestamp.isoformat(),
                    "response_time_avg": s.response_time_avg,
                    "response_time_p95": s.response_time_p95,
                    "throughput": s.throughput,
                    "error_rate": s.error_rate,
                    "availability": s.availability,
                    "active_users": s.active_users
                }
                for s in snapshots
            ],
            "count": len(snapshots),
            "period_hours": hours
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/performance/sla")
async def get_sla_status():
    """
    Get SLA compliance status

    Returns SLA metrics and compliance status
    """
    try:
        status = dashboard.performance_monitor.get_sla_status()
        return status

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Regulatory Reporting API Endpoints
# ============================================================================

@app.get("/api/v1/regulatory/compliance-status")
async def get_compliance_status():
    """
    Get EU AI Act compliance status

    Returns current compliance status for Article 72
    """
    try:
        status = dashboard.regulatory_reporter.get_compliance_status()
        return status

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/regulatory/reports")
async def get_regulatory_reports(
    report_type: Optional[str] = None,
    status: Optional[str] = None
):
    """
    Get regulatory reports list
    """
    try:
        from .data.storage import storage

        reports = storage.get_regulatory_reports(
            report_type=report_type,
            status=status
        )

        return {
            "reports": [
                {
                    "report_id": r.report_id,
                    "created_at": r.created_at.isoformat(),
                    "report_type": r.report_type.value,
                    "period_start": r.period_start.isoformat(),
                    "period_end": r.period_end.isoformat(),
                    "status": r.status.value,
                    "title": r.title
                }
                for r in reports
            ],
            "count": len(reports)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/regulatory/reports/generate")
async def generate_regulatory_report(request: ReportGenerateRequest):
    """
    Generate a new regulatory report

    Creates EU AI Act Article 72 compliant report
    """
    try:
        report = dashboard.regulatory_reporter.generate_report(
            report_type=request.report_type,
            period_days=request.period_days
        )

        return {
            "status": "generated",
            "report_id": report.report_id,
            "title": report.title,
            "summary": report.summary,
            "metrics_summary": report.metrics_summary,
            "incidents_summary": report.incidents_summary,
            "compliance_status": report.compliance_status,
            "recommendations": report.recommendations,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/regulatory/reports/{report_id}")
async def get_regulatory_report(report_id: str):
    """
    Get regulatory report details
    """
    try:
        from .data.storage import storage

        report = storage.get_regulatory_report(report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        return {
            "report_id": report.report_id,
            "created_at": report.created_at.isoformat(),
            "report_type": report.report_type.value,
            "period_start": report.period_start.isoformat(),
            "period_end": report.period_end.isoformat(),
            "status": report.status.value,
            "title": report.title,
            "summary": report.summary,
            "metrics_summary": report.metrics_summary,
            "incidents_summary": report.incidents_summary,
            "compliance_status": report.compliance_status,
            "recommendations": report.recommendations,
            "submitted_at": report.submitted_at.isoformat() if report.submitted_at else None,
            "submitted_to": report.submitted_to
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    print("\n" + "="*70)
    print("POST-MARKET MONITORING AGENT STARTING")
    print("="*70)
    print("FastAPI application initialized")
    print("PMM Core Agent ready")
    print("Dashboard Core initialized")
    print("  - Signal Detection: enabled")
    print("  - Trend Analysis: enabled")
    print("  - Complaint Tracking: enabled")
    print("  - Performance Monitoring: enabled")
    print("  - Regulatory Reporting: enabled")
    print("API endpoints available at /docs")
    print("="*70 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    print("\n" + "="*70)
    print("POST-MARKET MONITORING AGENT SHUTTING DOWN")
    print("="*70 + "\n")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
