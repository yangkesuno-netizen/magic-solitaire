#!/usr/bin/env python3
"""
Ollama 嵌入服务性能基准测试
测试不同长度文本的嵌入生成速度
"""

import json
import urllib.request
import time

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL = "mxbai-embed-large"

def test_embedding(text, description):
    """测试单个文本的嵌入生成时间"""
    payload = {
        "model": MODEL,
        "prompt": text
    }
    
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method='POST'
    )
    
    start_time = time.time()
    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode('utf-8'))
    end_time = time.time()
    
    elapsed = end_time - start_time
    vector_dim = len(result['embedding']) if 'embedding' in result else 0
    
    return elapsed, vector_dim

print("=" * 70)
print("Ollama 嵌入服务性能基准测试")
print("=" * 70)
print(f"模型: {MODEL}")
print(f"设备: 本地 CPU")
print()

# 测试用例
test_cases = [
    ("短文本 (10字)", "测试中文嵌入"),
    ("中等文本 (50字)", "这是一个用于测试Ollama嵌入服务性能的中等长度文本，包含一些中文内容。"),
    ("长文本 (100字)", "这是一个用于测试Ollama嵌入服务性能的较长文本。我们需要测试不同长度的文本对嵌入生成速度的影响。文本越长，处理时间通常也会相应增加。"),
    ("文章段落 (200字)", """自然语言处理是人工智能领域的重要分支。它研究如何让计算机理解、处理和生成人类语言。
    嵌入向量是将文本转换为数值表示的关键技术。通过将文本映射到高维向量空间，
    我们可以计算文本之间的相似度，实现语义搜索、文本分类等应用。
    Ollama提供了在本地运行大语言模型的能力，无需依赖云服务。"""),
    ("记忆搜索查询", "核心规矩 追求卓越 不断进化"),
]

results = []

for desc, text in test_cases:
    char_count = len(text)
    
    # 预热
    try:
        test_embedding(text[:10], "warmup")
    except:
        pass
    
    # 正式测试3次取平均
    times = []
    for _ in range(3):
        try:
            elapsed, dim = test_embedding(text, desc)
            times.append(elapsed)
        except Exception as e:
            print(f"[ERROR] {desc}: {e}")
            break
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        results.append((desc, char_count, avg_time, dim))
        
        print(f"{desc}:")
        print(f"  字符数: {char_count}")
        print(f"  平均时间: {avg_time:.3f}s")
        print(f"  时间范围: {min_time:.3f}s - {max_time:.3f}s")
        print(f"  向量维度: {dim}")
        print()

# 总结
print("=" * 70)
print("性能总结")
print("=" * 70)

if results:
    avg_all = sum(r[2] for r in results) / len(results)
    print(f"平均生成时间: {avg_all:.3f}s")
    print()
    
    # 评估性能
    if avg_all < 0.5:
        perf_level = "优秀"
        recommendation = "性能很好，可以放心使用"
    elif avg_all < 1.0:
        perf_level = "良好"
        recommendation = "性能不错，适合日常使用"
    elif avg_all < 2.0:
        perf_level = "一般"
        recommendation = "速度较慢，但可接受"
    elif avg_all < 5.0:
        perf_level = "较慢"
        recommendation = "建议考虑云端替代方案"
    else:
        perf_level = "很慢"
        recommendation = "强烈建议使用云端服务"
    
    print(f"性能评级: {perf_level}")
    print(f"建议: {recommendation}")
    
    print()
    print("对比参考:")
    print("  - OpenAI API: ~0.1-0.3s (云端GPU)")
    print("  - 阿里云 DashScope: ~0.2-0.5s (云端GPU)")
    print("  - Ollama本地(CPU): 取决于CPU性能")
    print()
    print("注意: 首次加载模型需要额外时间(模型预热)")

print("=" * 70)
