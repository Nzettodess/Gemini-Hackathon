"""
Example: Integrating Critical Alert Detector with your AI system

This example shows how to instrument your AI system to export metrics
for EU AI Act compliance monitoring.
"""

from metrics_exporter import AISystemMetricsExporter
import time
import random

class MyAISystem:
    """
    Example AI system with EU AI Act compliance monitoring
    """
    
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.metrics = AISystemMetricsExporter(port=8000)
        self.metrics.start()
        
        self.metrics.set_system_info(
            ai_system=system_name,
            provider='Your Company',
            risk_level='high',
            deployment_date='2024-08-02'
        )
    
    def make_prediction(self, input_data):
        """Make a prediction and track metrics"""
        start_time = time.time()
        
        try:
            result = self._internal_prediction(input_data)
            
            latency = time.time() - start_time
            self.metrics.update_general_metrics(
                ai_system=self.system_name,
                model_version='v1.0.0',
                error_rate=0.01,
                latency=latency
            )
            
            self.metrics.record_prediction(
                ai_system=self.system_name,
                model_version='v1.0.0',
                outcome='success'
            )
            
            self._check_safety_metrics(result)
            
            return result
            
        except Exception as e:
            self.metrics.record_prediction(
                ai_system=self.system_name,
                model_version='v1.0.0',
                outcome='error'
            )
            raise
    
    def _internal_prediction(self, input_data):
        """Your actual prediction logic here"""
        return {"prediction": "example", "confidence": 0.95}
    
    def _check_safety_metrics(self, result):
        """Check if prediction triggers any safety concerns"""
        
        if result.get('health_risk'):
            health_score = result.get('health_risk_score', 0)
            self.metrics.update_safety_001_metrics(
                ai_system=self.system_name,
                health_score=health_score,
                fatality=health_score > 9.5
            )
        
        if result.get('bias_detected'):
            bias_scores = result.get('bias_scores', {})
            self.metrics.update_safety_003_metrics(
                ai_system=self.system_name,
                rights_score=result.get('rights_violation_score', 0),
                bias_scores=bias_scores
            )
        
        self.metrics.set_compliance_status(
            ai_system=self.system_name,
            article='73',
            compliant=True
        )


def example_medical_ai():
    """Example: Medical diagnosis AI system"""
    
    ai_system = MyAISystem('medical_diagnosis_ai')
    
    print("Running medical AI system with compliance monitoring...")
    
    for i in range(10):
        patient_data = {
            'symptoms': ['fever', 'cough'],
            'age': random.randint(20, 80),
            'medical_history': []
        }
        
        result = ai_system.make_prediction(patient_data)
        
        health_risk_score = random.uniform(0, 10)
        result['health_risk'] = health_risk_score > 7.0
        result['health_risk_score'] = health_risk_score
        
        ai_system._check_safety_metrics(result)
        
        print(f"Prediction {i+1}: Health risk score = {health_risk_score:.2f}")
        time.sleep(1)


def example_hiring_ai():
    """Example: Hiring AI system with bias monitoring"""
    
    ai_system = MyAISystem('hiring_ai')
    
    print("Running hiring AI system with bias monitoring...")
    
    for i in range(10):
        candidate_data = {
            'experience_years': random.randint(0, 20),
            'education': 'Bachelor',
            'skills': ['python', 'ml']
        }
        
        result = ai_system.make_prediction(candidate_data)
        
        bias_scores = {
            'gender': random.uniform(0, 0.3),
            'race': random.uniform(0, 0.3),
            'age': random.uniform(0, 0.3)
        }
        
        result['bias_detected'] = any(score > 0.15 for score in bias_scores.values())
        result['bias_scores'] = bias_scores
        result['rights_violation_score'] = max(bias_scores.values()) * 10
        
        ai_system._check_safety_metrics(result)
        
        print(f"Prediction {i+1}: Max bias score = {max(bias_scores.values()):.3f}")
        time.sleep(1)


def example_infrastructure_ai():
    """Example: Critical infrastructure control AI"""
    
    metrics = AISystemMetricsExporter(port=8000)
    metrics.start()
    
    metrics.set_system_info(
        ai_system='traffic_control_ai',
        provider='City Infrastructure',
        risk_level='high',
        deployment_date='2024-08-02'
    )
    
    print("Running infrastructure AI with disruption monitoring...")
    
    for i in range(10):
        infrastructure_score = random.uniform(0, 10)
        disruption_minutes = random.uniform(0, 60)
        
        metrics.update_safety_002_metrics(
            ai_system='traffic_control_ai',
            infrastructure_score=infrastructure_score,
            disruption_minutes=disruption_minutes
        )
        
        if infrastructure_score > 8.5 and disruption_minutes > 15:
            print(f"⚠️  ALERT: Critical infrastructure disruption detected!")
            print(f"   Impact score: {infrastructure_score:.2f}")
            print(f"   Disruption: {disruption_minutes:.1f} minutes")
        else:
            print(f"Monitoring {i+1}: Impact={infrastructure_score:.2f}, Disruption={disruption_minutes:.1f}min")
        
        time.sleep(1)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        example_type = sys.argv[1]
        
        if example_type == 'medical':
            example_medical_ai()
        elif example_type == 'hiring':
            example_hiring_ai()
        elif example_type == 'infrastructure':
            example_infrastructure_ai()
        else:
            print("Usage: python alert_integration_example.py [medical|hiring|infrastructure]")
    else:
        print("Choose an example:")
        print("  python alert_integration_example.py medical")
        print("  python alert_integration_example.py hiring")
        print("  python alert_integration_example.py infrastructure")
