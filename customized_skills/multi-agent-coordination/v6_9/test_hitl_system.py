"""
Test Suite for HITL System v2.0

High Standard: 100% test pass rate
Tests all components with comprehensive coverage:
- HumanApprovalManager (approvals, timeouts)
- FeedbackCollector (feedback collection)
- ApprovalWorkflow (multi-stage workflows)
"""

import sys
import time
from datetime import datetime

from hitl_system import (
    HumanApprovalManager,
    FeedbackCollector,
    ApprovalWorkflow,
    ApprovalRequest,
    HumanFeedback,
    InteractiveTask,
    ApprovalLevel,
    ApprovalStatus,
    FeedbackType,
    create_approval_manager,
    create_feedback_collector,
    create_approval_workflow,
)


def test_approval_level_enum():
    """Test ApprovalLevel enum"""
    print("Testing ApprovalLevel...")
    
    assert ApprovalLevel.AUTO.name == "AUTO"
    assert ApprovalLevel.REQUIRE.name == "REQUIRE"
    assert ApprovalLevel.STRICT.name == "STRICT"
    
    print("  [OK] ApprovalLevel tests passed")
    return True


def test_approval_status_enum():
    """Test ApprovalStatus enum"""
    print("Testing ApprovalStatus...")
    
    assert ApprovalStatus.PENDING.name == "PENDING"
    assert ApprovalStatus.APPROVED.name == "APPROVED"
    assert ApprovalStatus.REJECTED.name == "REJECTED"
    
    print("  [OK] ApprovalStatus tests passed")
    return True


def test_feedback_type_enum():
    """Test FeedbackType enum"""
    print("Testing FeedbackType...")
    
    assert FeedbackType.APPROVAL.name == "APPROVAL"
    assert FeedbackType.CORRECTION.name == "CORRECTION"
    
    print("  [OK] FeedbackType tests passed")
    return True


def test_approval_request():
    """Test ApprovalRequest data class"""
    print("Testing ApprovalRequest...")
    
    request = ApprovalRequest(
        id="req_1",
        task_id="task_1",
        description="Test request",
        level=ApprovalLevel.REQUIRE,
        context={},
        requested_at=datetime.now(),
        timeout_seconds=300.0,
    )
    
    data = request.to_dict()
    assert data["id"] == "req_1"
    assert data["status"] == "PENDING"
    
    print("  [OK] ApprovalRequest tests passed")
    return True


def test_human_feedback():
    """Test HumanFeedback data class"""
    print("Testing HumanFeedback...")
    
    feedback = HumanFeedback(
        id="fb_1",
        task_id="task_1",
        type=FeedbackType.APPROVAL,
        content="Looks good",
        provided_by="user",
        provided_at=datetime.now(),
    )
    
    data = feedback.to_dict()
    assert data["type"] == "APPROVAL"
    assert data["content"] == "Looks good"
    
    print("  [OK] HumanFeedback tests passed")
    return True


def test_interactive_task():
    """Test InteractiveTask data class"""
    print("Testing InteractiveTask...")
    
    task = InteractiveTask(
        id="task_1",
        name="Test Task",
        description="A test task",
        approval_level=ApprovalLevel.REQUIRE,
        context={},
        created_at=datetime.now(),
    )
    
    data = task.to_dict()
    assert data["name"] == "Test Task"
    assert data["status"] == "pending"
    
    print("  [OK] InteractiveTask tests passed")
    return True


def test_approval_manager_creation():
    """Test HumanApprovalManager creation"""
    print("Testing HumanApprovalManager Creation...")
    
    manager = HumanApprovalManager(default_timeout=60.0)
    assert manager.default_timeout == 60.0
    
    print("  [OK] HumanApprovalManager creation tests passed")
    return True


def test_approval_manager_request():
    """Test HumanApprovalManager request"""
    print("Testing HumanApprovalManager Request...")
    
    manager = HumanApprovalManager()
    request = manager.request_approval(
        task_id="task_1",
        description="Test approval",
        level=ApprovalLevel.REQUIRE,
    )
    
    assert request.task_id == "task_1"
    assert request.status == ApprovalStatus.PENDING
    assert request.id is not None
    
    print("  [OK] HumanApprovalManager request tests passed")
    return True


def test_approval_manager_auto_approve():
    """Test HumanApprovalManager auto-approve"""
    print("Testing HumanApprovalManager Auto-Approve...")
    
    manager = HumanApprovalManager(auto_approve_levels={ApprovalLevel.AUTO})
    request = manager.request_approval(
        task_id="task_1",
        description="Auto approval test",
        level=ApprovalLevel.AUTO,
    )
    
    # Should be auto-approved
    assert request.status == ApprovalStatus.APPROVED
    
    print("  [OK] HumanApprovalManager auto-approve tests passed")
    return True


def test_approval_manager_approve():
    """Test HumanApprovalManager approve"""
    print("Testing HumanApprovalManager Approve...")
    
    manager = HumanApprovalManager()
    request = manager.request_approval(
        task_id="task_1",
        description="Test",
        level=ApprovalLevel.REQUIRE,
    )
    
    success = manager.approve(request.id, "Approved by test")
    assert success is True
    
    # Check status
    updated = manager.get_request(request.id)
    assert updated.status == ApprovalStatus.APPROVED
    assert updated.response == "Approved by test"
    
    print("  [OK] HumanApprovalManager approve tests passed")
    return True


def test_approval_manager_reject():
    """Test HumanApprovalManager reject"""
    print("Testing HumanApprovalManager Reject...")
    
    manager = HumanApprovalManager()
    request = manager.request_approval(
        task_id="task_1",
        description="Test",
        level=ApprovalLevel.REQUIRE,
    )
    
    success = manager.reject(request.id, "Rejected by test")
    assert success is True
    
    updated = manager.get_request(request.id)
    assert updated.status == ApprovalStatus.REJECTED
    
    print("  [OK] HumanApprovalManager reject tests passed")
    return True


def test_approval_manager_cancel():
    """Test HumanApprovalManager cancel"""
    print("Testing HumanApprovalManager Cancel...")
    
    manager = HumanApprovalManager()
    request = manager.request_approval(
        task_id="task_1",
        description="Test",
        level=ApprovalLevel.REQUIRE,
    )
    
    success = manager.cancel(request.id)
    assert success is True
    
    updated = manager.get_request(request.id)
    assert updated.status == ApprovalStatus.CANCELLED
    
    print("  [OK] HumanApprovalManager cancel tests passed")
    return True


def test_approval_manager_timeout():
    """Test HumanApprovalManager timeout"""
    print("Testing HumanApprovalManager Timeout...")
    
    manager = HumanApprovalManager()
    request = manager.request_approval(
        task_id="task_1",
        description="Test",
        level=ApprovalLevel.REQUIRE,
        timeout_seconds=0.01,  # Very short timeout
    )
    
    # Wait for timeout
    time.sleep(0.02)
    
    timed_out = manager.check_timeout(request.id)
    assert timed_out is True
    
    updated = manager.get_request(request.id)
    assert updated.status == ApprovalStatus.TIMEOUT
    
    print("  [OK] HumanApprovalManager timeout tests passed")
    return True


def test_approval_manager_pending_requests():
    """Test HumanApprovalManager pending requests"""
    print("Testing HumanApprovalManager Pending Requests...")
    
    manager = HumanApprovalManager()
    
    # Create pending requests
    req1 = manager.request_approval("task_1", "Test 1", ApprovalLevel.REQUIRE)
    req2 = manager.request_approval("task_2", "Test 2", ApprovalLevel.REQUIRE)
    
    pending = manager.get_pending_requests()
    assert len(pending) == 2
    
    # Approve one
    manager.approve(req1.id)
    
    pending = manager.get_pending_requests()
    assert len(pending) == 1
    assert pending[0].id == req2.id
    
    print("  [OK] HumanApprovalManager pending requests tests passed")
    return True


def test_approval_manager_stats():
    """Test HumanApprovalManager statistics"""
    print("Testing HumanApprovalManager Stats...")
    
    manager = HumanApprovalManager()
    
    manager.request_approval("task_1", "Test", ApprovalLevel.REQUIRE)
    req2 = manager.request_approval("task_2", "Test", ApprovalLevel.REQUIRE)
    manager.approve(req2.id)
    
    stats = manager.get_stats()
    assert stats["total_requests"] == 2
    assert stats["pending"] == 1
    assert stats["approved"] == 1
    
    print("  [OK] HumanApprovalManager stats tests passed")
    return True


def test_feedback_collector_creation():
    """Test FeedbackCollector creation"""
    print("Testing FeedbackCollector Creation...")
    
    collector = FeedbackCollector()
    assert collector is not None
    
    print("  [OK] FeedbackCollector creation tests passed")
    return True


def test_feedback_collector_collect():
    """Test FeedbackCollector collect"""
    print("Testing FeedbackCollector Collect...")
    
    collector = FeedbackCollector()
    feedback = collector.collect(
        task_id="task_1",
        feedback_type=FeedbackType.APPROVAL,
        content="Great work!",
        provided_by="user1",
    )
    
    assert feedback.task_id == "task_1"
    assert feedback.type == FeedbackType.APPROVAL
    assert feedback.content == "Great work!"
    
    print("  [OK] FeedbackCollector collect tests passed")
    return True


def test_feedback_collector_get_task_feedback():
    """Test FeedbackCollector get task feedback"""
    print("Testing FeedbackCollector Get Task Feedback...")
    
    collector = FeedbackCollector()
    
    collector.collect("task_1", FeedbackType.APPROVAL, "Good", "user1")
    collector.collect("task_1", FeedbackType.SUGGESTION, "Improve X", "user2")
    collector.collect("task_2", FeedbackType.APPROVAL, "Nice", "user3")
    
    task1_feedback = collector.get_task_feedback("task_1")
    assert len(task1_feedback) == 2
    
    task2_feedback = collector.get_task_feedback("task_2")
    assert len(task2_feedback) == 1
    
    print("  [OK] FeedbackCollector get task feedback tests passed")
    return True


def test_feedback_collector_analyze():
    """Test FeedbackCollector analyze"""
    print("Testing FeedbackCollector Analyze...")
    
    collector = FeedbackCollector()
    
    collector.collect("task_1", FeedbackType.APPROVAL, "Good")
    collector.collect("task_1", FeedbackType.CORRECTION, "Fix this")
    
    analysis = collector.analyze_feedback("task_1")
    assert analysis["count"] == 2
    assert analysis["has_corrections"] is True
    
    print("  [OK] FeedbackCollector analyze tests passed")
    return True


def test_feedback_collector_stats():
    """Test FeedbackCollector statistics"""
    print("Testing FeedbackCollector Stats...")
    
    collector = FeedbackCollector()
    
    collector.collect("task_1", FeedbackType.APPROVAL, "Good")
    collector.collect("task_1", FeedbackType.REJECTION, "Bad")
    
    stats = collector.get_stats()
    assert stats["total_feedback"] == 2
    assert stats["by_type"]["APPROVAL"] == 1
    assert stats["by_type"]["REJECTION"] == 1
    
    print("  [OK] FeedbackCollector stats tests passed")
    return True


def test_approval_workflow_creation():
    """Test ApprovalWorkflow creation"""
    print("Testing ApprovalWorkflow Creation...")
    
    manager = HumanApprovalManager()
    workflow = ApprovalWorkflow(manager)
    
    assert workflow.manager == manager
    
    print("  [OK] ApprovalWorkflow creation tests passed")
    return True


def test_approval_workflow_add_stage():
    """Test ApprovalWorkflow add stage"""
    print("Testing ApprovalWorkflow Add Stage...")
    
    manager = HumanApprovalManager()
    workflow = ApprovalWorkflow(manager)
    
    workflow.add_stage(
        name="Stage 1",
        description="First approval",
        level=ApprovalLevel.REQUIRE,
    ).add_stage(
        name="Stage 2",
        description="Second approval",
        level=ApprovalLevel.SUGGEST,
    )
    
    status = workflow.get_status()
    assert status["total_stages"] == 2
    
    print("  [OK] ApprovalWorkflow add stage tests passed")
    return True


def test_factory_functions():
    """Test factory functions"""
    print("Testing Factory Functions...")
    
    # Approval manager
    manager = create_approval_manager(default_timeout=120.0)
    assert isinstance(manager, HumanApprovalManager)
    assert manager.default_timeout == 120.0
    
    # Feedback collector
    collector = create_feedback_collector()
    assert isinstance(collector, FeedbackCollector)
    
    # Approval workflow
    workflow = create_approval_workflow(manager)
    assert isinstance(workflow, ApprovalWorkflow)
    
    print("  [OK] Factory functions tests passed")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("HITL System v2.0 - Test Suite")
    print("High Standard: 100% Pass Rate")
    print("=" * 60)
    
    tests = [
        test_approval_level_enum,
        test_approval_status_enum,
        test_feedback_type_enum,
        test_approval_request,
        test_human_feedback,
        test_interactive_task,
        test_approval_manager_creation,
        test_approval_manager_request,
        test_approval_manager_auto_approve,
        test_approval_manager_approve,
        test_approval_manager_reject,
        test_approval_manager_cancel,
        test_approval_manager_timeout,
        test_approval_manager_pending_requests,
        test_approval_manager_stats,
        test_feedback_collector_creation,
        test_feedback_collector_collect,
        test_feedback_collector_get_task_feedback,
        test_feedback_collector_analyze,
        test_feedback_collector_stats,
        test_approval_workflow_creation,
        test_approval_workflow_add_stage,
        test_factory_functions,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"  [FAILED] {test.__name__}")
        except Exception as e:
            failed += 1
            print(f"  [FAILED] {test.__name__}: {e}")
    
    print("=" * 60)
    print(f"Results: {passed}/{len(tests)} tests passed ({passed/len(tests)*100:.1f}%)")
    print("=" * 60)
    
    if failed == 0:
        print("[OK] ALL TESTS PASSED - High Standard Achieved!")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
