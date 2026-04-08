#!/usr/bin/env python3
"""
v6.9 Ultimate System - Clean Example
展示各模块如何协同配合
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from v6_9 import UltimateCoordinationSystem


def main():
    """主函数"""
    print("=" * 70)
    print("v6.9 Ultimate System - Clean Example")
    print("=" * 70)
    
    # 创建系统
    system = UltimateCoordinationSystem(
        project_path=".",
        enable_v60=True,
        enable_learning=True,
        enable_retrospection=True,
    )
    
    # 执行任务
    result = system.execute(
        name="Implement Feature",
        description="Create new feature",
        requirements={"priority": "high"},
    )
    
    # 输出结果
    print(f"\nResult: {'SUCCESS' if result.success else 'FAILED'}")
    print(f"Quality Score: {result.quality_score:.1f}/10.0")
    print(f"Duration: {result.duration_seconds}s")
    
    # 查看进化状态
    evolution = system.get_evolution_status()
    print(f"\nEvolution Status:")
    print(f"  Total Tasks: {evolution.total_tasks}")
    print(f"  Successful: {evolution.successful_tasks}")
    print(f"  Failed: {evolution.failed_tasks}")
    print(f"  Average Quality: {evolution.average_quality:.1f}")


if __name__ == "__main__":
    main()
