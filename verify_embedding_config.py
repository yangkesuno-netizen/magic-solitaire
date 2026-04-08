#!/usr/bin/env python3
"""
验证 Ollama 嵌入服务配置
"""

import os
import json
import urllib.request

print("=" * 70)
print("Ollama 嵌入服务配置验证")
print("=" * 70)

# 目标配置
target_config = {
    "EMBEDDING_BASE_URL": "http://localhost:11434",
    "EMBEDDING_MODEL_NAME": "mxbai-embed-large",
    "EMBEDDING_API_KEY": "ollama"
}

print("\n目标配置:")
for key, value in target_config.items():
    print(f"  {key}={value}")

print("\n当前环境变量 (os.environ):")
all_correct = True
for key, target_value in target_config.items():
    current = os.environ.get(key, 'NOT SET')
    status = "OK" if current == target_value else "MISMATCH"
    if status != "OK":
        all_correct = False
    print(f"  {key}: {current} [{status}]")

# 测试 Ollama 连接
print("\n测试 Ollama 嵌入服务...")
try:
    url = "http://localhost:11434/api/embeddings"
    payload = {
        "model": "mxbai-embed-large",
        "prompt": "测试中文嵌入"
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method='POST'
    )
    
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        
        if 'embedding' in result:
            embedding = result['embedding']
            print(f"  [SUCCESS] Ollama 服务正常")
            print(f"  模型: mxbai-embed-large")
            print(f"  维度: {len(embedding)}")
            print(f"  前3个值: {embedding[:3]}")
            service_ok = True
        else:
            print(f"  [FAIL] 返回异常")
            service_ok = False
            
except Exception as e:
    print(f"  [FAIL] {str(e)}")
    service_ok = False

print("\n" + "=" * 70)
if all_correct and service_ok:
    print("配置验证通过！Ollama 嵌入服务已就绪")
elif service_ok:
    print("服务正常，但环境变量可能需重启后生效")
else:
    print("配置存在问题，请检查")
print("=" * 70)
