"""
Test Suite for ReAct and Resilience Systems v3.0

High Standard: 100% test pass rate
Tests all components with comprehensive coverage:
- ReActAgent (reasoning, acting)
- ActionExecutor (action execution)
- CircuitBreaker (fault isolation)
- RetryHandler (retry logic)
- Bulkhead (resource isolation)
- ResilienceManager (unified resilience)
"""

import sys
import time
from datetime import datetime

from react_system import (
    ReActAgent,
    ActionExecutor,
    Thought,
    Action,
    Observation,
    ReActStep,
    ReActResult,
    StepType,
    ActionStatus,
    create_action_executor,
    create_react_agent,
)

from resilience_system import (
    ResilienceManager,
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerOpenError,
    Bulkhead,
    BulkheadFullError,
    RetryHandler,
    RetryPolicy,
    FallbackHandler,
    HealthStatus,
    CircuitState,
    RetryStrategy,
    create_retry_policy,
    create_circuit_breaker,
    create_bulkhead,
    create_resilience_manager,
)


# ============================================================================
# ReAct System Tests
# ============================================================================

def test_step_type_enum():
    """Test StepType enum"""
    print("Testing StepType...")
    assert StepType.THOUGHT.name == "THOUGHT"
    assert StepType.ACTION.name == "ACTION"
    assert StepType.OBSERVATION.name == "OBSERVATION"
    print("  [OK] StepType tests passed")
    return True


def test_action_status_enum():
    """Test ActionStatus enum"""
    print("Testing ActionStatus...")
    assert ActionStatus.PENDING.name == "PENDING"
    assert ActionStatus.SUCCESS.name == "SUCCESS"
    assert ActionStatus.FAILED.name == "FAILED"
    print("  [OK] ActionStatus tests passed")
    return True


def test_thought():
    """Test Thought data class"""
    print("Testing Thought...")
    thought = Thought(content="Test thought", step_number=1, timestamp=datetime.now())
    data = thought.to_dict()
    assert data["type"] == "thought"
    assert data["content"] == "Test thought"
    print("  [OK] Thought tests passed")
    return True


def test_action():
    """Test Action data class"""
    print("Testing Action...")
    action = Action(name="test", parameters={}, step_number=1, timestamp=datetime.now())
    data = action.to_dict()
    assert data["type"] == "action"
    assert data["name"] == "test"
    print("  [OK] Action tests passed")
    return True


def test_observation():
    """Test Observation data class"""
    print("Testing Observation...")
    obs = Observation(content="Result", step_number=1, timestamp=datetime.now())
    data = obs.to_dict()
    assert data["type"] == "observation"
    assert data["content"] == "Result"
    print("  [OK] Observation tests passed")
    return True


def test_action_executor():
    """Test ActionExecutor"""
    print("Testing ActionExecutor...")
    executor = ActionExecutor()
    
    def test_func(x):
        return x * 2
    
    executor.register_action("double", test_func)
    
    action = Action(name="double", parameters={"x": 5}, step_number=1, timestamp=datetime.now())
    result = executor.execute(action)
    
    assert result.status == ActionStatus.SUCCESS
    assert result.result == 10
    print("  [OK] ActionExecutor tests passed")
    return True


def test_react_agent_think():
    """Test ReActAgent think"""
    print("Testing ReActAgent Think...")
    agent = create_react_agent()
    
    thought = agent.think("I need to solve this")
    
    assert thought.content == "I need to solve this"
    assert thought.step_number == 1
    
    thoughts = agent.get_thoughts()
    assert len(thoughts) == 1
    print("  [OK] ReActAgent think tests passed")
    return True


def test_react_agent_act():
    """Test ReActAgent act"""
    print("Testing ReActAgent Act...")
    agent = create_react_agent()
    
    def multiply(x, y):
        return x * y
    
    agent.executor.register_action("multiply", multiply)
    action = agent.act("multiply", x=3, y=4)
    
    assert action.name == "multiply"
    assert action.status == ActionStatus.SUCCESS
    assert action.result == 12
    print("  [OK] ReActAgent act tests passed")
    return True


def test_react_agent_observe():
    """Test ReActAgent observe"""
    print("Testing ReActAgent Observe...")
    agent = create_react_agent()
    
    obs = agent.observe("The result is 42")
    
    assert obs.content == "The result is 42"
    assert obs.step_number == 1
    
    observations = agent.get_observations()
    assert len(observations) == 1
    print("  [OK] ReActAgent observe tests passed")
    return True


def test_react_agent_run():
    """Test ReActAgent run"""
    print("Testing ReActAgent Run...")
    agent = create_react_agent(max_steps=3)
    
    result = agent.run("What is 2+2?")
    
    assert isinstance(result, ReActResult)
    assert result.success is True
    assert result.total_steps > 0
    print("  [OK] ReActAgent run tests passed")
    return True


# ============================================================================
# Resilience System Tests
# ============================================================================

def test_circuit_state_enum():
    """Test CircuitState enum"""
    print("Testing CircuitState...")
    assert CircuitState.CLOSED.name == "CLOSED"
    assert CircuitState.OPEN.name == "OPEN"
    assert CircuitState.HALF_OPEN.name == "HALF_OPEN"
    print("  [OK] CircuitState tests passed")
    return True


def test_retry_strategy_enum():
    """Test RetryStrategy enum"""
    print("Testing RetryStrategy...")
    assert RetryStrategy.FIXED.name == "FIXED"
    assert RetryStrategy.EXPONENTIAL.name == "EXPONENTIAL"
    print("  [OK] RetryStrategy tests passed")
    return True


def test_retry_policy():
    """Test RetryPolicy"""
    print("Testing RetryPolicy...")
    policy = RetryPolicy(max_retries=3, base_delay=1.0, strategy=RetryStrategy.EXPONENTIAL)
    
    assert policy.calculate_delay(0) == 1.0
    assert policy.calculate_delay(1) == 2.0
    assert policy.calculate_delay(2) == 4.0
    print("  [OK] RetryPolicy tests passed")
    return True


def test_retry_handler():
    """Test RetryHandler"""
    print("Testing RetryHandler...")
    
    call_count = 0
    def flaky_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Failed")
        return "success"
    
    handler = RetryHandler(RetryPolicy(max_retries=5, base_delay=0.01))
    result, attempts = handler.execute(flaky_func)
    
    assert result == "success"
    assert attempts == 2  # 0-indexed, so 2 means 3rd attempt
    print("  [OK] RetryHandler tests passed")
    return True


def test_circuit_breaker_creation():
    """Test CircuitBreaker creation"""
    print("Testing CircuitBreaker Creation...")
    cb = create_circuit_breaker(name="test", failure_threshold=3)
    
    assert cb.name == "test"
    assert cb.get_state() == CircuitState.CLOSED
    print("  [OK] CircuitBreaker creation tests passed")
    return True


def test_circuit_breaker_success():
    """Test CircuitBreaker success"""
    print("Testing CircuitBreaker Success...")
    cb = create_circuit_breaker(failure_threshold=3)
    
    def success_func():
        return "ok"
    
    result = cb.call(success_func)
    assert result == "ok"
    assert cb.get_state() == CircuitState.CLOSED
    print("  [OK] CircuitBreaker success tests passed")
    return True


def test_circuit_breaker_failure():
    """Test CircuitBreaker failure"""
    print("Testing CircuitBreaker Failure...")
    cb = create_circuit_breaker(failure_threshold=2)
    
    def fail_func():
        raise ValueError("Error")
    
    # First failure
    try:
        cb.call(fail_func)
    except ValueError:
        pass
    
    assert cb.get_state() == CircuitState.CLOSED
    
    # Second failure - should open
    try:
        cb.call(fail_func)
    except ValueError:
        pass
    
    assert cb.get_state() == CircuitState.OPEN
    print("  [OK] CircuitBreaker failure tests passed")
    return True


def test_circuit_breaker_open():
    """Test CircuitBreaker open state"""
    print("Testing CircuitBreaker Open...")
    cb = create_circuit_breaker(failure_threshold=1)
    
    def fail_func():
        raise ValueError("Error")
    
    # Trigger open
    try:
        cb.call(fail_func)
    except ValueError:
        pass
    
    assert cb.get_state() == CircuitState.OPEN
    
    # Next call should fail immediately
    try:
        cb.call(lambda: "should not run")
        assert False, "Should have raised CircuitBreakerOpenError"
    except CircuitBreakerOpenError:
        pass
    
    print("  [OK] CircuitBreaker open tests passed")
    return True


def test_circuit_breaker_reset():
    """Test CircuitBreaker reset"""
    print("Testing CircuitBreaker Reset...")
    cb = create_circuit_breaker(failure_threshold=1)
    
    def fail_func():
        raise ValueError("Error")
    
    try:
        cb.call(fail_func)
    except ValueError:
        pass
    
    assert cb.get_state() == CircuitState.OPEN
    
    cb.reset()
    assert cb.get_state() == CircuitState.CLOSED
    print("  [OK] CircuitBreaker reset tests passed")
    return True


def test_bulkhead():
    """Test Bulkhead"""
    print("Testing Bulkhead...")
    bh = create_bulkhead(max_concurrent=2)
    
    def slow_func():
        time.sleep(0.01)
        return "done"
    
    result = bh.execute(slow_func)
    assert result == "done"
    
    stats = bh.get_stats()
    assert stats["max_concurrent"] == 2
    print("  [OK] Bulkhead tests passed")
    return True


def test_fallback_handler():
    """Test FallbackHandler"""
    print("Testing FallbackHandler...")
    handler = FallbackHandler()
    
    def fail_func():
        raise ValueError("Error")
    
    def fallback_func():
        return "fallback"
    
    # Register fallback
    handler.register("my_fallback", fallback_func)
    
    result = handler.execute(fail_func, fallback_name="my_fallback")
    assert result == "fallback"
    
    # Test with default
    result = handler.execute(fail_func, default="default_value")
    assert result == "default_value"
    print("  [OK] FallbackHandler tests passed")
    return True


def test_resilience_manager():
    """Test ResilienceManager"""
    print("Testing ResilienceManager...")
    manager = create_resilience_manager()
    
    def success_func():
        return "success"
    
    result = manager.with_retry(success_func)
    assert result == "success"
    
    health = manager.get_health()
    assert health.healthy is True
    print("  [OK] ResilienceManager tests passed")
    return True


def test_factory_functions():
    """Test factory functions"""
    print("Testing Factory Functions...")
    
    # ReAct
    executor = create_action_executor()
    assert isinstance(executor, ActionExecutor)
    
    agent = create_react_agent(max_steps=5)
    assert isinstance(agent, ReActAgent)
    assert agent.max_steps == 5
    
    # Resilience
    policy = create_retry_policy(max_retries=5)
    assert isinstance(policy, RetryPolicy)
    assert policy.max_retries == 5
    
    cb = create_circuit_breaker(name="test_cb")
    assert isinstance(cb, CircuitBreaker)
    
    bh = create_bulkhead(max_concurrent=5)
    assert isinstance(bh, Bulkhead)
    
    manager = create_resilience_manager()
    assert isinstance(manager, ResilienceManager)
    
    print("  [OK] Factory functions tests passed")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("ReAct & Resilience Systems v3.0 - Test Suite")
    print("High Standard: 100% Pass Rate")
    print("=" * 60)
    
    tests = [
        # ReAct
        test_step_type_enum,
        test_action_status_enum,
        test_thought,
        test_action,
        test_observation,
        test_action_executor,
        test_react_agent_think,
        test_react_agent_act,
        test_react_agent_observe,
        test_react_agent_run,
        # Resilience
        test_circuit_state_enum,
        test_retry_strategy_enum,
        test_retry_policy,
        test_retry_handler,
        test_circuit_breaker_creation,
        test_circuit_breaker_success,
        test_circuit_breaker_failure,
        test_circuit_breaker_open,
        test_circuit_breaker_reset,
        test_bulkhead,
        test_fallback_handler,
        test_resilience_manager,
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
