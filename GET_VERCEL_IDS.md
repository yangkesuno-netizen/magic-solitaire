# 获取 Vercel Org ID 和 Project ID 指南

**更新时间**: 2026-04-07  
**状态**: ⏳ 待完成

---

## 方法一：通过 Vercel Dashboard (推荐，5 分钟)

### Step 1: 创建 Vercel 项目

1. **访问**: https://vercel.com/new
2. **登录**: 使用 GitHub 账号登录
3. **Import Git Repository**:
   - 如果你的代码已推到 GitHub:
     - 点击 "Import Git Repository"
     - 选择 `magic-solitaire` 仓库
   - 如果还没创建 GitHub 仓库:
     - 先创建 GitHub 仓库 (见下方)
     - 然后返回导入

### Step 2: 部署项目

1. **Configure Project**:
   - Framework Preset: `Vite`
   - Root Directory: `./`
   - Build Command: `npm run build`
   - Output Directory: `dist`
2. **点击 "Deploy"**
3. **等待部署完成** (约 1-2 分钟)

### Step 3: 获取 Org ID 和 Project ID

1. **进入项目 Dashboard**:
   - 部署成功后，点击项目卡片
   - 或访问：https://vercel.com/dashboard

2. **查看 URL**:
   ```
   https://vercel.com/[ORG_ID]/[PROJECT_NAME]
   ```
   - `ORG_ID` = 你的组织 ID (通常是你的用户名或团队名)
   - `PROJECT_NAME` = 项目名称

3. **获取 Project ID**:
   - 点击项目 → Settings → General
   - 找到 **Project ID** (格式：`prj_xxxxxxxxxxxxx`)
   - 复制并填入 `.env`:
     ```bash
     VERCEL_PROJECT_ID=prj_xxxxxxxxxxxxx
     ```

4. **获取 Org ID**:
   - 在 Settings → General 页面
   - 找到 **Account** 或 **Team** 信息
   - 或使用 URL 中的 org ID
   - 填入 `.env`:
     ```bash
     VERCEL_ORG_ID=你的 org_id
     ```

---

## 方法二：使用 Vercel CLI (3 分钟)

### Step 1: 安装 Vercel CLI

```bash
npm install -g vercel
```

### Step 2: 登录

```bash
vercel login
```

选择登录方式 (推荐 GitHub)

### Step 3: 初始化项目

```bash
# 在项目根目录执行
vercel

# 首次会提示:
# - Set up and deploy? Y
# - Which scope? (选择你的账号)
# - Link to existing project? N
# - Project name? magic-solitaire
# - Directory? ./
```

### Step 4: 获取项目信息

```bash
# 查看项目列表
vercel ls

# 输出示例:
# ✅  magic-solitaire [your-username]
#    https://magic-solitaire-xxx.vercel.app
#    Project ID: prj_xxxxxxxxxxxxx
```

### Step 5: 更新 .env

```bash
VERCEL_ORG_ID=your-username
VERCEL_PROJECT_ID=prj_xxxxxxxxxxxxx
```

---

## 方法三：先创建 GitHub 仓库 (如果需要)

### Step 1: 创建 GitHub 仓库

**方式 A: GitHub 网页**
1. 访问：https://github.com/new
2. 填写:
   - Repository name: `magic-solitaire`
   - Description: `AI-powered Tri-Peaks Solitaire game`
   - Visibility: `Private` (推荐) 或 `Public`
   - **不要** 勾选 "Add a README file"
3. 点击 "Create repository"

**方式 B: GitHub CLI**
```bash
gh repo create magic-solitaire --private --source=. --remote=origin
```

### Step 2: 推送代码

```bash
# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: AI team workspace setup"

# 关联远程仓库
git remote add origin https://github.com/YOUR_USERNAME/magic-solitaire.git

# 推送
git push -u origin main
```

### Step 3: 导入到 Vercel

1. 访问：https://vercel.com/new
2. 点击 "Import Git Repository"
3. 选择 `magic-solitaire` 仓库
4. 点击 "Deploy"

---

## 📋 检查清单

- [ ] 创建 GitHub 仓库
- [ ] 推送代码到 GitHub
- [ ] 创建 Vercel 项目
- [ ] 部署成功
- [ ] 获取 Org ID
- [ ] 获取 Project ID
- [ ] 更新 `.env` 文件

---

## 🔒 安全提醒

- ✅ `.env` 文件已在 `.gitignore` 中，不会被提交
- ✅ Vercel Token 已配置，可以安全部署
- ⚠️ 不要将 `.env` 文件上传到公开仓库
- ⚠️ 如果 Token 泄露，立即在 Vercel 设置中撤销

---

## 📞 需要帮助？

如果你遇到问题：

1. **GitHub 创建失败**: 检查用户名是否正确
2. **Vercel 部署失败**: 查看部署日志
3. **找不到 Org ID**: 检查 URL 或 Settings 页面
4. **其他问题**: 查看 Vercel 文档 https://vercel.com/docs

---

**下一步**: 选择一种方法获取 Org ID 和 Project ID，然后更新 `.env` 文件！
