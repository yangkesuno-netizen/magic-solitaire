# GitHub 仓库创建指南

**用户名**: yangkesuno-netizen  
**仓库名**: magic-solitaire  
**更新时间**: 2026-04-08

---

## Step 1: 登录 GitHub CLI

```bash
gh auth login
```

**操作流程**:
1. 运行上述命令
2. 选择 `GitHub.com`
3. 选择 `HTTPS`
4. 选择 `Login with a web browser`
5. 复制 One-Time Code
6. 在浏览器打开 https://github.com/login/device
7. 粘贴代码并授权
8. 返回命令行，按 Enter

---

## Step 2: 创建 GitHub 仓库

```bash
# 创建私有仓库
gh repo create magic-solitaire --private --source=. --remote=origin
```

**说明**:
- `--private`: 私有仓库 (推荐)
- `--source=.`: 使用当前目录
- `--remote=origin`: 设置远程仓库名为 origin

---

## Step 3: 推送代码到 GitHub

```bash
# 初始化 Git (如果还没初始化)
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: AI team workspace setup

- AI Agent team configuration (v6.9 Ultimate)
- GitHub Actions CI/CD pipeline
- Vercel deployment config
- Issue templates (5 types)
- Environment variables setup
- Day 1 tasks ready

Co-Authored-By: AI Agent Team <ai-agent@copaw.local>"

# 推送
git push -u origin main
```

---

## Step 4: 验证推送

```bash
# 查看远程仓库
gh repo view magic-solitaire

# 或在浏览器打开
# https://github.com/yangkesuno-netizen/magic-solitaire
```

---

## Step 5: 导入到 Vercel

1. **访问**: https://vercel.com/new
2. **登录**: 使用 GitHub 账号
3. **Import Git Repository**:
   - 找到 `magic-solitaire`
   - 点击 "Import"
4. **配置项目**:
   - Framework Preset: `Vite`
   - Root Directory: `./`
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. **点击 "Deploy"**
6. **等待部署完成** (1-2 分钟)

---

## Step 6: 获取 Vercel Org ID 和 Project ID

### 方法 A: 从 URL 获取

1. 部署成功后，进入项目 Dashboard
2. 查看 URL:
   ```
   https://vercel.com/[ORG_ID]/magic-solitaire
   ```
3. `ORG_ID` = URL 中的第一部分

### 方法 B: 从 Settings 获取

1. 点击项目 → Settings → General
2. 找到:
   - **Project ID**: `prj_xxxxxxxxxxxxx`
   - **Team ID** (或 Account ID): 你的 org ID

### 方法 C: 使用 Vercel CLI

```bash
# 安装 Vercel CLI (如果还没安装)
npm install -g vercel

# 登录
vercel login

# 查看项目信息
vercel ls

# 输出示例:
# ✅  magic-solitaire [yangkesuno-netizen]
#    Project ID: prj_xxxxxxxxxxxxx
```

---

## Step 7: 更新 .env 文件

打开 `.env` 文件，填入获取的 IDs:

```bash
VERCEL_ORG_ID=yangkesuno-netizen
VERCEL_PROJECT_ID=prj_xxxxxxxxxxxxx
```

---

## 📋 检查清单

- [ ] 登录 GitHub CLI (`gh auth login`)
- [ ] 创建仓库 (`gh repo create`)
- [ ] 推送代码 (`git push`)
- [ ] 验证推送成功
- [ ] 导入到 Vercel
- [ ] 部署成功
- [ ] 获取 Org ID
- [ ] 获取 Project ID
- [ ] 更新 `.env` 文件

---

## 🔒 安全提醒

- ✅ 仓库已设为私有
- ✅ `.env` 文件在 `.gitignore` 中
- ✅ API Keys 不会被提交
- ⚠️ 如果改为公开仓库，确保 `.env` 不包含敏感信息

---

## 📞 遇到问题？

### 问题 1: gh auth login 失败
**解决**: 确保已登录 GitHub 网页版，然后重试

### 问题 2: 仓库已存在
**解决**: 使用不同名称或删除现有仓库

### 问题 3: git push 失败
**解决**: 检查是否已设置远程仓库
```bash
git remote -v
git remote add origin https://github.com/yangkesuno-netizen/magic-solitaire.git
```

### 问题 4: Vercel 导入失败
**解决**: 确保 GitHub 账号已授权 Vercel 访问

---

**下一步**: 执行 Step 1 登录 GitHub CLI，然后继续！
