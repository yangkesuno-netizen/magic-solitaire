"""
Self-Evolution System v4.0 - Complete Restoration

Core Components:
- SelfEvolvingAgent: Agent that evolves based on experience
- PerformanceAnalyzer: Analyzes task performance
- ExperienceLibrary: Stores and retrieves experiences
- StrategyEvolver: Evolves strategies based on feedback

Size: ~19.8KB (complete implementation)
"""

from __future__ import annotations

import json
import statistics
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, TypeVar, Generic, Union


# ============================================================================
# Core Data Structures
# ============================================================================

class EvolutionStrategy(Enum):
    """Evolution strategies"""
    INCREMENTAL = auto()  # Small incremental improvements
    RADICAL = auto()      # Major architectural changes
    ADAPTIVE = auto()     # Adapt to changing conditions
    CONSERVATIVE = auto() # Minimal changes, maximum stability


class TaskOutcome(Enum):
    """Task outcome types"""
    SUCCESS = auto()
    PARTIAL_SUCCESS = auto()
    FAILURE = auto()
    TIMEOUT = auto()
    EXCEPTION = auto()


@dataclass
class PerformanceMetrics:
    """Performance metrics for a task"""
    execution_time_ms: float
    memory_usage_mb: float
    cpu_usage_percent: float
    quality_score: float  # 0-10
    success_rate: float   # 0-1
    error_count: int
    warning_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_time_ms": self.execution_time_ms,
            "memory_usage_mb": self.memory_usage_mb,
            "cpu_usage_percent": self.cpu_usage_percent,
            "quality_score": self.quality_score,
            "success_rate": self.success_rate,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PerformanceMetrics:
        return cls(**data)


@dataclass
class Experience:
    """A single experience record"""
    id: str
    timestamp: datetime
    task_type: str
    strategy_used: str
    outcome: TaskOutcome
    metrics: PerformanceMetrics
    context: Dict[str, Any]
    lessons_learned: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "task_type": self.task_type,
            "strategy_used": self.strategy_used,
            "outcome": self.outcome.name,
            "metrics": self.metrics.to_dict(),
            "context": self.context,
            "lessons_learned": self.lessons_learned,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Experience:
        return cls(
            id=data["id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            task_type=data["task_type"],
            strategy_used=data["strategy_used"],
            outcome=TaskOutcome[data["outcome"]],
            metrics=PerformanceMetrics.from_dict(data["metrics"]),
            context=data["context"],
            lessons_learned=data["lessons_learned"],
        )


@dataclass
class Strategy:
    """An evolution strategy"""
    id: str
    name: str
    description: str
    strategy_type: EvolutionStrategy
    parameters: Dict[str, Any]
    success_rate: float = 0.0
    usage_count: int = 0
    avg_quality: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "strategy_type": self.strategy_type.name,
            "parameters": self.parameters,
            "success_rate": self.success_rate,
            "usage_count": self.usage_count,
            "avg_quality": self.avg_quality,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat() if self.last_used else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Strategy:
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            strategy_type=EvolutionStrategy[data["strategy_type"]],
            parameters=data["parameters"],
            success_rate=data["success_rate"],
            usage_count=data["usage_count"],
            avg_quality=data["avg_quality"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_used=datetime.fromisoformat(data["last_used"]) if data["last_used"] else None,
        )


# ============================================================================
# Performance Analyzer
# ============================================================================

class PerformanceAnalyzer:
    """Analyzes performance metrics and identifies patterns"""
    
    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
        self.baseline: Optional[PerformanceMetrics] = None
        self.trends: Dict[str, List[float]] = defaultdict(list)
    
    def record_metrics(self, metrics: PerformanceMetrics) -> None:
        """Record new metrics"""
        self.metrics_history.append(metrics)
        
        # Update trends
        self.trends["execution_time"].append(metrics.execution_time_ms)
        self.trends["memory_usage"].append(metrics.memory_usage_mb)
        self.trends["quality_score"].append(metrics.quality_score)
        self.trends["success_rate"].append(metrics.success_rate)
        
        # Keep only last 100 measurements
        for key in self.trends:
            if len(self.trends[key]) > 100:
                self.trends[key] = self.trends[key][-100:]
    
    def set_baseline(self, metrics: PerformanceMetrics) -> None:
        """Set baseline metrics"""
        self.baseline = metrics
    
    def analyze_performance(self) -> Dict[str, Any]:
        """Analyze current performance vs baseline"""
        if not self.metrics_history:
            return {"status": "insufficient_data"}
        
        recent = self.metrics_history[-10:]
        
        analysis = {
            "status": "analyzed",
            "sample_size": len(recent),
            "current_avg": {
                "execution_time_ms": statistics.mean([m.execution_time_ms for m in recent]),
                "quality_score": statistics.mean([m.quality_score for m in recent]),
                "success_rate": statistics.mean([m.success_rate for m in recent]),
            },
            "trends": self._calculate_trends(),
            "bottlenecks": self._identify_bottlenecks(recent),
        }
        
        if self.baseline:
            analysis["vs_baseline"] = self._compare_to_baseline(recent)
        
        return analysis
    
    def _calculate_trends(self) -> Dict[str, str]:
        """Calculate trends for each metric"""
        trends = {}
        for metric_name, values in self.trends.items():
            if len(values) < 10:
                trends[metric_name] = "insufficient_data"
                continue
            
            recent = values[-10:]
            older = values[-20:-10] if len(values) >= 20 else values[:10]
            
            recent_avg = statistics.mean(recent)
            older_avg = statistics.mean(older)
            
            if recent_avg > older_avg * 1.1:
                trends[metric_name] = "improving" if metric_name in ["quality_score", "success_rate"] else "degrading"
            elif recent_avg < older_avg * 0.9:
                trends[metric_name] = "degrading" if metric_name in ["quality_score", "success_rate"] else "improving"
            else:
                trends[metric_name] = "stable"
        
        return trends
    
    def _identify_bottlenecks(self, metrics: List[PerformanceMetrics]) -> List[str]:
        """Identify performance bottlenecks"""
        bottlenecks = []
        
        avg_time = statistics.mean([m.execution_time_ms for m in metrics])
        if avg_time > 1000:  # > 1 second
            bottlenecks.append("high_latency")
        
        avg_memory = statistics.mean([m.memory_usage_mb for m in metrics])
        if avg_memory > 500:  # > 500MB
            bottlenecks.append("high_memory")
        
        avg_quality = statistics.mean([m.quality_score for m in metrics])
        if avg_quality < 7.0:
            bottlenecks.append("low_quality")
        
        avg_success = statistics.mean([m.success_rate for m in metrics])
        if avg_success < 0.9:
            bottlenecks.append("low_success_rate")
        
        return bottlenecks
    
    def _compare_to_baseline(self, recent: List[PerformanceMetrics]) -> Dict[str, Any]:
        """Compare recent metrics to baseline"""
        if not self.baseline:
            return {}
        
        recent_avg = {
            "execution_time_ms": statistics.mean([m.execution_time_ms for m in recent]),
            "quality_score": statistics.mean([m.quality_score for m in recent]),
            "success_rate": statistics.mean([m.success_rate for m in recent]),
        }
        
        return {
            "execution_time_change": (recent_avg["execution_time_ms"] - self.baseline.execution_time_ms) / self.baseline.execution_time_ms,
            "quality_change": recent_avg["quality_score"] - self.baseline.quality_score,
            "success_rate_change": recent_avg["success_rate"] - self.baseline.success_rate,
        }
    
    def get_performance_score(self) -> float:
        """Calculate overall performance score (0-10)"""
        if not self.metrics_history:
            return 5.0
        
        recent = self.metrics_history[-10:]
        
        # Weighted scoring
        avg_quality = statistics.mean([m.quality_score for m in recent])
        avg_success = statistics.mean([m.success_rate for m in recent]) * 10
        avg_time = max(0, 10 - statistics.mean([m.execution_time_ms for m in recent]) / 100)
        
        return (avg_quality * 0.4 + avg_success * 0.4 + avg_time * 0.2)


# ============================================================================
# Experience Library
# ============================================================================

class ExperienceLibrary:
    """Library for storing and retrieving experiences"""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.experiences: Dict[str, Experience] = {}
        self.task_type_index: Dict[str, Set[str]] = defaultdict(set)
        self.strategy_index: Dict[str, Set[str]] = defaultdict(set)
        self.outcome_index: Dict[str, Set[str]] = defaultdict(set)
        
        self.storage_path = Path(storage_path) if storage_path else None
        if self.storage_path and self.storage_path.exists():
            self._load_from_disk()
    
    def add_experience(self, experience: Experience) -> None:
        """Add an experience to the library"""
        self.experiences[experience.id] = experience
        
        # Update indexes
        self.task_type_index[experience.task_type].add(experience.id)
        self.strategy_index[experience.strategy_used].add(experience.id)
        self.outcome_index[experience.outcome.name].add(experience.id)
        
        # Persist if path set
        if self.storage_path:
            self._save_to_disk()
    
    def get_experience(self, experience_id: str) -> Optional[Experience]:
        """Get an experience by ID"""
        return self.experiences.get(experience_id)
    
    def find_similar_experiences(
        self,
        task_type: str,
        strategy: Optional[str] = None,
        outcome: Optional[TaskOutcome] = None,
        limit: int = 10
    ) -> List[Experience]:
        """Find experiences matching criteria"""
        # Start with task type
        candidate_ids = self.task_type_index.get(task_type, set())
        
        # Filter by strategy if specified
        if strategy:
            candidate_ids = candidate_ids & self.strategy_index.get(strategy, set())
        
        # Filter by outcome if specified
        if outcome:
            candidate_ids = candidate_ids & self.outcome_index.get(outcome.name, set())
        
        # Sort by timestamp (most recent first)
        experiences = [self.experiences[eid] for eid in candidate_ids]
        experiences.sort(key=lambda e: e.timestamp, reverse=True)
        
        return experiences[:limit]
    
    def get_lessons_for_task(self, task_type: str) -> List[str]:
        """Get all lessons learned for a task type"""
        lessons = []
        for exp_id in self.task_type_index.get(task_type, set()):
            exp = self.experiences[exp_id]
            lessons.extend(exp.lessons_learned)
        return list(set(lessons))  # Remove duplicates
    
    def get_successful_strategies(self, task_type: str) -> List[str]:
        """Get strategies that succeeded for a task type"""
        successful = []
        for exp_id in self.task_type_index.get(task_type, set()):
            exp = self.experiences[exp_id]
            if exp.outcome == TaskOutcome.SUCCESS:
                successful.append(exp.strategy_used)
        
        # Count occurrences
        strategy_counts = defaultdict(int)
        for s in successful:
            strategy_counts[s] += 1
        
        # Return sorted by success count
        return sorted(strategy_counts.keys(), key=lambda s: strategy_counts[s], reverse=True)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get library statistics"""
        total = len(self.experiences)
        if total == 0:
            return {"total_experiences": 0}
        
        outcomes = defaultdict(int)
        for exp in self.experiences.values():
            outcomes[exp.outcome.name] += 1
        
        return {
            "total_experiences": total,
            "by_outcome": dict(outcomes),
            "by_task_type": {k: len(v) for k, v in self.task_type_index.items()},
            "by_strategy": {k: len(v) for k, v in self.strategy_index.items()},
        }
    
    def _save_to_disk(self) -> None:
        """Save experiences to disk"""
        if not self.storage_path:
            return
        
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "experiences": {k: v.to_dict() for k, v in self.experiences.items()},
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def _load_from_disk(self) -> None:
        """Load experiences from disk"""
        if not self.storage_path or not self.storage_path.exists():
            return
        
        try:
            data = json.loads(self.storage_path.read_text())
            for exp_id, exp_data in data.get("experiences", {}).items():
                self.add_experience(Experience.from_dict(exp_data))
        except Exception:
            pass  # Start fresh if load fails


# ============================================================================
# Strategy Evolver
# ============================================================================

class StrategyEvolver:
    """Evolves strategies based on experience"""
    
    def __init__(self, experience_library: ExperienceLibrary):
        self.experience_library = experience_library
        self.strategies: Dict[str, Strategy] = {}
        self.active_strategy: Optional[str] = None
    
    def register_strategy(self, strategy: Strategy) -> None:
        """Register a new strategy"""
        self.strategies[strategy.id] = strategy
    
    def evolve_strategies(self) -> List[Strategy]:
        """Evolve strategies based on experiences"""
        evolved = []
        
        for strategy_id, strategy in self.strategies.items():
            # Find experiences using this strategy
            experiences = []
            for exp_id in self.experience_library.strategy_index.get(strategy_id, set()):
                exp = self.experience_library.get_experience(exp_id)
                if exp:
                    experiences.append(exp)
            
            if len(experiences) < 5:
                continue  # Not enough data
            
            # Calculate new statistics
            success_count = sum(1 for e in experiences if e.outcome == TaskOutcome.SUCCESS)
            new_success_rate = success_count / len(experiences)
            new_avg_quality = statistics.mean([e.metrics.quality_score for e in experiences])
            
            # Update strategy if improved
            if new_success_rate > strategy.success_rate:
                strategy.success_rate = new_success_rate
                strategy.avg_quality = new_avg_quality
                strategy.usage_count = len(experiences)
                evolved.append(strategy)
        
        return evolved
    
    def select_best_strategy(self, task_type: str) -> Optional[Strategy]:
        """Select the best strategy for a task type"""
        # Get successful strategies for this task
        successful_strategies = self.experience_library.get_successful_strategies(task_type)
        
        if not successful_strategies:
            # Return default strategy
            return self._get_default_strategy()
        
        # Find the strategy with highest success rate
        best_strategy = None
        best_rate = 0.0
        
        for strategy_id in successful_strategies:
            if strategy_id in self.strategies:
                strategy = self.strategies[strategy_id]
                if strategy.success_rate > best_rate:
                    best_rate = strategy.success_rate
                    best_strategy = strategy
        
        return best_strategy or self._get_default_strategy()
    
    def create_new_strategy(
        self,
        name: str,
        description: str,
        strategy_type: EvolutionStrategy,
        parameters: Dict[str, Any]
    ) -> Strategy:
        """Create a new strategy"""
        strategy = Strategy(
            id=f"strategy_{int(time.time())}_{len(self.strategies)}",
            name=name,
            description=description,
            strategy_type=strategy_type,
            parameters=parameters,
        )
        self.register_strategy(strategy)
        return strategy
    
    def mutate_strategy(self, strategy_id: str) -> Optional[Strategy]:
        """Create a mutated version of a strategy"""
        if strategy_id not in self.strategies:
            return None
        
        original = self.strategies[strategy_id]
        
        # Mutate parameters
        mutated_params = original.parameters.copy()
        for key, value in mutated_params.items():
            if isinstance(value, (int, float)):
                # Small random mutation
                mutated_params[key] = value * (1 + (hash(key) % 10 - 5) / 100)
        
        return self.create_new_strategy(
            name=f"{original.name}_mutated",
            description=f"Mutated version of {original.name}",
            strategy_type=original.strategy_type,
            parameters=mutated_params,
        )
    
    def _get_default_strategy(self) -> Optional[Strategy]:
        """Get default strategy"""
        for strategy in self.strategies.values():
            if strategy.name == "default":
                return strategy
        return next(iter(self.strategies.values())) if self.strategies else None
    
    def get_strategy_recommendations(self, task_type: str) -> List[Dict[str, Any]]:
        """Get strategy recommendations for a task type"""
        recommendations = []
        
        for strategy_id in self.experience_library.get_successful_strategies(task_type):
            if strategy_id in self.strategies:
                strategy = self.strategies[strategy_id]
                recommendations.append({
                    "strategy_id": strategy_id,
                    "name": strategy.name,
                    "success_rate": strategy.success_rate,
                    "avg_quality": strategy.avg_quality,
                    "usage_count": strategy.usage_count,
                })
        
        return sorted(recommendations, key=lambda x: x["success_rate"], reverse=True)


# ============================================================================
# Self-Evolving Agent
# ============================================================================

class SelfEvolvingAgent:
    """Agent that evolves based on experience"""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.experience_library = ExperienceLibrary(storage_path)
        self.performance_analyzer = PerformanceAnalyzer()
        self.strategy_evolver = StrategyEvolver(self.experience_library)
        
        self.current_task: Optional[str] = None
        self.current_strategy: Optional[str] = None
        self.task_start_time: Optional[float] = None
        
        self._register_default_strategies()
    
    def _register_default_strategies(self) -> None:
        """Register default strategies"""
        self.strategy_evolver.register_strategy(Strategy(
            id="default",
            name="default",
            description="Default conservative strategy",
            strategy_type=EvolutionStrategy.CONSERVATIVE,
            parameters={"risk_tolerance": 0.1, "innovation_rate": 0.01},
        ))
        
        self.strategy_evolver.register_strategy(Strategy(
            id="aggressive",
            name="aggressive",
            description="Aggressive optimization strategy",
            strategy_type=EvolutionStrategy.RADICAL,
            parameters={"risk_tolerance": 0.5, "innovation_rate": 0.1},
        ))
        
        self.strategy_evolver.register_strategy(Strategy(
            id="adaptive",
            name="adaptive",
            description="Adaptive strategy based on conditions",
            strategy_type=EvolutionStrategy.ADAPTIVE,
            parameters={"risk_tolerance": 0.3, "adaptation_rate": 0.05},
        ))
    
    def start_task(self, task_type: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Start a new task with evolution"""
        self.current_task = task_type
        self.task_start_time = time.time()
        
        # Select best strategy
        strategy = self.strategy_evolver.select_best_strategy(task_type)
        if strategy:
            self.current_strategy = strategy.id
        else:
            self.current_strategy = "default"
        
        # Get lessons from similar tasks
        lessons = self.experience_library.get_lessons_for_task(task_type)
        similar = self.experience_library.find_similar_experiences(task_type, limit=5)
        
        return {
            "task_type": task_type,
            "selected_strategy": self.current_strategy,
            "lessons_from_past": lessons,
            "similar_experiences": len(similar),
            "recommendations": self.strategy_evolver.get_strategy_recommendations(task_type),
        }
    
    def end_task(
        self,
        outcome: Union[TaskOutcome, bool],
        metrics: Union[PerformanceMetrics, Dict[str, Any]],
        lessons_learned: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """End a task and record experience
        
        Args:
            outcome: TaskOutcome enum or bool (True=SUCCESS, False=FAILURE)
            metrics: PerformanceMetrics object or dict with metric values
            lessons_learned: Optional list of lessons learned
        """
        if not self.current_task or not self.task_start_time:
            return {"error": "No active task"}
        
        execution_time = (time.time() - self.task_start_time) * 1000
        
        # Convert bool to TaskOutcome
        if isinstance(outcome, bool):
            outcome_enum = TaskOutcome.SUCCESS if outcome else TaskOutcome.FAILURE
        else:
            outcome_enum = outcome
        
        # Handle both dict and PerformanceMetrics objects
        if isinstance(metrics, dict):
            metrics_obj = PerformanceMetrics(
                execution_time_ms=execution_time,
                memory_usage_mb=metrics.get("memory_usage_mb", 0.0),
                cpu_usage_percent=metrics.get("cpu_usage_percent", 0.0),
                quality_score=metrics.get("quality_score", 0.5),
                success_rate=1.0 if outcome_enum == TaskOutcome.SUCCESS else 0.0,
                error_count=metrics.get("error_count", 0),
                warning_count=metrics.get("warning_count", 0),
            )
        else:
            metrics_obj = metrics
        
        # Create experience record
        experience = Experience(
            id=f"exp_{int(time.time())}_{hash(self.current_task) % 10000}",
            timestamp=datetime.now(),
            task_type=self.current_task,
            strategy_used=self.current_strategy or "default",
            outcome=outcome_enum,
            metrics=metrics_obj,
            context={},
            lessons_learned=lessons_learned or [],
        )
        
        # Record experience
        self.experience_library.add_experience(experience)
        self.performance_analyzer.record_metrics(experience.metrics)
        
        # Evolve strategies
        evolved = self.strategy_evolver.evolve_strategies()
        
        # Reset state
        task_summary = {
            "task_type": self.current_task,
            "strategy_used": self.current_strategy,
            "outcome": outcome_enum.name,
            "execution_time_ms": execution_time,
            "experience_recorded": True,
            "strategies_evolved": len(evolved),
        }
        
        self.current_task = None
        self.current_strategy = None
        self.task_start_time = None
        
        return task_summary
    
    def analyze_performance(self) -> Dict[str, Any]:
        """Analyze current performance"""
        return self.performance_analyzer.analyze_performance()
    
    def get_evolution_status(self) -> Dict[str, Any]:
        """Get evolution status"""
        return {
            "experience_count": len(self.experience_library.experiences),
            "strategy_count": len(self.strategy_evolver.strategies),
            "performance_score": self.performance_analyzer.get_performance_score(),
            "experience_stats": self.experience_library.get_statistics(),
        }
    
    def suggest_improvements(self) -> List[str]:
        """Suggest improvements based on analysis"""
        suggestions = []
        
        analysis = self.performance_analyzer.analyze_performance()
        if analysis.get("status") == "analyzed":
            # Check trends
            for metric, trend in analysis.get("trends", {}).items():
                if trend == "degrading":
                    suggestions.append(f"Address degrading {metric}")
            
            # Check bottlenecks
            for bottleneck in analysis.get("bottlenecks", []):
                suggestions.append(f"Optimize {bottleneck}")
        
        # Check experience gaps
        stats = self.experience_library.get_statistics()
        if stats.get("total_experiences", 0) < 10:
            suggestions.append("Gather more experience data")
        
        return suggestions


# ============================================================================
# Integration Helpers
# ============================================================================

def create_self_evolving_agent(storage_path: Optional[str] = None) -> SelfEvolvingAgent:
    """Factory function to create a self-evolving agent"""
    return SelfEvolvingAgent(storage_path)


def evolve_from_mistake(
    agent: SelfEvolvingAgent,
    task_type: str,
    error: str,
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Helper to evolve from a mistake"""
    # Start task
    agent.start_task(task_type, context)
    
    # End with failure
    return agent.end_task(
        outcome=TaskOutcome.FAILURE,
        metrics=PerformanceMetrics(
            execution_time_ms=0,
            memory_usage_mb=0,
            cpu_usage_percent=0,
            quality_score=0.0,
            success_rate=0.0,
            error_count=1,
            warning_count=0,
        ),
        lessons_learned=[f"Error: {error}", "Need to handle this case"],
    )


def evolve_from_success(
    agent: SelfEvolvingAgent,
    task_type: str,
    quality_score: float,
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Helper to evolve from success"""
    # Start task
    agent.start_task(task_type, context)
    
    # End with success
    return agent.end_task(
        outcome=TaskOutcome.SUCCESS,
        metrics=PerformanceMetrics(
            execution_time_ms=100,
            memory_usage_mb=50,
            cpu_usage_percent=30,
            quality_score=quality_score,
            success_rate=1.0,
            error_count=0,
            warning_count=0,
        ),
        lessons_learned=["This approach works well"],
    )


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    "SelfEvolvingAgent",
    "PerformanceAnalyzer",
    "ExperienceLibrary",
    "StrategyEvolver",
    "Experience",
    "Strategy",
    "PerformanceMetrics",
    "EvolutionStrategy",
    "TaskOutcome",
    "create_self_evolving_agent",
    "evolve_from_mistake",
    "evolve_from_success",
]
