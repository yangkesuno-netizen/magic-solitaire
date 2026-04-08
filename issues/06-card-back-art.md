# Issue #6: 卡牌背面设计 - 魔法学院风格

**优先级**: P1  
**标签**: art, P1  
**估算**: 0.5-1 天  
**状态**: 待开始

---

## 任务描述

使用 AI 图像生成工具 (Zhipu AI / Nano Banana Pro) 生成 Tri-Peaks Solitaire 游戏的卡牌背面设计，采用魔法学院风格。

---

## 验收标准

### 设计要求
- [ ] 符合魔法主题（神秘、优雅）
- [ ] 适合卡牌尺寸 (100x140px 或比例 5:7)
- [ ] 颜色与游戏整体风格协调 (#1a1a2e 背景)
- [ ] 清晰可辨，无模糊
- [ ] 无缝纹理或对称设计

### 技术规格
- [ ] 格式：PNG (透明背景或纯色背景)
- [ ] 尺寸：200x280px (2x 放大，用于高清屏)
- [ ] 保存位置：`public/assets/cards/back.png`
- [ ] 文件大小：<100KB (优化后)

### 风格指南
- **主色调**: 深蓝 (#1a1a2e)、金色 (#ffd700)、紫色 (#7c3aed)
- **主题元素**: 星星、月亮、魔法阵、几何图案
- **风格**: 简约现代 + 魔法神秘感

---

## 技术方案

### 使用工具
- **Zhipu AI (CogView)**: 免费，中文提示词友好
- **Nano Banana Pro**: 高质量，支持图像编辑

### 提示词示例

#### Zhipu AI 提示词
```
生成一张扑克牌背面设计，魔法学院风格，深蓝色背景，
金色星星和月亮图案，对称设计，神秘优雅，
卡牌比例 5:7，高清，简约现代风格
```

#### Nano Banana Pro 提示词
```
Playing card back design, magical academy style,
dark blue background with golden stars and moon,
symmetrical pattern, mysterious and elegant,
card ratio 5:7, high quality, minimalist modern
```

### 生成流程
1. 使用 Zhipu AI 生成初始设计 (3-5 个变体)
2. 选择最佳设计
3. 使用 Nano Banana Pro 优化 (如需要)
4. 调整尺寸到 200x280px
5. 保存到 `public/assets/cards/back.png`

---

## 实现步骤

1. **准备提示词** (10 分钟)
   - 根据风格指南编写详细提示词
   - 包含颜色、元素、比例等信息

2. **生成初始设计** (30 分钟)
   - 使用 Zhipu AI 生成 3-5 个变体
   - 保存所有变体用于比较

3. **选择最佳设计** (10 分钟)
   - 对比所有变体
   - 选择最符合要求的 design

4. **优化和裁剪** (20 分钟)
   - 调整尺寸到 200x280px
   - 优化文件大小
   - 确保透明度 (如需要)

5. **集成到项目** (10 分钟)
   - 保存到 `public/assets/cards/back.png`
   - 更新 .gitignore (如需要)
   - 在 Phaser 中加载测试

---

## 测试计划

### 视觉测试
- [ ] 在游戏中显示正常
- [ ] 尺寸合适 (100x140px 显示)
- [ ] 颜色与背景协调
- [ ] 高清屏显示清晰 (2x 缩放)

### 性能测试
- [ ] 文件大小 <100KB
- [ ] 加载速度快
- [ ] 无内存泄漏

---

## 依赖关系

- ✅ Issue #1: 项目 setup
- ✅ Issue #2: Card 类
- ✅ Issue #3: CardStack 类
- ✅ Issue #4: Tri-Peaks 规则
- ✅ Issue #5: 基础 UI
- ⏳ Issue #6: 卡牌背面设计 (当前)
- ⏳ Issue #7: 卡牌正面设计
- ⏳ Issue #8: 关卡系统
- ⏳ Issue #9: 音效
- ⏳ Issue #10: 上线准备

---

## 完成定义 (DoD)

- [ ] 卡牌背面设计完成
- [ ] 保存到正确位置
- [ ] 在游戏中显示正常
- [ ] 文件大小优化
- [ ] Quality Gate v3.1 通过

---

## 备选方案

如果 AI 生成效果不理想：

1. **使用免费素材**:
   - OpenGameArt.org
   - itch.io 免费资源
   - Kenney.nl 卡牌素材

2. **简化设计**:
   - 纯色背景 + 简单几何图案
   - 使用 CSS 生成图案
   - Phaser 图形 API 绘制

---

**创建时间**: 2026-04-08  
**最后更新**: 2026-04-08  
**负责人**: ArtBot
