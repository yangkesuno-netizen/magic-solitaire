# 小红书技能可用性检查报告

**检查时间**: 2026-04-07 13:30  
**检查范围**: 3 个已安装小红书技能  
**检查项目**: 文件完整性、依赖配置、文档质量、Windows 兼容性

---

## 📊 检查结果总览

| 技能名 | 文件完整性 | 文档质量 | 依赖配置 | Windows 兼容 | 总体状态 |
|--------|-----------|---------|---------|-------------|---------|
| **xiaohongshu** | ✅ 完整 | ✅ 优秀 | ⚠️ 需配置 | ❌ 需适配 | ⚠️ 部分可用 |
| **write-xiaohongshu** | ⚠️ 仅 SKILL.md | ✅ 优秀 | ✅ 无依赖 | ✅ 纯逻辑 | ✅ 立即可用 |
| **xiaohongshu-note-analyzer** | ⚠️ 仅 SKILL.md+参考 | ✅ 优秀 | ✅ 无依赖 | ✅ 纯逻辑 | ✅ 立即可用 |

---

## 🔍 详细检查结果

### 1️⃣ xiaohongshu (6.7K installs)

**文件结构**:
```
✅ SKILL.md (6.5KB) - 完整文档
✅ README.md (9.5KB) - 中文文档
✅ README_CN.md (11KB) - 详细说明
✅ scripts/ (15 个脚本文件)
  - search.sh, post-detail.sh, comment.sh
  - start-mcp.sh, stop-mcp.sh, status.sh
  - track-topic.py, export-long-image.py
  - mcp-call.sh (核心 MCP 调用)
✅ tools/xhs-downloader/ - 下载工具
```

**依赖要求**:
| 依赖 | 状态 | 说明 |
|------|------|------|
| `xiaohongshu-mcp` 二进制 | ❌ 未安装 | 需从 GitHub Releases 下载 |
| `xiaohongshu-login` 二进制 | ❌ 未安装 | 需从 GitHub Releases 下载 |
| `jq` | ❌ 未安装 | Windows 需安装 `choco install jq` |
| `python3` | ✅ 已安装 | C:\Users\User\AppData\Local\Microsoft\WindowsApps\python3.exe |
| `bash` | ⚠️ 需 Git Bash | 脚本为 bash 格式 |

**问题**:
1. ❌ **缺少 MCP 二进制文件** - 需下载 `xiaohongshu-mcp-windows-amd64.exe`
2. ❌ **缺少 jq 工具** - JSON 处理必需
3. ❌ **脚本为 bash 格式** - Windows 需 Git Bash 或 WSL
4. ⚠️ **需扫码登录** - 首次使用需小红书 App 扫码

**解决方案**:
```powershell
# 1. 安装 jq
choco install jq  # 或从 https://stedolan.github.io/jq/download/ 下载

# 2. 下载 MCP 二进制
# 访问 https://github.com/xpzouying/xiaohongshu-mcp/releases
# 下载 xiaohongshu-mcp-windows-amd64.exe
# 下载 xiaohongshu-login-windows-amd64.exe

# 3. 安装到 ~/.local/bin
mkdir -p $HOME\.local\bin
mv xiaohongshu-mcp-windows-amd64.exe $HOME\.local\bin\xiaohongshu-mcp.exe
mv xiaohongshu-login-windows-amd64.exe $HOME\.local\bin\xiaohongshu-login.exe

# 4. 添加到 PATH
$env:PATH += ";$HOME\.local\bin"

# 5. 登录（扫码）
$HOME\.local\bin\xiaohongshu-login.exe

# 6. 启动 MCP 服务
$HOME\.local\bin\xiaohongshu-mcp.exe
```

**可用性**: ⚠️ **需要配置后才能使用**（预计 15 分钟 setup 时间）

---

### 2️⃣ write-xiaohongshu (2.5K installs)

**文件结构**:
```
✅ SKILL.md (10.6KB) - 完整文档（298 行）
  - 包含完整流程：研究→分析→写作→发布
  - 硬性限制：标题≤20 字符，正文≤1000 字符
  - 输出模板：标题 + 正文 + 标签 + 配图
  - 依赖：xiaohongshu MCP（调用发布接口）
```

**依赖要求**:
| 依赖 | 状态 | 说明 |
|------|------|------|
| `xiaohongshu` MCP | ⚠️ 需配置 | 用于发布笔记 |
| 网络搜索 | ✅ 可用 | 使用 tavily 或其他搜索技能 |
| 图像处理 | ✅ 可选 | zhipu-image 可生成配图 |

**特点**:
- ✅ **纯逻辑技能** - 无需额外安装
- ✅ **自动调用其他技能** - tavily 搜索、xiaohongshu 发布
- ✅ **完整工作流** - 从调研到发布一站式
- ⚠️ **依赖 xiaohongshu MCP** - 发布功能需 MCP 配置

**可用性**: ✅ **立即可用**（发布功能需等待 xiaohongshu MCP 配置）

---

### 3️⃣ xiaohongshu-note-analyzer (1.8K installs)

**文件结构**:
```
✅ SKILL.md (6.1KB) - 完整文档（191 行）
✅ references/
  - analysis-examples.md (6.3KB) - 分析案例
  - keyword-strategy.md (6.3KB) - 关键词策略
  - sensitive-words.md (2.9KB) - 敏感词列表
  - title-formulas.md (3.6KB) - 标题公式
```

**分析维度**:
1. ✅ 关键词分析 - 搜索热度、布局优化
2. ✅ 标题吸引力 - 爆款公式、首段优化
3. ✅ 敏感内容风险 - 违规词检测、限流评估
4. ✅ 商业化程度 - 软广识别、自然度评分
5. ✅ 互动潜力 - 讨论点、情感共鸣
6. ✅ 内容结构 - 排版、emoji、段落节奏

**依赖要求**:
| 依赖 | 状态 | 说明 |
|------|------|------|
| 小红书笔记内容 | ✅ 用户提供 | 输入文本即可分析 |
| 敏感词库 | ✅ 内置 | references/sensitive-words.md |
| 标题公式 | ✅ 内置 | references/title-formulas.md |

**特点**:
- ✅ **完全独立** - 无需外部 API 或 MCP
- ✅ **纯文本分析** - 输入笔记内容即可
- ✅ **参考文档齐全** - 4 个专业参考文档
- ✅ **立即可用** - 无需任何配置

**可用性**: ✅ **立即可用**

---

## 🚨 关键阻塞问题

### 问题 1: xiaohongshu MCP 二进制文件缺失
**影响**: 无法使用搜索、发布、评论等核心功能  
**严重性**: 🔴 高  
**解决时间**: 15-30 分钟

**解决步骤**:
1. 访问 https://github.com/xpzouying/xiaohongshu-mcp/releases
2. 下载 Windows 版本：
   - `xiaohongshu-mcp-windows-amd64.exe`
   - `xiaohongshu-login-windows-amd64.exe`
3. 安装到 `~/.local/bin/`
4. 扫码登录
5. 启动 MCP 服务

---

### 问题 2: jq 工具缺失
**影响**: 无法安全构建 JSON 参数  
**严重性**: 🟡 中  
**解决时间**: 5 分钟

**解决方案**:
```powershell
# 方式 1: Chocolatey
choco install jq

# 方式 2: 直接下载
# https://github.com/stedolan/jq/releases
# 下载 jq-win64.exe，重命名为 jq.exe，放到 PATH 中
```

---

### 问题 3: Bash 脚本兼容性
**影响**: 无法直接运行 .sh 脚本  
**严重性**: 🟡 中  
**解决方案**:

**选项 A**: 安装 Git Bash（推荐）
```powershell
choco install git
# 使用 Git Bash 运行脚本
```

**选项 B**: 使用 WSL
```powershell
wsl --install
# 在 WSL 中运行脚本
```

**选项 C**: 手动转换脚本（不推荐，工作量大）

---

## ✅ 立即可用功能

即使不配置 xiaohongshu MCP，以下功能也可立即使用：

### 1. 小红书文案生成 (write-xiaohongshu)
- ✅ 市场调研（使用 tavily 搜索）
- ✅ 竞品分析（分析 Top 帖子）
- ✅ 文案创作（标题≤20 字，正文≤1000 字）
- ✅ 标签优化（基于关键词策略）
- ⚠️ 发布功能（需 MCP 配置）

### 2. 笔记分析 (xiaohongshu-note-analyzer)
- ✅ 内容质量评估
- ✅ 关键词优化建议
- ✅ 敏感词检测
- ✅ 标题吸引力分析
- ✅ 商业化程度评估
- ✅ 互动潜力预测

### 3. 图像生成 (zhipu-image)
- ✅ 配图生成（100 张/天免费）
- ✅ 9:16 竖版格式
- ✅ 高清质量

---

## 📋 推荐行动清单

### 立即可以做的（无需配置）
1. ✅ 使用 `write-xiaohongshu` 创作文案
2. ✅ 使用 `xiaohongshu-note-analyzer` 分析笔记
3. ✅ 使用 `zhipu-image` 生成配图
4. ✅ 使用 `tavily` 进行市场调研

### 建议配置（15-30 分钟）
1. ⏳ 安装 jq (`choco install jq`)
2. ⏳ 下载 xiaohongshu-mcp 二进制文件
3. ⏳ 安装 Git Bash (`choco install git`)
4. ⏳ 扫码登录小红书
5. ⏳ 测试 MCP 服务

### 配置后解锁功能
1. 🔓 搜索小红书笔记
2. 🔓 发布图文/视频笔记
3. 🔓 获取帖子详情和评论
4. 🔓 用户主页管理
5. 🔓 自动评论互动

---

## 🎯 总体评估

| 评估维度 | 评分 | 说明 |
|----------|------|------|
| **文件完整性** | ⭐⭐⭐⭐ | xiaohongshu 完整，其他两个仅 SKILL.md |
| **文档质量** | ⭐⭐⭐⭐⭐ | 三个技能文档都非常详细 |
| **易用性** | ⭐⭐⭐ | 两个立即可用，一个需配置 |
| **功能覆盖** | ⭐⭐⭐⭐ | 调研→创作→分析→发布（发布需配置） |
| **Windows 兼容** | ⭐⭐ | xiaohongshu 需适配，其他两个无问题 |

**总体可用性**: **75%** ⭐⭐⭐⭐

**建议**: 
- 短期：使用现有可用功能（文案生成 + 笔记分析）
- 中期：配置 xiaohongshu MCP 解锁完整功能
- 长期：考虑将 bash 脚本转换为 PowerShell 或提供 Windows 版本

---

## 📞 需要帮助？

如需协助配置 xiaohongshu MCP，请告诉我：
1. 是否已安装 Chocolatey (`choco --version`)
2. 是否愿意安装 Git Bash 或使用 WSL
3. 是否有小红书账号可用于扫码登录

我可以逐步指导完成配置！
