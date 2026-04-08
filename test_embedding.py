#!/usr/bin/env python3
"""
测试嵌入服务配置
对比阿里云 vs Ollama 本地
"""

import os
import json
import urllib.request
import urllib.error

print("=" * 70)
print("嵌入服务测试")
print("=" * 70)

# 当前配置
aliyun_url = "https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings"
ollama_url = "http://localhost:11434/api/embeddings"

print("\n当前环境变量:")
print(f"  EMBEDDING_BASE_URL: {os.environ.get('EMBEDDING_BASE_URL', 'NOT SET')}")
print(f"  EMBEDDING_MODEL_NAME: {os.environ.get('EMBEDDING_MODEL_NAME', 'NOT SET')}")
print(f"  EMBEDDING_API_KEY: {os.environ.get('EMBEDDING_API_KEY', 'NOT SET')}")

# 测试文本
test_text = "测试中文嵌入向量生成"

# 测试 1: 阿里云 DashScope
print("\n" + "-" * 70)
print("测试 1: 阿里云 DashScope")
print("-" * 70)

aliyun_key = os.environ.get('EMBEDDING_API_KEY', '')
if not aliyun_key or aliyun_key == 'ollama':
    print("[SKIP] EMBEDDING_API_KEY 未配置或为 'ollama' (阿里云需要有效 key)")
else:
    try:
        payload = {
            "model": "text-embedding-v2",
            "input": test_text
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {aliyun_key}"
        }
        
        req = urllib.request.Request(
            aliyun_url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if 'data' in result and len(result['data']) > 0:
                embedding = result['data'][0]['embedding']
                print(f"[SUCCESS] 阿里云嵌入服务正常")
                print(f"  向量维度: {len(embedding)}")
                print(f"  前5个值: {embedding[:5]}")
            else:
                print(f"[WARNING] 返回异常: {result}")
                
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"[FAIL] HTTP {e.code}: {error_body[:200]}")
    except Exception as e:
        print(f"[FAIL] {str(e)}")

# 测试 2: Ollama 本地
print("\n" + "-" * 70)
print("测试 2: Ollama 本地 (mxbai-embed-large)")
print("-" * 70)

try:
    payload = {
        "model": "mxbai-embed-large",
        "prompt": test_text
    }
    
    req = urllib.request.Request(
        ollama_url,
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method='POST'
    )
    
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        
        if 'embedding' in result:
            embedding = result['embedding']
            print(f"[SUCCESS] Ollama 本地嵌入服务正常")
            print(f"  向量维度: {len(embedding)}")
            print(f"  前5个值: {embedding[:5]}")
        else:
            print(f"[WARNING] 返回异常: {result}")
            
except urllib.error.HTTPError as e:
    error_body = e.read().decode('utf-8')
    print(f"[FAIL] HTTP {e.code}: {error_body[:200]}")
except urllib.error.URLError as e:
    print(f"[FAIL] 无法连接 Ollama: {e.reason}")
    print("  请检查: 1) Ollama 是否运行 2) 端口 11434 是否开放")
except Exception as e:
    print(f"[FAIL] {str(e)}")

print("\n" + "=" * 70)
print("总结")
print("=" * 70)
print("当前 EMBEDDING_BASE_URL 指向阿里云，但:")
print("  - 如果 EMBEDDING_API_KEY=ollama，阿里云会拒绝请求")
print("  - 需要配置阿里云 DashScope 的有效 API Key")
print("  - 或改回 Ollama 本地: http://localhost:11434")
print("=" * 70)
