# Solitaire 网页版开发计划 (2-4 周 MVP)

**版本**: 1.0
**生成时间**: 2026-04-07
**团队**: 1 人 + AI Agent (CoPaw v6.9)
**目标**: 2-4 周上线网页版 MVP，验证核心玩法和变现

---

## 一、开发概览

### 1.1 时间线

```
Week 1: 准备 + 核心玩法原型
Week 2: Meta 系统 + 美术
Week 3: 变现 + 数据分析 + 优化
Week 4: 测试 + 上线 + 平台提交
```

### 1.2 里程碑

| 时间 | 里程碑 | 交付物 |
|------|--------|--------|
| **Day 3** | 核心玩法可玩 | Tri-Peaks 基础关卡 |
| **Day 7** | MVP 原型完成 | 50 关 + 基础 UI |
| **Day 14** | Meta 系统完成 | 装饰 + 收集系统 |
| **Day 18** | 变现接入完成 | AdSense + 激励视频 |
| **Day 21** | 测试完成 | Bug 修复 + 性能优化 |
| **Day 28** | 正式上线 | 网站 + 平台提交 |

---

## 二、Week 1: 准备 + 核心玩法

### Day 1-2: 项目 setup

#### 任务清单

```
□ 技术选型确认
□ 开发环境搭建
□ 项目脚手架创建
□ AI Agent 配置
```

#### 技术栈

| 组件 | 选择 | 理由 |
|------|------|------|
| **游戏引擎** | Phaser 3 | 轻量、Web 优先、学习曲线低 |
| **语言** | TypeScript | 类型安全、AI 生成质量好 |
| **构建工具** | Vite | 快速开发、热更新 |
| **托管** | Vercel | 免费、自动部署 |
| **版本控制** | GitHub | 免费、AI 友好 |

#### AI Agent 分工

| Agent | 任务 | 输出 |
|-------|------|------|
| **开发 Agent** | 项目脚手架、构建配置 | 可运行项目 |
| **文件管理** | 目录结构、配置文件 | 规范化项目 |

#### 执行命令 (AI Agent 辅助)

```bash
# 1. 创建项目
npm create vite@latest magic-solitaire -- --template vanilla-ts

# 2. 安装 Phaser
npm install phaser

# 3. 安装依赖
npm install -D typescript @types/node

# 4. 初始化 Git
git init
git add .
git commit -m "Initial commit"
```

#### 目录结构

```
magic-solitaire/
├── public/
│   ├── assets/
│   │   ├── cards/          # 卡牌素材
│   │   ├── backgrounds/    # 背景图
│   │   ├── ui/             # UI 元素
│   │   └── audio/          # 音效
│   └── ads.txt             # AdSense 配置
├── src/
│   ├── scenes/
│   │   ├── BootScene.ts    # 加载场景
│   │   ├── MenuScene.ts    # 主菜单
│   │   ├── GameScene.ts    # 游戏主场景
│   │   └── UIScene.ts      # UI 层
│   ├── objects/
│   │   ├── Card.ts         # 卡牌类
│   │   ├── CardStack.ts    # 牌堆类
│   │   └── Foundation.ts   # 基础堆类
│   ├── config/
│   │   ├── gameConfig.ts   # 游戏配置
│   │   └── levelData.ts    # 关卡数据
│   ├── utils/
│   │   ├── cardUtils.ts    # 卡牌工具
│   │   └── storage.ts      # 本地存储
│   ├── styles/
│   │   └── main.css        # 样式
│   └── main.ts             # 入口文件
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

---

### Day 3-5: 核心玩法开发

#### 任务清单

```
□ Tri-Peaks 玩法规则实现
□ 卡牌系统 (发牌、选牌、消除)
□ 关卡生成逻辑
□ 基础 UI (分数、步数、关卡)
□ 胜利/失败判定
```

#### 核心功能详解

**1. Tri-Peaks 规则**

```typescript
// Tri-Peaks 规则:
// - 牌堆顶部卡牌为"目标牌"
// - 玩家可选择比目标牌大 1 或小 1 的卡牌
// - 消除所有卡牌 = 通关
// - 无牌可消 = 失败

// 示例: 目标牌是 7，玩家可消 6 或 8
```

**2. 卡牌类 (Card.ts)**

```typescript
// AI Agent 生成任务:
// - 卡牌属性：花色、点数、位置、状态
// - 卡牌方法：翻转、移动、高亮、消除
// - 卡牌动画：翻转动画、消除特效
```

**3. 关卡生成**

```typescript
// Tri-Peaks 布局:
// Row 1: 3 张牌 (峰顶)
// Row 2: 6 张牌
// Row 3: 10 张牌
// 牌堆：剩余卡牌

// AI 生成 100 个不同关卡布局
```

#### AI Agent 分工

| Agent | 任务 | 预计时间 |
|-------|------|---------|
| **开发 Agent** | Card 类实现 | 2 小时 |
| **开发 Agent** | GameScene 实现 | 3 小时 |
| **开发 Agent** | 关卡生成逻辑 | 2 小时 |
| **测试 Agent** | 玩法测试 | 1 小时 |
| **人类** | Code Review + 调整 | 1 小时 |

#### Day 5 验收标准

```
✅ 可完整玩一局 Tri-Peaks
✅ 50 个关卡可玩
✅ 分数系统正常
✅ 胜利/失败判定正确
✅ 无严重 Bug
```

---

### Day 6-7: 基础 UI/UX

#### 任务清单

```
□ 主菜单界面
□ 关卡选择界面
□ 游戏内 UI (分数、步数、重置)
□ 设置界面 (音效、音乐开关)
□ 响应式适配 (手机/平板/桌面)
```

#### UI 设计规范

| 元素 | 规范 |
|------|------|
| **字体** | Google Fonts (Nunito/Rubik) |
| **配色** | 魔法主题 (紫色/金色/深蓝) |
| **按钮** | 大尺寸 (移动端友好) |
| **动画** | 流畅 (60fps) |
| **适配** | 响应式 (320px - 1920px) |

#### AI Agent 分工

| Agent | 任务 | 输出 |
|-------|------|------|
| **美术 Agent** | UI 元素生成 (按钮、图标) | PNG/SVG |
| **开发 Agent** | UI 场景实现 | TypeScript |
| **开发 Agent** | 响应式适配 | CSS |

#### Day 7 验收标准 (MVP 原型)

```
✅ 主菜单可进入关卡选择
✅ 50 关可玩
✅ 完整 UI 流程
✅ 移动端适配良好
✅ 可部署到 Vercel 测试
```

---

## 三、Week 2: Meta 系统 + 美术

### Day 8-10: Meta 系统开发

#### 任务清单

```
□ 装饰系统 (魔法学院主题)
□ 收集系统 (魔法生物/咒语书)
□ 货币系统 (金币/宝石)
□ 商店系统 (购买装饰)
□ 任务系统 (每日任务)
```

#### 装饰系统设计

```typescript
// 装饰物类型:
// - 建筑：图书馆、塔楼、温室
// - 植物：魔法花、发光树
// - 装饰：水晶球、魔法书、坩埚
// - 角色：猫头鹰、黑猫、学徒

// 装饰物属性:
// - 价格 (金币/宝石)
// - 稀有度 (普通/稀有/史诗)
// - 解锁条件 (关卡进度)
```

#### 收集系统设计

```typescript
// 收集册:
// - 魔法生物册 (50 种生物)
// - 咒语书 (30 个咒语)
// - 成就系统 (100 个成就)

// 获取方式:
// - 关卡奖励
// - 任务完成
// - 商店购买
// - 活动限定
```

#### AI Agent 分工

| Agent | 任务 | 预计时间 |
|-------|------|---------|
| **开发 Agent** | 装饰系统逻辑 | 3 小时 |
| **开发 Agent** | 商店系统 | 2 小时 |
| **开发 Agent** | 任务系统 | 2 小时 |
| **美术 Agent** | 装饰物素材 (20 个) | 4 小时 |
| **策划 Agent** | 关卡奖励配置 | 1 小时 |

#### Day 10 验收标准

```
✅ 装饰系统可购买/放置
✅ 收集册可查看
✅ 货币系统正常 (赚取/消费)
✅ 每日任务可完成
✅ 数据本地存储
```

---

### Day 11-14: 美术资源

#### 任务清单

```
□ 卡牌素材 (52 张 + 背面)
□ 背景图 (主菜单、关卡、装饰场景)
□ UI 元素 (按钮、图标、边框)
□ 装饰物素材 (30-50 个)
□ 特效 (消除、胜利、升级)
□ 音效 (翻牌、消除、胜利、BGM)
```

#### 美术风格

| 元素 | 风格 | 参考 |
|------|------|------|
| **整体** | 魔法学院 | 哈利波特、魔法学院 |
| **色彩** | 紫色/金色/深蓝 | 神秘、高贵 |
| **卡牌** | 经典 + 魔法边框 | 传统纸牌 + 魔法元素 |
| **装饰** | 卡通渲染 | 轻松、可爱 |

#### AI 生成美术 (智谱 AI / Nano Banana Pro)

```python
# 卡牌背面生成 prompt:
"Magic themed playing card back design, 
purple and gold colors, mystical symbols, 
vector style, game asset, high quality"

# 背景图生成 prompt:
"Magic academy courtyard at sunset, 
fantasy castle in background, warm lighting, 
game background art, mobile game style"

# 装饰物生成 prompt:
"Magic crystal ball with glowing effect, 
cartoon style, game asset, white background"
```

#### 美术资源清单

| 类型 | 数量 | 来源 | 时间 |
|------|------|------|------|
| 卡牌 | 54 张 | AI 生成 | 4 小时 |
| 背景 | 5 张 | AI 生成 | 2 小时 |
| UI 元素 | 30 个 | AI 生成 + Canva | 4 小时 |
| 装饰物 | 30 个 | AI 生成 | 6 小时 |
| 特效 | 10 个 | AI 生成/开源 | 2 小时 |
| 音效 | 15 个 | 开源/免费 | 1 小时 |
| **总计** | | | **19 小时** |

#### 免费音效资源

| 网站 | 用途 | 链接 |
|------|------|------|
| **Freesound** | 音效 | freesound.org |
| **OpenGameArt** | 音效 + 音乐 | opengameart.org |
| **Kenney** | 游戏素材 | kenney.nl |
| **itch.io 免费包** | 素材包 | itch.io/game-assets |

#### Day 14 验收标准

```
✅ 所有美术资源到位
✅ 美术风格统一
✅ 素材优化 (文件大小、格式)
✅ 游戏内正确显示
✅ 加载速度快
```

---

## 四、Week 3: 变现 + 数据分析

### Day 15-17: 广告变现接入

#### 任务清单

```
□ Google AdSense 申请
□ 展示广告接入 (Banner)
□ 激励视频接入 (Rewarded)
□ 插屏广告接入 (Interstitial)
□ 广告频率优化
```

#### 广告位设计

| 广告类型 | 位置 | 触发时机 | 频率 |
|---------|------|---------|------|
| **Banner** | 底部 | 常驻 | 1 个/页面 |
| **激励视频** | 弹窗 | 用户主动 | 无限 (奖励驱动) |
| **插屏** | 全屏 | 关卡结束 | 每 2-3 关 1 次 |

#### 激励视频奖励

| 行为 | 奖励 | 触发 |
|------|------|------|
| 观看视频 | +50 金币 | 商店按钮 |
| 观看视频 | 复活一次 | 失败时 |
| 观看视频 | 提示一次 | 卡关时 |
| 观看视频 | 双倍奖励 | 通关后 |

#### AdSense 配置

```html
<!-- index.html -->
<head>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX"
     crossorigin="anonymous"></script>
</head>

<!-- 广告位 -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
```

#### AI Agent 分工

| Agent | 任务 | 输出 |
|-------|------|------|
| **开发 Agent** | AdSense 接入代码 | TypeScript |
| **开发 Agent** | 广告管理器 | 广告控制逻辑 |
| **开发 Agent** | 激励视频逻辑 | 奖励发放 |
| **人类** | AdSense 申请 | 账号审批 |

#### Day 17 验收标准

```
✅ AdSense 账号获批
✅ Banner 广告正常显示
✅ 激励视频可观看 + 奖励发放
✅ 插屏广告按频率显示
✅ 广告不影响核心体验
```

---

### Day 18-19: 数据分析接入

#### 任务清单

```
□ Google Analytics 4 配置
□ 事件追踪 (关卡开始/结束、购买、广告)
□ 用户行为分析 (留存、时长)
□ 变现数据追踪 (广告展示、收入)
□ 自定义 Dashboard
```

#### 关键事件追踪

```typescript
// 游戏事件
- level_start: { level_id: number }
- level_complete: { level_id: number, stars: number, time: number }
- level_fail: { level_id: number, moves: number }

// 变现事件
- ad_impression: { type: string, reward: number }
- purchase_attempt: { item: string, price: number }
- currency_earn: { type: string, amount: number, source: string }

// 用户行为
- session_start: { timestamp: number }
- setting_change: { key: string, value: any }
```

#### GA4 配置

```typescript
// Google Analytics 4
import { getAnalytics, logEvent } from "firebase/analytics";

const analytics = getAnalytics();

// 追踪关卡完成
logEvent(analytics, 'level_complete', {
  level_id: 42,
  stars: 3,
  time_seconds: 120
});

// 追踪广告
logEvent(analytics, 'ad_impression', {
  ad_type: 'rewarded_video',
  reward_amount: 50
});
```

#### 数据看板 (Google Analytics)

| 看板 | 指标 |
|------|------|
| **概览** | DAU、会话数、留存率 |
| **游戏** | 关卡完成率、平均时长、失败率 |
| **变现** | 广告展示、eCPM、ARPU |
| **用户** | 地域、设备、来源 |

#### Day 19 验收标准

```
✅ GA4 正常追踪
✅ 关键事件完整记录
✅ 数据看板可访问
✅ 每日数据自动汇总
```

---

### Day 20-21: 性能优化

#### 任务清单

```
□ 加载速度优化 (<3 秒)
□ 内存优化 (无内存泄漏)
□ 帧率优化 (稳定 60fps)
□ 资源压缩 (图片、音频)
□ 缓存策略 (Service Worker)
```

#### 优化清单

| 优化项 | 目标 | 方法 |
|--------|------|------|
| **首屏加载** | <3 秒 | 资源懒加载、代码分割 |
| **图片大小** | <100KB/张 | WebP 格式、压缩 |
| **音频大小** | <50KB/个 | MP3 压缩、复用 |
| **包体大小** | <5MB | 按需加载、Tree Shaking |
| **帧率** | 60fps | 减少绘制、对象池 |
| **内存** | <200MB | 及时释放、对象池 |

#### AI Agent 分工

| Agent | 任务 | 工具 |
|-------|------|------|
| **开发 Agent** | 代码优化 | ESLint、性能分析 |
| **开发 Agent** | 资源压缩 | ImageMagick、ffmpeg |
| **测试 Agent** | 性能测试 | Lighthouse、DevTools |
| **测试 Agent** | 兼容性测试 | BrowserStack |

#### Day 21 验收标准

```
✅ Lighthouse 分数 >90
✅ 首屏加载 <3 秒
✅ 帧率稳定 60fps
✅ 无内存泄漏 (30 分钟测试)
✅ 主流浏览器兼容 (Chrome/Firefox/Safari/Edge)
```

---

## 五、Week 4: 测试 + 上线

### Day 22-24: 测试

#### 任务清单

```
□ 功能测试 (所有功能正常)
□ 兼容性测试 (浏览器/设备)
□ 性能测试 (压力测试)
□ 广告测试 (正常展示)
□ Bug 修复
```

#### 测试用例

| 测试类型 | 用例数 | 重点 |
|---------|--------|------|
| **功能测试** | 50+ | 核心玩法、变现、存储 |
| **兼容性测试** | 10+ | Chrome/Firefox/Safari/Edge |
| **设备测试** | 10+ | 手机/平板/桌面 |
| **性能测试** | 5+ | 加载、帧率、内存 |
| **广告测试** | 10+ | 展示、奖励、频率 |

#### Bug 优先级

| 优先级 | 定义 | 响应 |
|--------|------|------|
| **P0** | 阻塞性 Bug (无法游戏) | 立即修复 |
| **P1** | 严重 Bug (功能失效) | 24 小时内 |
| **P2** | 一般 Bug (体验问题) | 本周内 |
| **P3** | 轻微 Bug (UI 小问题) | 后续迭代 |

#### AI Agent 分工

| Agent | 任务 | 输出 |
|-------|------|------|
| **测试 Agent** | 自动化测试脚本 | Jest/Playwright |
| **测试 Agent** | Bug 报告 | 详细记录 |
| **开发 Agent** | Bug 修复 | 修复代码 |
| **人类** | 验收测试 | 最终确认 |

#### Day 24 验收标准

```
✅ P0/P1 Bug 清零
✅ P2 Bug <5 个
✅ 测试覆盖率 >80%
✅ 性能指标达标
✅ 准备上线
```

---

### Day 25-26: 上线准备

#### 任务清单

```
□ 域名配置 (magic-solitaire.com)
□ Vercel 部署配置
□ SSL 证书 (HTTPS)
□ SEO 优化 (Meta 标签、描述)
□ 隐私政策/用户协议
□ 联系方式 (客服邮箱)
```

#### SEO 配置

```html
<!-- index.html -->
<head>
  <title>Play Free Solitaire Online - Magic TriPeaks Adventure</title>
  <meta name="description" content="Play the best free solitaire card game online. 
  Magic-themed TriPeaks solitaire with 500+ levels, decorations, and daily rewards. 
  No download required!">
  <meta name="keywords" content="solitaire, card game, tripeaks, free, online, magic">
  
  <!-- Open Graph (社交媒体分享) -->
  <meta property="og:title" content="Magic Solitaire - Free Online Card Game">
  <meta property="og:description" content="Play 500+ levels of magic-themed solitaire!">
  <meta property="og:image" content="https://magic-solitaire.com/og-image.png">
  
  <!-- Favicon -->
  <link rel="icon" type="image/png" href="/favicon.png">
</head>
```

#### 隐私政策 (模板)

```
Privacy Policy for Magic Solitaire

1. Information We Collect
- We do not collect personal information
- We use cookies for game progress saving
- Third-party advertisers (Google AdSense) may collect data

2. How We Use Information
- To save your game progress
- To display ads (revenue source)
- To improve game experience

3. Third-Party Services
- Google AdSense (ads)
- Google Analytics (analytics)
- Vercel (hosting)

4. Contact Us
Email: support@magic-solitaire.com
```

#### Day 26 验收标准

```
✅ 网站可访问 (HTTPS)
✅ SEO 配置完整
✅ 隐私政策页面
✅ 客服邮箱设置
✅ 404 页面
✅ 准备平台提交
```

---

### Day 27-28: 平台提交 + 宣传

#### 任务清单

```
□ 提交 CrazyGames
□ 提交 Poki
□ 提交 Armor Games
□ 提交 Itch.io
□ 提交 Facebook Gaming
□ Reddit 宣传
□ TikTok 首发视频
```

#### 平台提交信息

| 平台 | 提交内容 | 审核时间 |
|------|---------|---------|
| **CrazyGames** | 游戏文件 + 截图 + 描述 | 3-7 天 |
| **Poki** | 游戏文件 + 截图 + 描述 | 3-7 天 |
| **Armor Games** | 游戏文件 + 截图 + 描述 | 7-14 天 |
| **Itch.io** | 游戏文件 + 截图 + 描述 | 1-3 天 |
| **Facebook Gaming** | 游戏文件 + 截图 + 描述 | 7-14 天 |

#### 提交材料准备

```
□ 游戏文件 (HTML5/ZIP)
□ 截图 (5-8 张，1920x1080)
□ 游戏描述 (200-500 字)
□ 分类标签 (Card/Solitaire/Puzzle)
□ 年龄分级 (All Ages)
□ 控制说明 (Mouse/Touch)
```

#### 宣传计划

| 渠道 | 内容 | 时间 |
|------|------|------|
| **Reddit** | r/Solitaire 发帖 | Day 27 |
| **TikTok** | 首发视频 (3-5 条) | Day 27-28 |
| **Facebook** | Group 分享 | Day 28 |
| **Twitter** | 发布推文 | Day 28 |
| **Discord** | 游戏服务器分享 | Day 28 |

#### Reddit 发帖模板

```
标题: I made a free magic-themed Solitaire game! Looking for feedback

正文:
Hi everyone!

I've been working on a magic academy themed TriPeaks Solitaire 
game for the past month. It has 500+ levels, decoration system, 
and daily rewards.

Would love to get some feedback from this community!

Play here: https://magic-solitaire.com

Thanks! 🎴✨
```

#### Day 28 验收标准 (上线！)

```
✅ 网站正式上线
✅ 5+ 平台提交完成
✅ 首条 TikTok 发布
✅ Reddit 发帖完成
✅ 数据分析正常
✅ 庆祝！🎉
```

---

## 六、AI Agent 工作流

### 6.1 每日工作流

```
早晨 (30 分钟):
□ 查看昨日进度
□ 分配今日任务给 AI Agent
□ Code Review (AI 生成代码)

白天 (AI 自动执行):
□ 开发 Agent: 代码生成
□ 测试 Agent: 自动化测试
□ 美术 Agent: 素材生成

晚上 (30 分钟):
□ 验收 AI 工作成果
□ 提交代码到 GitHub
□ 部署到 Vercel (自动)
□ 记录进度
```

### 6.2 AI Agent 配置

| Agent | 职责 | 工具 |
|-------|------|------|
| **开发 Agent** | 代码生成、Bug 修复 | CoPaw + Cursor |
| **测试 Agent** | 测试用例、Bug 报告 | Playwright |
| **美术 Agent** | 素材生成 | 智谱 AI/Nano Banana |
| **策划 Agent** | 关卡配置、数值平衡 | Notion/Excel |

### 6.3 AI 使用技巧

```
✅ 明确任务描述 (具体到函数级)
✅ 提供代码示例 (AI 学习参考)
✅ 分小任务 (避免过大)
✅ 及时 Code Review (保证质量)
✅ 保存 Prompt (复用优化)

❌ 避免模糊需求 ("做个游戏")
❌ 避免一次性大任务 ("完成所有功能")
❌ 避免不 Review (AI 可能出错)
```

---

## 七、风险管理

### 7.1 风险清单

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| **AdSense 拒批** | 中 | 高 | 备用广告平台 (AdMob) |
| **平台审核失败** | 低 | 中 | 修改后重新提交 |
| **性能不达标** | 中 | 中 | 优化资源、减少特效 |
| **进度延期** | 中 | 中 | 优先核心功能、砍 Meta |
| **Bug 过多** | 低 | 高 | 延长测试时间 |

### 7.2 应急预案

```
Plan B (AdSense 拒批):
→ 使用 AdMob for Web 或 Unity Ads
→ 或先上线，1 月后重新申请

Plan B (进度延期):
→ 砍装饰系统 (保留核心玩法)
→ 减少关卡数 (50→30)
→ 延后 Meta 系统

Plan B (性能问题):
→ 减少特效
→ 降低画质
→ 延迟加载资源
```

---

## 八、上线后运营计划

### 8.1 每日任务 (30 分钟)

```
□ 检查数据 (DAU、留存、收入)
□ 回复用户反馈 (邮件/评论)
□ TikTok 发 1 条视频
□ 监控广告展示 (正常/异常)
```

### 8.2 每周任务 (2-3 小时)

```
□ 数据分析 (周报)
□ 内容更新 (50 新关卡)
□ SEO 优化 (关键词排名)
□ 平台优化 (截图/描述 A/B 测试)
□ 社区互动 (Reddit/FB)
```

### 8.3 每月任务 (1 天)

```
□ 月度复盘 (数据、收入、用户反馈)
□ 大版本更新 (新功能/新系统)
□ 活动策划 (节日/主题活动)
□ 竞品分析 (学习优秀产品)
```

---

## 九、预算汇总

### 9.1 开发期预算 (4 周)

| 项目 | 金额 | 说明 |
|------|------|------|
| **域名** | $12/年 | Namecheap |
| **托管** | $0 | Vercel 免费 |
| **AI API** | $50-100 | 智谱/硅基流动 |
| **素材** | $0 | AI 生成 + 开源 |
| **音效** | $0 | 免费资源 |
| **总计** | **$62-112** | 一次性 |

### 9.2 运营期预算 (月度)

| 项目 | 金额 | 说明 |
|------|------|------|
| **AI API** | $20-50/月 | 内容生成 |
| **域名** | $1/月 | 均摊 |
| **托管** | $0 | Vercel 免费 |
| **总计** | **$21-51/月** | 持续 |

---

## 十、成功指标

### 10.1 上线后 30 天目标

| 指标 | 目标 | 及格线 |
|------|------|--------|
| **DAU** | 500+ | 200+ |
| **D1 留存** | 25%+ | 20%+ |
| **D7 留存** | 10%+ | 8%+ |
| **月收入** | $200+ | $100+ |
| **平台收录** | 5+ | 3+ |

### 10.2 上线后 90 天目标

| 指标 | 目标 | 及格线 |
|------|------|--------|
| **DAU** | 2000+ | 1000+ |
| **D1 留存** | 30%+ | 25%+ |
| **月收入** | $1000+ | $500+ |
| **SEO 排名** | Top 20 | Top 50 |

### 10.3 决策点

```
30 天复盘:
- DAU > 500 且 收入 > $200? → 继续投入
- DAU < 200 或 收入 < $100? → 优化或 Pivot

90 天复盘:
- DAU > 2000 且 LTV/CPI > 3:1? → 考虑手游版
- 数据不达标? → 深度优化或考虑新项目
```

---

## 十一、总结

### 开发计划概览

| 阶段 | 时间 | 目标 | 交付物 |
|------|------|------|--------|
| **Week 1** | Day 1-7 | 核心玩法 + 基础 UI | MVP 原型 |
| **Week 2** | Day 8-14 | Meta 系统 + 美术 | 完整游戏 |
| **Week 3** | Day 15-21 | 变现 + 数据 + 优化 | 可上线版本 |
| **Week 4** | Day 22-28 | 测试 + 上线 + 宣传 | 正式发布 |

### 核心原则

```
✅ 小步快跑 (每周可上线版本)
✅ 数据驱动 (GA4 追踪一切)
✅ AI 优先 (85% 工作 AI 完成)
✅ 用户反馈 (快速迭代)
✅ 成本最低 ($100 内启动)
```

### 一句话总结

**4 周时间，$100 预算，1 人 + AI Agent，上线可盈利的网页版 Solitaire MVP。**

---

**完整计划已保存**: `solitaire_development_plan_4weeks.md`

**下一步**:
1. 确认开发计划
2. Day 1 开始执行 (项目 setup)
3. 每日汇报进度

**准备好了吗？我们明天开始 Day 1！** 🚀
