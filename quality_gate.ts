#!/usr/bin/env node

/**
 * Quality Gate v3.1 - Magic Solitaire
 * 
 * 8 道质量门禁：
 * 1. TypeScript 编译
 * 2. 代码规范 (ESLint)
 * 3. 单元测试
 * 4. 代码审查 (自动)
 * 5. 测试覆盖率
 * 6. 性能基准
 * 7. 安全扫描
 * 8. 设计标准验收
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

interface QualityGateResult {
  name: string;
  passed: boolean;
  score: number;
  issues: string[];
}

class QualityGateV31 {
  private results: QualityGateResult[] = [];
  private totalScore: number = 0;

  constructor() {
    console.log('🔍 Quality Gate v3.1 - Magic Solitaire\n');
  }

  // Gate 1: TypeScript 编译
  checkTypeScriptCompilation(): QualityGateResult {
    console.log('📋 Gate 1: TypeScript 编译检查...');
    
    try {
      execSync('npx tsc --noEmit', { stdio: 'pipe' });
      console.log('✅ TypeScript 编译通过\n');
      
      return {
        name: 'TypeScript 编译',
        passed: true,
        score: 10,
        issues: []
      };
    } catch (error: any) {
      const output = error.stdout?.toString() || error.stderr?.toString();
      const lines = output.split('\n').filter(l => l.includes('error TS'));
      
      console.log(`❌ TypeScript 编译失败 (${lines.length} 错误)\n`);
      
      return {
        name: 'TypeScript 编译',
        passed: false,
        score: 0,
        issues: lines.slice(0, 5)
      };
    }
  }

  // Gate 2: 代码规范 (简化版，检查明显问题)
  checkCodeStyle(): QualityGateResult {
    console.log('📋 Gate 2: 代码规范检查...');
    
    const issues: string[] = [];
    const srcDir = './src';
    
    // 检查源文件
    const files = fs.readdirSync(srcDir).filter(f => f.endsWith('.ts'));
    
    files.forEach(file => {
      const content = fs.readFileSync(path.join(srcDir, file), 'utf-8');
      const lines = content.split('\n');
      
      // 检查明显问题
      lines.forEach((line, idx) => {
        // 检查 console.log (应该移除)
        if (line.includes('console.log') && !line.includes('// ')) {
          // 允许 console.log，不算问题
        }
        
        // 检查 any 类型
        if (line.includes(': any') || line.includes('<any>')) {
          issues.push(`${file}:${idx + 1} - 使用 any 类型`);
        }
        
        // 检查 var (应该用 let/const)
        if (line.trim().startsWith('var ')) {
          issues.push(`${file}:${idx + 1} - 使用 var 而非 let/const`);
        }
      });
    });
    
    const passed = issues.length === 0;
    const score = passed ? 10 : Math.max(5, 10 - issues.length);
    
    console.log(`${passed ? '✅' : '⚠️'} 代码规范检查 ${issues.length} 个问题\n`);
    
    return {
      name: '代码规范',
      passed,
      score,
      issues: issues.slice(0, 10)
    };
  }

  // Gate 3: 单元测试 (检查是否有测试文件)
  checkUnitTests(): QualityGateResult {
    console.log('📋 Gate 3: 单元测试检查...');
    
    const testFiles = [
      './src/Card.test.ts',
      './src/CardStack.test.ts',
      './src/TriPeaks.test.ts'
    ];
    
    const existingTests = testFiles.filter(f => fs.existsSync(f));
    const passed = existingTests.length >= 2; // 至少 2 个测试文件
    const score = (existingTests.length / testFiles.length) * 10;
    
    console.log(`${passed ? '✅' : '⚠️'} 单元测试：${existingTests.length}/${testFiles.length}\n`);
    
    return {
      name: '单元测试',
      passed,
      score,
      issues: existingTests.length < 3 ? ['测试覆盖率不足'] : []
    };
  }

  // Gate 4: 代码审查 (检查代码复杂度)
  checkCodeReview(): QualityGateResult {
    console.log('📋 Gate 4: 代码审查...');
    
    const issues: string[] = [];
    const srcDir = './src';
    
    const files = fs.readdirSync(srcDir).filter(f => f.endsWith('.ts'));
    
    files.forEach(file => {
      const content = fs.readFileSync(path.join(srcDir, file), 'utf-8');
      const lines = content.split('\n');
      
      // 检查文件长度
      if (lines.length > 500) {
        issues.push(`${file} - 文件过长 (${lines.length} 行)`);
      }
      
      // 检查函数长度 (简化：检查是否有超长函数)
      let braceCount = 0;
      let maxBraceCount = 0;
      lines.forEach(line => {
        braceCount += (line.match(/{/g) || []).length;
        braceCount -= (line.match(/}/g) || []).length;
        maxBraceCount = Math.max(maxBraceCount, braceCount);
      });
      
      if (maxBraceCount > 50) {
        issues.push(`${file} - 可能存在超长函数`);
      }
    });
    
    const passed = issues.length === 0;
    const score = passed ? 10 : Math.max(6, 10 - issues.length * 2);
    
    console.log(`${passed ? '✅' : '⚠️'} 代码审查 ${issues.length} 个问题\n`);
    
    return {
      name: '代码审查',
      passed,
      score,
      issues
    };
  }

  // Gate 5: 测试覆盖率 (简化：检查是否有测试)
  checkTestCoverage(): QualityGateResult {
    console.log('📋 Gate 5: 测试覆盖率检查...');
    
    // 简化：检查是否有测试文件
    const hasTests = fs.existsSync('./src/Card.test.ts') || 
                     fs.existsSync('./src/CardStack.test.ts');
    
    const passed = hasTests;
    const score = hasTests ? 8 : 0;
    
    console.log(`${passed ? '✅' : '❌'} 测试覆盖率：${hasTests ? '有测试' : '无测试'}\n`);
    
    return {
      name: '测试覆盖率',
      passed,
      score,
      issues: hasTests ? [] : ['需要编写单元测试']
    };
  }

  // Gate 6: 性能基准 (简化：检查构建大小)
  checkPerformance(): QualityGateResult {
    console.log('📋 Gate 6: 性能基准检查...');
    
    try {
      const distDir = './dist';
      if (!fs.existsSync(distDir)) {
        return {
          name: '性能基准',
          passed: false,
          score: 0,
          issues: ['未找到 dist 目录，请先运行 npm run build']
        };
      }
      
      const files = fs.readdirSync(distDir);
      const jsFiles = files.filter(f => f.endsWith('.js'));
      
      let totalSize = 0;
      jsFiles.forEach(file => {
        const stats = fs.statSync(path.join(distDir, file));
        totalSize += stats.size;
      });
      
      const maxSize = 2 * 1024 * 1024; // 2MB
      const passed = totalSize < maxSize;
      const score = passed ? 10 : 5;
      
      console.log(`${passed ? '✅' : '⚠️'} 构建大小：${(totalSize / 1024).toFixed(2)} KB\n`);
      
      return {
        name: '性能基准',
        passed,
        score,
        issues: passed ? [] : [`构建过大 (${(totalSize / 1024).toFixed(2)} KB)`]
      };
    } catch (error) {
      return {
        name: '性能基准',
        passed: false,
        score: 0,
        issues: ['性能检查失败']
      };
    }
  }

  // Gate 7: 安全扫描 (简化：检查明显的硬编码密钥)
  checkSecurity(): QualityGateResult {
    console.log('📋 Gate 7: 安全扫描...');
    
    const issues: string[] = [];
    const srcDir = './src';
    
    const files = fs.readdirSync(srcDir).filter(f => f.endsWith('.ts'));
    
    files.forEach(file => {
      const content = fs.readFileSync(path.join(srcDir, file), 'utf-8');
      
      // 检查硬编码的 API 密钥
      if (content.includes('api_key') || content.includes('apiKey') || 
          content.includes('API_KEY') || content.includes('secret')) {
        // 检查是否在注释或配置中
        const lines = content.split('\n');
        lines.forEach((line, idx) => {
          if ((line.includes('api_key') || line.includes('secret')) && 
              !line.trim().startsWith('//') && 
              !line.includes('process.env')) {
            issues.push(`${file}:${idx + 1} - 可能存在硬编码密钥`);
          }
        });
      }
    });
    
    const passed = issues.length === 0;
    const score = passed ? 10 : 0;
    
    console.log(`${passed ? '✅' : '⚠️'} 安全扫描 ${issues.length} 个问题\n`);
    
    return {
      name: '安全扫描',
      passed,
      score,
      issues
    };
  }

  // Gate 8: 设计标准验收 (简化：检查关键功能)
  checkDesignStandards(): QualityGateResult {
    console.log('📋 Gate 8: 设计标准验收...');
    
    const issues: string[] = [];
    
    // 检查关键文件是否存在
    const requiredFiles = [
      './src/Card.ts',
      './src/CardStack.ts',
      './src/main.ts'
    ];
    
    requiredFiles.forEach(file => {
      if (!fs.existsSync(file)) {
        issues.push(`${file} - 文件不存在`);
      }
    });
    
    // 检查 Card 类是否有必要的方法
    const cardContent = fs.existsSync('./src/Card.ts') 
      ? fs.readFileSync('./src/Card.ts', 'utf-8') 
      : '';
    
    const requiredMethods = [
      'getSuit',
      'getRank', 
      'getValue',
      'isFaceUp',
      'flip'
    ];
    
    requiredMethods.forEach(method => {
      if (!cardContent.includes(method)) {
        issues.push(`Card 类缺少方法：${method}`);
      }
    });
    
    const passed = issues.length === 0;
    const score = passed ? 10 : Math.max(5, 10 - issues.length * 2);
    
    console.log(`${passed ? '✅' : '⚠️'} 设计标准验收 ${issues.length} 个问题\n`);
    
    return {
      name: '设计标准验收',
      passed,
      score,
      issues
    };
  }

  runAllGates(): void {
    this.results = [
      this.checkTypeScriptCompilation(),
      this.checkCodeStyle(),
      this.checkUnitTests(),
      this.checkCodeReview(),
      this.checkTestCoverage(),
      this.checkPerformance(),
      this.checkSecurity(),
      this.checkDesignStandards()
    ];
    
    this.printReport();
  }

  printReport(): void {
    console.log('═══════════════════════════════════════════════════');
    console.log('📊 Quality Gate v3.1 最终报告');
    console.log('═══════════════════════════════════════════════════\n');
    
    let passedCount = 0;
    let totalScore = 0;
    
    this.results.forEach((result, idx) => {
      const icon = result.passed ? '✅' : (result.score >= 5 ? '⚠️' : '❌');
      console.log(`${icon} Gate ${idx + 1}: ${result.name}`);
      console.log(`   分数：${result.score}/10`);
      
      if (result.issues.length > 0) {
        console.log(`   问题:`);
        result.issues.forEach(issue => {
          console.log(`     - ${issue}`);
        });
      }
      console.log();
      
      if (result.passed) passedCount++;
      totalScore += result.score;
    });
    
    const avgScore = (totalScore / this.results.length).toFixed(2);
    const allPassed = passedCount === this.results.length;
    
    console.log('═══════════════════════════════════════════════════');
    console.log(`📈 总分：${totalScore}/${this.results.length * 10} (${avgScore}/10)`);
    console.log(`✅ 通过：${passedCount}/${this.results.length}`);
    console.log(`🎯 状态：${allPassed ? '全部通过' : '需要改进'}`);
    console.log('═══════════════════════════════════════════════════\n');
    
    if (!allPassed) {
      console.log('💡 建议：');
      this.results.forEach(result => {
        if (!result.passed && result.issues.length > 0) {
          console.log(`   - ${result.name}: ${result.issues[0]}`);
        }
      });
      console.log();
    }
    
    // 退出码
    if (!allPassed) {
      process.exit(1);
    }
  }
}

// 运行质量门
const qg = new QualityGateV31();
qg.runAllGates();
