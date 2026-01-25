# Grafana Configuration for EU AI Act Compliance

This directory contains all configuration files for the Critical Alert Detector system.

## Quick Start

1. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

2. **Start the monitoring stack:**
   ```bash
   docker-compose up -d
   ```

3. **Verify services are running:**
   ```bash
   docker-compose ps
   ```

4. **Access Grafana:**
   - URL: http://localhost:3000
   - Username: `admin`
   - Password: `admin` (change on first login)

## Configuration Files

### Core Configuration
- `docker-compose.yml` - Docker stack definition
- `prometheus.yml` - Prometheus scrape and alerting config
- `alertmanager.yml` - Alert routing and notification channels
- `datasources.yaml` - Grafana data source provisioning
- `eu_ai_act_alerts.yaml` - Alert rule definitions

### Log Aggregation
- `loki-config.yaml` - Loki log storage configuration
- `promtail-config.yaml` - Log collection and parsing

### Dashboards
- `dashboard.json` - EU AI Act compliance monitoring dashboard
- `dashboards/dashboard-provider.yaml` - Dashboard provisioning config

## Customization

### Update Alert Thresholds

Edit alert conditions in `eu_ai_act_alerts.yaml` or regenerate using:

```bash
cd ..
python critical_alert_detector.py --export-config --output-dir ./grafana_config
```

### Configure Notifications

Edit `alertmanager.yml` to configure:
- Email SMTP settings
- Slack webhook URLs
- PagerDuty service keys
- Custom webhook endpoints

### Add Custom Metrics

Add new scrape targets in `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'my_ai_system'
    static_configs:
      - targets: ['my-service:8080']
        labels:
          ai_system: 'my_system'
          risk_level: 'high'
```

## Ports

- **3000** - Grafana UI
- **9090** - Prometheus UI
- **3100** - Loki (logs)
- **9093** - Alertmanager UI

## Troubleshooting

### Check service logs
```bash
docker-compose logs -f grafana
docker-compose logs -f prometheus
docker-compose logs -f alertmanager
```

### Restart services
```bash
docker-compose restart
```

### Reset everything
```bash
docker-compose down -v
docker-compose up -d
```

## Production Deployment

For production use:

1. Change default passwords in `docker-compose.yml`
2. Configure persistent volumes
3. Set up SSL/TLS certificates
4. Configure proper SMTP credentials
5. Set up backup for Grafana dashboards and Prometheus data
6. Configure authentication (LDAP/OAuth)
7. Set resource limits in docker-compose.yml

## References

- [Grafana Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)
- [Prometheus Configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)
- [Alertmanager Configuration](https://prometheus.io/docs/alerting/latest/configuration/)
