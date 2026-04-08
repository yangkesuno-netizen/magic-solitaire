"""
v6.9 Ultimate System - Usage Example
Demonstrates how to use the ultimate coordination system for 3D Chess development
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from v6_9 import UltimateCoordinationSystem, TaskContext, execute_task


def example_basic_usage():
    """Basic usage example"""
    print("=" * 70)
    print("Example 1: Basic Task Execution")
    print("=" * 70)
    
    # Create system
    system = UltimateCoordinationSystem(
        project_path=".",
        enable_learning=True,
        enable_retrospection=True,
    )
    
    # Execute task
    result = system.execute(
        name="Implement Spectator Mode",
        description="Create real-time spectator functionality for 3D chess",
        requirements={
            "fps": 60,
            "latency_ms": 100,
            "max_spectators": 100,
        },
        design_doc="docs/spectator_design.md",
    )
    
    print(f"\nResult: {'SUCCESS' if result.success else 'FAILED'}")
    print(f"Quality Score: {result.quality_score:.1f}/10.0")
    print(f"Duration: {result.duration_seconds}s")
    
    return result


def example_convenience_function():
    """Using convenience function"""
    print("\n" + "=" * 70)
    print("Example 2: Convenience Function")
    print("=" * 70)
    
    result = execute_task(
        name="Fix AI Engine Bug",
        description="Fix the minimax algorithm issue in AI engine",
        requirements={"priority": "high", "test_coverage": 0.9},
        project_path=".",
    )
    
    print(f"\nResult: {'SUCCESS' if result.success else 'FAILED'}")
    print(f"Quality Score: {result.quality_score:.1f}/10.0")
    
    return result


def example_evolution_tracking():
    """Track system evolution"""
    print("\n" + "=" * 70)
    print("Example 3: Evolution Tracking")
    print("=" * 70)
    
    system = UltimateCoordinationSystem()
    
    # Execute multiple tasks
    tasks = [
        ("Task 1", "Description 1"),
        ("Task 2", "Description 2"),
        ("Task 3", "Description 3"),
    ]
    
    for name, desc in tasks:
        system.execute(name=name, description=desc)
    
    # Get evolution status
    evolution = system.get_evolution_status()
    
    print(f"\nEvolution Status:")
    print(f"  Total Tasks: {evolution.total_tasks}")
    print(f"  Successful: {evolution.successful_tasks}")
    print(f"  Failed: {evolution.failed_tasks}")
    print(f"  Average Quality: {evolution.average_quality:.1f}")
    print(f"  Success Rate: {evolution.successful_tasks/evolution.total_tasks*100:.1f}%")


def example_task_history():
    """Access task history"""
    print("\n" + "=" * 70)
    print("Example 4: Task History")
    print("=" * 70)
    
    system = UltimateCoordinationSystem()
    
    # Execute some tasks
    system.execute(name="Task A", description="Test task A")
    system.execute(name="Task B", description="Test task B")
    
    # Get history
    history = system.get_task_history()
    
    print(f"\nTask History ({len(history)} tasks):")
    for i, task in enumerate(history, 1):
        status = "SUCCESS" if task.success else "FAILED"
        print(f"  {i}. {task.task_name}: {status} ({task.quality_score:.1f})")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("v6.9 Ultimate System - Usage Examples")
    print("=" * 70 + "\n")
    
    # Run examples
    example_basic_usage()
    example_convenience_function()
    example_evolution_tracking()
    example_task_history()
    
    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
