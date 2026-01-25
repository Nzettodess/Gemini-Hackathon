# Critical Alert Detector for EU AI Act Compliance

Grafana-based alerting system for AI-specific critical events configured for EU AI Act compliance, including safety incidents and performance degradation monitoring.

## Overview

This system provides real-time monitoring and alerting for critical AI safety events as defined by the EU AI Act (Regulation 2024/1689), specifically Article 73 on serious incident reporting.

### Capabilities

- ✅ **Real-time alerting** - Immediate notification of critical events
- ✅ **Threshold monitoring** - Configurable thresholds per risk category
- ✅ **Anomaly detection** - Pattern-based detection of unusual behavior
- ✅ **Custom rules** - EU AI Act Article 73 compliant alert rules
- ✅ **Dashboard integration** - Comprehensive Grafana dashboards
- ✅ **Incident management** - Automatic incident creation and tracking

## Risk ID Mappings

The system monitors four critical risk categories aligned with EU AI Act Article 3(49):

| Risk ID | Article Reference | Incident Type | Reporting Deadline | Severity |
|---------|------------------|---------------|-------------------|----------|
| **safety-001** | Article 3(49)(a), 73(4) | Death or serious harm to health | **10 days** | CRITICAL |
| **safety-002** | Article 3(49)(b), 73(3) | Critical infrastructure disruption | **2 days** | CRITICAL |
| **safety-003** | Article 3(49)(c), 73(2) | Fundamental rights violation | **15 days** | HIGH |
| **safety-005** | Article 3(49)(d), 73(2) | Property/environmental harm | **15 days** | HIGH |

## Architecture

```
┌─────────────────┐
│   AI Systems    │
│  (Your Apps)    │
└────────┬────────┘
         │ Metrics
         ▼
┌─────────────────┐      ┌──────────────┐
│  Prometheus     │◄─────┤ Metrics      │
│  (Metrics DB)   │      │ Exporter     │
└────────┬────────┘      └──────────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│    Grafana      │◄─────┤ Alert Rules  │
│  (Monitoring)   │      │ (EU AI Act)  │
└────────┬────────┘      └──────────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  Alertmanager   │─────►│  Webhook     │
│ (Notifications) │      │  Handler     │
└─────────────────┘      └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  Incident    │
                         │  Management  │
                         └──────────────┘
```

## Installation

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Grafana API key (optional, for programmatic access)

### Quick Start

1. **Install Python dependencies:**

```bash
pip install prometheus-client flask pyyaml rich requests
```

2. **Start the monitoring stack:**

```bash
cd grafana_config
docker-compose up -d
```

This starts:
- Grafana (port 3000)
- Prometheus (port 9090)
- Loki (port 3100)
- Alertmanager (port 9093)

3. **Start the metrics exporter:**

```bash
# Terminal 1: Start metrics exporter
python metrics_exporter.py
```

4. **Start the webhook handler:**

```bash
# Terminal 2: Start alert webhook handler
python alert_webhook_handler.py
```

5. **Access Grafana:**

Open http://localhost:3000
- Username: `admin`
- Password: `admin`

## Configuration

### Alert Thresholds

Alert thresholds are configured in `critical_alert_detector.py`:

```python
# safety-001: Death or serious harm
threshold_config={
    "health_impact_score": 9.0,
    "fatality_detected": True,
    "immediate_notification": True
}

# safety-002: Critical infrastructure
threshold_config={
    "infrastructure_impact_score": 8.5,
    "disruption_duration_minutes": 15,
    "affected_services": 1
}

# safety-003: Fundamental rights
threshold_config={
    "rights_violation_score": 7.0,
    "affected_individuals": 1,
    "bias_detection_threshold": 0.15
}

# safety-005: Property/environmental harm
threshold_config={
    "damage_value_eur": 50000,
    "environmental_impact_score": 7.5,
    "affected_area_km2": 0.1
}
```

### Notification Channels

Configure notification channels in `grafana_config/alertmanager.yml`:

- **Email**: SMTP settings for email notifications
- **Slack**: Webhook URLs for Slack channels
- **PagerDuty**: Service keys for critical alerts
- **Webhook**: Integration with incident management system

### Exporting Alert Configuration

Generate Grafana provisioning files:

```bash
python critical_alert_detector.py --export-config --output-dir ./grafana_config
```

This creates:
- `eu_ai_act_alerts.yaml` - Alert rule definitions
- `datasources.yaml` - Data source configuration
- `dashboard.json` - Monitoring dashboard

## Usage

### Display Alert Configuration

```bash
python critical_alert_detector.py --display
```

### Export Configuration Files

```bash
python critical_alert_detector.py --export-config --output-dir ./grafana_config
```

### Simulate Metrics (Testing)

```bash
python metrics_exporter.py
```

This simulates AI system metrics for testing the alert system.

### Test Alert Webhook

```bash
curl -X POST http://localhost:8002/api/alerts/test
```

## Metrics Reference

### Safety-001 Metrics (Death/Serious Harm)

- `ai_system_health_impact_score` - Health impact severity (0-10)
- `ai_system_fatality_detected` - Fatality flag (0 or 1)

### Safety-002 Metrics (Critical Infrastructure)

- `ai_system_infrastructure_impact_score` - Infrastructure impact (0-10)
- `ai_system_disruption_duration_minutes` - Disruption duration

### Safety-003 Metrics (Fundamental Rights)

- `ai_system_rights_violation_score` - Rights violation severity (0-10)
- `ai_system_bias_score` - Bias detection score (0-1)

### Safety-005 Metrics (Property/Environmental)

- `ai_system_damage_value_eur` - Estimated damage in EUR
- `ai_system_environmental_impact_score` - Environmental impact (0-10)

### General Metrics

- `ai_system_error_rate` - Error rate (0-1)
- `ai_system_prediction_latency_seconds` - Prediction latency
- `ai_system_predictions_total` - Total predictions counter
- `ai_system_serious_incidents_total` - Serious incidents counter

## Integration with Incident Management

The alert system automatically integrates with the existing incident management system:

```python
from alert_webhook_handler import AlertWebhookHandler

handler = AlertWebhookHandler()
result = handler.process_alert(alert_data)
```

When a critical alert fires:
1. Alert is received via webhook
2. Incident is automatically created
3. AI classification determines severity and reporting timeline
4. Incident is tracked in the incident management system

## Compliance Notes

### Article 73 Requirements

The system ensures compliance with EU AI Act Article 73:

- **Immediate reporting** for critical infrastructure (2 days)
- **Fast reporting** for death/serious harm (10 days)
- **Standard reporting** for other serious incidents (15 days)

### Notification Escalation

- **CRITICAL alerts** (safety-001, safety-002): PagerDuty + Email + Slack + SMS
- **HIGH alerts** (safety-003, safety-005): Email + Slack

### Audit Trail

All alerts and incidents are logged with:
- Timestamp of detection
- Alert conditions that triggered
- Metrics values at time of alert
- Notification channels used
- Incident creation details

## Troubleshooting

### Grafana not starting

```bash
docker-compose logs grafana
```

### Metrics not appearing

Check Prometheus targets:
```bash
open http://localhost:9090/targets
```

### Alerts not firing

1. Check alert rules in Grafana UI
2. Verify metrics are being exported: `curl http://localhost:8000/metrics`
3. Check Alertmanager: `open http://localhost:9093`

### Webhook not receiving alerts

```bash
# Check webhook handler logs
curl http://localhost:8002/health
```

## File Structure

```
geminihackathon/
├── critical_alert_detector.py      # Main alert detector module
├── metrics_exporter.py              # Prometheus metrics exporter
├── alert_webhook_handler.py         # Grafana webhook handler
├── grafana_config/
│   ├── docker-compose.yml           # Docker stack definition
│   ├── prometheus.yml               # Prometheus configuration
│   ├── alertmanager.yml             # Alert routing & notifications
│   ├── loki-config.yaml             # Log aggregation config
│   ├── promtail-config.yaml         # Log collection config
│   ├── datasources.yaml             # Grafana data sources
│   ├── eu_ai_act_alerts.yaml        # Alert rule definitions
│   ├── dashboard.json               # Monitoring dashboard
│   └── dashboards/
│       └── dashboard-provider.yaml  # Dashboard provisioning
└── CRITICAL_ALERT_DETECTOR_README.md
```

## API Reference

### Metrics Exporter API

```python
from metrics_exporter import AISystemMetricsExporter

exporter = AISystemMetricsExporter(port=8000)
exporter.start()

# Update safety-001 metrics
exporter.update_safety_001_metrics(
    ai_system='medical_ai',
    health_score=8.5,
    fatality=False
)

# Update safety-002 metrics
exporter.update_safety_002_metrics(
    ai_system='traffic_ai',
    infrastructure_score=9.0,
    disruption_minutes=30
)
```

### Webhook Handler API

**POST /api/alerts/webhook**
- Receives Grafana alerts
- Creates incidents automatically
- Returns processing status

**POST /api/alerts/test**
- Test endpoint for alert simulation
- Returns test alert processing result

**GET /health**
- Health check endpoint
- Returns service status

## References

- [EU AI Act Regulation 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- [Article 73 - Reporting of serious incidents](https://eur-lex.europa.eu/eli/reg/2024/1689/oj#art_73)
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Grafana and Prometheus logs
3. Consult the EU AI Act compliance documentation
4. Review incident management integration

## License

Part of the EU AI Act Compliance Project
