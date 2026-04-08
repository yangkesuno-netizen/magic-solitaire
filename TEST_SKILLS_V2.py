#!/usr/bin/env python3
"""
Skills 功能测试脚本 V2
测试各个 skill 是否可用
"""

import os
import sys
from pathlib import Path

COPAW_DIR = r"C:\Users\User\.copaw"
ACTIVE_SKILLS = Path(COPAW_DIR) / "active_skills"

def test_skill(skill_name):
    """测试单个 skill"""
    skill_dir = ACTIVE_SKILLS / skill_name
    
    if not skill_dir.exists():
        return {"exists": False, "status": "MISSING"}
    
    result = {"exists": True, "has_readme": False, "has_scripts": False, "scripts": []}
    
    # Check README
    for rf in ["SKILL.md", "README.md", "readme.md"]:
        if (skill_dir / rf).exists():
            result["has_readme"] = True
            break
    
    # Check scripts
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        result["scripts"] = [s.name for s in scripts_dir.glob("*.py")]
        result["has_scripts"] = len(result["scripts"]) > 0
    
    if result["has_readme"]:
        result["status"] = "READY"
    else:
        result["status"] = "NO_DOC"
    
    return result

def main():
    print("=" * 70)
    print("CoPaw Skills 功能测试报告")
    print("=" * 70)
    print()
    
    skills = sorted([d.name for d in ACTIVE_SKILLS.iterdir() if d.is_dir()])
    print(f"发现 {len(skills)} 个已激活 skills\n")
    
    categories = {
        "浏览器与网络": ["agent-browser", "browser_visible", "tavily", "news", "baidu-search", "desearch-web-search"],
        "文档处理": ["docx", "pdf", "pptx", "xlsx", "file_reader", "summarize"],
        "AI与图像": ["nano-banana-pro", "zhipu-image", "zhipu-image.skill"],
        "记忆管理": ["elite-longterm-memory", "neural-memory", "obsidian", "ontology"],
        "多智能体": ["multi-agent-coordination", "evolver", "self-improving", 
                    "self-improving-agent", "self-check"],
        "营销研究": ["marketing-mode", "market-research", "seo-competitor-analysis",
                    "idea-storm", "research-engine"],
        "频道通信": ["dingtalk_channel", "himalaya", "github", "cron"],
        "安全质量": ["moltguard", "skill-vetter", "humanizer"],
        "开发设计": ["frontend", "skill-creator", "find-skills", "openclaw-starter-guide"],
        "其他": ["polymarket", "desktop-control"]
    }
    
    ready_count = 0
    missing_skills = []
    
    for category, skill_list in categories.items():
        print(f"\n## {category}")
        print("-" * 70)
        
        for skill_name in skill_list:
            if skill_name not in skills:
                print(f"  [MISSING] {skill_name}")
                missing_skills.append(skill_name)
                continue
            
            result = test_skill(skill_name)
            
            if result["status"] == "READY":
                ready_count += 1
                scripts_info = f" ({len(result['scripts'])} scripts)" if result["has_scripts"] else ""
                print(f"  [READY] {skill_name}{scripts_info}")
            else:
                print(f"  [NO_DOC] {skill_name}")
    
    # Uncategorized
    categorized = set()
    for s in categories.values():
        categorized.update(s)
    uncategorized = set(skills) - categorized
    
    if uncategorized:
        print(f"\n## 未分类 Skills")
        print("-" * 70)
        for skill_name in sorted(uncategorized):
            result = test_skill(skill_name)
            if result["status"] == "READY":
                ready_count += 1
                print(f"  [READY] {skill_name}")
            else:
                print(f"  [NO_DOC] {skill_name}")
    
    print("\n" + "=" * 70)
    print("测试总结")
    print("=" * 70)
    print(f"  总 Skills 数: {len(skills)}")
    print(f"  完全可用: {ready_count}")
    print(f"  缺失技能: {len(missing_skills)}")
    if missing_skills:
        print(f"    缺失: {', '.join(missing_skills)}")
    print()
    
    # API Keys
    print("## API Keys 状态")
    print("-" * 70)
    
    api_keys = {
        "OPENAI_API_KEY": "SiliconFlow API",
        "OPENAI_BASE_URL": "API Base URL",
        "EMBEDDING_BASE_URL": "Ollama 嵌入服务",
        "EMBEDDING_MODEL_NAME": "嵌入模型名称",
        "EMBEDDING_API_KEY": "嵌入 API Key",
        "ZHIPU_API_KEY": "智谱 AI (图像生成)",
        "TAVILY_API_KEY": "Tavily 搜索",
        "GEMINI_API_KEY": "Gemini (nano-banana-pro)",
    }
    
    configured = 0
    for key, desc in api_keys.items():
        value = os.environ.get(key)
        if value:
            configured += 1
            if "KEY" in key and len(value) > 10:
                masked = value[:8] + "..." + value[-4:]
            else:
                masked = value
            print(f"  [SET] {key}: {masked}")
        else:
            print(f"  [NOT SET] {key}: ({desc})")
    
    print()
    print(f"API Keys 配置: {configured}/{len(api_keys)}")
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
