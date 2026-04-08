"""
Test Suite for Self-Evolution System v4.0

Tests all components:
- PerformanceAnalyzer
- ExperienceLibrary
- StrategyEvolver
- SelfEvolvingAgent
"""

import pytest
import tempfile
from datetime import datetime
from pathlib import Path

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
    create_self_evolving_agent,
    evolve_from_mistake,
    evolve_from_success,
)


class TestPerformanceAnalyzer:
    """Test PerformanceAnalyzer"""
    
    def test_initialization(self):
        analyzer = PerformanceAnalyzer()
        assert analyzer.metrics_history == []
        assert analyzer.baseline is None
    
    def test_record_metrics(self):
        analyzer = PerformanceAnalyzer()
        metrics = PerformanceMetrics(
            execution_time_ms=100,
            memory_usage_mb=50,
            cpu_usage_percent=30,
            quality_score=8.5,
            success_rate=0.95,
            error_count=0,
            warning_count=1,
        )
        analyzer.record_metrics(metrics)
        assert len(analyzer.metrics_history) == 1
        assert analyzer.trends["quality_score"] == [8.5]
    
    def test_set_baseline(self):
        analyzer = PerformanceAnalyzer()
        baseline = PerformanceMetrics(
            execution_time_ms=100,
            memory_usage_mb=50,
            cpu_usage_percent=30,
            quality_score=8.0,
            success_rate=0.9,
            error_count=0,
            warning_count=0,
        )
        analyzer.set_baseline(baseline)
        assert analyzer.baseline == baseline
    
    def test_analyze_performance_insufficient_data(self):
        analyzer = PerformanceAnalyzer()
        result = analyzer.analyze_performance()
        assert result["status"] == "insufficient_data"
    
    def test_analyze_performance_with_data(self):
        analyzer = PerformanceAnalyzer()
        for i in range(15):
            metrics = PerformanceMetrics(
                execution_time_ms=100 + i * 10,
                memory_usage_mb=50,
                cpu_usage_percent=30,
                quality_score=8.0 + i * 0.1,
                success_rate=0.9,
                error_count=0,
                warning_count=0,
            )
            analyzer.record_metrics(metrics)
        
        result = analyzer.analyze_performance()
        assert result["status"] == "analyzed"
        assert "trends" in result
        assert "bottlenecks" in result
    
    def test_get_performance_score(self):
        analyzer = PerformanceAnalyzer()
        # No data
        assert analyzer.get_performance_score() == 5.0
        
        # With data
        for _ in range(10):
            analyzer.record_metrics(PerformanceMetrics(
                execution_time_ms=100,
                memory_usage_mb=50,
                cpu_usage_percent=30,
                quality_score=9.0,
                success_rate=0.95,
                error_count=0,
                warning_count=0,
            ))
        
        score = analyzer.get_performance_score()
        assert 8.0 < score <= 10.0


class TestExperienceLibrary:
    """Test ExperienceLibrary"""
    
    def test_initialization(self):
        lib = ExperienceLibrary()
        assert lib.experiences == {}
        assert lib.storage_path is None
    
    def test_add_experience(self):
        lib = ExperienceLibrary()
        exp = Experience(
            id="test_1",
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
            context={},
            lessons_learned=["Test lesson"],
        )
        lib.add_experience(exp)
        assert len(lib.experiences) == 1
        assert "coding" in lib.task_type_index
    
    def test_get_experience(self):
        lib = ExperienceLibrary()
        exp = Experience(
            id="test_1",
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
            context={},
            lessons_learned=[],
        )
        lib.add_experience(exp)
        retrieved = lib.get_experience("test_1")
        assert retrieved == exp
    
    def test_find_similar_experiences(self):
        lib = ExperienceLibrary()
        
        # Add multiple experiences
        for i in range(5):
            exp = Experience(
                id=f"test_{i}",
                timestamp=datetime.now(),
                task_type="coding",
                strategy_used="default",
                outcome=TaskOutcome.SUCCESS if i % 2 == 0 else TaskOutcome.FAILURE,
                metrics=PerformanceMetrics(
                    execution_time_ms=100,
                    memory_usage_mb=50,
                    cpu_usage_percent=30,
                    quality_score=8.0 + i,
                    success_rate=1.0 if i % 2 == 0 else 0.0,
                    error_count=0,
                    warning_count=0,
                ),
                context={},
                lessons_learned=[],
            )
            lib.add_experience(exp)
        
        # Find all coding experiences
        results = lib.find_similar_experiences("coding")
        assert len(results) == 5
        
        # Find successful coding experiences
        results = lib.find_similar_experiences("coding", outcome=TaskOutcome.SUCCESS)
        assert len(results) == 3
    
    def test_get_lessons_for_task(self):
        lib = ExperienceLibrary()
        
        exp1 = Experience(
            id="test_1",
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
            context={},
            lessons_learned=["Lesson 1", "Lesson 2"],
        )
        lib.add_experience(exp1)
        
        lessons = lib.get_lessons_for_task("coding")
        assert "Lesson 1" in lessons
        assert "Lesson 2" in lessons
    
    def test_get_successful_strategies(self):
        lib = ExperienceLibrary()
        
        # Add experiences with different strategies
        strategies = ["aggressive", "conservative", "aggressive"]
        for i, strat in enumerate(strategies):
            exp = Experience(
                id=f"test_{i}",
                timestamp=datetime.now(),
                task_type="coding",
                strategy_used=strat,
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
        
        successful = lib.get_successful_strategies("coding")
        assert "aggressive" in successful
        assert "conservative" in successful
    
    def test_persistence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = Path(tmpdir) / "experiences.json"
            
            # Create and save
            lib = ExperienceLibrary(str(storage_path))
            exp = Experience(
                id="test_1",
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
                context={},
                lessons_learned=["Test"],
            )
            lib.add_experience(exp)
            
            # Load
            lib2 = ExperienceLibrary(str(storage_path))
            assert len(lib2.experiences) == 1
            assert lib2.get_experience("test_1") is not None


class TestStrategyEvolver:
    """Test StrategyEvolver"""
    
    def test_initialization(self):
        lib = ExperienceLibrary()
        evolver = StrategyEvolver(lib)
        assert evolver.strategies == {}
        assert evolver.active_strategy is None
    
    def test_register_strategy(self):
        lib = ExperienceLibrary()
        evolver = StrategyEvolver(lib)
        
        strategy = Strategy(
            id="test_strat",
            name="Test Strategy",
            description="A test strategy",
            strategy_type=EvolutionStrategy.INCREMENTAL,
            parameters={"param1": 1.0},
        )
        evolver.register_strategy(strategy)
        assert "test_strat" in evolver.strategies
    
    def test_select_best_strategy(self):
        lib = ExperienceLibrary()
        evolver = StrategyEvolver(lib)
        
        # Register strategies
        strat1 = Strategy(
            id="strat1",
            name="Strategy 1",
            description="First strategy",
            strategy_type=EvolutionStrategy.INCREMENTAL,
            parameters={},
            success_rate=0.9,
        )
        strat2 = Strategy(
            id="strat2",
            name="Strategy 2",
            description="Second strategy",
            strategy_type=EvolutionStrategy.RADICAL,
            parameters={},
            success_rate=0.5,
        )
        evolver.register_strategy(strat1)
        evolver.register_strategy(strat2)
        
        # Add experiences
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
        
        best = evolver.select_best_strategy("coding")
        assert best is not None
        assert best.id == "strat1"
    
    def test_create_new_strategy(self):
        lib = ExperienceLibrary()
        evolver = StrategyEvolver(lib)
        
        strategy = evolver.create_new_strategy(
            name="New Strategy",
            description="A new strategy",
            strategy_type=EvolutionStrategy.ADAPTIVE,
            parameters={"adaptation_rate": 0.1},
        )
        
        assert strategy.name == "New Strategy"
        assert strategy.strategy_type == EvolutionStrategy.ADAPTIVE
        assert strategy.id in evolver.strategies


class TestSelfEvolvingAgent:
    """Test SelfEvolvingAgent"""
    
    def test_initialization(self):
        agent = SelfEvolvingAgent()
        assert agent.current_task is None
        assert agent.current_strategy is None
        assert len(agent.strategy_evolver.strategies) >= 3  # Default strategies
    
    def test_start_task(self):
        agent = SelfEvolvingAgent()
        result = agent.start_task("coding", {"language": "python"})
        
        assert result["task_type"] == "coding"
        assert "selected_strategy" in result
        assert "lessons_from_past" in result
        assert agent.current_task == "coding"
    
    def test_end_task_success(self):
        agent = SelfEvolvingAgent()
        agent.start_task("coding")
        
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
            lessons_learned=["This works"],
        )
        
        assert result["outcome"] == "SUCCESS"
        assert result["experience_recorded"] is True
        assert agent.current_task is None
    
    def test_end_task_failure(self):
        agent = SelfEvolvingAgent()
        agent.start_task("coding")
        
        result = agent.end_task(
            outcome=TaskOutcome.FAILURE,
            metrics=PerformanceMetrics(
                execution_time_ms=100,
                memory_usage_mb=50,
                cpu_usage_percent=30,
                quality_score=3.0,
                success_rate=0.0,
                error_count=1,
                warning_count=0,
            ),
            lessons_learned=["This doesn't work"],
        )
        
        assert result["outcome"] == "FAILURE"
        assert result["experience_recorded"] is True
    
    def test_get_evolution_status(self):
        agent = SelfEvolvingAgent()
        status = agent.get_evolution_status()
        
        assert "experience_count" in status
        assert "strategy_count" in status
        assert "performance_score" in status
    
    def test_analyze_performance(self):
        agent = SelfEvolvingAgent()
        
        # Add some experiences
        for i in range(15):
            agent.start_task("coding")
            agent.end_task(
                outcome=TaskOutcome.SUCCESS,
                metrics=PerformanceMetrics(
                    execution_time_ms=100 + i * 10,
                    memory_usage_mb=50,
                    cpu_usage_percent=30,
                    quality_score=8.0 + i * 0.1,
                    success_rate=1.0,
                    error_count=0,
                    warning_count=0,
                ),
                lessons_learned=[],
            )
        
        analysis = agent.analyze_performance()
        assert analysis["status"] == "analyzed"


class TestHelperFunctions:
    """Test helper functions"""
    
    def test_create_self_evolving_agent(self):
        agent = create_self_evolving_agent()
        assert isinstance(agent, SelfEvolvingAgent)
    
    def test_evolve_from_mistake(self):
        agent = create_self_evolving_agent()
        result = evolve_from_mistake(
            agent,
            task_type="coding",
            error="Syntax error",
            context={"file": "test.py"},
        )
        
        assert result["outcome"] == "FAILURE"
        assert result["experience_recorded"] is True
    
    def test_evolve_from_success(self):
        agent = create_self_evolving_agent()
        result = evolve_from_success(
            agent,
            task_type="coding",
            quality_score=9.5,
            context={"file": "test.py"},
        )
        
        assert result["outcome"] == "SUCCESS"
        assert result["experience_recorded"] is True


class TestDataClasses:
    """Test data class serialization"""
    
    def test_experience_serialization(self):
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
        
        assert restored.id == exp.id
        assert restored.task_type == exp.task_type
        assert restored.outcome == exp.outcome
    
    def test_strategy_serialization(self):
        strategy = Strategy(
            id="test",
            name="Test",
            description="Test strategy",
            strategy_type=EvolutionStrategy.INCREMENTAL,
            parameters={"param": 1.0},
        )
        
        data = strategy.to_dict()
        restored = Strategy.from_dict(data)
        
        assert restored.id == strategy.id
        assert restored.name == strategy.name
        assert restored.strategy_type == strategy.strategy_type
    
    def test_metrics_serialization(self):
        metrics = PerformanceMetrics(
            execution_time_ms=100,
            memory_usage_mb=50,
            cpu_usage_percent=30,
            quality_score=9.0,
            success_rate=1.0,
            error_count=0,
            warning_count=0,
        )
        
        data = metrics.to_dict()
        restored = PerformanceMetrics.from_dict(data)
        
        assert restored.execution_time_ms == metrics.execution_time_ms
        assert restored.quality_score == metrics.quality_score


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
