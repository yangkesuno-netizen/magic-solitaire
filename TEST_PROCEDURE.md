# 标准测试流程

**目标：确保每次部署前功能完整，不再出现 Vercel 部署后资源 404 的问题**

---

## 🧪 测试金字塔

```
        /🧪\
       / E2E \      10% - Playwright 端到端测试
      /-------\
     /  Integration \  30% - 场景集成测试
    /---------------\
   /    Unit Tests    \ 60% - 单元测试（已有 83 个）
  /-------------------\
```

---

## 📋 本地测试流程（每次部署前必须执行）

### 阶段 1：构建验证
```bash
# 1. 清理构建
rm -rf dist

# 2. 重新构建
npm run build

# 3. 检查输出
ls dist/
ls dist/assets/
ls dist/assets/cards/  # 确认卡牌资源

# 4. 检查文件大小
du -sh dist/
```

**预期输出**：
```
dist/
├── index.html
└── assets/
    ├── index-xxxx.js
    ├── phaser-core-xxxx.js
    └── cards/
        ├── back.png
        ├── A_hearts.png
        └── ... (共 53 张)
```

---

### 阶段 2：本地预览测试
```bash
# 启动本地服务器
npm run preview

# 浏览器打开 http://localhost:4173
```

**测试清单**：
- [ ] 页面加载完成（<5 秒）
- [ ] 主菜单显示正常
- [ ] 点击 START GAME 进入游戏
- [ ] 卡牌布局正确（金字塔 + 发牌堆）
- [ ] 卡牌背面显示正常
- [ ] 点击卡牌可消除
- [ ] 发牌堆可发牌
- [ ] 分数显示正常
- [ ] 胜利/失败界面正常

**浏览器 DevTools 检查**：
- [ ] Console 无错误
- [ ] Network 无 404
- [ ] 所有资源加载成功

---

### 阶段 3：自动化测试
```bash
# 1. 单元测试
npm test

# 2. 覆盖率（可选）
npm run test:coverage

# 3. 质量门
./quality_gate.bat
```

**通过标准**：
- 单元测试：100% 通过
- 质量门：≥9.0 分

---

### 阶段 4：E2E 测试（Playwright）

创建 `tests/e2e.spec.ts`：

```typescript
import { test, expect } from '@playwright/test';

test('游戏完整流程', async ({ page }) => {
  // 1. 打开页面
  await page.goto('http://localhost:4173');
  
  // 2. 检查主菜单
  await expect(page).toHaveTitle('Magic Solitaire');
  await expect(page.locator('text=START GAME')).toBeVisible();
  
  // 3. 开始游戏
  await page.click('text=START GAME');
  
  // 4. 检查游戏界面
  await expect(page.locator('canvas')).toBeVisible();
  
  // 5. 检查卡牌加载
  const cards = page.locator('.card');
  await expect(cards.first()).toBeVisible();
  
  // 6. 点击卡牌
  await cards.first().click();
  
  // 7. 检查分数变化
  const score = page.locator('.score');
  await expect(score).toBeVisible();
});
```

运行：
```bash
npx playwright test
```

---

## 🚀 部署测试流程

### 步骤 1：提交前检查
```bash
./pre_commit_check.bat
```

### 步骤 2：Git 推送
```bash
git add .
git commit -m "feat: ..."
git push
```

### 步骤 3：Vercel 部署监控
1. 访问 https://vercel.com/yangkesuno-7253s-projects/magic-solitaire
2. 查看构建日志
3. 确认部署状态：Ready

### 步骤 4：生产环境测试
1. 打开 https://magic-solitaire.vercel.app
2. 执行本地测试清单
3. 检查性能（加载时间、FPS）

### 步骤 5：回滚计划（如有问题）
```bash
# Vercel 支持一键回滚
# 访问 Vercel Dashboard → Deployments → 选择上一个版本 → Rollback
```

---

## 📊 测试报告模板

创建 `TEST_REPORT.md`：

```markdown
# 测试报告

**版本**: v0.1.0  
**日期**: 2026-04-08  
**测试人**: Copaw

## 测试结果

| 测试项 | 状态 | 备注 |
|--------|------|------|
| 构建 | ✅ | 23.61KB + 1.48MB |
| 单元测试 | ✅ | 83/83 通过 |
| 质量门 | ✅ | 10.0/10 |
| 本地预览 | ✅ | 功能正常 |
| E2E 测试 | ⏳ | 待创建 |
| 生产测试 | ⏳ | 待部署 |

## 问题清单

| 问题 | 严重性 | 状态 |
|------|--------|------|
| 无 | - | - |

## 性能指标

| 指标 | 值 | 目标 |
|------|-----|------|
| 首次加载 | 3.2s | <5s |
| FCP | 1.5s | <2s |
| LCP | 2.8s | <3s |

## 结论

✅ 可以部署 / ❌ 禁止部署
```

---

## ⚠️ 红线（任何一项失败，禁止部署）

- [ ] 构建失败 → ❌ 禁止部署
- [ ] 单元测试失败 → ❌ 禁止部署
- [ ] 质量门 <9.0 → ❌ 禁止部署
- [ ] 本地预览功能异常 → ❌ 禁止部署
- [ ] 资源 404 → ❌ 禁止部署
- [ ] Console 有未处理错误 → ❌ 禁止部署

---

## 🔧 自动化脚本

创建 `test_and_deploy.sh`：

```bash
#!/bin/bash
set -e

echo "🧪 开始测试流程..."

echo "[1/4] 构建..."
npm run build

echo "[2/4] 检查输出..."
test -d dist/assets || exit 1
test -d dist/assets/cards || exit 1

echo "[3/4] 测试..."
npm test

echo "[4/4] 质量门..."
./quality_gate.bat

echo "✅ 所有测试通过！"
echo "准备部署..."

# 自动提交
git add .
git commit -m "chore: pre-deployment checks passed"
git push

echo "🚀 已推送，Vercel 将自动部署"
```

---

## 📝 测试记录

| 日期 | 版本 | 测试结果 | 部署结果 | 备注 |
|------|------|----------|----------|------|
| 2026-04-08 | v0.1.0 | ❌ | ❌ | 资源未复制 |
| 2026-04-08 | v0.1.1 | ✅ | ✅ | 修复配置 |

---

**创建日期**: 2026-04-08  
**强制执行**: ✅ 是  
**违反后果**: 禁止部署
