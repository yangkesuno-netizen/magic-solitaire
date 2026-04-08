"""
Simple test for Self-Evolution System v4.0
No pytest dependency required
"""

import sys
from datetime import datetime

from self_evolution import (
    SelfEvolvingAgent,
    PerformanceAnalyzer,
    ExperienceLibrary,
    StrategyEvolver,
    Experience,
    Strategy,
    PerformanceMetrics,
    EvolutionStrategy,
    TaskOutcome,
)


def test_performance_analyzer():
    """Test PerformanceAnalyzer"""
    print("Testing PerformanceAnalyzer...")
    
    analyzer = PerformanceAnalyzer()
    
    # Test record_metrics
    for i in range(15):
        metrics = PerformanceMetrics(
            execution_time_ms=100 + i * 10,
            memory_usage_mb=50,
            cpu_usage_percent=30,
            quality_score=8.0 + i * 0.1,
            success_rate=0.95,
            error_count=0,
            warning_count=0,
        )
        analyzer.record_metrics(metrics)
    
    # Test analyze_performance
    result = analyzer.analyze_performance()
    assert result["status"] == "analyzed", "Should have analyzed"
    assert "trends" in result, "Should have trends"
    assert "bottlenecks" in result, "Should have bottlenecks"
    
    # Test get_performance_score
    score = analyzer.get_performance_score()
    assert 0 <= score <= 10, f"Score should be 0-10, got {score}"
    
    print(f"  [OK] PerformanceAnalyzer tests passed (score: {score:.2f})")
    return True


def test_experience_library():
    """Test ExperienceLibrary"""
    print("Testing ExperienceLibrary...")
    
    lib = ExperienceLibrary()
    
    # Test add_experience
    for i in range(5):
        exp = Experience(
            id=f"exp_{i}",
            timestamp=datetime.now(),
            task_type="coding",
            strategy_used="default" if i % 2 == 0 else "aggressive",
            outcome=TaskOutcome.SUCCESS if i % 2 == 0 else TaskOutcome.FAILURE,
            metrics=PerformanceMetrics(
                execution_time_ms=100 + i * 10,
                memory_usage_mb=50,
                cpu_usage_percent=30,
                quality_score=8.0 + i,
                success_rate=1.0 if i % 2 == 0 else 0.0,
                error_count=0,
                warning_count=0,
            ),
            context={"test": True},
            lessons_learned=[f"Lesson {i}"],
        )
        lib.add_experience(exp)
    
    assert len(lib.experiences) == 5, "Should have 5 experiences"
    
    # Test get_experience
    exp = lib.get_experience("exp_0")
    assert exp is not None, "Should retrieve experience"
    assert exp.task_type == "coding", "Task type should match"
    
    # Test find_similar_experiences
    results = lib.find_similar_experiences("coding")
    assert len(results) == 5, "Should find all coding experiences"
    
    results = lib.find_similar_experiences("coding", outcome=TaskOutcome.SUCCESS)
    assert len(results) == 3, "Should find 3 successful experiences"
    
    # Test get_lessons_for_task
    lessons = lib.get_lessons_for_task("coding")
    assert len(lessons) == 5, "Should have 5 unique lessons"
    
    # Test get_successful_strategies
    successful = lib.get_successful_strategies("coding")
    assert "default" in successful, "Default should be successful"
    
    # Test get_statistics
    stats = lib.get_statistics()
    assert stats["total_experiences"] == 5, "Should have 5 total"
    
    print("  [OK] ExperienceLibrary tests passed")
    return True


def test_strategy_evolver():
    """Test StrategyEvolver"""
    print("Testing StrategyEvolver...")
    
    lib = ExperienceLibrary()
    evolver = StrategyEvolver(lib)
    
    # Test register_strategy
    strat1 = Strategy(
        id="strat1",
        name="Strategy 1",
        description="First strategy",
        strategy_type=EvolutionStrategy.INCREMENTAL,
        parameters={"param": 1.0},
        success_rate=0.9,
    )
    evolver.register_strategy(strat1)
    assert "strat1" in evolver.strategies, "Should register strategy"
    
    # Test create_new_strategy
    strat2 = evolver.create_new_strategy(
        name="Strategy 2",
        description="Second strategy",
        strategy_type=EvolutionStrategy.ADAPTIVE,
        parameters={"adaptation": 0.1},
    )
    assert strat2.name == "Strategy 2", "Should create strategy"
    
    # Add experiences for strat1
    for i in range(10):
        exp = Experience(
            id=f"exp_{i}",
            timestamp=datetime.now(),
            task_type="coding",
            strategy_used="strat1",
            outcome=TaskOutcome.SUCCESS,
            metrics=PerformanceMetrics(
                execution_time_ms=100,
                memory_usage_mb=50,
                cpu_usage_percent=30,
                quality_score=9.0,
                success_rate=1.0,
                error_count=0,
                warning_count=0,
            ),
            context={},
            lessons_learned=[],
        )
        lib.add_experience(exp)
    
    # Test select_best_strategy
    best = evolver.select_best_strategy("coding")
    assert best is not None, "Should select best strategy"
    assert best.id == "strat1", "Should select strat1"
    
    # Test get_strategy_recommendations
    recs = evolver.get_strategy_recommendations("coding")
    assert len(recs) > 0, "Should have recommendations"
    
    print("  [OK] StrategyEvolver tests passed")
    return True


def test_self_evolving_agent():
    """Test SelfEvolvingAgent"""
    print("Testing SelfEvolvingAgent...")
    
    agent = SelfEvolvingAgent()
    
    # Test start_task
    result = agent.start_task("coding", {"language": "python"})
    assert result["task_type"] == "coding", "Task type should match"
    assert "selected_strategy" in result, "Should select strategy"
    assert agent.current_task == "coding", "Should set current task"
    
    # Test end_task
    result = agent.end_task(
        outcome=TaskOutcome.SUCCESS,
        metrics=PerformanceMetrics(
            execution_time_ms=100,
            memory_usage_mb=50,
            cpu_usage_percent=30,
            quality_score=9.0,
            success_rate=1.0,
            error_count=0,
            warning_count=0,
        ),
        lessons_learned=["This approach works well"],
    )
    assert result["outcome"] == "SUCCESS", "Should record success"
    assert result["experience_recorded"] is True, "Should record experience"
    assert agent.current_task is None, "Should reset task"
    
    # Test multiple tasks for evolution
    for i in range(10):
        agent.start_task("coding")
        agent.end_task(
            outcome=TaskOutcome.SUCCESS if i % 3 != 0 else TaskOutcome.FAILURE,
            metrics=PerformanceMetrics(
                execution_time_ms=100 + i * 5,
                memory_usage_mb=50,
                cpu_usage_percent=30,
                quality_score=8.0 + i * 0.1,
                success_rate=1.0 if i % 3 != 0 else 0.0,
                error_count=0 if i % 3 != 0 else 1,
                warning_count=0,
            ),
            lessons_learned=[f"Lesson {i}"],
        )
    
    # Test get_evolution_status
    status = agent.get_evolution_status()
    assert status["experience_count"] > 0, "Should have experiences"
    assert status["strategy_count"] >= 3, "Should have default strategies"
    assert 0 <= status["performance_score"] <= 10, "Score should be valid"
    
    # Test analyze_performance
    analysis = agent.analyze_performance()
    assert analysis["status"] == "analyzed", "Should analyze performance"
    
    # Test suggest_improvements
    suggestions = agent.suggest_improvements()
    assert isinstance(suggestions, list), "Should return list"
    
    print(f"  [OK] SelfEvolvingAgent tests passed (experiences: {status['experience_count']})")
    return True


def test_data_serialization():
    """Test data class serialization"""
    print("Testing data serialization...")
    
    # Test Experience serialization
    exp = Experience(
        id="test",
        timestamp=datetime.now(),
        task_type="coding",
        strategy_used="default",
        outcome=TaskOutcome.SUCCESS,
        metrics=PerformanceMetrics(
            execution_time_ms=100,
            memory_usage_mb=50,
            cpu_usage_percent=30,
            quality_score=9.0,
            success_rate=1.0,
            error_count=0,
            warning_count=0,
        ),
        context={"key": "value"},
        lessons_learned=["Lesson 1"],
    )
    
    data = exp.to_dict()
    restored = Experience.from_dict(data)
    assert restored.id == exp.id, "Should restore ID"
    assert restored.task_type == exp.task_type, "Should restore task type"
    
    # Test Strategy serialization
    strat = Strategy(
        id="test",
        name="Test",
        description="Test strategy",
        strategy_type=EvolutionStrategy.INCREMENTAL,
        parameters={"param": 1.0},
    )
    
    data = strat.to_dict()
    restored = Strategy.from_dict(data)
    assert restored.name == strat.name, "Should restore name"
    assert restored.strategy_type == strat.strategy_type, "Should restore type"
    
    print("  [OK] Data serialization tests passed")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Self-Evolution System v4.0 - Test Suite")
    print("=" * 60)
    
    tests = [
        test_performance_analyzer,
        test_experience_library,
        test_strategy_evolver,
        test_self_evolving_agent,
        test_data_serialization,
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
    print(f"Results: {passed}/{len(tests)} tests passed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
