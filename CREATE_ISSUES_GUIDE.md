# 创建 Day 1 Issues 指南

**时间**: 2026-04-08  
**仓库**: https://github.com/yangkesuno-netizen/magic-solitaire

---

## 方法 1: 在 GitHub 网页创建 (简单)

### Step 1: 访问 Issues 页面

**打开**: https://github.com/yangkesuno-netizen/magic-solitaire/issues

---

### Step 2: 点击 "New issue"

---

### Step 3: 创建以下 9 个 Issues

#### Issue #1: 项目 setup ✅ (已存在)
```
Title: [Feature] 项目 setup - 初始化 Phaser 3 + TypeScript + Vite
Labels: feature, P0
```

---

#### Issue #2: Card 类实现
```
Title: [Feature] 实现 Card 类 - 卡牌对象基础功能
Labels: feature, P0

Body:
## 任务描述
实现 Card 类，作为游戏卡牌的基础对象

## 技术要求
- 使用 Phaser 3 Sprite
- 支持卡牌面值 (1-13)
- 支持花色 (红桃/黑桃/方块/梅花)
- 支持选中/取消选中状态

## 验收标准
- [ ] Card 类创建成功
- [ ] 可以设置面值和花色
- [ ] 可以点击选中/取消选中
- [ ] 单元测试通过

## 相关文件
- src/game/Card.ts
- src/game/__tests__/Card.test.ts
```

---

#### Issue #3: CardStack 类
```
Title: [Feature] 实现 CardStack 类 - 牌堆管理
Labels: feature, P0

Body:
## 任务描述
实现 CardStack 类，管理牌堆中的卡牌

## 技术要求
- 支持添加/移除卡牌
- 支持牌堆叠放视觉效果
- 支持发牌动画

## 验收标准
- [ ] CardStack 类创建成功
- [ ] 可以添加/移除卡牌
- [ ] 牌堆视觉效果正确
- [ ] 单元测试通过

## 相关文件
- src/game/CardStack.ts
- src/game/__tests__/CardStack.test.ts
```

---

#### Issue #4: Tri-Peaks 规则
```
Title: [Feature] 实现 Tri-Peaks 消除规则
Labels: feature, P0

Body:
## 任务描述
实现 Tri-Peaks Solitaire 的核心消除规则

## 游戏规则
- 牌面差 1 的卡牌可以消除 (A=1, K=13)
- 从 7 个牌堆顶部选牌
- 清空所有牌堆获胜

## 验收标准
- [ ] 规则逻辑实现
- [ ] 可以判断是否可消除
- [ ] 胜负判定正确
- [ ] 单元测试通过

## 相关文件
- src/game/TriPeaksRules.ts
- src/game/__tests__/TriPeaksRules.test.ts
```

---

#### Issue #5: 基础 UI
```
Title: [Feature] 基础 UI - 游戏流程界面
Labels: feature, P1

Body:
## 任务描述
实现游戏基础 UI 界面

## 界面元素
- 游戏区域 (牌堆 + 手牌)
- 分数显示
- 重新开始按钮
- 关卡选择

## 验收标准
- [ ] UI 布局完成
- [ ] 分数显示正确
- [ ] 按钮可点击
- [ ] 移动端适配

## 相关文件
- src/ui/GameUI.ts
- src/scenes/GameScene.ts
```

---

#### Issue #6: 卡牌背面设计
```
Title: [Art] 卡牌背面设计 - 魔法学院风格
Labels: art, P1

Body:
## 任务描述
使用智谱 AI 生成卡牌背面设计

## 设计要求
- 魔法学院风格
- 紫色和金色配色
- 神秘符号、星星、月亮
- 矢量风格，游戏素材

## 技术规格
- 格式：PNG (透明背景)
- 尺寸：200x300 像素
- 数量：1 个

## 验收标准
- [ ] 设计符合魔法主题
- [ ] 清晰度高
- [ ] 透明背景
- [ ] 保存到 public/assets/cards/back.png

## 使用工具
- 智谱 AI API (已配置)
- scripts/generate_card_back.py
```

---

#### Issue #7: 背景图生成
```
Title: [Art] 背景图生成 (5 张) - 魔法学院场景
Labels: art, P1

Body:
## 任务描述
使用智谱 AI 生成 5 张魔法学院风格背景图

## 设计要求
1. 魔法图书馆
2. 星空魔法阵
3. 古老城堡
4. 神秘森林
5. 魔法塔楼

## 技术规格
- 格式：PNG
- 尺寸：1920x1080 像素
- 数量：5 张

## 验收标准
- [ ] 5 张背景图完成
- [ ] 符合魔法主题
- [ ] 保存到 public/assets/backgrounds/

## 使用工具
- 智谱 AI API
- scripts/generate_backgrounds.py
```

---

#### Issue #8: 关卡配置
```
Title: [Design] 生成 50 关 Tri-Peaks 配置
Labels: design, P1

Body:
## 任务描述
生成 50 个 Tri-Peaks 关卡配置

## 难度曲线
- 关卡 1-10: 简单 (教学)
- 关卡 11-30: 中等
- 关卡 31-50: 困难

## 验收标准
- [ ] 50 个关卡配置完成
- [ ] 难度递进合理
- [ ] 每关都可解
- [ ] 保存到 src/data/levels.json

## 相关文件
- src/data/levels.json
- scripts/generate_levels.py
```

---

#### Issue #9: 核心玩法测试
```
Title: [Test] 核心玩法测试 - 单元测试 + E2E
Labels: test, P0

Body:
## 任务描述
编写核心玩法的测试用例

## 测试范围
- Card 类单元测试
- CardStack 类单元测试
- TriPeaksRules 单元测试
- E2E 测试 (完整游戏流程)

## 验收标准
- [ ] 单元测试覆盖率 >80%
- [ ] E2E 测试通过
- [ ] CI/CD 集成测试通过

## 相关文件
- src/game/__tests__/*.test.ts
- tests/e2e/gameplay.spec.ts
```

---

## 方法 2: 使用 GitHub CLI (可选)

如果已安装 GitHub CLI：

```bash
# 创建 Issue #2
gh issue create --title "[Feature] 实现 Card 类 - 卡牌对象基础功能" --body "## 任务描述\n实现 Card 类..." --label "feature,P0"

# 创建其他 Issues...
```

---

## ✅ 检查清单

- [ ] Issue #1: 项目 setup
- [ ] Issue #2: Card 类实现
- [ ] Issue #3: CardStack 类
- [ ] Issue #4: Tri-Peaks 规则
- [ ] Issue #5: 基础 UI
- [ ] Issue #6: 卡牌背面设计
- [ ] Issue #7: 背景图生成
- [ ] Issue #8: 关卡配置
- [ ] Issue #9: 核心玩法测试

---

## 🎯 下一步

创建 Issues 后：

1. 在 GitHub Projects 中创建看板
2. 将 Issues 添加到看板
3. 开始开发 Issue #1 (项目 setup)

---

**现在请打开**: https://github.com/yangkesuno-netizen/magic-solitaire/issues

**开始创建 Issues 吧！** 🚀
