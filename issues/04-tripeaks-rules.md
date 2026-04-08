---
name: Day 1 - Tri-Peaks Rules
about: 实现 Tri-Peaks Solitaire 消除规则
---

## 任务描述

实现 Tri-Peaks Solitaire 的核心消除规则，包括牌型布局、发牌逻辑、消除规则和胜利条件

## 用户故事

- 作为 **玩家**, 我想要 **按照 Tri-Peaks 规则消除卡牌**, 以便 **完成关卡并获取分数**

## 技术要求

- [x] TypeScript 严格模式
- [x] 继承 Phaser.GameObjects.Container
- [x] Tri-Peaks 牌型布局算法
- [x] 发牌堆 (Stock) 逻辑
- [x] 废牌堆 (Waste) 逻辑
- [x] 消除规则 (相邻值 ±1)
- [x] 胜利条件检测

## 详细任务

### 1. Tri-Peaks 牌型布局

**金字塔结构** (28 张牌):
```
        Row 0:        1 张
      Row 1:       2 张
    Row 2:      3 张
  Row 3:     4 张
Row 4:    5 张 (基础行)
```

**布局配置**:
- 行间距：垂直 30px, 水平 60px
- 卡牌偏移：每行居中对齐
- 遮挡关系：下一行牌被上一行部分遮挡

### 2. 发牌堆 (Stock)

**功能**:
- 存放剩余 24 张牌 (52 - 28 = 24)
- 点击发牌到废牌堆
- 可循环发牌 (无限重新发牌)

**属性**:
- `stockPile: CardStack`
- `cardsRemaining: number`

### 3. 废牌堆 (Waste)

**功能**:
- 显示从发牌堆发出的牌
- 作为"当前可出牌"
- 可与金字塔中的牌消除

**属性**:
- `wastePile: CardStack`
- `topCard: Card | null`

### 4. 消除规则

**Tri-Peaks 规则**:
- 废牌堆顶牌可以与金字塔中"暴露"的牌消除
- 暴露条件：不被其他牌遮挡
- 消除条件：值差为 ±1 (A=1, K=13)
- 特殊：K 可以消除 Q 和 A (循环规则可选)

**实现**:
```typescript
canEliminate(card1: Card, card2: Card): boolean {
  if (!card1.isFaceUp() || !card2.isFaceUp()) return false;
  if (card2.isEliminatedCard()) return false;
  if (!this.isCardExposed(card2)) return false;
  
  const diff = Math.abs(card1.getValue() - card2.getValue());
  return diff === 1;
}

isCardExposed(card: Card): boolean {
  // 检查是否有上一行的牌遮挡
  // 每张牌最多被 2 张上一行的牌遮挡
}
```

### 5. 胜利条件

**胜利条件**:
- 金字塔所有 28 张牌都被消除
- 游戏胜利，显示胜利界面

**检测**:
```typescript
checkWin(): boolean {
  const pyramidCards = this.pyramidStack.getCards();
  return pyramidCards.every(card => card.isEliminatedCard());
}
```

### 6. 游戏流程

1. **初始化**: 发 28 张牌到金字塔，24 张到发牌堆
2. **发牌**: 点击发牌堆 → 发到废牌堆
3. **消除**: 点击金字塔牌 → 检查是否可消除 → 消除
4. **循环**: 废牌堆为空时继续发牌
5. **胜利**: 所有牌消除 → 胜利

## 验收标准

- [ ] 金字塔布局正确 (28 张牌，5 行)
- [ ] 发牌堆可以点击发牌
- [ ] 废牌堆显示当前牌
- [ ] 消除规则正确 (值差±1)
- [ ] 暴露检测正确 (不被遮挡的牌才能消除)
- [ ] 胜利条件检测正确
- [ ] 单元测试覆盖率>80%
- [ ] Quality Gate v3.1 评分>8.0

## 任务分配

- **负责 Agent**: @DevBot
- **预计时间**: 6 小时
- **优先级**: P0 (紧急)

## 相关文件

- `src/TriPeaksScene.ts` - 新增
- `src/Pyramid.ts` - 新增 (金字塔管理)
- `src/Stock.ts` - 新增 (发牌堆)
- `src/Waste.ts` - 新增 (废牌堆)
- `src/Card.ts` - 已存在
- `src/CardStack.ts` - 已存在

## 测试计划

### 单元测试

1. **Pyramid 测试**:
   - 布局正确 (28 张牌)
   - 暴露检测正确
   - 行/列索引正确

2. **Stock 测试**:
   - 发牌逻辑正确
   - 循环发牌正确

3. **Waste 测试**:
   - 接收牌正确
   - 顶牌访问正确

4. **消除规则测试**:
   - 值差±1 可消除
   - 被遮挡不可消除
   - 已消除不可消除

### E2E 测试

- 完整游戏流程
- 胜利条件触发

## 备注

这是游戏核心玩法的关键任务，需要仔细实现 Tri-Peaks 规则。
