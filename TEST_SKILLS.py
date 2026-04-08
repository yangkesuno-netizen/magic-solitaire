#!/usr/bin/env python3
"""
Skills 功能测试脚本
测试各个 skill 是否可用
"""

import os
import sys
import subprocess
from pathlib import Path

COPAW_DIR = r"C:\Users\User\.copaw"
ACTIVE_SKILLS = Path(COPAW_DIR) / "active_skills"

def check_skill_readme(skill_name):
    """检查 skill 的 README/SKILL.md"""
    skill_dir = ACTIVE_SKILLS / skill_name
    readme_files = ["SKILL.md", "README.md", "readme.md"]
    for rf in readme_files:
        if (skill_dir / rf).exists():
            return True, rf
    return False, None

def check_skill_scripts(skill_name):
    """检查 skill 是否有可执行脚本"""
    skill_dir = ACTIVE_SKILLS / skill_name
    scripts_dir = skill_dir / "scripts"
    
    if scripts_dir.exists():
        py_files = list(scripts_dir.glob("*.py"))
        sh_files = list(scripts_dir.glob("*.sh"))
        return len(py_files) + len(sh_files) > 0, py_files + sh_files
    
    # Check root for scripts
    py_files = list(skill_dir.glob("*.py"))
    return len(py_files) > 0, py_files

def test_skill(skill_name):
    """测试单个 skill"""
    skill_dir = ACTIVE_SKILLS / skill_name
    
    if not skill_dir.exists():
        return {"exists": False, "status": "MISSING"}
    
    result = {
        "exists": True,
        "has_readme": False,
        "readme_file": None,
        "has_scripts": False,
        "scripts": [],
        "status": "UNKNOWN"
    }
    
    # Check README
    has_readme, readme_file = check_skill_readme(skill_name)
    result["has_readme"] = has_readme
    result["readme_file"] = readme_file
    
    # Check scripts
    has_scripts, scripts = check_skill_scripts(skill_name)
    result["has_scripts"] = has_scripts
    result["scripts"] = [str(s.name) for s in scripts]
    
    # Determine status
    if has_readme:
        result["status"] = "✅ READY"
    else:
        result["status"] = "⚠️ NO DOC"
    
    return result

def main():
    print("=" * 70)
    print("CoPaw Skills 功能测试报告")
    print("=" * 70)
    print()
    
    # Get all skills
    skills = sorted([d.name for d in ACTIVE_SKILLS.iterdir() if d.is_dir()])
    
    print(f"发现 {len(skills)} 个已激活 skills\n")
    
    # Test each skill
    ready_count = 0
    no_doc_count = 0
    
    categories = {
        "浏览器与网络": ["agent-browser", "browser_visible", "tavily", "news"],
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
    
    for category, skill_list in categories.items():
        print(f"\n## {category}")
        print("-" * 70)
        
        for skill_name in skill_list:
            if skill_name not in skills:
                print(f"  ❌ {skill_name}: NOT FOUND")
                continue
            
            result = test_skill(skill_name)
            
            if result["status"] == "✅ READY":
                ready_count += 1
                scripts_info = f" ({len(result['scripts'])} scripts)" if result["has_scripts"] else ""
                print(f"  ✅ {skill_name}: READY{scripts_info}")
            elif result["status"] == "⚠️ NO DOC":
                no_doc_count += 1
                print(f"  ⚠️  {skill_name}: NO DOCUMENTATION")
            else:
                print(f"  ❓ {skill_name}: {result['status']}")
    
    # Check for uncategorized skills
    categorized = set()
    for s in categories.values():
        categorized.update(s)
    
    uncategorized = set(skills) - categorized
    if uncategorized:
        print(f"\n## 未分类 Skills")
        print("-" * 70)
        for skill_name in sorted(uncategorized):
            result = test_skill(skill_name)
            if result["status"] == "✅ READY":
                ready_count += 1
                print(f"  ✅ {skill_name}: READY")
            else:
                print(f"  ⚠️  {skill_name}: {result['status']}")
    
    print("\n" + "=" * 70)
    print("测试总结")
    print("=" * 70)
    print(f"  总 Skills 数: {len(skills)}")
    print(f"  ✅ 完全可用: {ready_count}")
    print(f"  ⚠️  缺少文档: {no_doc_count}")
    print()
    
    # Check API keys
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
    
    for key, desc in api_keys.items():
        value = os.environ.get(key)
        if value:
            # Mask the key for security
            if "KEY" in key and len(value) > 10:
                masked = value[:8] + "..." + value[-4:]
            else:
                masked = value
            print(f"  ✅ {key}: {masked}")
        else:
            print(f"  ❌ {key}: NOT SET ({desc})")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
