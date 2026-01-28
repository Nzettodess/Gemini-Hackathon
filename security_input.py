from __future__ import annotations

import html
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple


class InputValidationError(ValueError):
    pass


@dataclass
class RateLimitConfig:
    requests: int = 60
    per_seconds: int = 60


class InMemoryRateLimiter:
    def __init__(self, config: Optional[RateLimitConfig] = None):
        self.config = config or RateLimitConfig()
        self._buckets: Dict[str, list[float]] = {}

    def allow(self, key: str, now: Optional[float] = None) -> bool:
        current = time.time() if now is None else now
        window_start = current - float(self.config.per_seconds)
        bucket = self._buckets.get(key, [])
        bucket = [t for t in bucket if t >= window_start]

        if len(bucket) >= self.config.requests:
            self._buckets[key] = bucket
            return False

        bucket.append(current)
        self._buckets[key] = bucket
        return True


_CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def sanitize_text(value: str, max_len: int = 10_000) -> str:
    if not isinstance(value, str):
        raise InputValidationError("Expected string")

    trimmed = value[:max_len]
    cleaned = _CONTROL_CHARS_RE.sub("", trimmed)
    return html.escape(cleaned, quote=True)


def validate_grafana_alert_payload(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if not isinstance(payload, dict):
        raise InputValidationError("Payload must be a JSON object")

    status = payload.get("status")
    if status not in {"firing", "resolved"}:
        raise InputValidationError("Invalid or missing 'status'")

    alerts = payload.get("alerts")
    if not isinstance(alerts, list):
        raise InputValidationError("Invalid or missing 'alerts' array")

    if len(alerts) > 200:
        raise InputValidationError("Too many alerts in one request")

    normalized_alerts = []
    for alert in alerts:
        if not isinstance(alert, dict):
            raise InputValidationError("Each alert must be an object")

        labels = alert.get("labels")
        annotations = alert.get("annotations")
        if labels is not None and not isinstance(labels, dict):
            raise InputValidationError("Alert 'labels' must be an object")
        if annotations is not None and not isinstance(annotations, dict):
            raise InputValidationError("Alert 'annotations' must be an object")

        safe_labels = {}
        for k, v in (labels or {}).items():
            if isinstance(v, (str, int, float, bool)):
                safe_labels[str(k)[:128]] = sanitize_text(str(v), max_len=2048)

        safe_annotations = {}
        for k, v in (annotations or {}).items():
            if isinstance(v, (str, int, float, bool)):
                safe_annotations[str(k)[:128]] = sanitize_text(str(v), max_len=4096)

        normalized = dict(alert)
        normalized["labels"] = safe_labels
        normalized["annotations"] = safe_annotations
        normalized_alerts.append(normalized)

    safe_payload = dict(payload)
    safe_payload["alerts"] = normalized_alerts

    metadata = {
        "status": status,
        "alerts_count": len(normalized_alerts),
    }
    return safe_payload, metadata
