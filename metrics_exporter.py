"""
Prometheus Metrics Exporter for EU AI Act Compliance Monitoring
Exposes AI system metrics for Grafana alerting
REFACTORED: Uses unified metrics definitions from eu_ai_act_metrics.py
"""

from prometheus_client import start_http_server, Gauge, Counter, Histogram, Info
import time
import random
from typing import Dict, Optional
import json
from datetime import datetime

# Import unified metrics definitions
from eu_ai_act_metrics import (
    RiskCategory, EU_AI_ACT_RISK_MAPPINGS, MetricNames,
    get_threshold_config
)

class AISystemMetricsExporter:
    """
    Exports AI system metrics in Prometheus format for EU AI Act compliance monitoring
    """
    
    def __init__(self, port: int = 8000):
        self.port = port
        
        self.health_impact_score = Gauge(
            'ai_system_health_impact_score',
            'Health impact severity score (0-10)',
            ['ai_system', 'risk_id']
        )
        
        self.fatality_detected = Gauge(
            'ai_system_fatality_detected',
            'Fatality detection flag (0 or 1)',
            ['ai_system', 'risk_id']
        )
        
        self.infrastructure_impact_score = Gauge(
            'ai_system_infrastructure_impact_score',
            'Critical infrastructure impact score (0-10)',
            ['ai_system', 'risk_id']
        )
        
        self.disruption_duration_minutes = Gauge(
            'ai_system_disruption_duration_minutes',
            'Duration of service disruption in minutes',
            ['ai_system', 'risk_id']
        )
        
        self.rights_violation_score = Gauge(
            'ai_system_rights_violation_score',
            'Fundamental rights violation score (0-10)',
            ['ai_system', 'risk_id']
        )
        
        self.bias_score = Gauge(
            'ai_system_bias_score',
            'Bias detection score (0-1)',
            ['ai_system', 'risk_id', 'protected_attribute']
        )
        
        self.damage_value_eur = Gauge(
            'ai_system_damage_value_eur',
            'Estimated damage value in EUR',
            ['ai_system', 'risk_id']
        )
        
        self.environmental_impact_score = Gauge(
            'ai_system_environmental_impact_score',
            'Environmental impact severity score (0-10)',
            ['ai_system', 'risk_id']
        )
        
        self.error_rate = Gauge(
            'ai_system_error_rate',
            'AI system error rate (0-1)',
            ['ai_system', 'model_version']
        )
        
        self.prediction_latency = Histogram(
            'ai_system_prediction_latency_seconds',
            'Prediction latency in seconds',
            ['ai_system', 'model_version']
        )
        
        self.predictions_total = Counter(
            'ai_system_predictions_total',
            'Total number of predictions',
            ['ai_system', 'model_version', 'outcome']
        )
        
        self.serious_incidents_total = Counter(
            'ai_system_serious_incidents_total',
            'Total serious incidents by type',
            ['ai_system', 'incident_type', 'risk_id']
        )
        
        self.compliance_status = Gauge(
            'ai_system_compliance_status',
            'Compliance status (1=compliant, 0=non-compliant)',
            ['ai_system', 'article']
        )
        
        self.system_info = Info(
            'ai_system_info',
            'AI system information'
        )
    
    def update_safety_001_metrics(self, ai_system: str, health_score: float, fatality: bool = False):
        """Update metrics for safety-001 (death/serious harm)"""
        self.health_impact_score.labels(ai_system=ai_system, risk_id='safety-001').set(health_score)
        self.fatality_detected.labels(ai_system=ai_system, risk_id='safety-001').set(1 if fatality else 0)
        
        if health_score > 9.0 or fatality:
            self.serious_incidents_total.labels(
                ai_system=ai_system,
                incident_type='death_or_harm',
                risk_id='safety-001'
            ).inc()
    
    def update_safety_002_metrics(self, ai_system: str, infrastructure_score: float, 
                                  disruption_minutes: float):
        """Update metrics for safety-002 (critical infrastructure)"""
        self.infrastructure_impact_score.labels(ai_system=ai_system, risk_id='safety-002').set(infrastructure_score)
        self.disruption_duration_minutes.labels(ai_system=ai_system, risk_id='safety-002').set(disruption_minutes)
        
        if infrastructure_score > 8.5 and disruption_minutes > 15:
            self.serious_incidents_total.labels(
                ai_system=ai_system,
                incident_type='infrastructure_disruption',
                risk_id='safety-002'
            ).inc()
    
    def update_safety_003_metrics(self, ai_system: str, rights_score: float, 
                                  bias_scores: Dict[str, float]):
        """Update metrics for safety-003 (fundamental rights)"""
        self.rights_violation_score.labels(ai_system=ai_system, risk_id='safety-003').set(rights_score)
        
        for attribute, score in bias_scores.items():
            self.bias_score.labels(
                ai_system=ai_system,
                risk_id='safety-003',
                protected_attribute=attribute
            ).set(score)
        
        if rights_score > 7.0 or any(score > 0.15 for score in bias_scores.values()):
            self.serious_incidents_total.labels(
                ai_system=ai_system,
                incident_type='rights_violation',
                risk_id='safety-003'
            ).inc()
    
    def update_safety_005_metrics(self, ai_system: str, damage_eur: float, 
                                  environmental_score: float):
        """Update metrics for safety-005 (property/environmental harm)"""
        self.damage_value_eur.labels(ai_system=ai_system, risk_id='safety-005').set(damage_eur)
        self.environmental_impact_score.labels(ai_system=ai_system, risk_id='safety-005').set(environmental_score)
        
        if damage_eur > 50000 or environmental_score > 7.5:
            self.serious_incidents_total.labels(
                ai_system=ai_system,
                incident_type='property_environmental_harm',
                risk_id='safety-005'
            ).inc()
    
    def update_general_metrics(self, ai_system: str, model_version: str, 
                              error_rate: float, latency: float):
        """Update general AI system performance metrics"""
        self.error_rate.labels(ai_system=ai_system, model_version=model_version).set(error_rate)
        self.prediction_latency.labels(ai_system=ai_system, model_version=model_version).observe(latency)
    
    def record_prediction(self, ai_system: str, model_version: str, outcome: str):
        """Record a prediction outcome"""
        self.predictions_total.labels(
            ai_system=ai_system,
            model_version=model_version,
            outcome=outcome
        ).inc()
    
    def set_compliance_status(self, ai_system: str, article: str, compliant: bool):
        """Set compliance status for specific article"""
        self.compliance_status.labels(ai_system=ai_system, article=article).set(1 if compliant else 0)
    
    def set_system_info(self, ai_system: str, provider: str, risk_level: str, 
                       deployment_date: str):
        """Set AI system information"""
        self.system_info.info({
            'ai_system': ai_system,
            'provider': provider,
            'risk_level': risk_level,
            'deployment_date': deployment_date,
            'regulation': 'EU AI Act 2024/1689'
        })
    
    def start(self):
        """Start the metrics HTTP server"""
        start_http_server(self.port)
        print(f"Metrics server started on port {self.port}")
        print(f"Metrics available at http://localhost:{self.port}/metrics")


def simulate_metrics():
    """Simulate AI system metrics for testing"""
    exporter = AISystemMetricsExporter(port=8000)
    exporter.start()
    
    exporter.set_system_info(
        ai_system='medical_diagnosis_ai',
        provider='HealthTech Corp',
        risk_level='high',
        deployment_date='2024-08-02'
    )
    
    print("Simulating AI system metrics...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            health_score = random.uniform(0, 10)
            exporter.update_safety_001_metrics(
                ai_system='medical_diagnosis_ai',
                health_score=health_score,
                fatality=health_score > 9.5
            )
            
            infra_score = random.uniform(0, 10)
            disruption = random.uniform(0, 60)
            exporter.update_safety_002_metrics(
                ai_system='traffic_control_ai',
                infrastructure_score=infra_score,
                disruption_minutes=disruption
            )
            
            rights_score = random.uniform(0, 10)
            bias_scores = {
                'gender': random.uniform(0, 0.3),
                'race': random.uniform(0, 0.3),
                'age': random.uniform(0, 0.3)
            }
            exporter.update_safety_003_metrics(
                ai_system='hiring_ai',
                rights_score=rights_score,
                bias_scores=bias_scores
            )
            
            damage = random.uniform(0, 100000)
            env_score = random.uniform(0, 10)
            exporter.update_safety_005_metrics(
                ai_system='industrial_control_ai',
                damage_eur=damage,
                environmental_score=env_score
            )
            
            error_rate = random.uniform(0, 0.2)
            latency = random.uniform(0.01, 0.5)
            exporter.update_general_metrics(
                ai_system='medical_diagnosis_ai',
                model_version='v2.1.0',
                error_rate=error_rate,
                latency=latency
            )
            
            outcome = random.choice(['success', 'error', 'timeout'])
            exporter.record_prediction(
                ai_system='medical_diagnosis_ai',
                model_version='v2.1.0',
                outcome=outcome
            )
            
            exporter.set_compliance_status(
                ai_system='medical_diagnosis_ai',
                article='73',
                compliant=health_score < 9.0
            )
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nStopping metrics simulation...")


if __name__ == '__main__':
    simulate_metrics()
