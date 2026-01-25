#!/usr/bin/env python3
"""
Test client for PMM API
Tests all API endpoints
"""
import requests
import time
from datetime import datetime
import json


BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print section header"""
    print("\n" + "="*70)
    print(title)
    print("="*70 + "\n")


def test_health():
    """Test health endpoint"""
    print_section("Testing Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200


def test_log_interaction():
    """Test logging interaction"""
    print_section("Testing Interaction Logging")

    interaction = {
        "interaction_id": f"test_int_{int(time.time())}",
        "user_id": "test_user_1",
        "prompt": "What is machine learning?",
        "response": "Machine learning is a subset of artificial intelligence...",
        "response_time": 0.523,
        "model_version": "test-model-1.0",
        "metadata": {"temperature": 0.7},
        "demographics": {
            "gender": "female",
            "age": "25-35",
            "race": "asian"
        }
    }

    response = requests.post(f"{BASE_URL}/api/v1/interactions/log", json=interaction)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200


def test_submit_feedback():
    """Test submitting feedback"""
    print_section("Testing Feedback Submission")

    feedback = {
        "interaction_id": "test_int_001",
        "user_id": "test_user_1",
        "rating": 4,
        "comment": "Good response but could be more detailed and accurate.",
        "issues": []
    }

    response = requests.post(f"{BASE_URL}/api/v1/feedback/submit", json=feedback)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200


def test_query_metrics():
    """Test querying metrics"""
    print_section("Testing Metrics Query")

    query = {
        "metric_names": ["response_accuracy", "hallucination_rate"],
        "hours": 24
    }

    response = requests.post(f"{BASE_URL}/api/v1/metrics/query", json=query)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(json.dumps(result, indent=2))
    return response.status_code == 200


def test_current_metrics():
    """Test current metrics"""
    print_section("Testing Current Metrics")

    response = requests.get(f"{BASE_URL}/api/v1/metrics/current")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200


def test_active_alerts():
    """Test active alerts"""
    print_section("Testing Active Alerts")

    response = requests.get(f"{BASE_URL}/api/v1/alerts/active")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Active Alerts: {result['count']}")
    if result['alerts']:
        print(json.dumps(result['alerts'][:3], indent=2))  # Show first 3
    return response.status_code == 200


def test_active_incidents():
    """Test active incidents"""
    print_section("Testing Active Incidents")

    response = requests.get(f"{BASE_URL}/api/v1/incidents/active")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Active Incidents: {result['count']}")
    if result['incidents']:
        print(json.dumps(result['incidents'], indent=2))
    return response.status_code == 200


def test_bias_report():
    """Test bias report"""
    print_section("Testing Bias Report")

    response = requests.get(f"{BASE_URL}/api/v1/reports/bias")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(result['report'])
    return response.status_code == 200


def test_summary_report():
    """Test summary report"""
    print_section("Testing Summary Report")

    response = requests.get(f"{BASE_URL}/api/v1/reports/summary?days=7")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(result['report'])
    return response.status_code == 200


def test_statistics():
    """Test statistics"""
    print_section("Testing Statistics")

    response = requests.get(f"{BASE_URL}/api/v1/stats")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200


# ============================================================================
# Dashboard API Tests
# ============================================================================

def test_dashboard_overview():
    """Test dashboard overview"""
    print_section("Testing Dashboard Overview")

    response = requests.get(f"{BASE_URL}/api/v1/dashboard/overview")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Health Score: {result.get('health_score', 'N/A')}")
    print(f"Health Status: {result.get('health_status', 'N/A')}")
    print(f"Active Signals: {result.get('active_signals', 0)}")
    print(f"Active Alerts: {result.get('active_alerts', 0)}")
    return response.status_code == 200


def test_dashboard_kpis():
    """Test dashboard KPIs"""
    print_section("Testing Dashboard KPIs")

    response = requests.get(f"{BASE_URL}/api/v1/dashboard/kpis")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200


def test_signal_detection():
    """Test signal detection"""
    print_section("Testing Signal Detection")

    response = requests.get(f"{BASE_URL}/api/v1/signals/detect")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Signals Detected: {result.get('signals_detected', 0)}")
    if result.get('signals'):
        print(json.dumps(result['signals'][:3], indent=2))
    return response.status_code == 200


def test_signal_history():
    """Test signal history"""
    print_section("Testing Signal History")

    response = requests.get(f"{BASE_URL}/api/v1/signals/history?hours=24")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Total Signals: {result.get('count', 0)}")
    return response.status_code == 200


def test_trend_metrics():
    """Test trend metrics"""
    print_section("Testing Trend Metrics")

    response = requests.get(f"{BASE_URL}/api/v1/trends/metrics?hours=24")
    print(f"Status: {response.status_code}")
    result = response.json()
    trends = result.get('trends', {})
    for metric, data in list(trends.items())[:3]:
        print(f"  {metric}: {data.get('trend_direction', 'N/A')}")
    return response.status_code == 200


def test_create_complaint():
    """Test creating a complaint"""
    print_section("Testing Complaint Creation")

    complaint = {
        "user_id": "test_user_1",
        "category": "accuracy",
        "subject": "Incorrect response about EU regulations",
        "description": "The AI provided outdated information about EU AI Act requirements.",
        "priority": "medium",
        "tags": ["accuracy", "eu-ai-act"]
    }

    response = requests.post(f"{BASE_URL}/api/v1/complaints", json=complaint)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200


def test_get_complaints():
    """Test getting complaints"""
    print_section("Testing Get Complaints")

    response = requests.get(f"{BASE_URL}/api/v1/complaints?days=30")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Total Complaints: {result.get('count', 0)}")
    return response.status_code == 200


def test_complaints_analytics():
    """Test complaints analytics"""
    print_section("Testing Complaints Analytics")

    response = requests.get(f"{BASE_URL}/api/v1/complaints/analytics?days=30")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200


def test_realtime_performance():
    """Test real-time performance"""
    print_section("Testing Real-time Performance")

    response = requests.get(f"{BASE_URL}/api/v1/performance/realtime")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response Time Avg: {result.get('response_time', {}).get('avg_ms', 'N/A')} ms")
    print(f"Availability: {result.get('availability', {}).get('percentage', 'N/A')}%")
    print(f"Active Users: {result.get('active_users', 'N/A')}")
    return response.status_code == 200


def test_sla_status():
    """Test SLA status"""
    print_section("Testing SLA Status")

    response = requests.get(f"{BASE_URL}/api/v1/performance/sla")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"SLA Status: {result.get('status', 'N/A')}")
    print(f"Breaches: {result.get('breaches', [])}")
    return response.status_code == 200


def test_compliance_status():
    """Test EU AI Act compliance status"""
    print_section("Testing Compliance Status")

    response = requests.get(f"{BASE_URL}/api/v1/regulatory/compliance-status")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Framework: {result.get('framework', 'N/A')}")
    print(f"Monitoring Status: {result.get('monitoring_status', 'N/A')}")
    return response.status_code == 200


def test_generate_report():
    """Test generating regulatory report"""
    print_section("Testing Report Generation")

    request_data = {
        "report_type": "periodic",
        "period_days": 30
    }

    response = requests.post(f"{BASE_URL}/api/v1/regulatory/reports/generate", json=request_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Report ID: {result.get('report_id', 'N/A')}")
    print(f"Title: {result.get('title', 'N/A')}")
    return response.status_code == 200


def test_get_reports():
    """Test getting regulatory reports"""
    print_section("Testing Get Reports")

    response = requests.get(f"{BASE_URL}/api/v1/regulatory/reports")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Total Reports: {result.get('count', 0)}")
    return response.status_code == 200


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("PMM API TEST CLIENT")
    print("="*70)
    print(f"Testing API at: {BASE_URL}")
    print(f"Started: {datetime.now().isoformat()}")

    tests = [
        # Core PMM API
        ("Health Check", test_health),
        ("Log Interaction", test_log_interaction),
        ("Submit Feedback", test_submit_feedback),
        ("Query Metrics", test_query_metrics),
        ("Current Metrics", test_current_metrics),
        ("Active Alerts", test_active_alerts),
        ("Active Incidents", test_active_incidents),
        ("Bias Report", test_bias_report),
        ("Summary Report", test_summary_report),
        ("Statistics", test_statistics),
        # Dashboard API
        ("Dashboard Overview", test_dashboard_overview),
        ("Dashboard KPIs", test_dashboard_kpis),
        ("Signal Detection", test_signal_detection),
        ("Signal History", test_signal_history),
        ("Trend Metrics", test_trend_metrics),
        ("Create Complaint", test_create_complaint),
        ("Get Complaints", test_get_complaints),
        ("Complaints Analytics", test_complaints_analytics),
        ("Real-time Performance", test_realtime_performance),
        ("SLA Status", test_sla_status),
        ("Compliance Status", test_compliance_status),
        ("Generate Report", test_generate_report),
        ("Get Reports", test_get_reports),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
            time.sleep(0.5)  # Brief pause between tests
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append((name, False))

    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\n{'='*70}")
    print(f"Results: {passed}/{total} tests passed")
    print(f"{'='*70}\n")

    return passed == total


if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server")
        print("Please make sure the API server is running:")
        print("  python -m pmm_agent.main")
        exit(1)
