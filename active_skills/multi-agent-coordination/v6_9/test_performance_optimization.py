"""
Test Suite for Performance Optimization System v6.5

High Standard: 100% test pass rate
Tests all components with comprehensive coverage:
- StreamingHandler (streaming, backpressure)
- AsyncExecutor (async execution)
- CacheManager (caching)
- PerformanceMonitor (metrics, suggestions)
"""

import sys
import time
from datetime import datetime

from performance_optimization import (
    StreamingHandler,
    AsyncExecutor,
    CacheManager,
    PerformanceMonitor,
    PerformanceMetrics,
    OptimizationSuggestion,
    StreamChunk,
    AsyncTaskResult,
    PerformanceLevel,
    OptimizationType,
    create_streaming_handler,
    create_async_executor,
    create_cache_manager,
    create_performance_monitor,
)


def test_performance_level_enum():
    """Test PerformanceLevel enum"""
    print("Testing PerformanceLevel...")
    
    assert PerformanceLevel.EXCELLENT.name == "EXCELLENT"
    assert PerformanceLevel.CRITICAL.name == "CRITICAL"
    
    print("  [OK] PerformanceLevel tests passed")
    return True


def test_optimization_type_enum():
    """Test OptimizationType enum"""
    print("Testing OptimizationType...")
    
    assert OptimizationType.STREAMING.name == "STREAMING"
    assert OptimizationType.CACHING.name == "CACHING"
    
    print("  [OK] OptimizationType tests passed")
    return True


def test_performance_metrics():
    """Test PerformanceMetrics data class"""
    print("Testing PerformanceMetrics...")
    
    metrics = PerformanceMetrics(
        timestamp=datetime.now(),
        cpu_percent=50.0,
        memory_mb=1024.0,
        throughput=100.0,
        latency_ms=50.0,
        error_rate=0.01,
        queue_depth=10,
    )
    
    data = metrics.to_dict()
    assert data["cpu_percent"] == 50.0
    assert data["memory_mb"] == 1024.0
    
    print("  [OK] PerformanceMetrics tests passed")
    return True


def test_optimization_suggestion():
    """Test OptimizationSuggestion data class"""
    print("Testing OptimizationSuggestion...")
    
    suggestion = OptimizationSuggestion(
        type=OptimizationType.CACHING,
        description="Cache frequent operations",
        priority=8,
        expected_improvement=25.0,
        implementation="Use CacheManager",
    )
    
    data = suggestion.to_dict()
    assert data["type"] == "CACHING"
    assert data["priority"] == 8
    
    print("  [OK] OptimizationSuggestion tests passed")
    return True


def test_stream_chunk():
    """Test StreamChunk data class"""
    print("Testing StreamChunk...")
    
    chunk = StreamChunk(
        data="test data",
        sequence=1,
        timestamp=datetime.now(),
        is_last=False,
    )
    
    data = chunk.to_dict()
    assert data["sequence"] == 1
    assert data["is_last"] is False
    
    print("  [OK] StreamChunk tests passed")
    return True


def test_async_task_result():
    """Test AsyncTaskResult data class"""
    print("Testing AsyncTaskResult...")
    
    result = AsyncTaskResult(
        task_id="test_1",
        success=True,
        result="output",
        error=None,
        duration_ms=100.0,
        timestamp=datetime.now(),
    )
    
    data = result.to_dict()
    assert data["task_id"] == "test_1"
    assert data["success"] is True
    
    print("  [OK] AsyncTaskResult tests passed")
    return True


def test_streaming_handler_creation():
    """Test StreamingHandler creation"""
    print("Testing StreamingHandler Creation...")
    
    handler = StreamingHandler(chunk_size=100, max_queue_size=1000)
    assert handler.chunk_size == 100
    assert handler.max_queue_size == 1000
    
    print("  [OK] StreamingHandler creation tests passed")
    return True


def test_streaming_handler_write():
    """Test StreamingHandler write"""
    print("Testing StreamingHandler Write...")
    
    handler = StreamingHandler()
    
    # Write single item
    success = handler.write("data1")
    assert success is True
    
    # Check queue
    stats = handler.get_stats()
    assert stats["queue_depth"] == 1
    
    print("  [OK] StreamingHandler write tests passed")
    return True


def test_streaming_handler_write_batch():
    """Test StreamingHandler batch write"""
    print("Testing StreamingHandler Batch Write...")
    
    handler = StreamingHandler()
    data = ["item1", "item2", "item3"]
    
    written = handler.write_batch(data)
    assert written == 3
    
    stats = handler.get_stats()
    assert stats["queue_depth"] == 3
    
    print("  [OK] StreamingHandler batch write tests passed")
    return True


def test_streaming_handler_process():
    """Test StreamingHandler process"""
    print("Testing StreamingHandler Process...")
    
    handler = StreamingHandler()
    processed = []
    
    def collect(chunk):
        processed.append(chunk.data)
    
    handler.add_handler(collect)
    handler.write("data1")
    handler.write("data2")
    
    # Process all
    count = handler.process_all()
    assert count == 2
    assert "data1" in processed
    assert "data2" in processed
    
    print("  [OK] StreamingHandler process tests passed")
    return True


def test_streaming_handler_backpressure():
    """Test StreamingHandler backpressure"""
    print("Testing StreamingHandler Backpressure...")
    
    handler = StreamingHandler(max_queue_size=10, backpressure_threshold=0.5)
    
    # Fill queue to 60% (above 50% threshold)
    for i in range(6):
        handler.write(f"data{i}")
    
    assert handler.is_backpressured() is True
    
    # Clear queue
    handler.clear()
    assert handler.is_backpressured() is False
    
    print("  [OK] StreamingHandler backpressure tests passed")
    return True


def test_streaming_handler_stats():
    """Test StreamingHandler statistics"""
    print("Testing StreamingHandler Stats...")
    
    handler = StreamingHandler()
    handler.write("data")
    
    stats = handler.get_stats()
    assert "queue_depth" in stats
    assert "total_chunks" in stats
    assert stats["total_chunks"] == 1
    
    print("  [OK] StreamingHandler stats tests passed")
    return True


def test_async_executor_creation():
    """Test AsyncExecutor creation"""
    print("Testing AsyncExecutor Creation...")
    
    executor = AsyncExecutor(max_workers=2)
    assert executor.max_workers == 2
    
    executor.shutdown()
    
    print("  [OK] AsyncExecutor creation tests passed")
    return True


def test_async_executor_submit():
    """Test AsyncExecutor submit"""
    print("Testing AsyncExecutor Submit...")
    
    executor = AsyncExecutor(max_workers=2)
    
    def task():
        time.sleep(0.01)
        return "result"
    
    task_id = executor.submit(task)
    assert task_id.startswith("task_")
    
    # Wait for completion
    result = executor.get_result(task_id, timeout=1.0)
    assert result is not None
    assert result.success is True
    assert result.result == "result"
    
    executor.shutdown()
    
    print("  [OK] AsyncExecutor submit tests passed")
    return True


def test_async_executor_error():
    """Test AsyncExecutor error handling"""
    print("Testing AsyncExecutor Error...")
    
    executor = AsyncExecutor(max_workers=2)
    
    def failing_task():
        raise ValueError("Test error")
    
    task_id = executor.submit(failing_task)
    result = executor.get_result(task_id, timeout=1.0)
    
    assert result is not None
    assert result.success is False
    assert "Test error" in result.error
    
    executor.shutdown()
    
    print("  [OK] AsyncExecutor error tests passed")
    return True


def test_async_executor_submit_many():
    """Test AsyncExecutor submit many"""
    print("Testing AsyncExecutor Submit Many...")
    
    executor = AsyncExecutor(max_workers=4)
    
    def task(n):
        time.sleep(0.01)
        return n * 2
    
    tasks = [
        (task, (1,), {}),
        (task, (2,), {}),
        (task, (3,), {}),
    ]
    
    task_ids = executor.submit_many(tasks)
    assert len(task_ids) == 3
    
    results = executor.get_results(task_ids, timeout=2.0)
    assert len(results) == 3
    assert all(r.success for r in results)
    
    executor.shutdown()
    
    print("  [OK] AsyncExecutor submit many tests passed")
    return True


def test_async_executor_stats():
    """Test AsyncExecutor statistics"""
    print("Testing AsyncExecutor Stats...")
    
    executor = AsyncExecutor(max_workers=2)
    
    def task():
        time.sleep(0.05)
        return "done"
    
    executor.submit(task)
    executor.submit(task)
    
    stats = executor.get_stats()
    assert stats["workers"] == 2
    assert stats["total_tasks"] >= 2
    
    executor.shutdown()
    
    print("  [OK] AsyncExecutor stats tests passed")
    return True


def test_cache_manager_creation():
    """Test CacheManager creation"""
    print("Testing CacheManager Creation...")
    
    cache = CacheManager(max_size=100, ttl_seconds=60)
    assert cache.max_size == 100
    assert cache.ttl_seconds == 60
    
    print("  [OK] CacheManager creation tests passed")
    return True


def test_cache_manager_get_set():
    """Test CacheManager get/set"""
    print("Testing CacheManager Get/Set...")
    
    cache = CacheManager()
    
    # Set value
    cache.set("key1", "value1")
    
    # Get value
    value = cache.get("key1")
    assert value == "value1"
    
    # Get non-existent
    value = cache.get("nonexistent")
    assert value is None
    
    print("  [OK] CacheManager get/set tests passed")
    return True


def test_cache_manager_cached_decorator():
    """Test CacheManager cached decorator"""
    print("Testing CacheManager Cached Decorator...")
    
    cache = CacheManager()
    call_count = 0
    
    @cache.cached
    def expensive_function(x):
        nonlocal call_count
        call_count += 1
        return x * x
    
    # First call
    result1 = expensive_function(5)
    assert result1 == 25
    assert call_count == 1
    
    # Second call (cached)
    result2 = expensive_function(5)
    assert result2 == 25
    assert call_count == 1  # Not called again
    
    print("  [OK] CacheManager cached decorator tests passed")
    return True


def test_cache_manager_stats():
    """Test CacheManager statistics"""
    print("Testing CacheManager Stats...")
    
    cache = CacheManager()
    
    # Miss
    cache.get("key1")
    
    # Hit
    cache.set("key1", "value1")
    cache.get("key1")
    
    stats = cache.get_stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    assert stats["hit_rate"] == 0.5
    
    print("  [OK] CacheManager stats tests passed")
    return True


def test_cache_manager_invalidate():
    """Test CacheManager invalidate"""
    print("Testing CacheManager Invalidate...")
    
    cache = CacheManager()
    cache.set("key1", "value1")
    
    # Invalidate existing
    success = cache.invalidate("key1")
    assert success is True
    assert cache.get("key1") is None
    
    # Invalidate non-existent
    success = cache.invalidate("nonexistent")
    assert success is False
    
    print("  [OK] CacheManager invalidate tests passed")
    return True


def test_performance_monitor_creation():
    """Test PerformanceMonitor creation"""
    print("Testing PerformanceMonitor Creation...")
    
    monitor = PerformanceMonitor(history_size=500)
    assert monitor.history_size == 500
    
    print("  [OK] PerformanceMonitor creation tests passed")
    return True


def test_performance_monitor_start_stop():
    """Test PerformanceMonitor start/stop"""
    print("Testing PerformanceMonitor Start/Stop...")
    
    monitor = PerformanceMonitor()
    
    monitor.start()
    assert monitor._running is True
    assert monitor._start_time is not None
    
    monitor.stop()
    assert monitor._running is False
    
    print("  [OK] PerformanceMonitor start/stop tests passed")
    return True


def test_performance_monitor_record():
    """Test PerformanceMonitor record"""
    print("Testing PerformanceMonitor Record...")
    
    monitor = PerformanceMonitor()
    
    metrics = PerformanceMetrics(
        timestamp=datetime.now(),
        cpu_percent=50.0,
        memory_mb=1024.0,
        throughput=100.0,
        latency_ms=50.0,
        error_rate=0.01,
        queue_depth=10,
    )
    
    monitor.record(metrics)
    
    history = monitor.get_history()
    assert len(history) == 1
    assert history[0].cpu_percent == 50.0
    
    print("  [OK] PerformanceMonitor record tests passed")
    return True


def test_performance_monitor_average():
    """Test PerformanceMonitor average"""
    print("Testing PerformanceMonitor Average...")
    
    monitor = PerformanceMonitor()
    
    # Record multiple metrics
    for i in range(5):
        metrics = PerformanceMetrics(
            timestamp=datetime.now(),
            cpu_percent=float(i * 10),
            memory_mb=1000.0,
            throughput=100.0,
            latency_ms=50.0,
            error_rate=0.01,
            queue_depth=10,
        )
        monitor.record(metrics)
    
    avg = monitor.get_average(window=5)
    assert avg is not None
    assert avg.cpu_percent == 20.0  # Average of 0, 10, 20, 30, 40
    
    print("  [OK] PerformanceMonitor average tests passed")
    return True


def test_performance_monitor_performance_level():
    """Test PerformanceMonitor performance level"""
    print("Testing PerformanceMonitor Performance Level...")
    
    monitor = PerformanceMonitor()
    
    # Record high CPU metrics
    for _ in range(5):
        metrics = PerformanceMetrics(
            timestamp=datetime.now(),
            cpu_percent=95.0,
            memory_mb=1000.0,
            throughput=100.0,
            latency_ms=50.0,
            error_rate=0.01,
            queue_depth=10,
        )
        monitor.record(metrics)
    
    level = monitor.get_performance_level()
    # High CPU (95%) means low score (5%), should be CRITICAL
    assert level == PerformanceLevel.CRITICAL
    
    print("  [OK] PerformanceMonitor performance level tests passed")
    return True


def test_performance_monitor_stats():
    """Test PerformanceMonitor statistics"""
    print("Testing PerformanceMonitor Stats...")
    
    monitor = PerformanceMonitor()
    monitor.start()
    
    metrics = PerformanceMetrics(
        timestamp=datetime.now(),
        cpu_percent=50.0,
        memory_mb=1000.0,
        throughput=100.0,
        latency_ms=50.0,
        error_rate=0.01,
        queue_depth=10,
    )
    monitor.record(metrics)
    
    stats = monitor.get_stats()
    assert stats["samples"] == 1
    assert stats["running"] is True
    
    print("  [OK] PerformanceMonitor stats tests passed")
    return True


def test_factory_functions():
    """Test factory functions"""
    print("Testing Factory Functions...")
    
    # Streaming handler
    handler = create_streaming_handler(chunk_size=500)
    assert isinstance(handler, StreamingHandler)
    assert handler.chunk_size == 500
    
    # Async executor
    executor = create_async_executor(max_workers=2)
    assert isinstance(executor, AsyncExecutor)
    executor.shutdown()
    
    # Cache manager
    cache = create_cache_manager(max_size=50)
    assert isinstance(cache, CacheManager)
    assert cache.max_size == 50
    
    # Performance monitor
    monitor = create_performance_monitor(history_size=200)
    assert isinstance(monitor, PerformanceMonitor)
    assert monitor.history_size == 200
    
    print("  [OK] Factory functions tests passed")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Performance Optimization System v6.5 - Test Suite")
    print("High Standard: 100% Pass Rate")
    print("=" * 60)
    
    tests = [
        test_performance_level_enum,
        test_optimization_type_enum,
        test_performance_metrics,
        test_optimization_suggestion,
        test_stream_chunk,
        test_async_task_result,
        test_streaming_handler_creation,
        test_streaming_handler_write,
        test_streaming_handler_write_batch,
        test_streaming_handler_process,
        test_streaming_handler_backpressure,
        test_streaming_handler_stats,
        test_async_executor_creation,
        test_async_executor_submit,
        test_async_executor_error,
        test_async_executor_submit_many,
        test_async_executor_stats,
        test_cache_manager_creation,
        test_cache_manager_get_set,
        test_cache_manager_cached_decorator,
        test_cache_manager_stats,
        test_cache_manager_invalidate,
        test_performance_monitor_creation,
        test_performance_monitor_start_stop,
        test_performance_monitor_record,
        test_performance_monitor_average,
        test_performance_monitor_performance_level,
        test_performance_monitor_stats,
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
