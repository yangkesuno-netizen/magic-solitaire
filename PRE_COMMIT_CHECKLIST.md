# 提交前强制检查清单

**每次 `git commit` 前必须逐项检查，全部打勾才能提交！**

---

## ✅ 代码质量检查

- [ ] TypeScript 编译通过：`npm run build` 无错误
- [ ] 单元测试通过：`npm test` 全部通过
- [ ] 质量门检测：`./quality_gate.bat` 评分 ≥9.0
- [ ] 无 console.error/warning（除预期日志）
- [ ] 无 TypeScript 警告（noImplicitAny 等）

---

## ✅ 构建输出检查

- [ ] `dist/` 目录存在
- [ ] `dist/index.html` 存在
- [ ] `dist/assets/*.js` 存在
- [ ] `dist/assets/*.css` 存在
- [ ] `dist/assets/cards/` 目录存在（如有图片资源）
- [ ] 资源文件数量正确（如 53 张卡牌）
- [ ] 构建大小合理（与上次对比无异常增长）

**检查命令**：
```bash
npm run build
ls dist/
ls dist/assets/
ls dist/assets/cards/ | wc -l  # 应该输出 53
```

---

## ✅ 本地功能测试

- [ ] `npm run preview` 启动本地服务器
- [ ] 浏览器打开 http://localhost:4173
- [ ] 主页面加载正常
- [ ] 核心功能可交互（点击按钮、卡牌等）
- [ ] 控制台无错误日志
- [ ] 网络面板无 404 资源

**测试命令**：
```bash
npm run preview
# 浏览器打开测试
# 按 F12 检查控制台和网络
```

---

## ✅ 资源/API 检查

- [ ] API 额度/余额充足（智谱、Gemini 等）
- [ ] 环境变量已配置（.env 文件）
- [ ] 外部资源可访问（图片、字体等）
- [ ] 网络可访问目标服务（GitHub、Vercel 等）

**检查命令**：
```bash
# 测试网络
ping github.com
curl -I https://generativelanguage.googleapis.com

# 检查环境变量
cat .env | grep API_KEY
```

---

## ✅ 文档检查

- [ ] 相关 Skill 文档已阅读（SKILL.md）
- [ ] 变更已记录（更新日志或提交信息）
- [ ] 需求文档已更新（issues/*.md）
- [ ] 测试报告已生成（如有重大变更）

---

## ✅ Git 检查

- [ ] 当前分支正确（main 或 feature 分支）
- [ ] 无敏感文件提交（.env、密钥等）
- [ ] 提交信息规范（feat/fix/docs 等前缀）
- [ ] 已拉取最新代码（git pull）

---

## 🚨 红线（任何一项为否，禁止提交）

- [ ] 构建失败 → ❌ 禁止提交
- [ ] 测试失败 → ❌ 禁止提交
- [ ] 核心功能不可用 → ❌ 禁止提交
- [ ] 资源 404 → ❌ 禁止提交
- [ ] 控制台有未处理错误 → ❌ 禁止提交

---

## 📋 快速检查脚本

创建 `pre_commit_check.sh` 或 `pre_commit_check.bat`：

```bash
#!/bin/bash
echo "🔍 开始提交前检查..."

echo "1/5 TypeScript 编译..."
npm run build || { echo "❌ 编译失败"; exit 1; }

echo "2/5 检查 dist 目录..."
test -d dist/assets || { echo "❌ dist/assets 不存在"; exit 1; }

echo "3/5 运行测试..."
npm test || { echo "❌ 测试失败"; exit 1; }

echo "4/5 检查资源..."
# 自定义检查逻辑

echo "5/5 质量门..."
./quality_gate.bat || { echo "❌ 质量门未通过"; exit 1; }

echo "✅ 所有检查通过！"
```

---

## 📝 检查记录

| 日期 | 提交内容 | 检查人 | 状态 | 备注 |
|------|----------|--------|------|------|
| 2026-04-08 | Issue #6-7 | Copaw | ❌ | 未检查 dist 目录 |
| 2026-04-08 | Vite 配置修复 | Copaw | ✅ | 已补检查 |

---

**最后确认**：

> ⚠️ **记住今天的教训**：2026-04-08 因为未检查 `dist/` 目录，导致 Vercel 部署后资源 404，浪费 2 小时排查。
> 
> **不再犯同样的错误！**

---

**创建日期**: 2026-04-08  
**更新日期**: 2026-04-08  
**版本**: 1.0  
**强制执行**: ✅ 是
