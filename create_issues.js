#!/usr/bin/env node

/**
 * GitHub Issues 批量创建脚本
 * 使用 GitHub REST API 创建 Day 1 Issues
 */

import { execSync } from 'child_process';

// 获取 GitHub Token (从环境变量或 gh CLI)
function getGitHubToken() {
  try {
    // 先尝试环境变量
    if (process.env.GITHUB_TOKEN) {
      return process.env.GITHUB_TOKEN;
    }
    
    // 尝试从 gh CLI 获取 token
    const token = execSync('gh auth token', { encoding: 'utf8' }).trim();
    return token;
  } catch (error) {
    console.error('❌ 无法获取 GitHub Token');
    console.error('请先运行：gh auth login');
    console.error('或者设置环境变量：GITHUB_TOKEN=your_token');
    process.exit(1);
  }
}

// GitHub API 请求
async function githubAPI(endpoint, method = 'GET', data = null) {
  const token = getGitHubToken();
  const url = `https://api.github.com${endpoint}`;
  
  const options = {
    method,
    headers: {
      'Authorization': `token ${token}`,
      'Accept': 'application/vnd.github.v3+json',
      'Content-Type': 'application/json',
    },
  };
  
  if (data) {
    options.body = JSON.stringify(data);
  }
  
  try {
    const response = await fetch(url, options);
    const result = await response.json();
    
    if (!response.ok) {
      throw new Error(result.message || `HTTP ${response.status}`);
    }
    
    return result;
  } catch (error) {
    console.error(`❌ API 请求失败：${endpoint}`);
    console.error(`   ${error.message}`);
    throw error;
  }
}

// 创建 Label
async function createLabel(owner, repo, name, color) {
  try {
    await githubAPI(`/repos/${owner}/${repo}/labels`, 'POST', {
      name,
      color,
    });
    console.log(`✅ Label 创建成功：${name}`);
  } catch (error) {
    if (error.message.includes('already exists')) {
      console.log(`⚠️  Label 已存在：${name}`);
    } else {
      console.error(`❌ 创建 Label 失败：${name}`);
    }
  }
}

// 创建 Issue
async function createIssue(owner, repo, issue) {
  console.log(`\n📝 创建 Issue: ${issue.title}`);
  
  try {
    const result = await githubAPI(`/repos/${owner}/${repo}/issues`, 'POST', {
      title: issue.title,
      body: issue.body,
      labels: issue.labels,
    });
    
    console.log(`✅ Issue #${result.number} 创建成功`);
    console.log(`   URL: ${result.html_url}`);
    return result;
  } catch (error) {
    console.error(`❌ Issue 创建失败：${issue.title}`);
    console.error(`   ${error.message}`);
    return null;
  }
}

// Day 1 Issues 列表
const issues = [
  {
    title: '[Feature] 项目 setup - 初始化 Phaser 3 + TypeScript + Vite',
    body: `## 任务描述
初始化游戏项目基础结构，配置 Phaser 3 + TypeScript + Vite

## 技术要求
- Phaser 3.80+
- TypeScript 5.2+
- Vite 5.0+
- 支持热重载

## 验收标准
- [ ] package.json 配置完成
- [ ] TypeScript 配置完成
- [ ] Vite 构建成功
- [ ] Phaser 游戏窗口显示
- [ ] npm run dev 可启动

## 相关文件
- package.json
- tsconfig.json
- vite.config.ts
- src/main.ts
- index.html`,
    labels: ['feature', 'P0'],
  },
  {
    title: '[Feature] 实现 Card 类 - 卡牌对象基础功能',
    body: `## 任务描述
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
- src/game/__tests__/Card.test.ts`,
    labels: ['feature', 'P0'],
  },
  {
    title: '[Feature] 实现 CardStack 类 - 牌堆管理',
    body: `## 任务描述
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
- src/game/__tests__/CardStack.test.ts`,
    labels: ['feature', 'P0'],
  },
  {
    title: '[Feature] 实现 Tri-Peaks 消除规则',
    body: `## 任务描述
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
- src/game/__tests__/TriPeaksRules.test.ts`,
    labels: ['feature', 'P0'],
  },
  {
    title: '[Feature] 基础 UI - 游戏流程界面',
    body: `## 任务描述
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
- src/scenes/GameScene.ts`,
    labels: ['feature', 'P1'],
  },
  {
    title: '[Art] 卡牌背面设计 - 魔法学院风格',
    body: `## 任务描述
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
- 智谱 AI API (已配置)`,
    labels: ['art', 'P1'],
  },
  {
    title: '[Art] 背景图生成 (5 张) - 魔法学院场景',
    body: `## 任务描述
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
- 智谱 AI API`,
    labels: ['art', 'P1'],
  },
  {
    title: '[Design] 生成 50 关 Tri-Peaks 配置',
    body: `## 任务描述
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
- src/data/levels.json`,
    labels: ['design', 'P1'],
  },
  {
    title: '[Test] 核心玩法测试 - 单元测试 + E2E',
    body: `## 任务描述
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
- tests/e2e/gameplay.spec.ts`,
    labels: ['test', 'P0'],
  },
];

// 主函数
async function main() {
  const owner = 'yangkesuno-netizen';
  const repo = 'magic-solitaire';
  
  console.log('🚀 开始创建 GitHub Issues');
  console.log(`📁 仓库：${owner}/${repo}`);
  console.log('=' .repeat(50));
  
  // 先创建 Labels
  console.log('\n📋 创建 Labels...');
  const labels = [
    { name: 'feature', color: 'a2eeef' },
    { name: 'art', color: '0075ca' },
    { name: 'design', color: 'c5def5' },
    { name: 'test', color: 'e4e669' },
    { name: 'P0', color: 'd73a4a' },
    { name: 'P1', color: 'fbca04' },
  ];
  
  for (const label of labels) {
    await createLabel(owner, repo, label.name, label.color);
  }
  
  // 创建 Issues
  console.log('\n📝 创建 Issues...');
  console.log('=' .repeat(50));
  
  let successCount = 0;
  for (const issue of issues) {
    const result = await createIssue(owner, repo, issue);
    if (result) {
      successCount++;
    }
  }
  
  // 总结
  console.log('\n' + '=' .repeat(50));
  console.log(`✅ 完成！创建 ${successCount}/${issues.length} 个 Issues`);
  console.log(`📋 查看：https://github.com/${owner}/${repo}/issues`);
}

// 运行
main().catch(console.error);
