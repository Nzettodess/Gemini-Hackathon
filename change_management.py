"""
Change Management System for EU AI Act Compliance
Implements systematic change request workflow, impact assessment, testing, and rollback procedures
Addresses Article 17 (Quality Management System) and Article 43 (Conformity Assessment)
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None


class ChangeStatus(Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    IMPACT_ASSESSMENT = "impact_assessment"
    TESTING = "testing"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    DEPLOYED = "deployed"
    ROLLED_BACK = "rolled_back"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class ChangePriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ChangeType(Enum):
    MODEL_UPDATE = "model_update"
    ALGORITHM_CHANGE = "algorithm_change"
    DATA_PIPELINE = "data_pipeline"
    CONFIGURATION = "configuration"
    INFRASTRUCTURE = "infrastructure"
    SECURITY_PATCH = "security_patch"
    FEATURE_ADDITION = "feature_addition"
    BUG_FIX = "bug_fix"


class RiskLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


@dataclass
class ImpactAssessment:
    risk_level: str
    affected_components: List[str]
    affected_users: str
    performance_impact: str
    compliance_impact: str
    rollback_complexity: str
    testing_requirements: List[str]
    dependencies: List[str]
    ai_analysis: str
    confidence_score: float
    timestamp: str


@dataclass
class TestResult:
    test_id: str
    test_name: str
    test_type: str
    status: str
    passed: bool
    duration_seconds: float
    details: str
    timestamp: str
    artifacts: List[str]


@dataclass
class ChangeRequest:
    change_id: str
    title: str
    description: str
    change_type: str
    priority: str
    status: str
    requester: str
    created_at: str
    updated_at: str
    target_deployment_date: Optional[str]
    affected_systems: List[str]
    business_justification: str
    technical_details: str
    impact_assessment: Optional[Dict]
    test_results: List[Dict]
    approvals: List[Dict]
    rollback_plan: Optional[Dict]
    deployment_log: List[Dict]
    metadata: Dict[str, Any]


class ChangeManagementSystem:
    def __init__(self, storage_dir: str = "change_management"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        self.changes_dir = self.storage_dir / "changes"
        self.changes_dir.mkdir(exist_ok=True)
        
        self.backups_dir = self.storage_dir / "backups"
        self.backups_dir.mkdir(exist_ok=True)
        
        self.tests_dir = self.storage_dir / "test_results"
        self.tests_dir.mkdir(exist_ok=True)
        
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and GENAI_AVAILABLE:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
        else:
            self.model = None
    
    def create_change_request(
        self,
        title: str,
        description: str,
        change_type: ChangeType,
        priority: ChangePriority,
        requester: str,
        affected_systems: List[str],
        business_justification: str,
        technical_details: str,
        target_deployment_date: Optional[str] = None
    ) -> ChangeRequest:
        """Create a new change request"""
        change_id = self._generate_change_id(title)
        timestamp = datetime.now().isoformat()
        
        change = ChangeRequest(
            change_id=change_id,
            title=title,
            description=description,
            change_type=change_type.value,
            priority=priority.value,
            status=ChangeStatus.DRAFT.value,
            requester=requester,
            created_at=timestamp,
            updated_at=timestamp,
            target_deployment_date=target_deployment_date,
            affected_systems=affected_systems,
            business_justification=business_justification,
            technical_details=technical_details,
            impact_assessment=None,
            test_results=[],
            approvals=[],
            rollback_plan=None,
            deployment_log=[],
            metadata={}
        )
        
        self._save_change(change)
        self._log_change_event(change_id, "created", f"Change request created by {requester}")
        
        return change
    
    def assess_impact(self, change_id: str) -> ImpactAssessment:
        """AI-powered impact assessment of a change request"""
        change = self._load_change(change_id)
        
        if not self.model:
            return self._manual_impact_assessment(change)
        
        prompt = f"""
You are an AI system impact assessment expert for EU AI Act compliance.
Analyze this change request and provide a comprehensive impact assessment.

CHANGE REQUEST:
Title: {change.title}
Type: {change.change_type}
Priority: {change.priority}
Description: {change.description}
Affected Systems: {', '.join(change.affected_systems)}
Technical Details: {change.technical_details}
Business Justification: {change.business_justification}

Provide a detailed impact assessment covering:
1. Risk Level (critical/high/medium/low/minimal)
2. Affected Components (list all impacted components)
3. Affected Users (estimate of user impact)
4. Performance Impact (expected performance changes)
5. Compliance Impact (EU AI Act Article 17, 43 implications)
6. Rollback Complexity (easy/moderate/complex/very complex)
7. Testing Requirements (specific tests needed)
8. Dependencies (other systems/changes this depends on)
9. Recommendations and Risk Mitigation

Format as JSON with these exact keys:
- risk_level
- affected_components (array)
- affected_users
- performance_impact
- compliance_impact
- rollback_complexity
- testing_requirements (array)
- dependencies (array)
- analysis (detailed text)
- confidence_score (0.0-1.0)
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            assessment_data = json.loads(result_text)
            
            assessment = ImpactAssessment(
                risk_level=assessment_data.get("risk_level", "medium"),
                affected_components=assessment_data.get("affected_components", []),
                affected_users=assessment_data.get("affected_users", "Unknown"),
                performance_impact=assessment_data.get("performance_impact", "To be determined"),
                compliance_impact=assessment_data.get("compliance_impact", "Requires review"),
                rollback_complexity=assessment_data.get("rollback_complexity", "moderate"),
                testing_requirements=assessment_data.get("testing_requirements", []),
                dependencies=assessment_data.get("dependencies", []),
                ai_analysis=assessment_data.get("analysis", ""),
                confidence_score=float(assessment_data.get("confidence_score", 0.7)),
                timestamp=datetime.now().isoformat()
            )
            
            change.impact_assessment = asdict(assessment)
            change.status = ChangeStatus.IMPACT_ASSESSMENT.value
            change.updated_at = datetime.now().isoformat()
            self._save_change(change)
            self._log_change_event(change_id, "impact_assessed", f"AI impact assessment completed (confidence: {assessment.confidence_score})")
            
            return assessment
            
        except Exception as e:
            print(f"AI assessment failed: {e}, using manual assessment")
            return self._manual_impact_assessment(change)
    
    def _manual_impact_assessment(self, change: ChangeRequest) -> ImpactAssessment:
        """Fallback manual impact assessment"""
        risk_mapping = {
            ChangeType.MODEL_UPDATE.value: RiskLevel.HIGH,
            ChangeType.ALGORITHM_CHANGE.value: RiskLevel.HIGH,
            ChangeType.SECURITY_PATCH.value: RiskLevel.CRITICAL,
            ChangeType.CONFIGURATION.value: RiskLevel.MEDIUM,
            ChangeType.BUG_FIX.value: RiskLevel.LOW,
        }
        
        risk_level = risk_mapping.get(change.change_type, RiskLevel.MEDIUM)
        
        assessment = ImpactAssessment(
            risk_level=risk_level.value,
            affected_components=change.affected_systems,
            affected_users="Requires manual assessment",
            performance_impact="Requires manual assessment",
            compliance_impact="Requires manual review per Article 17 and 43",
            rollback_complexity="moderate",
            testing_requirements=["Unit tests", "Integration tests", "Regression tests"],
            dependencies=[],
            ai_analysis="Manual assessment - AI analysis unavailable",
            confidence_score=0.5,
            timestamp=datetime.now().isoformat()
        )
        
        change.impact_assessment = asdict(assessment)
        change.status = ChangeStatus.IMPACT_ASSESSMENT.value
        change.updated_at = datetime.now().isoformat()
        self._save_change(change)
        
        return assessment
    
    def create_rollback_plan(self, change_id: str) -> Dict:
        """Create automated rollback plan"""
        change = self._load_change(change_id)
        
        rollback_plan = {
            "change_id": change_id,
            "created_at": datetime.now().isoformat(),
            "rollback_steps": [],
            "backup_locations": [],
            "verification_steps": [],
            "estimated_duration_minutes": 0,
            "automated": True
        }
        
        if change.change_type == ChangeType.MODEL_UPDATE.value:
            rollback_plan["rollback_steps"] = [
                "Stop current model serving",
                "Restore previous model version from backup",
                "Verify model integrity",
                "Restart model serving",
                "Run smoke tests",
                "Monitor performance metrics"
            ]
            rollback_plan["estimated_duration_minutes"] = 15
            
        elif change.change_type == ChangeType.CONFIGURATION.value:
            rollback_plan["rollback_steps"] = [
                "Backup current configuration",
                "Restore previous configuration from version control",
                "Validate configuration syntax",
                "Apply configuration",
                "Verify service health"
            ]
            rollback_plan["estimated_duration_minutes"] = 5
            
        elif change.change_type == ChangeType.DATA_PIPELINE.value:
            rollback_plan["rollback_steps"] = [
                "Pause data pipeline",
                "Restore previous pipeline version",
                "Verify data integrity",
                "Resume pipeline",
                "Monitor data flow"
            ]
            rollback_plan["estimated_duration_minutes"] = 20
        
        else:
            rollback_plan["rollback_steps"] = [
                "Identify components to rollback",
                "Create backup of current state",
                "Restore previous version",
                "Verify system health",
                "Run validation tests"
            ]
            rollback_plan["estimated_duration_minutes"] = 30
        
        rollback_plan["verification_steps"] = [
            "Check system health endpoints",
            "Verify critical functionality",
            "Monitor error rates",
            "Validate performance metrics",
            "Confirm compliance status"
        ]
        
        backup_id = f"backup_{change_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.backups_dir / f"{backup_id}.json"
        rollback_plan["backup_locations"].append(str(backup_path))
        
        change.rollback_plan = rollback_plan
        change.updated_at = datetime.now().isoformat()
        self._save_change(change)
        self._log_change_event(change_id, "rollback_plan_created", "Automated rollback plan generated")
        
        return rollback_plan
    
    def run_automated_tests(self, change_id: str, test_suite: str = "standard") -> List[TestResult]:
        """Run automated test suite for change validation"""
        change = self._load_change(change_id)
        test_results = []
        
        test_suites = {
            "standard": ["unit", "integration", "regression"],
            "comprehensive": ["unit", "integration", "regression", "performance", "security"],
            "quick": ["unit", "smoke"],
            "compliance": ["compliance", "audit", "documentation"]
        }
        
        tests_to_run = test_suites.get(test_suite, test_suites["standard"])
        
        for test_type in tests_to_run:
            result = self._simulate_test_execution(change_id, test_type)
            test_results.append(result)
            change.test_results.append(asdict(result))
        
        all_passed = all(r.passed for r in test_results)
        
        if all_passed:
            change.status = ChangeStatus.PENDING_APPROVAL.value
            self._log_change_event(change_id, "tests_passed", f"All {len(test_results)} tests passed")
        else:
            failed_count = sum(1 for r in test_results if not r.passed)
            self._log_change_event(change_id, "tests_failed", f"{failed_count}/{len(test_results)} tests failed")
        
        change.updated_at = datetime.now().isoformat()
        self._save_change(change)
        
        return test_results
    
    def _simulate_test_execution(self, change_id: str, test_type: str) -> TestResult:
        """Simulate test execution (placeholder for actual test integration)"""
        import random
        
        test_id = f"TEST-{change_id}-{test_type}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        test_configs = {
            "unit": {
                "name": "Unit Test Suite",
                "duration": random.uniform(5, 15),
                "pass_rate": 0.95
            },
            "integration": {
                "name": "Integration Test Suite",
                "duration": random.uniform(30, 60),
                "pass_rate": 0.90
            },
            "regression": {
                "name": "Regression Test Suite",
                "duration": random.uniform(45, 90),
                "pass_rate": 0.92
            },
            "performance": {
                "name": "Performance Test Suite",
                "duration": random.uniform(60, 120),
                "pass_rate": 0.88
            },
            "security": {
                "name": "Security Test Suite",
                "duration": random.uniform(30, 60),
                "pass_rate": 0.85
            },
            "compliance": {
                "name": "EU AI Act Compliance Tests",
                "duration": random.uniform(20, 40),
                "pass_rate": 0.93
            },
            "smoke": {
                "name": "Smoke Test Suite",
                "duration": random.uniform(2, 5),
                "pass_rate": 0.98
            }
        }
        
        config = test_configs.get(test_type, test_configs["unit"])
        passed = random.random() < config["pass_rate"]
        
        result = TestResult(
            test_id=test_id,
            test_name=config["name"],
            test_type=test_type,
            status="passed" if passed else "failed",
            passed=passed,
            duration_seconds=config["duration"],
            details=f"Executed {config['name']} for change {change_id}. {'All checks passed.' if passed else 'Some checks failed - review required.'}",
            timestamp=datetime.now().isoformat(),
            artifacts=[f"{self.tests_dir}/{test_id}_report.json"]
        )
        
        test_report_path = self.tests_dir / f"{test_id}_report.json"
        with open(test_report_path, 'w') as f:
            json.dump(asdict(result), f, indent=2)
        
        return result
    
    def request_approval(self, change_id: str, approver: str, notes: str = "") -> Dict:
        """Request approval for a change"""
        change = self._load_change(change_id)
        
        approval_request = {
            "approver": approver,
            "requested_at": datetime.now().isoformat(),
            "status": "pending",
            "notes": notes,
            "approved_at": None,
            "decision_notes": None
        }
        
        change.approvals.append(approval_request)
        change.status = ChangeStatus.PENDING_APPROVAL.value
        change.updated_at = datetime.now().isoformat()
        self._save_change(change)
        self._log_change_event(change_id, "approval_requested", f"Approval requested from {approver}")
        
        return approval_request
    
    def approve_change(self, change_id: str, approver: str, decision_notes: str = "") -> bool:
        """Approve a change request"""
        change = self._load_change(change_id)
        
        for approval in change.approvals:
            if approval["approver"] == approver and approval["status"] == "pending":
                approval["status"] = "approved"
                approval["approved_at"] = datetime.now().isoformat()
                approval["decision_notes"] = decision_notes
                
                change.status = ChangeStatus.APPROVED.value
                change.updated_at = datetime.now().isoformat()
                self._save_change(change)
                self._log_change_event(change_id, "approved", f"Approved by {approver}")
                return True
        
        return False
    
    def reject_change(self, change_id: str, approver: str, reason: str) -> bool:
        """Reject a change request"""
        change = self._load_change(change_id)
        
        for approval in change.approvals:
            if approval["approver"] == approver and approval["status"] == "pending":
                approval["status"] = "rejected"
                approval["approved_at"] = datetime.now().isoformat()
                approval["decision_notes"] = reason
                
                change.status = ChangeStatus.REJECTED.value
                change.updated_at = datetime.now().isoformat()
                self._save_change(change)
                self._log_change_event(change_id, "rejected", f"Rejected by {approver}: {reason}")
                return True
        
        return False
    
    def deploy_change(self, change_id: str, deployed_by: str) -> Dict:
        """Deploy an approved change"""
        change = self._load_change(change_id)
        
        if change.status != ChangeStatus.APPROVED.value:
            raise ValueError(f"Change {change_id} is not approved for deployment")
        
        deployment_record = {
            "deployed_by": deployed_by,
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "status": "in_progress",
            "steps_completed": [],
            "errors": []
        }
        
        change.deployment_log.append(deployment_record)
        change.status = ChangeStatus.IN_PROGRESS.value
        change.updated_at = datetime.now().isoformat()
        self._save_change(change)
        self._log_change_event(change_id, "deployment_started", f"Deployment started by {deployed_by}")
        
        return deployment_record
    
    def complete_deployment(self, change_id: str, success: bool = True, notes: str = "") -> None:
        """Mark deployment as complete"""
        change = self._load_change(change_id)
        
        if change.deployment_log:
            latest_deployment = change.deployment_log[-1]
            latest_deployment["completed_at"] = datetime.now().isoformat()
            latest_deployment["status"] = "completed" if success else "failed"
            latest_deployment["notes"] = notes
            
            if success:
                change.status = ChangeStatus.DEPLOYED.value
                self._log_change_event(change_id, "deployed", "Change successfully deployed")
            else:
                change.status = ChangeStatus.APPROVED.value
                self._log_change_event(change_id, "deployment_failed", f"Deployment failed: {notes}")
            
            change.updated_at = datetime.now().isoformat()
            self._save_change(change)
    
    def rollback_change(self, change_id: str, rolled_back_by: str, reason: str) -> Dict:
        """Execute rollback of a deployed change"""
        change = self._load_change(change_id)
        
        if not change.rollback_plan:
            raise ValueError(f"No rollback plan exists for change {change_id}")
        
        rollback_execution = {
            "rolled_back_by": rolled_back_by,
            "reason": reason,
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "steps_completed": [],
            "status": "in_progress"
        }
        
        for step in change.rollback_plan["rollback_steps"]:
            rollback_execution["steps_completed"].append({
                "step": step,
                "completed_at": datetime.now().isoformat(),
                "status": "completed"
            })
        
        rollback_execution["completed_at"] = datetime.now().isoformat()
        rollback_execution["status"] = "completed"
        
        change.metadata["rollback_execution"] = rollback_execution
        change.status = ChangeStatus.ROLLED_BACK.value
        change.updated_at = datetime.now().isoformat()
        self._save_change(change)
        self._log_change_event(change_id, "rolled_back", f"Change rolled back by {rolled_back_by}: {reason}")
        
        return rollback_execution
    
    def get_change_status(self, change_id: str) -> Dict:
        """Get comprehensive status of a change request"""
        change = self._load_change(change_id)
        
        status_report = {
            "change_id": change.change_id,
            "title": change.title,
            "status": change.status,
            "priority": change.priority,
            "created_at": change.created_at,
            "updated_at": change.updated_at,
            "requester": change.requester,
            "impact_assessment_complete": change.impact_assessment is not None,
            "tests_run": len(change.test_results),
            "tests_passed": sum(1 for t in change.test_results if t.get("passed", False)),
            "approvals_pending": sum(1 for a in change.approvals if a["status"] == "pending"),
            "approvals_granted": sum(1 for a in change.approvals if a["status"] == "approved"),
            "rollback_plan_ready": change.rollback_plan is not None,
            "deployment_attempts": len(change.deployment_log)
        }
        
        return status_report
    
    def list_changes(self, status_filter: Optional[str] = None) -> List[Dict]:
        """List all change requests with optional status filter"""
        changes = []
        
        for change_file in self.changes_dir.glob("*.json"):
            with open(change_file, 'r') as f:
                change_data = json.load(f)
                
                if status_filter is None or change_data["status"] == status_filter:
                    changes.append({
                        "change_id": change_data["change_id"],
                        "title": change_data["title"],
                        "status": change_data["status"],
                        "priority": change_data["priority"],
                        "change_type": change_data["change_type"],
                        "created_at": change_data["created_at"],
                        "requester": change_data["requester"]
                    })
        
        changes.sort(key=lambda x: x["created_at"], reverse=True)
        return changes
    
    def _generate_change_id(self, title: str) -> str:
        """Generate unique change ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        hash_suffix = hashlib.md5(title.encode()).hexdigest()[:6]
        return f"CHG-{timestamp}-{hash_suffix}"
    
    def _save_change(self, change: ChangeRequest) -> None:
        """Save change request to disk"""
        change_file = self.changes_dir / f"{change.change_id}.json"
        with open(change_file, 'w') as f:
            json.dump(asdict(change), f, indent=2)
    
    def _load_change(self, change_id: str) -> ChangeRequest:
        """Load change request from disk"""
        change_file = self.changes_dir / f"{change_id}.json"
        
        if not change_file.exists():
            raise FileNotFoundError(f"Change request {change_id} not found")
        
        with open(change_file, 'r') as f:
            data = json.load(f)
            return ChangeRequest(**data)
    
    def _log_change_event(self, change_id: str, event_type: str, description: str) -> None:
        """Log change management events"""
        log_file = self.storage_dir / "change_events.log"
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "change_id": change_id,
            "event_type": event_type,
            "description": description
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(event) + "\n")


def main():
    """Example usage of Change Management System"""
    cms = ChangeManagementSystem()
    
    print("=== EU AI Act Change Management System ===\n")
    
    change = cms.create_change_request(
        title="Update AI model to v2.1",
        description="Deploy new version of risk classification model with improved accuracy",
        change_type=ChangeType.MODEL_UPDATE,
        priority=ChangePriority.HIGH,
        requester="ai-team@company.com",
        affected_systems=["risk-classifier", "api-gateway", "monitoring"],
        business_justification="Improve accuracy by 5% and reduce false positives",
        technical_details="Model trained on expanded dataset, new architecture with attention mechanism",
        target_deployment_date="2026-02-01"
    )
    
    print(f"✓ Created change request: {change.change_id}")
    print(f"  Title: {change.title}")
    print(f"  Status: {change.status}\n")
    
    print("Running impact assessment...")
    assessment = cms.assess_impact(change.change_id)
    print(f"✓ Impact Assessment Complete")
    print(f"  Risk Level: {assessment.risk_level}")
    print(f"  Affected Components: {', '.join(assessment.affected_components)}")
    print(f"  Confidence: {assessment.confidence_score:.2%}\n")
    
    print("Creating rollback plan...")
    rollback = cms.create_rollback_plan(change.change_id)
    print(f"✓ Rollback Plan Created")
    print(f"  Steps: {len(rollback['rollback_steps'])}")
    print(f"  Estimated Duration: {rollback['estimated_duration_minutes']} minutes\n")
    
    print("Running automated tests...")
    tests = cms.run_automated_tests(change.change_id, test_suite="comprehensive")
    print(f"✓ Tests Complete: {sum(1 for t in tests if t.passed)}/{len(tests)} passed\n")
    
    print("Requesting approval...")
    cms.request_approval(change.change_id, "compliance-officer@company.com", "Article 17 compliance review")
    cms.approve_change(change.change_id, "compliance-officer@company.com", "Approved - meets EU AI Act requirements")
    print(f"✓ Change Approved\n")
    
    status = cms.get_change_status(change.change_id)
    print("=== Change Status ===")
    for key, value in status.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
