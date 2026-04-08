---
summary: "Agent 长期记忆 — 工具设置与经验教训"
read_when:
  - 手动引导工作区
---

## 工具设置

Skills 定义工具怎么用。这文件记你的具体情况 — 你独有的设置。

### 这里记什么

加上任何能帮你干活的东西。这是你的小抄。

比如：

- SSH 主机和别名
- 其他执行skills的时候，和用户相关的设置

### 示例

```markdown
### SSH

- home-server → 192.168.1.100，用户：admin
```

---

## API Keys 配置

### 已配置的 API Keys

| 服务 | 环境变量 | 状态 | 说明 |
|------|----------|------|------|
| SiliconFlow | `OPENAI_API_KEY` | ✅ 已配置 | 主 LLM API (sk-hkfs...) |
| Tavily | `TAVILY_API_KEY` | ✅ 已配置 | AI 搜索 (tvly-dev...) |
| 智谱 AI | `ZHIPU_API_KEY` | ✅ 已配置 | 图像生成 (CogView) |
| **阿里云 DashScope** | **`DASHSCOPE_API_KEY`** | **✅ 已配置** | **嵌入服务 (text-embedding-v3)** |
| Mem0 | `MEM0_API_KEY` | ⚠️ 占位符 | 自动事实提取 |

---

## 设计技能库

### 已安装的美工设计技能 (2026-03-18)

| 技能 | 来源 | 用途 | 状态 |
|------|------|------|------|
| **threejs-textures** | cloudai-x/threejs-skills | 3D纹理、材质、UV映射 | ✅ 已安装 |
| **game-ui-design** | omer-metin/skills-for-antigravity | 游戏UI/UX设计 | ✅ 已安装 |
| **software-ui-ux-design** | vasilyu1983/ai-agents-public | 软件UI/UX设计 | ✅ 已安装 |
| **bencium-innovative-ux-designer** | bencium/bencium-claude-code-design-skill | 创新UX设计 | ✅ 已安装 |
| **frontend** | 系统自带 | 前端设计、配色、字体 | ✅ 已激活 |
| **zhipu-image** | 系统自带 | AI图像生成 | ✅ 已激活 |

### 技能组合应用场景

**3D象棋游戏美工优化**:
1. `threejs-textures` - 棋盘/棋子材质、PBR纹理
2. `game-ui-design` - 游戏界面、HUD、菜单设计
3. `frontend` - 配色系统、字体、动画
4. `zhipu-image` - 生成主题概念图、素材

### 阿里云 DashScope (嵌入服务)
- **用途**: 高性能文本嵌入 (替代 Ollama)
- **Key**: `sk-dc36...8327` (32 chars)
- **Base URL**: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- **模型**: `text-embedding-v3` (1024维向量)
- **性能**: ~352ms/请求 (vs Ollama 2288ms，**快 6.5 倍**)
- **环境变量**:
  - `EMBEDDING_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1`
  - `EMBEDDING_MODEL_NAME=text-embedding-v3`
  - `EMBEDDING_API_KEY=sk-dc366fa6f2e04ceb91bdd52c4af08327`

### 智谱 AI (Zhipu)
- **用途**: 免费图像生成 (CogView-3)
- **Key**: `973ccc63...gSVI` (49 chars)
- **限制**: 100 张/天免费额度
- **文档**: https://open.bigmodel.cn/
- **Skill**: zhipu-image

### SiliconFlow
- **用途**: 主 LLM API (OpenAI 兼容)
- **Base URL**: https://api.siliconflow.cn/v1
- **Key**: `sk-hkfs...tozj`
- **特点**: 国内可用，免费额度 generous

### Tavily
- **用途**: AI 优化搜索
- **Key**: `tvly-dev...gVOh`
- **特点**: 专为 LLM 设计的搜索结果

---

## 本地服务

### Ollama (已弃用)
- **状态**: ❌ 已删除 (2026-03-18)
- **原因**: 性能过慢（2288ms），DashScope 快 6.5 倍
- **历史**: 曾部署 mxbai-embed-large (669MB) 作为本地嵌入方案
