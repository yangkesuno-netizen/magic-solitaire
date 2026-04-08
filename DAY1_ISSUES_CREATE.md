# Day 1 Issues - GitHub Issues 批量创建脚本

**用途**: 使用 GitHub CLI (`gh`) 批量创建 Day 1 任务

---

## 前置要求

1. 安装 GitHub CLI: https://cli.github.com/
2. 登录 GitHub: `gh auth login`
3. 创建仓库: `gh repo create magic-solitaire --private`

---

## 创建 Issue 命令

### Issue #1: 项目 setup

```bash
gh issue create \
  --title "[Feature] 项目 setup - 初始化 Phaser 3 + TypeScript + Vite" \
  --body-file "issues/01-project-setup.md" \
  --label "feature,devbot,P0" \
  --assignee "your-username"
```

### Issue #2: Card 类实现

```bash
gh issue create \
  --title "[Feature] 实现 Card 类 - 卡牌对象基础功能" \
  --body-file "issues/02-card-class.md" \
  --label "feature,devbot,P0" \
  --assignee "your-username"
```

### Issue #3: CardStack 类

```bash
gh issue create \
  --title "[Feature] 实现 CardStack 类 - 牌堆管理" \
  --body-file "issues/03-cardstack-class.md" \
  --label "feature,devbot,P0" \
  --assignee "your-username"
```

### Issue #4: Tri-Peaks 规则

```bash
gh issue create \
  --title "[Feature] 实现 Tri-Peaks 消除规则" \
  --body-file "issues/04-tripeaks-rules.md" \
  --label "feature,devbot,P0" \
  --assignee "your-username"
```

### Issue #5: 基础 UI

```bash
gh issue create \
  --title "[Feature] 基础 UI - 游戏流程界面" \
  --body-file "issues/05-basic-ui.md" \
  --label "feature,devbot,P1" \
  --assignee "your-username"
```

### Issue #6: 卡牌背面设计

```bash
gh issue create \
  --title "[Art] 卡牌背面设计 - 魔法学院风格" \
  --body-file "issues/06-card-back-art.md" \
  --label "art,artbot,P1" \
  --assignee "your-username"
```

### Issue #7: 背景图生成

```bash
gh issue create \
  --title "[Art] 背景图生成 (5 张) - 魔法学院场景" \
  --body-file "issues/07-background-art.md" \
  --label "art,artbot,P1" \
  --assignee "your-username"
```

### Issue #8: 关卡配置

```bash
gh issue create \
  --title "[Design] 生成 50 关 Tri-Peaks 配置" \
  --body-file "issues/08-level-design.md" \
  --label "design,designbot,P1" \
  --assignee "your-username"
```

### Issue #9: 核心玩法测试

```bash
gh issue create \
  --title "[Test] 核心玩法测试 - 单元测试 + E2E" \
  --body-file "issues/09-core-gameplay-test.md" \
  --label "test,testbot,P0" \
  --assignee "your-username"
```

---

## 批量创建脚本

```bash
#!/bin/bash

# Create issues directory
mkdir -p issues

# Copy issue templates
cp .github/ISSUE_TEMPLATE/*.md issues/

# Create all Day 1 issues
echo "Creating Day 1 issues..."

gh issue create --title "[Feature] 项目 setup - 初始化 Phaser 3 + TypeScript + Vite" --body-file "issues/01-project-setup.md" --label "feature,devbot,P0"
gh issue create --title "[Feature] 实现 Card 类 - 卡牌对象基础功能" --body-file "issues/02-card-class.md" --label "feature,devbot,P0"
gh issue create --title "[Feature] 实现 CardStack 类 - 牌堆管理" --body-file "issues/03-cardstack-class.md" --label "feature,devbot,P0"
gh issue create --title "[Feature] 实现 Tri-Peaks 消除规则" --body-file "issues/04-tripeaks-rules.md" --label "feature,devbot,P0"
gh issue create --title "[Feature] 基础 UI - 游戏流程界面" --body-file "issues/05-basic-ui.md" --label "feature,devbot,P1"
gh issue create --title "[Art] 卡牌背面设计 - 魔法学院风格" --body-file "issues/06-card-back-art.md" --label "art,artbot,P1"
gh issue create --title "[Art] 背景图生成 (5 张) - 魔法学院场景" --body-file "issues/07-background-art.md" --label "art,artbot,P1"
gh issue create --title "[Design] 生成 50 关 Tri-Peaks 配置" --body-file "issues/08-level-design.md" --label "design,designbot,P1"
gh issue create --title "[Test] 核心玩法测试 - 单元测试 + E2E" --body-file "issues/09-core-gameplay-test.md" --label "test,testbot,P0"

echo "✅ All Day 1 issues created!"
```

---

## 手动创建 (无 GitHub CLI)

如果不想安装 GitHub CLI，可以:

1. 进入 GitHub 仓库
2. 点击 "Issues" → "New issue"
3. 选择合适的模板
4. 复制下方详细内容
5. 添加标签和分配

详细内容见下方各 Issue 文件。

---

## 下一步

1. ✅ 阅读本配置文档
2. ⏳ 安装 GitHub CLI (可选)
3. ⏳ 创建 GitHub 仓库
4. ⏳ 创建 Day 1 Issues
5. ⏳ 开始开发!

---

**预计时间**: 15 分钟  
**难度**: ⭐⭐☆☆☆
