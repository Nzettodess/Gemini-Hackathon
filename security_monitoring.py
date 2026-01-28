#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import time
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None


class ThreatLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class EventCategory(Enum):
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    DATA_ACCESS = "data_access"
    SYSTEM_INTEGRITY = "system_integrity"
    NETWORK_ACTIVITY = "network_activity"
    INJECTION_ATTEMPT = "injection_attempt"
    RATE_LIMIT_VIOLATION = "rate_limit_violation"
    ANOMALY = "anomaly"


@dataclass
class SecurityEvent:
    event_id: str
    timestamp: str
    category: str
    source_ip: str
    user_agent: str
    endpoint: str
    method: str
    status_code: int
    response_time_ms: float
    payload_size_bytes: int
    metadata: Dict[str, Any]


@dataclass
class ThreatDetection:
    detection_id: str
    timestamp: str
    threat_level: str
    category: str
    title: str
    description: str
    affected_events: List[str]
    indicators: Dict[str, Any]
    confidence_score: float
    recommended_actions: List[str]
    eu_ai_act_article: str


class AnomalyDetector:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.event_history: deque = deque(maxlen=window_size)
        self.baseline_stats: Dict[str, Any] = {}
        self.ip_request_counts: Dict[str, deque] = defaultdict(lambda: deque(maxlen=60))
        self.endpoint_stats: Dict[str, Dict[str, float]] = defaultdict(lambda: {"count": 0, "avg_time": 0.0, "max_time": 0.0})

    def add_event(self, event: SecurityEvent) -> None:
        self.event_history.append(event)
        self._update_baseline(event)

    def _update_baseline(self, event: SecurityEvent) -> None:
        endpoint_key = f"{event.method}:{event.endpoint}"
        stats = self.endpoint_stats[endpoint_key]
        
        stats["count"] += 1
        stats["avg_time"] = (stats["avg_time"] * (stats["count"] - 1) + event.response_time_ms) / stats["count"]
        stats["max_time"] = max(stats["max_time"], event.response_time_ms)

        now = time.time()
        self.ip_request_counts[event.source_ip].append(now)

    def detect_anomalies(self, event: SecurityEvent) -> List[Dict[str, Any]]:
        anomalies = []

        anomalies.extend(self._detect_rate_anomaly(event))
        anomalies.extend(self._detect_response_time_anomaly(event))
        anomalies.extend(self._detect_error_spike(event))
        anomalies.extend(self._detect_suspicious_payload(event))

        return anomalies

    def _detect_rate_anomaly(self, event: SecurityEvent) -> List[Dict[str, Any]]:
        now = time.time()
        recent_requests = [t for t in self.ip_request_counts[event.source_ip] if now - t < 60]
        
        if len(recent_requests) > 100:
            return [{
                "type": "rate_limit_violation",
                "severity": "high",
                "details": f"IP {event.source_ip} made {len(recent_requests)} requests in 60s (threshold: 100)",
                "indicator": "requests_per_minute",
                "value": len(recent_requests)
            }]
        return []

    def _detect_response_time_anomaly(self, event: SecurityEvent) -> List[Dict[str, Any]]:
        endpoint_key = f"{event.method}:{event.endpoint}"
        stats = self.endpoint_stats.get(endpoint_key)
        
        if stats and stats["count"] > 10:
            threshold = stats["avg_time"] * 3
            if event.response_time_ms > threshold and event.response_time_ms > 1000:
                return [{
                    "type": "performance_anomaly",
                    "severity": "medium",
                    "details": f"Response time {event.response_time_ms}ms exceeds 3x baseline ({stats['avg_time']:.1f}ms)",
                    "indicator": "response_time_deviation",
                    "value": event.response_time_ms / stats["avg_time"]
                }]
        return []

    def _detect_error_spike(self, event: SecurityEvent) -> List[Dict[str, Any]]:
        if event.status_code >= 500:
            recent_errors = sum(1 for e in list(self.event_history)[-20:] if e.status_code >= 500)
            if recent_errors > 5:
                return [{
                    "type": "error_spike",
                    "severity": "high",
                    "details": f"{recent_errors} server errors in last 20 requests",
                    "indicator": "error_rate",
                    "value": recent_errors / 20
                }]
        return []

    def _detect_suspicious_payload(self, event: SecurityEvent) -> List[Dict[str, Any]]:
        suspicious_patterns = [
            ("sql_injection", ["' OR ", "UNION SELECT", "DROP TABLE", "; --"]),
            ("xss_attempt", ["<script>", "javascript:", "onerror=", "onload="]),
            ("path_traversal", ["../", "..\\", "%2e%2e"]),
            ("command_injection", ["; ls", "| cat", "&& whoami", "`id`"]),
        ]

        payload_str = json.dumps(event.metadata).lower()
        
        for attack_type, patterns in suspicious_patterns:
            for pattern in patterns:
                if pattern.lower() in payload_str:
                    return [{
                        "type": attack_type,
                        "severity": "critical",
                        "details": f"Potential {attack_type.replace('_', ' ')} detected: pattern '{pattern}'",
                        "indicator": "malicious_pattern",
                        "value": pattern
                    }]
        return []


class SecurityMonitor:
    def __init__(self, use_ai: bool = True, incident_manager=None):
        self.use_ai = use_ai and GENAI_AVAILABLE
        self.client = None
        self.incident_manager = incident_manager
        self.anomaly_detector = AnomalyDetector()
        self.threat_detections: List[ThreatDetection] = []
        self.event_buffer: List[SecurityEvent] = []
        
        if self.use_ai:
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                try:
                    self.client = genai.Client(api_key=api_key)
                except Exception:
                    self.use_ai = False

    def ingest_event(self, event: SecurityEvent) -> Optional[ThreatDetection]:
        self.event_buffer.append(event)
        self.anomaly_detector.add_event(event)
        
        anomalies = self.anomaly_detector.detect_anomalies(event)
        
        if anomalies:
            threat = self._create_threat_detection(event, anomalies)
            self.threat_detections.append(threat)
            
            if self.incident_manager and threat.threat_level in ["critical", "high"]:
                self._create_security_incident(threat)
            
            return threat
        
        return None

    def _create_threat_detection(self, event: SecurityEvent, anomalies: List[Dict[str, Any]]) -> ThreatDetection:
        severity_map = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}
        max_severity = max((a.get("severity", "low") for a in anomalies), key=lambda s: severity_map.get(s, 0))
        
        categories = list(set(a.get("type", "anomaly") for a in anomalies))
        primary_category = categories[0] if categories else "anomaly"
        
        detection_id = f"THR-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{len(self.threat_detections)}"
        
        title = f"Security threat detected: {primary_category.replace('_', ' ').title()}"
        description = "; ".join(a.get("details", "") for a in anomalies)
        
        indicators = {a.get("indicator", "unknown"): a.get("value") for a in anomalies}
        
        recommended_actions = self._generate_recommendations(anomalies)
        
        eu_article = self._map_to_eu_ai_act_article(primary_category, max_severity)
        
        confidence = self._calculate_confidence(anomalies)
        
        if self.use_ai and self.client:
            ai_analysis = self._ai_threat_analysis(event, anomalies)
            if ai_analysis:
                description = f"{description}\n\nAI Analysis: {ai_analysis}"
        
        return ThreatDetection(
            detection_id=detection_id,
            timestamp=datetime.now().isoformat(),
            threat_level=max_severity,
            category=primary_category,
            title=title,
            description=description,
            affected_events=[event.event_id],
            indicators=indicators,
            confidence_score=confidence,
            recommended_actions=recommended_actions,
            eu_ai_act_article=eu_article
        )

    def _generate_recommendations(self, anomalies: List[Dict[str, Any]]) -> List[str]:
        recommendations = []
        
        for anomaly in anomalies:
            atype = anomaly.get("type", "")
            
            if atype == "rate_limit_violation":
                recommendations.append("Implement stricter rate limiting for this IP")
                recommendations.append("Consider temporary IP blocking")
            elif atype in ["sql_injection", "xss_attempt", "command_injection"]:
                recommendations.append("Block request immediately")
                recommendations.append("Review and strengthen input validation")
                recommendations.append("Audit recent requests from this source")
            elif atype == "error_spike":
                recommendations.append("Investigate backend service health")
                recommendations.append("Check for potential DoS attack")
            elif atype == "performance_anomaly":
                recommendations.append("Monitor system resources")
                recommendations.append("Check for resource exhaustion attacks")
        
        return list(set(recommendations)) or ["Monitor situation and collect additional data"]

    def _map_to_eu_ai_act_article(self, category: str, severity: str) -> str:
        if category in ["sql_injection", "xss_attempt", "command_injection", "path_traversal"]:
            return "Article 15(4) - Resilience against attacks"
        elif category == "rate_limit_violation":
            return "Article 15(4) - System integrity protection"
        elif severity in ["critical", "high"]:
            return "Article 73 - Serious incident reporting"
        else:
            return "Article 15(1) - System security"

    def _calculate_confidence(self, anomalies: List[Dict[str, Any]]) -> float:
        if not anomalies:
            return 0.0
        
        severity_weights = {"critical": 1.0, "high": 0.8, "medium": 0.6, "low": 0.4, "info": 0.2}
        
        total_weight = sum(severity_weights.get(a.get("severity", "low"), 0.5) for a in anomalies)
        return min(total_weight / len(anomalies), 1.0)

    def _ai_threat_analysis(self, event: SecurityEvent, anomalies: List[Dict[str, Any]]) -> Optional[str]:
        if not self.client:
            return None
        
        try:
            prompt = f"""You are a cybersecurity analyst. Analyze this security event and anomalies.

EVENT:
- Endpoint: {event.endpoint}
- Method: {event.method}
- Source IP: {event.source_ip}
- Status: {event.status_code}
- Response Time: {event.response_time_ms}ms

ANOMALIES DETECTED:
{json.dumps(anomalies, indent=2)}

Provide a brief (2-3 sentences) threat assessment including:
1. Likely attack type or security concern
2. Potential impact on AI system integrity
3. Urgency level

Keep response concise and actionable."""

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return (response.text or "").strip()[:500]
        except Exception:
            return None

    def _create_security_incident(self, threat: ThreatDetection) -> None:
        if not self.incident_manager:
            return
        
        try:
            incident = self.incident_manager.create_incident(
                title=threat.title,
                description=f"{threat.description}\n\nThreat Level: {threat.threat_level}\n"
                           f"Confidence: {threat.confidence_score:.2%}\n"
                           f"Indicators: {json.dumps(threat.indicators, indent=2)}\n"
                           f"Recommended Actions:\n" + "\n".join(f"- {a}" for a in threat.recommended_actions),
                ai_system_id="SECURITY-MONITOR-001",
                ai_system_name="Security Monitoring System",
                member_state="EU",
                detected_by="automated_security_monitor",
                metadata={
                    "threat_detection_id": threat.detection_id,
                    "threat_level": threat.threat_level,
                    "category": threat.category,
                    "confidence_score": threat.confidence_score,
                    "eu_ai_act_article": threat.eu_ai_act_article,
                    "affected_events": threat.affected_events
                }
            )
            
            if self.incident_manager.use_ai:
                self.incident_manager.classify_severity(incident)
        except Exception as e:
            print(f"Failed to create incident: {e}")

    def get_threat_summary(self, hours: int = 24) -> Dict[str, Any]:
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_threats = [
            t for t in self.threat_detections
            if datetime.fromisoformat(t.timestamp) > cutoff
        ]
        
        by_level = defaultdict(int)
        by_category = defaultdict(int)
        
        for threat in recent_threats:
            by_level[threat.threat_level] += 1
            by_category[threat.category] += 1
        
        return {
            "period_hours": hours,
            "total_threats": len(recent_threats),
            "by_threat_level": dict(by_level),
            "by_category": dict(by_category),
            "critical_threats": [asdict(t) for t in recent_threats if t.threat_level == "critical"],
            "high_threats": [asdict(t) for t in recent_threats if t.threat_level == "high"]
        }


def create_sample_event(
    event_id: str,
    category: str = "data_access",
    source_ip: str = "192.168.1.100",
    endpoint: str = "/api/data",
    method: str = "GET",
    status_code: int = 200,
    response_time_ms: float = 150.0,
    metadata: Optional[Dict] = None
) -> SecurityEvent:
    return SecurityEvent(
        event_id=event_id,
        timestamp=datetime.now().isoformat(),
        category=category,
        source_ip=source_ip,
        user_agent="Mozilla/5.0",
        endpoint=endpoint,
        method=method,
        status_code=status_code,
        response_time_ms=response_time_ms,
        payload_size_bytes=1024,
        metadata=metadata or {}
    )
