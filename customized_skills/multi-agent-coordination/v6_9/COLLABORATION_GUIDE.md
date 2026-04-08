# v6.9 Ultimate System - Collaboration Guide

## 模块协同架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    Task Execution Flow                          │
└─────────────────────────────────────────────────────────────────┘
│
├─[STEP 1] Prediction Analysis (v6.9 AnomalyDetector)
│   Input:  metrics {"response_time": 0.5, "error_rate": 0.02}
│   Method: detector.detect(metrics)
│   Output: {"is_anomaly": False, "confidence": 0.0}
│
├─[STEP 2] Health Check (v6.9 SelfAwarenessMonitor)
│   Method: monitor.check()
│   Output: {"overall": "healthy", "metrics": {}, "timestamp": "..."}
│
├─[STEP 3] Knowledge Retrieval (v6.0 KnowledgeBase)
│   Method: knowledge.retrieve(query)
│   Output: relevant patterns, lessons
│
├─[STEP 4] SOP Execution (v6.0 SOPEngine)
│   Method: sop.execute(sop_id, context)
│   Output: sop_results
│
├─[STEP 5] Unified Coordination (v6.9 UnifiedCoordinationSystem)
│   Method: unified.coordinate(data)
│   Input:  {"task": "name", "data": {...}}
│   Output: CoordinationResult
│     - success: bool
│     - predictions: dict
│     - health: dict
│     - quality: dict
│     - reasoning: dict
│     - learning: dict
│     - errors: list
│     - timestamp: str
│
├─[STEP 6] Quality Gates (v6.0 8 Quality Gates)
│   Gates:
│     1. Design Review
│     2. Code Review
│     3. Type Check
│     4. Build Check
│     5. Visual Acceptance
│     6. Performance
│     7. Test Coverage
│     8. Security
│
├─[STEP 7] Causal Reasoning (v6.9 CausalGraph)
│   Methods:
│     - causal.add_node(name)
│     - causal.add_edge(from, to, strength)
│     - causal.is_d_separated(a, b, conditioning_set)
│
├─[STEP 8] Learning (v6.0/v6.9 AdaptiveLearning)
│   Methods:
│     - learning.learn_from_success(task, result, context, project)
│     - learning.learn_from_mistake(task, error, context, project)
│
└─[STEP 9] Retrospection (v6.0 RetrospectionEngine)
    Methods:
      - retro.analyze(task_result)
      - retro.generate_prevention(issue)
```

## 数据流示例

### 完整执行流程

```python
from v6_9 import (
    UltimateCoordinationSystem,
    UnifiedCoordinationSystem,
    AnomalyDetector,
    SelfAwarenessMonitor,
    CausalGraph,
)

# 1. 创建模块
predictor = AnomalyDetector()
monitor = SelfAwarenessMonitor()
causal = CausalGraph()
unified = UnifiedCoordinationSystem()

# 2. 预测分析
metrics = {"response_time": 0.5, "error_rate": 0.02}
prediction = predictor.detect(metrics)
# Output: {"is_anomaly": False, "confidence": 0.0}

# 3. 健康检查
health = monitor.check()
# Output: {"overall": "healthy", "metrics": {}, "timestamp": "..."}

# 4. 因果分析
causal.add_edge("A", "B", 1.0)
causal.add_edge("B", "C", 1.0)
is_dsep = causal.is_d_separated("A", "C", {"B"})
# Output: True (A and C are d-separated given B)

# 5. 统一协调
result = unified.coordinate({
    "task": "implement_feature",
    "data": {"priority": "high"}
})
# Output: CoordinationResult with all module outputs
```

## 模块接口速查

### AnomalyDetector (v6.9)

```python
detector = AnomalyDetector(
    method="iqr",      # "iqr" | "zscore" | "isolation_forest"
    threshold=1.5      # IQR multiplier
)

# Detect anomaly
result = detector.detect(metrics)
# Returns: {"is_anomaly": bool, "confidence": float}
```

### SelfAwarenessMonitor (v6.9)

```python
monitor = SelfAwarenessMonitor(
    thresholds={
        "response_time_ms": 1000,
        "error_rate": 0.01,
        "cpu_percent": 80
    }
)

# Check health
health = monitor.check()
# Returns: {"overall": "healthy"|"degraded"|"critical", "metrics": dict, "timestamp": str}

# Record metric
monitor.record("response_time_ms", 500)
```

### CausalGraph (v6.9)

```python
graph = CausalGraph()

# Add nodes
graph.add_node("A")
graph.add_node("B")

# Add edges (with strength)
graph.add_edge("A", "B", 0.8)

# Get parents/children
parents = graph.get_parents("B")    # ["A"]
children = graph.get_children("A")  # ["B"]

# Check d-separation
is_dsep = graph.is_d_separated("A", "C", {"B"})
```

### UnifiedCoordinationSystem (v6.9)

```python
unified = UnifiedCoordinationSystem(
    enable_prediction=True,
    enable_monitoring=True,
    enable_quality=True,
    enable_reasoning=True,
    enable_learning=True
)

# Coordinate task
result = unified.coordinate({
    "task": "task_name",
    "data": {...}
})

# Access results
result.success      # bool
result.predictions  # dict
result.health       # dict
result.quality      # dict
result.reasoning    # dict
result.learning     # dict
result.errors       # list
result.timestamp    # str

# Check status
status = unified.check_status()
```

### UltimateCoordinationSystem (v6.9 + v6.0)

```python
ultimate = UltimateCoordinationSystem(
    project_path=".",
    enable_v60=True,
    enable_learning=True,
    enable_retrospection=True
)

# Execute task
result = ultimate.execute(
    name="Task Name",
    description="Task description",
    requirements={"priority": "high"}
)

# Access results
result.success          # bool
result.quality_score    # float (0-10)
result.duration_seconds # int
result.errors           # list
result.warnings         # list
result.metrics          # dict

# Get evolution status
evolution = ultimate.get_evolution_status()
evolution.total_tasks       # int
evolution.successful_tasks  # int
evolution.failed_tasks      # int
evolution.average_quality   # float
```

## 协同模式

### Pattern 1: Sequential Execution

```python
# Step-by-step execution with data passing
prediction = predictor.detect(metrics)
if prediction["is_anomaly"]:
    health = monitor.check()
    if health["overall"] == "critical":
        # Handle critical state
        pass
```

### Pattern 2: Parallel Coordination

```python
# All modules run in coordination
result = unified.coordinate(data)
# Access all outputs in result
```

### Pattern 3: Conditional Execution

```python
# Execute based on conditions
result = unified.coordinate(data)
if result.quality["score"] < 9.0:
    # Learn from mistakes
    learning.learn_from_mistake(...)
else:
    # Learn from success
    learning.learn_from_success(...)
```

### Pattern 4: Full Pipeline

```python
# Complete 9-step pipeline
ultimate = UltimateCoordinationSystem(...)
result = ultimate.execute(...)
# All 9 steps executed automatically
```

## 错误处理

```python
try:
    result = unified.coordinate(data)
    if not result.success:
        print(f"Errors: {result.errors}")
except Exception as e:
    print(f"Exception: {e}")
```

## 最佳实践

1. **Use UnifiedCoordinationSystem** for most tasks
   - Combines all v6.9 modules
   - Consistent interface
   - Automatic error handling

2. **Use UltimateCoordinationSystem** for complex projects
   - Includes v6.0 features
   - Full 9-step pipeline
   - Evolution tracking

3. **Individual modules** for specific needs
   - Direct control
   - Custom workflows
   - Testing/debugging

4. **Always check results**
   - `result.success` for boolean status
   - `result.errors` for details
   - `result.quality` for metrics

5. **Use learning**
   - Record successes
   - Record failures
   - Apply patterns
