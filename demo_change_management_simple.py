"""
Simple Demo/Test for Change Management System
Demonstrates all features without requiring external API dependencies
"""

import os
import json
from datetime import datetime

# Temporarily disable Gemini API to run demo without it
os.environ.pop("GEMINI_API_KEY", None)

from change_management import (
    ChangeManagementSystem,
    ChangeType,
    ChangePriority,
    ChangeStatus
)


def print_section(title):
    """Print section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_success(message):
    """Print success message"""
    print(f"✓ {message}")


def print_info(message):
    """Print info message"""
    print(f"  {message}")


def main():
    print("\n" + "=" * 80)
    print("  CHANGE MANAGEMENT SYSTEM - COMPREHENSIVE DEMO")
    print("  EU AI Act Article 17 & 43 Compliance")
    print("=" * 80)
    
    cms = ChangeManagementSystem()
    change_ids = []
    
    # ========================================================================
    # DEMO 1: Create Change Requests
    # ========================================================================
    print_section("DEMO 1: Creating Change Requests")
    
    changes_config = [
        {
            "title": "Update AI Risk Classification Model to v2.1",
            "description": "Deploy improved risk classification model with 5% accuracy increase",
            "type": ChangeType.MODEL_UPDATE,
            "priority": ChangePriority.HIGH,
            "systems": ["risk-classifier", "api-gateway", "monitoring"],
            "justification": "Improve accuracy and reduce false positives per Article 17",
            "technical": "New attention mechanism, trained on 2M samples"
        },
        {
            "title": "Security Patch: Update Authentication Library",
            "description": "Critical security update for OAuth2 library",
            "type": ChangeType.SECURITY_PATCH,
            "priority": ChangePriority.CRITICAL,
            "systems": ["auth-service", "api-gateway"],
            "justification": "Address CVE-2026-1234 vulnerability",
            "technical": "Update oauth2-lib from v3.2 to v3.3.1"
        },
        {
            "title": "Add Explainability Dashboard Feature",
            "description": "New dashboard for AI decision explanations per Article 13",
            "type": ChangeType.FEATURE_ADDITION,
            "priority": ChangePriority.MEDIUM,
            "systems": ["frontend", "explainability-service"],
            "justification": "EU AI Act Article 13 transparency requirements",
            "technical": "React dashboard with SHAP value visualizations"
        }
    ]
    
    for config in changes_config:
        change = cms.create_change_request(
            title=config["title"],
            description=config["description"],
            change_type=config["type"],
            priority=config["priority"],
            requester="demo-user@company.com",
            affected_systems=config["systems"],
            business_justification=config["justification"],
            technical_details=config["technical"],
            target_deployment_date="2026-02-15"
        )
        change_ids.append(change.change_id)
        print_success(f"Created: {change.change_id}")
        print_info(f"  Title: {change.title}")
        print_info(f"  Type: {change.change_type}, Priority: {change.priority}")
    
    print(f"\n✓ Total changes created: {len(change_ids)}")
    
    # ========================================================================
    # DEMO 2: AI Impact Assessment
    # ========================================================================
    print_section("DEMO 2: AI-Powered Impact Assessment")
    
    for change_id in change_ids:
        assessment = cms.assess_impact(change_id)
        print_success(f"Assessment complete: {change_id}")
        print_info(f"  Risk Level: {assessment.risk_level.upper()}")
        print_info(f"  Affected Components: {len(assessment.affected_components)}")
        print_info(f"  Rollback Complexity: {assessment.rollback_complexity}")
        print_info(f"  AI Confidence: {assessment.confidence_score:.0%}")
        print_info(f"  Testing Requirements: {', '.join(assessment.testing_requirements)}")
        print()
    
    # ========================================================================
    # DEMO 3: Rollback Plan Generation
    # ========================================================================
    print_section("DEMO 3: Automated Rollback Plan Generation")
    
    for change_id in change_ids:
        plan = cms.create_rollback_plan(change_id)
        print_success(f"Rollback plan created: {change_id}")
        print_info(f"  Steps: {len(plan['rollback_steps'])}")
        print_info(f"  Estimated Duration: {plan['estimated_duration_minutes']} minutes")
        print_info(f"  Automated: {'Yes' if plan['automated'] else 'No'}")
        print_info(f"  Sample steps:")
        for i, step in enumerate(plan['rollback_steps'][:3], 1):
            print_info(f"    {i}. {step}")
        print()
    
    # ========================================================================
    # DEMO 4: Automated Testing
    # ========================================================================
    print_section("DEMO 4: Automated Testing")
    
    test_suites = ["quick", "standard", "comprehensive"]
    
    for i, change_id in enumerate(change_ids):
        suite = test_suites[i % len(test_suites)]
        print_info(f"Running '{suite}' test suite on {change_id}...")
        
        results = cms.run_automated_tests(change_id, suite)
        passed = sum(1 for r in results if r.passed)
        
        print_success(f"Tests complete: {passed}/{len(results)} passed")
        for result in results:
            status = "✓ PASS" if result.passed else "✗ FAIL"
            print_info(f"  {status} - {result.test_name} ({result.duration_seconds:.1f}s)")
        print()
    
    # ========================================================================
    # DEMO 5: Approval Workflow
    # ========================================================================
    print_section("DEMO 5: Approval Workflow")
    
    approvers = [
        ("compliance-officer@company.com", "Article 17 compliance review"),
        ("security-team@company.com", "Security impact assessment"),
        ("tech-lead@company.com", "Technical review")
    ]
    
    for i, change_id in enumerate(change_ids):
        approver, notes = approvers[i]
        
        # Request approval
        cms.request_approval(change_id, approver, notes)
        print_info(f"Approval requested from {approver}")
        
        # Approve (or reject one)
        if i < 2:
            cms.approve_change(change_id, approver, f"Approved - {notes} complete")
            print_success(f"Change approved: {change_id}")
        else:
            cms.reject_change(change_id, approver, "Requires additional security testing")
            print_info(f"Change rejected: {change_id}")
        print()
    
    # ========================================================================
    # DEMO 6: Deployment
    # ========================================================================
    print_section("DEMO 6: Change Deployment")
    
    approved_changes = []
    for change_id in change_ids:
        status = cms.get_change_status(change_id)
        if status["status"] == "approved":
            approved_changes.append(change_id)
    
    print_info(f"Deploying {len(approved_changes)} approved changes...")
    print()
    
    for change_id in approved_changes:
        deployment = cms.deploy_change(change_id, "ops-team@company.com")
        print_info(f"Deployment started: {change_id}")
        
        cms.complete_deployment(change_id, success=True, 
                               notes="Deployment successful. All health checks passed.")
        print_success(f"Deployment complete: {change_id}")
        print()
    
    # ========================================================================
    # DEMO 7: Rollback
    # ========================================================================
    print_section("DEMO 7: Rollback Execution")
    
    if approved_changes:
        rollback_change = approved_changes[0]
        print_info(f"Simulating performance issue with {rollback_change}...")
        print_info("⚠ Performance degradation detected - initiating rollback")
        print()
        
        rollback_result = cms.rollback_change(
            rollback_change,
            "ops-team@company.com",
            "Performance degradation: 95th percentile latency increased by 200ms"
        )
        
        print_success(f"Rollback complete: {rollback_change}")
        print_info(f"  Steps completed: {len(rollback_result['steps_completed'])}")
        print_info(f"  Status: {rollback_result['status']}")
        print_info(f"  Reason: {rollback_result['reason']}")
        print()
    
    # ========================================================================
    # DEMO 8: Statistics and Reporting
    # ========================================================================
    print_section("DEMO 8: Statistics and Reporting")
    
    all_changes = cms.list_changes()
    
    stats = {
        "total": len(all_changes),
        "by_status": {},
        "by_priority": {},
        "by_type": {}
    }
    
    for change in all_changes:
        stats["by_status"][change["status"]] = stats["by_status"].get(change["status"], 0) + 1
        stats["by_priority"][change["priority"]] = stats["by_priority"].get(change["priority"], 0) + 1
        stats["by_type"][change["change_type"]] = stats["by_type"].get(change["change_type"], 0) + 1
    
    print_info("Change Management Statistics:")
    print()
    
    print_info("By Status:")
    for status, count in sorted(stats["by_status"].items()):
        print_info(f"  {status.replace('_', ' ').title()}: {count}")
    
    print()
    print_info("By Priority:")
    for priority, count in sorted(stats["by_priority"].items()):
        print_info(f"  {priority.upper()}: {count}")
    
    print()
    print_info("By Type:")
    for change_type, count in sorted(stats["by_type"].items()):
        print_info(f"  {change_type.replace('_', ' ').title()}: {count}")
    
    # ========================================================================
    # DEMO 9: Detailed Status Tracking
    # ========================================================================
    print_section("DEMO 9: Detailed Status Tracking")
    
    print_info("Change Status Overview:")
    print()
    
    for change_id in change_ids:
        status = cms.get_change_status(change_id)
        print_info(f"Change: {change_id}")
        print_info(f"  Title: {status['title'][:60]}...")
        print_info(f"  Status: {status['status'].replace('_', ' ').title()}")
        print_info(f"  Priority: {status['priority'].upper()}")
        print_info(f"  Tests: {status['tests_passed']}/{status['tests_run']} passed")
        print_info(f"  Approvals: {status['approvals_granted']} granted, {status['approvals_pending']} pending")
        print_info(f"  Rollback Plan: {'Ready' if status['rollback_plan_ready'] else 'Not Ready'}")
        print_info(f"  Deployments: {status['deployment_attempts']}")
        print()
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print_section("DEMO COMPLETE - SUMMARY")
    
    print_success("All Change Management Features Demonstrated:")
    print()
    print_info("✓ Change request creation (3 different types)")
    print_info("✓ AI-powered impact assessment (with fallback)")
    print_info("✓ Automated rollback plan generation")
    print_info("✓ Automated testing (multiple test suites)")
    print_info("✓ Multi-approver workflow (approval & rejection)")
    print_info("✓ Change deployment")
    print_info("✓ Rollback execution")
    print_info("✓ Statistics and reporting")
    print_info("✓ Detailed status tracking")
    print()
    print_info("EU AI Act Compliance:")
    print_info("✓ Article 17: Quality Management System")
    print_info("✓ Article 43: Conformity Assessment")
    print()
    print_info(f"Data stored in: {cms.storage_dir}")
    print_info(f"Total changes processed: {len(all_changes)}")
    print()
    
    # Show sample change data
    print_section("SAMPLE CHANGE REQUEST DATA")
    sample_change = cms._load_change(change_ids[0])
    print(json.dumps({
        "change_id": sample_change.change_id,
        "title": sample_change.title,
        "status": sample_change.status,
        "priority": sample_change.priority,
        "impact_assessment": {
            "risk_level": sample_change.impact_assessment["risk_level"],
            "confidence": sample_change.impact_assessment["confidence_score"]
        } if sample_change.impact_assessment else None,
        "tests_run": len(sample_change.test_results),
        "approvals": len(sample_change.approvals),
        "rollback_plan_ready": sample_change.rollback_plan is not None
    }, indent=2))
    
    print("\n" + "=" * 80)
    print("  ✓ DEMO COMPLETED SUCCESSFULLY")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
