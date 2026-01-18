# Start the API server
source /home/kali/Code/geminihackathon/.venv/bin/activate
cd /home/kali/Code/geminihackathon/pmm_system
PYTHONPATH=$PWD python -m pmm_agent.main

# Access API documentation
# Open browser: http://localhost:8000/docs

# Run demo
python scripts/demo.py

# Run tests
PYTHONPATH=$PWD pytest tests/test_basic.py -v
python scripts/test_client.py

# Demo

```
======================================================================
POST-MARKET MONITORING SYSTEM - DEMO
======================================================================

This demo shows:
1. AI interaction monitoring
2. Bias detection
3. Alert triggering
4. Incident creation
5. User feedback processing
6. Report generation

======================================================================

Initializing PMM Agent...
✓ PMM Core Agent initialized
  - 10 safety metrics configured
  - Ethics monitoring enabled
  - Incident response ready

======================================================================
PHASE 1: Simulating 20 AI Interactions
======================================================================

Processing interaction 1/20... ⚠️  Alert: response_accuracy = 0.840 (threshold: 0.900)

============================================================
🚨 INCIDENT CREATED: INC-20260115-0001
============================================================
Priority: P1
Classification: security_breach
Response Time SLA: < 5 minutes
Alert Type: response_accuracy_threshold_violation
Severity: critical
Metric: response_accuracy = 0.840
Threshold: 0.900

Recommended Actions:
  1. Initial assessment of impact scope
  2. Preserve evidence and logs
  3. Notify response team
  4. Analyze recent model changes
  5. Review input data quality
  6. Check for data drift
  7. Consider model rollback
  8. Document findings and actions
============================================================

✓ (alerts: 1, bias alerts: 0)
Processing interaction 2/20... ✓ (alerts: 0, bias alerts: 0)
Processing interaction 3/20... ⚠️  Alert: citation_accuracy = 0.870 (threshold: 0.950)

============================================================
🚨 INCIDENT CREATED: INC-20260115-0002
============================================================
Priority: P1
Classification: security_breach
Response Time SLA: < 5 minutes
Alert Type: citation_accuracy_threshold_violation
Severity: critical
Metric: citation_accuracy = 0.870
Threshold: 0.950

Recommended Actions:
  1. Initial assessment of impact scope
  2. Preserve evidence and logs
  3. Notify response team
  4. Analyze recent model changes
  5. Review input data quality
  6. Check for data drift
  7. Consider model rollback
  8. Document findings and actions
============================================================

✓ (alerts: 1, bias alerts: 0)
Processing interaction 4/20... ⚠️  Alert: response_accuracy = 0.831 (threshold: 0.900)
⚠️  Alert: citation_accuracy = 0.926 (threshold: 0.950)

============================================================
🚨 INCIDENT CREATED: INC-20260115-0003
============================================================
Priority: P1
Classification: security_breach
Response Time SLA: < 5 minutes
Alert Type: response_accuracy_threshold_violation
Severity: critical
Metric: response_accuracy = 0.831
Threshold: 0.900

Recommended Actions:
  1. Initial assessment of impact scope
  2. Preserve evidence and logs
  3. Notify response team
  4. Analyze recent model changes
  5. Review input data quality
  6. Check for data drift
  7. Consider model rollback
  8. Document findings and actions
============================================================

✓ (alerts: 2, bias alerts: 0)
Processing interaction 5/20... ✓ (alerts: 0, bias alerts: 0)

Processing interaction 6/20... ✓ (alerts: 0, bias alerts: 0)
Processing interaction 7/20... ⚠️  Alert: citation_accuracy = 0.945 (threshold: 0.950)
✓ (alerts: 1, bias alerts: 0)
Processing interaction 8/20... ⚠️  Alert: response_accuracy = 0.857 (threshold: 0.900)
⚠️  Alert: citation_accuracy = 0.904 (threshold: 0.950)
✓ (alerts: 2, bias alerts: 0)
Processing interaction 9/20... ✓ (alerts: 0, bias alerts: 0)
Processing interaction 10/20... ⚠️  Alert: citation_accuracy = 0.950 (threshold: 0.950)
✓ (alerts: 1, bias alerts: 0)

Processing interaction 11/20... ⚠️  Alert: response_accuracy = 0.855 (threshold: 0.900)
✓ (alerts: 1, bias alerts: 0)
Processing interaction 12/20... ✓ (alerts: 0, bias alerts: 0)
Processing interaction 13/20... ⚠️  Alert: response_accuracy = 0.850 (threshold: 0.900)
⚠️  Alert: citation_accuracy = 0.920 (threshold: 0.950)

============================================================
🚨 INCIDENT CREATED: INC-20260115-0004
============================================================
Priority: P1
Classification: security_breach
Response Time SLA: < 5 minutes
Alert Type: response_accuracy_threshold_violation
Severity: critical
Metric: response_accuracy = 0.850
Threshold: 0.900

Recommended Actions:
  1. Initial assessment of impact scope
  2. Preserve evidence and logs
  3. Notify response team
  4. Analyze recent model changes
  5. Review input data quality
  6. Check for data drift
  7. Consider model rollback
  8. Document findings and actions
============================================================

✓ (alerts: 2, bias alerts: 0)
Processing interaction 14/20... ⚠️  Alert: response_accuracy = 0.891 (threshold: 0.900)
⚠️  Alert: citation_accuracy = 0.939 (threshold: 0.950)
✓ (alerts: 2, bias alerts: 0)
Processing interaction 15/20... ⚠️  Alert: hallucination_rate = 0.105 (threshold: 0.100)
⚠️  Alert: citation_accuracy = 0.940 (threshold: 0.950)
✓ (alerts: 2, bias alerts: 0)

Processing interaction 16/20... ⚠️  Alert: response_accuracy = 0.838 (threshold: 0.900)

============================================================
🚨 INCIDENT CREATED: INC-20260115-0005
============================================================
Priority: P1
Classification: security_breach
Response Time SLA: < 5 minutes
Alert Type: response_accuracy_threshold_violation
Severity: critical
Metric: response_accuracy = 0.838
Threshold: 0.900

Recommended Actions:
  1. Initial assessment of impact scope
  2. Preserve evidence and logs
  3. Notify response team
  4. Analyze recent model changes
  5. Review input data quality
  6. Check for data drift
  7. Consider model rollback
  8. Document findings and actions
============================================================

✓ (alerts: 1, bias alerts: 0)
Processing interaction 17/20... ⚠️  Alert: response_accuracy = 0.845 (threshold: 0.900)
⚠️  Alert: citation_accuracy = 0.910 (threshold: 0.950)

============================================================
🚨 INCIDENT CREATED: INC-20260115-0006
============================================================
Priority: P1
Classification: security_breach
Response Time SLA: < 5 minutes
Alert Type: response_accuracy_threshold_violation
Severity: critical
Metric: response_accuracy = 0.845
Threshold: 0.900

Recommended Actions:
  1. Initial assessment of impact scope
  2. Preserve evidence and logs
  3. Notify response team
  4. Analyze recent model changes
  5. Review input data quality
  6. Check for data drift
  7. Consider model rollback
  8. Document findings and actions
============================================================

✓ (alerts: 2, bias alerts: 0)
Processing interaction 18/20... ✓ (alerts: 0, bias alerts: 0)
Processing interaction 19/20... ✓ (alerts: 0, bias alerts: 0)
Processing interaction 20/20... ⚠️  Alert: hallucination_rate = 0.103 (threshold: 0.100)
⚠️  Alert: citation_accuracy = 0.920 (threshold: 0.950)
✓ (alerts: 2, bias alerts: 0)


======================================================================
PHASE 2: Simulating User Feedback
======================================================================

✓ Feedback processed: demo_fb_001 (sentiment: positive, rating: 5/5)
✓ Feedback 1: Rating 5/5, Sentiment: positive, Action Needed: False
✓ Feedback processed: demo_fb_002 (sentiment: positive, rating: 4/5)
✓ Feedback 2: Rating 4/5, Sentiment: positive, Action Needed: False
✓ Feedback processed: demo_fb_003 (sentiment: negative, rating: 2/5)
✓ Feedback 3: Rating 2/5, Sentiment: negative, Action Needed: True
✓ Feedback processed: demo_fb_004 (sentiment: negative, rating: 1/5)
✓ Feedback 4: Rating 1/5, Sentiment: negative, Action Needed: True
✓ Feedback processed: demo_fb_005 (sentiment: neutral, rating: 3/5)
✓ Feedback 5: Rating 3/5, Sentiment: neutral, Action Needed: False

======================================================================
PHASE 3: Generating Reports
======================================================================

📊 Metrics Summary (Last 24 hours):
----------------------------------------------------------------------
✓ OK response_accuracy: 0.905 (target: 0.950, trend: stable)
✓ OK hallucination_rate: 0.074 (target: 0.050, trend: improving)
✓ OK user_satisfaction: 4.175 (target: 4.000, trend: improving)
✓ OK privacy_incidents: 0.016 (target: 0.000, trend: stable)
✓ OK citation_accuracy: 0.953 (target: 0.990, trend: improving)

👥 Bias Monitoring Report:
----------------------------------------------------------------------
============================================================
BIAS MONITORING REPORT
============================================================

Attribute: gender
----------------------------------------
Selection Rates:
  male: 1.000
  female: 1.000
  ✓ All groups pass 4/5ths rule

Attribute: race
----------------------------------------
Selection Rates:
  caucasian: 1.000
  asian: 1.000
  african_american: 1.000
  hispanic: 1.000
  ✓ All groups pass 4/5ths rule

Attribute: age
----------------------------------------
Selection Rates:
  25-35: 1.000
  35-45: 1.000
  45-55: 1.000
  ✓ All groups pass 4/5ths rule

✓ No active alerts

🚨 Incident Statistics:
----------------------------------------------------------------------
  Total Incidents: 6
  Active: 6
  Closed: 0

======================================================================
COMPREHENSIVE REPORT
======================================================================

======================================================================
POST-MARKET MONITORING REPORT
======================================================================
Generated: 2026-01-15T16:48:35.806046+00:00
Period: Last 1 days

INTERACTIONS: 20 total
----------------------------------------------------------------------

METRICS SUMMARY:
----------------------------------------------------------------------
✓ OK response_accuracy: 0.905 (target: 0.950, trend: stable)
✓ OK hallucination_rate: 0.074 (target: 0.050, trend: improving)
✓ OK user_satisfaction: 4.175 (target: 4.000, trend: improving)
✓ OK privacy_incidents: 0.016 (target: 0.000, trend: stable)
✓ OK citation_accuracy: 0.953 (target: 0.990, trend: improving)

ACTIVE ALERTS: 20
----------------------------------------------------------------------
  [CRITICAL] response_accuracy_threshold_violation: response_accuracy=0.838
  [CRITICAL] response_accuracy_threshold_violation: response_accuracy=0.845
  [HIGH] citation_accuracy_threshold_violation: citation_accuracy=0.910
  [HIGH] hallucination_rate_threshold_violation: hallucination_rate=0.103
  [HIGH] citation_accuracy_threshold_violation: citation_accuracy=0.920

BIAS MONITORING:
----------------------------------------------------------------------
============================================================
BIAS MONITORING REPORT
============================================================

Attribute: gender
----------------------------------------
Selection Rates:
  male: 1.000
  female: 1.000
  ✓ All groups pass 4/5ths rule

Attribute: race
----------------------------------------
Selection Rates:
  caucasian: 1.000
  asian: 1.000
  african_american: 1.000
  hispanic: 1.000
  ✓ All groups pass 4/5ths rule

Attribute: age
----------------------------------------
Selection Rates:
  25-35: 1.000
  35-45: 1.000
  45-55: 1.000
  ✓ All groups pass 4/5ths rule

✓ No active alerts

INCIDENT STATISTICS:
----------------------------------------------------------------------
  Total: 6
  Active: 6
  Closed: 0

USER FEEDBACK: 5 submissions
----------------------------------------------------------------------
  Average Rating: 3.00/5
  Sentiment: {'positive': 2, 'neutral': 1, 'negative': 2}

======================================================================

======================================================================
DEMO COMPLETED SUCCESSFULLY
======================================================================

Next steps:
1. Start the API server: python -m pmm_agent.main
2. Visit http://localhost:8000/docs for API documentation
3. Try the test client: python scripts/test_client.py

======================================================================
```

# API test

```
┌──(.venv)(kali㉿DESKTOP-B3351FI)-[~/Code/geminihackathon/pmm_system]
└─$ python scripts/test_client.py

======================================================================
PMM API TEST CLIENT
======================================================================
Testing API at: http://localhost:8000
Started: 2026-01-16T00:54:50.050870

======================================================================
Testing Health Check
======================================================================

Status: 200
{
  "status": "healthy",
  "timestamp": "2026-01-15T16:54:50.054509+00:00",
  "integrations": {
    "safety_provider": "connected",
    "ethics_bridge": "connected",
    "incident_trigger": "connected"
  }
}

======================================================================
Testing Interaction Logging
======================================================================

Status: 200
{
  "status": "logged",
  "interaction_id": "test_int_1768496090",
  "summary": {
    "interaction_id": "test_int_1768496090",
    "metrics_computed": 5,
    "alerts_triggered": 0,
    "bias_alerts": 0,
    "incidents_created": 0,
    "ethics_assessment": false,
    "timestamp": "2026-01-15T16:54:50.564586+00:00"
  }
}

======================================================================
Testing Feedback Submission
======================================================================

Status: 200
{
  "status": "received",
  "feedback_id": "FB-1768496091.07026",
  "analysis": {
    "feedback_id": "FB-1768496091.07026",
    "sentiment": "positive",
    "categories": [
      "high_satisfaction"
    ],
    "requires_action": false
  }
}

======================================================================
Testing Metrics Query
======================================================================

Status: 200
{
  "metrics": {
    "response_accuracy": {
      "average": 0.9274437173773238,
      "count": 2,
      "target": 0.95,
      "status": "\u2713 OK",
      "trend": "improving"
    },
    "hallucination_rate": {
      "average": 0.06485447978678391,
      "count": 2,
      "target": 0.05,
      "status": "\u2713 OK",
      "trend": "improving"
    }
  },
  "period_hours": 24,
  "timestamp": "2026-01-15T16:54:51.578000+00:00"
}

======================================================================
Testing Current Metrics
======================================================================

Status: 200
{
  "metrics": {
    "response_accuracy": {
      "current_value": 0.957073908697422,
      "recent_average": 0.9274437173773238,
      "samples": 2
    },
    "hallucination_rate": {
      "current_value": 0.08294753373650743,
      "recent_average": 0.06485447978678391,
      "samples": 2
    },
    "user_satisfaction": {
      "current_value": 4.102669065720898,
      "recent_average": 4.134020026215777,
      "samples": 2
    },
    "citation_accuracy": {
      "current_value": 0.9608121088442342,
      "recent_average": 0.971238882641714,
      "samples": 2
    },
    "privacy_incidents": {
      "current_value": 0.0,
      "recent_average": 0.0,
      "samples": 2
    }
  },
  "timestamp": "2026-01-15T16:54:52.083809+00:00"
}

======================================================================
Testing Active Alerts
======================================================================

Status: 200
Active Alerts: 1
[
  {
    "alert_id": "ALT-1768494904.812479",
    "timestamp": "2026-01-15T16:35:04.812496+00:00",
    "severity": "high",
    "alert_type": "response_accuracy_threshold_violation",
    "metric_name": "response_accuracy",
    "current_value": 0.8978135260572255,
    "threshold": 0.9
  }
]

======================================================================
Testing Active Incidents
======================================================================

Status: 200
Active Incidents: 0

======================================================================
Testing Bias Report
======================================================================

Status: 200
============================================================
BIAS MONITORING REPORT
============================================================

Attribute: gender
----------------------------------------
Selection Rates:
  female: 1.000

Attribute: race
----------------------------------------
Selection Rates:
  asian: 1.000

Attribute: age
----------------------------------------
Selection Rates:
  25-35: 1.000

✓ No active alerts

======================================================================
Testing Summary Report
======================================================================

Status: 200

======================================================================
POST-MARKET MONITORING REPORT
======================================================================
Generated: 2026-01-15T16:54:54.106223+00:00
Period: Last 7 days

INTERACTIONS: 2 total
----------------------------------------------------------------------

METRICS SUMMARY:
----------------------------------------------------------------------
✓ OK response_accuracy: 0.927 (target: 0.950, trend: improving)
✓ OK hallucination_rate: 0.065 (target: 0.050, trend: improving)
✓ OK user_satisfaction: 4.134 (target: 4.000, trend: declining)
✓ OK privacy_incidents: 0.000 (target: 0.000, trend: stable)
✓ OK citation_accuracy: 0.971 (target: 0.990, trend: declining)

ACTIVE ALERTS: 1
----------------------------------------------------------------------
  [HIGH] response_accuracy_threshold_violation: response_accuracy=0.898

BIAS MONITORING:
----------------------------------------------------------------------
============================================================
BIAS MONITORING REPORT
============================================================

Attribute: gender
----------------------------------------
Selection Rates:
  female: 1.000

Attribute: race
----------------------------------------
Selection Rates:
  asian: 1.000

Attribute: age
----------------------------------------
Selection Rates:
  25-35: 1.000

✓ No active alerts

INCIDENT STATISTICS:
----------------------------------------------------------------------
  Total: 0
  Active: 0
  Closed: 0

USER FEEDBACK: 2 submissions
----------------------------------------------------------------------
  Average Rating: 4.00/5
  Sentiment: {'positive': 2, 'neutral': 0, 'negative': 0}

======================================================================

======================================================================
Testing Statistics
======================================================================

Status: 200
{
  "interactions": {
    "total": 2,
    "last_24h": 2
  },
  "alerts": {
    "total": 1,
    "active": 1
  },
  "feedback": {
    "total": 2,
    "last_7d": 2
  },
  "incidents": {
    "total_incidents": 0,
    "active_incidents": 0,
    "closed_incidents": 0,
    "by_priority": {},
    "by_classification": {}
  }
}

======================================================================
TEST SUMMARY
======================================================================

✓ PASS: Health Check
✓ PASS: Log Interaction
✓ PASS: Submit Feedback
✓ PASS: Query Metrics
✓ PASS: Current Metrics
✓ PASS: Active Alerts
✓ PASS: Active Incidents
✓ PASS: Bias Report
✓ PASS: Summary Report
✓ PASS: Statistics

======================================================================
Results: 10/10 tests passed
======================================================================


┌──(.venv)(kali㉿DESKTOP-B3351FI)-[~/Code/geminihackathon/pmm_system]
└─$ PYTHONPATH=/home/kali/Code/geminihackathon/pmm_system:$PYTHONPATH pytest tests/test_basic.py -v
=================================================================== test session starts ====================================================================
platform linux -- Python 3.13.6, pytest-9.0.2, pluggy-1.6.0 -- /home/kali/Code/geminihackathon/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/kali/Code/geminihackathon/pmm_system
plugins: asyncio-1.3.0, anyio-4.12.1
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 4 items

tests/test_basic.py::test_safety_provider PASSED                                                                                                     [ 25%]
tests/test_basic.py::test_ethics_bridge PASSED                                                                                                       [ 50%]
tests/test_basic.py::test_ai_interaction_model PASSED                                                                                                [ 75%]
tests/test_basic.py::test_user_feedback_model PASSED                                                                                                 [100%]

==================================================================== 4 passed in 0.02s =====================================================================
```