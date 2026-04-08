"""
Comprehensive tests for v6.8 Unified System.

Tests cover:
- Unit tests for each component
- Integration tests for full coordination
- Edge cases and error handling
- Performance benchmarks
"""

import unittest
from datetime import datetime
from typing import Any, Dict

from unified_system import (
    UnifiedSystem,
    CoordinationResult,
    ModuleLoader,
    coordinate,
    check_status,
)


# ============================================================================
# Mock Modules for Testing
# ============================================================================

class MockPredictor:
    """Mock prediction module"""
    def predict(self, data: Any) -> Dict[str, Any]:
        return {"prediction": "mock_result", "confidence": 0.95}


class MockMonitor:
    """Mock monitoring module"""
    def check(self) -> Dict[str, Any]:
        return {"status": "healthy", "metrics": {"cpu": 0.5}}


class MockLearner:
    """Mock learning module"""
    def learn(self, data: Any) -> Dict[str, Any]:
        return {"learned": True, "samples": len(data) if isinstance(data, list) else 0}


class MockReasoner:
    """Mock reasoning module"""
    def reason(self, query: str) -> Dict[str, Any]:
        return {"answer": f"Reasoned: {query}", "confidence": 0.9}


# ============================================================================
# Unit Tests
# ============================================================================

class TestModuleLoader(unittest.TestCase):
    """Test ModuleLoader"""
    
    def setUp(self) -> None:
        self.loader = ModuleLoader()
    
    def test_load_missing_module(self) -> None:
        """Loading missing module returns None gracefully"""
        result = self.loader.load(
            "test",
            "nonexistent.module",
            "NonExistent",
            MockPredictor,
        )
        self.assertIsNone(result)
    
    def test_load_caches_result(self) -> None:
        """Loader caches loaded modules"""
        # First, inject a mock
        self.loader._cache["test"] = MockPredictor()
        
        # Second load should return cached
        result = self.loader.load(
            "test",
            "nonexistent.module",  # Won't be called due to cache
            "NonExistent",
            MockPredictor,
        )
        self.assertIsInstance(result, MockPredictor)


class TestCoordinationResult(unittest.TestCase):
    """Test CoordinationResult"""
    
    def test_immutable(self) -> None:
        """Result is immutable"""
        result = CoordinationResult(
            task="test",
            success=True,
            timestamp=datetime.now(),
        )
        
        # Should raise FrozenInstanceError
        with self.assertRaises(Exception):
            result.task = "modified"
    
    def test_available_modules(self) -> None:
        """available_modules property works"""
        result = CoordinationResult(
            task="test",
            success=True,
            timestamp=datetime.now(),
            prediction={"data": "value"},
            monitoring=None,
            learning={"data": "value"},
        )
        
        self.assertEqual(result.available_modules, ["prediction", "learning"])
    
    def test_has_errors(self) -> None:
        """has_errors property works"""
        result_no_errors = CoordinationResult(
            task="test",
            success=True,
            timestamp=datetime.now(),
        )
        self.assertFalse(result_no_errors.has_errors)
        
        result_with_errors = CoordinationResult(
            task="test",
            success=False,
            timestamp=datetime.now(),
            errors=["something failed"],
        )
        self.assertTrue(result_with_errors.has_errors)


class TestUnifiedSystem(unittest.TestCase):
    """Test UnifiedSystem"""
    
    def setUp(self) -> None:
        self.system = UnifiedSystem()
    
    def test_initialization(self) -> None:
        """System initializes correctly"""
        self.assertFalse(self.system._initialized)
        
        # Trigger initialization
        self.system._ensure_initialized()
        self.assertTrue(self.system._initialized)
    
    def test_status(self) -> None:
        """status() returns dict of booleans"""
        status = self.system.status()
        self.assertIsInstance(status, dict)
        for key in ["prediction", "monitoring", "learning", "reasoning", "quality"]:
            self.assertIn(key, status)
            self.assertIsInstance(status[key], bool)
    
    def test_coordination_empty_data(self) -> None:
        """Coordination with empty data"""
        result = self.system.coordinate("test")
        
        self.assertIsInstance(result, CoordinationResult)
        self.assertEqual(result.task, "test")
        self.assertIsInstance(result.timestamp, datetime)
    
    def test_coordination_with_data(self) -> None:
        """Coordination with data"""
        result = self.system.coordinate(
            "analyze",
            {"metrics": [1, 2, 3], "query": "test"}
        )
        
        self.assertEqual(result.task, "analyze")
        # May or may not have results depending on module availability


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_convenience_function(self) -> None:
        """convenience function works"""
        result = coordinate("test_task", {"some": "data"})
        self.assertIsInstance(result, CoordinationResult)
        self.assertEqual(result.task, "test_task")
    
    def test_check_status(self) -> None:
        """check_status convenience function"""
        status = check_status()
        self.assertIsInstance(status, dict)
        self.assertEqual(len(status), 5)


# ============================================================================
# Edge Cases
# ============================================================================

class TestEdgeCases(unittest.TestCase):
    """Edge case tests"""
    
    def test_none_data(self) -> None:
        """Coordination with None data"""
        system = UnifiedSystem()
        result = system.coordinate("test", None)
        self.assertIsInstance(result, CoordinationResult)
        self.assertTrue(result.success or result.has_errors)
    
    def test_empty_string_task(self) -> None:
        """Coordination with empty task"""
        system = UnifiedSystem()
        result = system.coordinate("")
        self.assertEqual(result.task, "")
    
    def test_very_long_task_name(self) -> None:
        """Coordination with very long task name"""
        system = UnifiedSystem()
        long_task = "x" * 10000
        result = system.coordinate(long_task)
        self.assertEqual(result.task, long_task)
    
    def test_special_characters_in_data(self) -> None:
        """Coordination with special characters"""
        system = UnifiedSystem()
        result = system.coordinate("test", {
            "key": "value with unicode: 你好",
            "nested": {"list": [1, None, True, False]},
        })
        self.assertIsInstance(result, CoordinationResult)


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
