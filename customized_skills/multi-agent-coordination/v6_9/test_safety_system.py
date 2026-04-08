"""
Test Suite for Safety System v5.0

High Standard: 100% test pass rate
Tests all safety components with comprehensive coverage:
- BackupManager (git-based backup/restore)
- CircuitBreaker (fault tolerance)
- SafetyContext (operation tracking)
- SafetyMonitor (system health)
"""

import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

from safety_system import (
    BackupManager,
    CircuitBreaker,
    CircuitBreakerConfig,
    SafetyContext,
    SafetyMonitor,
    OperationRecord,
    BackupPoint,
    CircuitState,
    OperationStatus,
    SafetyLevel,
    CircuitBreakerOpenError,
    create_safety_system,
    create_circuit_breaker,
)


def test_circuit_breaker_config():
    """Test CircuitBreakerConfig"""
    print("Testing CircuitBreakerConfig...")
    
    config = CircuitBreakerConfig(
        failure_threshold=3,
        recovery_timeout=10.0,
        half_open_max_calls=2,
        success_threshold=1,
    )
    
    assert config.failure_threshold == 3
    assert config.recovery_timeout == 10.0
    
    data = config.to_dict()
    assert data["failure_threshold"] == 3
    
    print("  [OK] CircuitBreakerConfig tests passed")
    return True


def test_circuit_breaker_initial_state():
    """Test circuit breaker initial state"""
    print("Testing CircuitBreaker Initial State...")
    
    cb = CircuitBreaker("test")
    
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0
    assert cb.name == "test"
    
    status = cb.get_status()
    assert status["state"] == "CLOSED"
    
    print("  [OK] CircuitBreaker initial state tests passed")
    return True


def test_circuit_breaker_success():
    """Test circuit breaker with successful calls"""
    print("Testing CircuitBreaker Success...")
    
    cb = CircuitBreaker("test")
    
    # Successful calls should work
    result = cb.call(lambda: 42)
    assert result == 42
    
    result = cb.call(lambda x: x * 2, 21)
    assert result == 42
    
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0
    
    print("  [OK] CircuitBreaker success tests passed")
    return True


def test_circuit_breaker_failure():
    """Test circuit breaker failure handling"""
    print("Testing CircuitBreaker Failure...")
    
    cb = CircuitBreaker("test", CircuitBreakerConfig(failure_threshold=3))
    
    # Record failures
    for i in range(3):
        try:
            cb.call(lambda: 1/0)
        except ZeroDivisionError:
            pass
    
    # Circuit should be open
    assert cb.state == CircuitState.OPEN
    assert cb.failure_count == 3
    
    # Next call should fail immediately
    try:
        cb.call(lambda: 42)
        assert False, "Should have raised CircuitBreakerOpenError"
    except CircuitBreakerOpenError:
        pass
    
    print("  [OK] CircuitBreaker failure tests passed")
    return True


def test_circuit_breaker_recovery():
    """Test circuit breaker recovery"""
    print("Testing CircuitBreaker Recovery...")
    
    cb = CircuitBreaker("test", CircuitBreakerConfig(
        failure_threshold=2,
        recovery_timeout=0.1,  # Short timeout for testing
    ))
    
    # Open the circuit
    for _ in range(2):
        try:
            cb.call(lambda: 1/0)
        except ZeroDivisionError:
            pass
    
    assert cb.state == CircuitState.OPEN
    
    # Wait for recovery timeout
    time.sleep(0.15)
    
    # Should transition to half-open and allow call
    result = cb.call(lambda: 42)
    assert result == 42
    assert cb.state == CircuitState.HALF_OPEN
    
    print("  [OK] CircuitBreaker recovery tests passed")
    return True


def test_circuit_breaker_reset():
    """Test circuit breaker manual reset"""
    print("Testing CircuitBreaker Reset...")
    
    cb = CircuitBreaker("test", CircuitBreakerConfig(failure_threshold=2))
    
    # Open the circuit
    for _ in range(2):
        try:
            cb.call(lambda: 1/0)
        except ZeroDivisionError:
            pass
    
    assert cb.state == CircuitState.OPEN
    
    # Reset
    cb.reset()
    
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0
    
    # Should work again
    result = cb.call(lambda: 42)
    assert result == 42
    
    print("  [OK] CircuitBreaker reset tests passed")
    return True


def test_circuit_breaker_callbacks():
    """Test circuit breaker callbacks"""
    print("Testing CircuitBreaker Callbacks...")
    
    cb = CircuitBreaker("test", CircuitBreakerConfig(failure_threshold=2))
    
    state_changes = []
    failures = []
    
    def on_state_change(old, new):
        state_changes.append((old, new))
    
    def on_failure(error):
        failures.append(error)
    
    cb.on_state_change(on_state_change)
    cb.on_failure(on_failure)
    
    # Trigger failures
    for _ in range(2):
        try:
            cb.call(lambda: 1/0)
        except ZeroDivisionError:
            pass
    
    assert len(failures) == 2
    assert len(state_changes) == 1
    assert state_changes[0] == (CircuitState.CLOSED, CircuitState.OPEN)
    
    print("  [OK] CircuitBreaker callbacks tests passed")
    return True


def test_backup_manager_creation():
    """Test BackupManager creation"""
    print("Testing BackupManager Creation...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = BackupManager(tmpdir)
        
        assert manager.repo_path == Path(tmpdir)
        assert manager.backup_points == []
    
    print("  [OK] BackupManager creation tests passed")
    return True


def test_backup_manager_git_check():
    """Test BackupManager git availability check"""
    print("Testing BackupManager Git Check...")
    
    manager = BackupManager()
    
    # Should detect git availability
    assert isinstance(manager._git_available, bool)
    
    print("  [OK] BackupManager git check tests passed")
    return True


def test_safety_context_creation():
    """Test SafetyContext creation"""
    print("Testing SafetyContext Creation...")
    
    context = SafetyContext()
    
    assert context.operations == {}
    assert context.active_operations == set()
    
    print("  [OK] SafetyContext creation tests passed")
    return True


def test_safety_context_operation():
    """Test SafetyContext operation lifecycle"""
    print("Testing SafetyContext Operation...")
    
    context = SafetyContext()
    
    # Start operation
    record = context.start_operation(
        name="Test Operation",
        safety_level=SafetyLevel.LOW,
        create_backup=False,
    )
    
    assert record.name == "Test Operation"
    assert record.status == OperationStatus.IN_PROGRESS
    assert record.id in context.active_operations
    
    # Complete operation
    completed = context.complete_operation(record.id, success=True)
    
    assert completed.status == OperationStatus.SUCCESS
    assert completed.id not in context.active_operations
    assert completed.completed_at is not None
    
    print("  [OK] SafetyContext operation tests passed")
    return True


def test_safety_context_failed_operation():
    """Test SafetyContext failed operation"""
    print("Testing SafetyContext Failed Operation...")
    
    context = SafetyContext()
    
    # Start and fail operation
    record = context.start_operation(
        name="Failing Operation",
        safety_level=SafetyLevel.LOW,
        create_backup=False,
    )
    
    completed = context.complete_operation(
        record.id,
        success=False,
        error_message="Something went wrong"
    )
    
    assert completed.status == OperationStatus.FAILED
    assert completed.error_message == "Something went wrong"
    
    print("  [OK] SafetyContext failed operation tests passed")
    return True


def test_safety_context_query():
    """Test SafetyContext query operations"""
    print("Testing SafetyContext Query...")
    
    context = SafetyContext()
    
    # Create multiple operations
    op1 = context.start_operation("Op 1", SafetyLevel.LOW, False)
    context.complete_operation(op1.id, success=True)
    
    op2 = context.start_operation("Op 2", SafetyLevel.LOW, False)
    context.complete_operation(op2.id, success=False)
    
    op3 = context.start_operation("Op 3", SafetyLevel.LOW, False)
    # Leave active
    
    # Query tests
    assert len(context.get_active_operations()) == 1
    assert len(context.get_operations_by_status(OperationStatus.SUCCESS)) == 1
    assert len(context.get_operations_by_status(OperationStatus.FAILED)) == 1
    
    # Get operation by ID
    retrieved = context.get_operation(op1.id)
    assert retrieved.name == "Op 1"
    
    print("  [OK] SafetyContext query tests passed")
    return True


def test_safety_context_summary():
    """Test SafetyContext summary"""
    print("Testing SafetyContext Summary...")
    
    context = SafetyContext()
    
    # Create operations with different statuses
    op1 = context.start_operation("Op 1", SafetyLevel.LOW, False)
    context.complete_operation(op1.id, success=True)
    
    op2 = context.start_operation("Op 2", SafetyLevel.LOW, False)
    context.complete_operation(op2.id, success=False)
    
    summary = context.get_safety_summary()
    
    assert summary["total_operations"] == 2
    assert summary["successful"] == 1
    assert summary["failed"] == 1
    assert summary["success_rate"] == 0.5
    
    print("  [OK] SafetyContext summary tests passed")
    return True


def test_safety_monitor():
    """Test SafetyMonitor"""
    print("Testing SafetyMonitor...")
    
    monitor = SafetyMonitor()
    
    # Register circuit breaker
    cb = CircuitBreaker("test")
    monitor.register_circuit_breaker(cb)
    
    assert "test" in monitor.circuit_breakers
    
    # Register safety context
    context = SafetyContext()
    monitor.register_safety_context("default", context)
    
    assert "default" in monitor.safety_contexts
    
    # Get system health
    health = monitor.get_system_health()
    
    assert "health_score" in health
    assert "status" in health
    assert health["status"] == "HEALTHY"
    
    print("  [OK] SafetyMonitor tests passed")
    return True


def test_safety_monitor_alerts():
    """Test SafetyMonitor alerts"""
    print("Testing SafetyMonitor Alerts...")
    
    monitor = SafetyMonitor()
    
    # Register circuit breaker that will open
    cb = CircuitBreaker("test", CircuitBreakerConfig(failure_threshold=1))
    monitor.register_circuit_breaker(cb)
    
    # Trigger failure to open circuit
    try:
        cb.call(lambda: 1/0)
    except ZeroDivisionError:
        pass
    
    # Should have recorded an alert
    assert len(monitor.alerts) >= 1
    assert monitor.alerts[-1]["level"] == "WARNING"
    assert "opened" in monitor.alerts[-1]["message"]
    
    print("  [OK] SafetyMonitor alerts tests passed")
    return True


def test_safety_monitor_health_degraded():
    """Test SafetyMonitor health degradation"""
    print("Testing SafetyMonitor Health Degraded...")
    
    monitor = SafetyMonitor()
    
    # Create context with failures
    context = SafetyContext()
    
    # Add many failed operations
    for i in range(10):
        op = context.start_operation(f"Op {i}", SafetyLevel.LOW, False)
        context.complete_operation(op.id, success=(i < 3))  # 70% failure rate
    
    monitor.register_safety_context("test", context)
    
    # Add open circuit breaker
    cb = CircuitBreaker("failing", CircuitBreakerConfig(failure_threshold=1))
    try:
        cb.call(lambda: 1/0)
    except ZeroDivisionError:
        pass
    monitor.register_circuit_breaker(cb)
    
    health = monitor.get_system_health()
    
    assert health["health_score"] < 100
    assert health["failed_operations"] == 7
    assert "failing" in health["open_circuit_breakers"]
    
    print("  [OK] SafetyMonitor health degraded tests passed")
    return True


def test_factory_functions():
    """Test factory functions"""
    print("Testing Factory Functions...")
    
    # Test create_circuit_breaker
    cb = create_circuit_breaker("factory_test", failure_threshold=5)
    assert cb.name == "factory_test"
    assert cb.config.failure_threshold == 5
    
    # Test create_safety_system
    context, monitor = create_safety_system()
    assert isinstance(context, SafetyContext)
    assert isinstance(monitor, SafetyMonitor)
    
    print("  [OK] Factory functions tests passed")
    return True


def test_safety_levels():
    """Test SafetyLevel enum"""
    print("Testing SafetyLevel...")
    
    assert SafetyLevel.LOW.name == "LOW"
    assert SafetyLevel.MEDIUM.name == "MEDIUM"
    assert SafetyLevel.HIGH.name == "HIGH"
    assert SafetyLevel.CRITICAL.name == "CRITICAL"
    
    print("  [OK] SafetyLevel tests passed")
    return True


def test_circuit_states():
    """Test CircuitState enum"""
    print("Testing CircuitState...")
    
    assert CircuitState.CLOSED.name == "CLOSED"
    assert CircuitState.OPEN.name == "OPEN"
    assert CircuitState.HALF_OPEN.name == "HALF_OPEN"
    
    print("  [OK] CircuitState tests passed")
    return True


def test_operation_status():
    """Test OperationStatus enum"""
    print("Testing OperationStatus...")
    
    assert OperationStatus.PENDING.name == "PENDING"
    assert OperationStatus.IN_PROGRESS.name == "IN_PROGRESS"
    assert OperationStatus.SUCCESS.name == "SUCCESS"
    assert OperationStatus.FAILED.name == "FAILED"
    assert OperationStatus.ROLLED_BACK.name == "ROLLED_BACK"
    
    print("  [OK] OperationStatus tests passed")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Safety System v5.0 - Test Suite")
    print("High Standard: 100% Pass Rate")
    print("=" * 60)
    
    tests = [
        test_circuit_breaker_config,
        test_circuit_breaker_initial_state,
        test_circuit_breaker_success,
        test_circuit_breaker_failure,
        test_circuit_breaker_recovery,
        test_circuit_breaker_reset,
        test_circuit_breaker_callbacks,
        test_backup_manager_creation,
        test_backup_manager_git_check,
        test_safety_context_creation,
        test_safety_context_operation,
        test_safety_context_failed_operation,
        test_safety_context_query,
        test_safety_context_summary,
        test_safety_monitor,
        test_safety_monitor_alerts,
        test_safety_monitor_health_degraded,
        test_factory_functions,
        test_safety_levels,
        test_circuit_states,
        test_operation_status,
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
