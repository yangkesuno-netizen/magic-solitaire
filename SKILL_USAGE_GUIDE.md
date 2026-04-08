# Skill 使用规范

**核心原则：使用任何 Skill 前，必须先读 SKILL.md！**

---

## 📖 标准使用流程

### 步骤 1：查找 Skill
```bash
# 查看已安装的 Skill
ls active_skills/
# 或
ls ~/.codex/skills/
```

### 步骤 2：阅读文档（必须！）
```bash
# 阅读 SKILL.md
read_file active_skills/{skill-name}/SKILL.md
```

**必读内容**：
- [ ] 使用方法（Usage）
- [ ] 参数说明（Parameters）
- [ ] API Key 配置
- [ ] 示例命令
- [ ] 常见错误

### 步骤 3：检查环境
```bash
# 检查依赖
command -v uv
command -v python

# 检查 API Key
echo $GEMINI_API_KEY
echo $ZHIPU_API_KEY

# 检查路径
ls active_skills/{skill-name}/scripts/
```

### 步骤 4：执行命令
```bash
# 严格按照文档示例执行
uv run ~/.codex/skills/{skill-name}/scripts/xxx.py --arg value
```

### 步骤 5：验证结果
```bash
# 检查输出文件
ls -la output.png
# 或查看日志
```

---

## 🚫 常见错误（不再犯！）

### ❌ 错误 1：不读文档直接用
**今天犯的错**：
- 没用过 nano-banana-pro
- 不知道脚本路径
- 自己写脚本调用 API，失败

**正确做法**：
```bash
# 先读文档
read_file active_skills/nano-banana-pro/SKILL.md

# 文档明确写了：
# uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "..."
```

### ❌ 错误 2：不检查 API 额度
**今天犯的错**：
- 智谱余额不足还不知道
- Gemini 额度用完才发现

**正确做法**：
```bash
# 使用前检查
# 智谱：登录 https://open.bigmodel.cn 查看余额
# Gemini：登录 https://aistudio.google.com 查看配额
```

### ❌ 错误 3：路径搞错
**今天犯的错**：
- 以为 Skill 在 `~/.codex/skills/`
- 实际在 `active_skills/`

**正确做法**：
```bash
# 先查找确认位置
dir /s /b SKILL.md | findstr nano-banana-pro
```

---

## 📋 Skill 使用检查清单

使用任何 Skill 前，逐项检查：

- [ ] SKILL.md 已阅读
- [ ] 使用命令已理解
- [ ] 依赖已安装（uv、python 等）
- [ ] API Key 已配置
- [ ] API 额度充足
- [ ] 脚本路径正确
- [ ] 输出路径明确
- [ ] 错误处理方法已知

---

## 🔧 已安装 Skill 清单

| Skill | 用途 | API Key | 状态 | 备注 |
|-------|------|---------|------|------|
| nano-banana-pro | 图片生成 | GEMINI_API_KEY | ⚠️ 额度用完 | 明天刷新 |
| zhipu-image | 图片生成 | ZHIPU_API_KEY | ⚠️ 余额不足 | 需充值 |
| browser_use | 浏览器自动化 | 无 | ✅ 可用 | - |
| tavily | AI 搜索 | TAVILY_API_KEY | ✅ 可用 | - |
| ... | ... | ... | ... | ... |

---

## 📝 使用记录

| 日期 | Skill | 用途 | 结果 | 备注 |
|------|-------|------|------|------|
| 2026-04-08 | nano-banana-pro | 生成卡牌 | ❌ 失败 | 路径错误 + 额度用完 |
| 2026-04-08 | zhipu-image | 生成卡牌背面 | ✅ 成功 | 余额不足 |

---

## 💡 最佳实践

### 1. 创建 Skill 速查表
```bash
# 为常用 Skill 创建快捷命令
# 例如：scripts/generate_image.bat
@echo off
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py %*
```

### 2. 统一 API Key 管理
```bash
# 在 .env 中统一管理
GEMINI_API_KEY=xxx
ZHIPU_API_KEY=xxx
TAVILY_API_KEY=xxx

# 使用前 source
source .env
```

### 3. 测试脚本
```bash
# 创建测试脚本验证 Skill 可用
# scripts/test_skills.py
import os
import subprocess

skills = ['nano-banana-pro', 'zhipu-image']
for skill in skills:
    print(f"Testing {skill}...")
    # 执行测试命令
```

---

## ⚠️ 红线

**以下情况禁止使用 Skill**：

- [ ] 未读 SKILL.md → ❌ 禁止使用
- [ ] API Key 未配置 → ❌ 禁止使用
- [ ] 额度未知 → ❌ 禁止使用
- [ ] 路径不确定 → ❌ 禁止使用

---

**创建日期**: 2026-04-08  
**强制执行**: ✅ 是  
**违反后果**: 复盘 + 重新学习
