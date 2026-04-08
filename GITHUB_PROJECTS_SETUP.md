# GitHub Projects 任务看板配置

**项目**: Magic Solitaire  
**看板类型**: GitHub Projects (Beta)  
**自动化**: 启用  

---

## 一、看板结构

### 列设置

| 列名 | 说明 | 自动化规则 |
|------|------|-----------|
| 📋 Backlog | 未来功能池 | 新 Issue 默认进入 |
| 📝 To Do | 本周计划 | 手动拖入 |
| 🔨 In Progress | 进行中 | 分配后自动进入 |
| 👀 Review | 代码审核 | PR 创建后自动进入 |
| ✅ Done | 已完成 | PR 合并后自动进入 |

---

## 二、Issue 标签系统

### 类型标签

| 标签 | 颜色 | 说明 |
|------|------|------|
| `feature` | #0E8A16 | 新功能开发 |
| `bug` | #D73A4A | Bug 修复 |
| `test` | #FBCA04 | 测试任务 |
| `art` | #FF79C6 | 美术需求 |
| `design` | #0366D6 | 策划需求 |
| `docs` | #6A737D | 文档任务 |

### Agent 标签

| 标签 | 颜色 | 说明 |
|------|------|------|
| `devbot` | #1D76DB | DevBot 负责 |
| `testbot` | #FBCA04 | TestBot 负责 |
| `artbot` | #FF79C6 | ArtBot 负责 |
| `designbot` | #0366D6 | DesignBot 负责 |

### 优先级标签

| 标签 | 颜色 | 说明 |
|------|------|------|
| `P0` | #B60205 | 紧急 - 立即处理 |
| `P1` | #D93F0B | 高优先级 |
| `P2` | #FBCA04 | 中优先级 |
| `P3` | #0E8A16 | 低优先级 |

---

## 三、自动化规则

### Rule 1: 新 Issue 自动标记

```yaml
When:
  - Issue is opened
  
Then:
  - Add label: "backlog"
  - Add to project: "Magic Solitaire"
  - Set status: "📋 Backlog"
```

### Rule 2: 分配后自动进入 In Progress

```yaml
When:
  - Issue is assigned
  
Then:
  - Set status: "🔨 In Progress"
  - Add comment: "任务已分配，开始执行"
```

### Rule 3: PR 创建后自动进入 Review

```yaml
When:
  - Pull request is created
  
Then:
  - Set status: "👀 Review"
  - Add label: "needs-review"
  - Assign reviewer
```

### Rule 4: PR 合并后自动完成

```yaml
When:
  - Pull request is merged
  
Then:
  - Close linked issues
  - Set status: "✅ Done"
  - Add comment: "任务完成！🎉"
```

---

## 四、Week 1 任务看板

### Sprint: Week 1 (Day 1-7)

**Sprint Goal**: 完成核心玩法原型，50 关可玩

---

### 📋 Backlog (未来功能)

| # | 任务 | 类型 | 优先级 | Agent |
|---|------|------|--------|-------|
| 10 | PVP 对战系统 | feature | P3 | DevBot |
| 11 | 公会系统 | feature | P3 | DevBot |
| 12 | 每日挑战活动 | feature | P3 | DesignBot |
| 13 | 成就系统 | feature | P3 | DesignBot |

---

### 📝 To Do (本周计划)

| # | 任务 | 类型 | 优先级 | Agent | 预计 |
|---|------|------|--------|-------|------|
| 1 | 项目 setup | feature | P0 | DevBot | 4h |
| 2 | Card 类实现 | feature | P0 | DevBot | 6h |
| 3 | CardStack 类 | feature | P0 | DevBot | 4h |
| 4 | Tri-Peaks 规则 | feature | P0 | DevBot | 8h |
| 5 | 基础 UI | feature | P1 | DevBot | 6h |
| 6 | 卡牌背面设计 | art | P1 | ArtBot | 2h |
| 7 | 背景图生成 (5 张) | art | P1 | ArtBot | 4h |
| 8 | 关卡配置 (50 关) | design | P1 | DesignBot | 6h |
| 9 | 核心玩法测试 | test | P0 | TestBot | 4h |

---

### 🔨 In Progress (进行中)

*无 - 等待启动*

---

### 👀 Review (代码审核)

*无 - 等待提交*

---

### ✅ Done (已完成)

| # | 任务 | 类型 | 完成日期 | 质量评分 |
|---|------|------|---------|---------|
| 0 | AI 团队配置 | docs | 2026-04-07 | 10.0/10 |
| 0 | GitHub 仓库配置 | docs | 2026-04-07 | - |
| 0 | CI/CD 配置 | docs | 2026-04-07 | - |

---

## 五、使用指南

### 创建新 Issue

1. 点击 "New Issue"
2. 选择合适的模板 (Feature/Bug/Art/Test/Design)
3. 填写详细信息
4. 添加标签 (类型 + Agent + 优先级)
5. 分配到对应 Agent

### 移动任务

1. 拖动 Issue 到对应列
2. 或使用快捷键:
   - `b` - Backlog
   - `t` - To Do
   - `p` - In Progress
   - `r` - Review
   - `d` - Done

### 每日站会

**时间**: 每天 9:00 AM  
**内容**:
1. 查看昨日完成的 Issue (Done 列)
2. 检查进行中的 Issue (In Progress 列)
3. 分配今日任务 (移动到 To Do 列)
4. 识别阻塞问题

---

## 六、GitHub Projects 设置步骤

### Step 1: 创建 Project

1. 进入 GitHub 仓库
2. 点击 "Projects" 标签
3. 点击 "New project"
4. 选择 "Board" 模板
5. 命名: "Magic Solitaire"

### Step 2: 配置列

1. 点击 "..." → "Edit"
2. 添加 5 列: Backlog, To Do, In Progress, Review, Done
3. 设置自动化规则 (见上文)

### Step 3: 添加 Issue 模板

1. 仓库已包含 `.github/ISSUE_TEMPLATE/`
2. 自动在创建 Issue 时显示模板选择

### Step 4: 配置自动化

1. 点击 "..." → "Settings"
2. 启用 "Automations"
3. 配置上述自动化规则

---

## 七、最佳实践

### Issue 命名规范

```
[类型] 简短描述

示例:
[Feature] 实现 Card 类
[Bug] 翻转动画卡顿
[Art] 卡牌背面设计
[Test] 核心玩法测试
[Design] 50 关配置生成
```

### 评论规范

```markdown
## 进度更新 (2026-04-07 10:00)

### 今日完成
- [x] 任务项 1
- [x] 任务项 2

### 进行中
- [ ] 任务项 3 (50%)

### 遇到问题
⚠️ 问题描述

### 下一步
- [ ] 任务项 4
```

### 完成标准

- ✅ 所有验收标准满足
- ✅ 代码通过 CI/CD
- ✅ 测试覆盖率 >80%
- ✅ 人类审核通过
- ✅ 文档已更新

---

## 八、度量指标

### 每周追踪

| 指标 | 目标 | 实际 |
|------|------|------|
| 完成任务数 | 10+ | - |
| 平均完成时间 | <2 天 | - |
| Bug 数量 | <5 | - |
| 代码覆盖率 | >80% | - |

### 图表视图

1. **Cumulative Flow**: 查看任务流动
2. **Burnup Chart**: 追踪 Sprint 进度
3. **Age Report**: 识别停滞任务

---

**配置完成时间**: 2026-04-07  
**下次回顾**: 2026-04-14 (Week 1 结束)
