"""
Test Suite for v6.9 Unified System

验证所有组件功能正常。
"""

import sys
import random
import math

# Test v6.5: Anomaly Detection
def test_anomaly_detector():
    """测试异常检测器"""
    from unified_system import AnomalyDetector
    
    detector = AnomalyDetector(method="iqr")
    
    # 正常数据
    for i in range(20):
        detector.detect(float(i))
    
    # 异常值
    result = detector.detect(100.0)
    
    assert result["is_anomaly"] == True, "Should detect anomaly"
    assert result["iqr"] > 0, "Should have IQR"
    print("[PASS] v6.5 AnomalyDetector passed")


# Test v6.6: Self-Awareness
def test_self_awareness():
    """测试自我意识监控"""
    from unified_system import SelfAwarenessMonitor, HealthStatus
    
    monitor = SelfAwarenessMonitor()
    
    # 记录指标
    for i in range(10):
        monitor.record("latency", float(i * 10))
    
    # 检查健康
    health = monitor.check()
    
    assert "metrics" in health, "Should have metrics"
    assert "latency" in health["metrics"], "Should have latency metric"
    print("[PASS] v6.6 SelfAwarenessMonitor passed")


# Test v6.7: Federated Learning
def test_federated_learning():
    """测试联邦学习"""
    from unified_system import FederatedLearner
    
    learner = FederatedLearner(algorithm="fedavg")
    
    # 模拟更新
    updates = [
        {"layer": [1.0, 2.0, 3.0]},
        {"layer": [3.0, 4.0, 5.0]}
    ]
    
    result = learner.aggregate(updates)
    
    assert result["layer"] == [2.0, 3.0, 4.0], "Should average correctly"
    print("[PASS] v6.7 FederatedLearner passed")


# Test v6.7: FedProx
def test_fedprox():
    """测试FedProx算法"""
    from unified_system import FederatedLearner
    
    learner = FederatedLearner(algorithm="fedprox", mu=0.1)
    learner.global_model = {"layer": [1.0, 1.0, 1.0]}
    
    updates = [
        {"layer": [2.0, 2.0, 2.0]},
        {"layer": [2.0, 2.0, 2.0]}
    ]
    
    result = learner.aggregate(updates)
    
    # FedProx应该比FedAvg更接近全局模型
    assert len(result["layer"]) == 3, "Should have correct shape"
    print("[PASS] v6.7 FedProx passed")


# Test v6.8: Causal Graph
def test_causal_graph():
    """测试因果图"""
    from unified_system import CausalGraph, CausalRelation
    
    graph = CausalGraph()
    graph.add_node("X")
    graph.add_node("Y")
    graph.add_node("Z")
    
    # 链式结构 X -> Y -> Z
    graph.add_edge("X", "Y", 1.0, relation=CausalRelation.CAUSE)
    graph.add_edge("Y", "Z", 1.0, relation=CausalRelation.CAUSE)
    
    # d-分离检验
    assert graph.is_d_separated("X", "Z", {"Y"}) == True, "X and Z should be d-separated given Y"
    assert graph.is_d_separated("X", "Z", set()) == False, "X and Z should not be d-separated unconditionally"
    
    print("[PASS] v6.8 CausalGraph passed")


# Test v6.8: Causal Discovery
def test_causal_discovery():
    """测试因果发现"""
    from unified_system import CausalDiscovery
    
    discovery = CausalDiscovery()
    
    # v结构数据 X -> Z <- Y
    n = 1000
    random.seed(42)
    x = [random.gauss(0, 1) for _ in range(n)]
    y = [random.gauss(0, 1) for _ in range(n)]
    z = [xi + yi + random.gauss(0, 0.1) for xi, yi in zip(x, y)]
    
    discovery.add_data("X", x)
    discovery.add_data("Y", y)
    discovery.add_data("Z", z)
    
    graph = discovery.discover(["X", "Y", "Z"], method="pc")
    
    # 应该发现边
    assert len(graph._edges) > 0, "Should discover edges"
    print("[PASS] v6.8 CausalDiscovery passed")


# Test v3.1: Quality Gate
def test_quality_gate():
    """测试质量门禁"""
    from unified_system import QualityGateV31
    
    gate = QualityGateV31()
    
    code = '"""Module docstring"""\ndef foo(): pass'
    result = gate.evaluate(code)
    
    assert "score" in result, "Should have score"
    assert "passed" in result, "Should have passed status"
    print("[PASS] v3.1 QualityGateV31 passed")


# Test Unified System
def test_unified_system():
    """测试统一系统"""
    from unified_system import UnifiedCoordinationSystem
    
    system = UnifiedCoordinationSystem()
    
    # 协调（简单float数据）
    result = system.coordinate(1.0)
    
    assert result.success == True, f"Should succeed but got errors: {result.errors}"
    assert result.predictions is not None, "Should have predictions"
    
    # 检查状态
    status = system.check_status()
    assert status["status"] == "coordinated", "Should be coordinated"
    
    print("[PASS] UnifiedCoordinationSystem passed")


# Test Public API
def test_public_api():
    """测试公共API"""
    from unified_system import coordinate, check_status
    
    result = coordinate(1.0)
    assert result.success == True, "coordinate() should work"
    
    status = check_status()
    assert "components" in status, "check_status() should work"
    
    print("[PASS] Public API passed")


if __name__ == "__main__":
    print("Running v6.9 Test Suite...\n")
    
    test_anomaly_detector()
    test_self_awareness()
    test_federated_learning()
    test_fedprox()
    test_causal_graph()
    test_causal_discovery()
    test_quality_gate()
    test_unified_system()
    test_public_api()
    
    print("\n[ALL PASS] All tests passed!")
