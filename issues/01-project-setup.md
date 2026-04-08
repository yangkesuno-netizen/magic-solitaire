---
name: Day 1 - 项目 Setup
about: 初始化项目脚手架
---

## 任务描述

初始化 Magic Solitaire 项目脚手架，包含 Phaser 3 + TypeScript + Vite 配置

## 用户故事

- 作为 **开发者**, 我想要 **快速开始项目**, 以便 **立即开始开发游戏**

## 技术要求

- [x] TypeScript 严格模式
- [x] ESLint 配置
- [x] Vite 构建工具
- [x] Phaser 3 游戏引擎
- [x] 基础目录结构

## 详细任务

### 1. 初始化 npm 项目

```bash
npm init -y
```

### 2. 安装依赖

```bash
# 核心依赖
npm install phaser

# 开发依赖
npm install -D typescript vite @vitejs/plugin-react
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
npm install -D jest ts-jest @types/jest
npm install -D @types/node
```

### 3. 创建配置文件

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "types": ["phaser"]
  },
  "include": ["src"]
}
```

**vite.config.ts**:
```typescript
import { defineConfig } from 'vite'

export default defineConfig({
  resolve: {
    alias: {
      '@': '/src',
    },
  },
  server: {
    port: 3000,
  },
})
```

### 4. 创建目录结构

```
src/
├── objects/          # 游戏对象
├── scenes/           # Phaser 场景
├── config/           # 配置
├── types/            # 类型定义
└── main.ts           # 入口文件

public/
└── assets/           # 游戏资源
```

### 5. 创建入口文件

**src/main.ts**:
```typescript
import Phaser from 'phaser'

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: 'game-container',
  backgroundColor: '#1a1a2e',
  scene: [],
}

const game = new Phaser.Game(config)

console.log('🎮 Magic Solitaire initialized!')
```

### 6. 创建 HTML 文件

**index.html**:
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Magic Solitaire</title>
    <style>
      body {
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background: #0f0f1a;
      }
      #game-container {
        border: 2px solid #4a4a6a;
      }
    </style>
  </head>
  <body>
    <div id="game-container"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

### 7. 配置 package.json scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext .ts",
    "test": "jest"
  }
}
```

## 验收标准

- [ ] `npm run dev` 可以启动开发服务器
- [ ] 浏览器打开 http://localhost:3000 显示游戏窗口
- [ ] TypeScript 无错误
- [ ] ESLint 检查通过
- [ ] 目录结构完整

## 任务分配

- **负责 Agent**: @DevBot
- **预计时间**: 4 小时
- **优先级**: P0 (紧急)

## 相关文件

- `package.json`
- `tsconfig.json`
- `vite.config.ts`
- `src/main.ts`
- `index.html`

## 备注

这是 Day 1 的第一个任务，完成后才能进行其他开发任务。
