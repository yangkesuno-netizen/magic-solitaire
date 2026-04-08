#!/usr/bin/env python3
"""
测试智谱 AI API Key 是否有效
"""

import os
import json
import urllib.request
import urllib.error

api_key = "973ccc639962481c8503d8e42b2d8a44.3GNlrfBErfKLgSVI"

print("=" * 60)
print("智谱 AI API Key 测试")
print("=" * 60)

# Test API Key format
if not api_key:
    print("❌ API Key 未设置")
    exit(1)

if len(api_key) < 20:
    print(f"❌ API Key 格式异常 (长度: {len(api_key)})")
    exit(1)

print(f"✓ API Key 已设置 (长度: {len(api_key)})")
print(f"  Key: {api_key[:8]}...{api_key[-4:]}")

# Test API connection
url = "https://open.bigmodel.cn/api/paas/v4/images/generations"

payload = {
    "model": "cogview-3",
    "prompt": "一只可爱的猫咪",
    "n": 1,
    "size": "1024x1024"
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

print("\n测试 API 连接...")
print(f"  URL: {url}")
print(f"  Model: cogview-3")

try:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.loads(response.read().decode('utf-8'))
        
        if 'data' in result:
            image_url = result['data'][0]['url']
            print(f"\n✅ API 测试成功!")
            print(f"  图片 URL: {image_url[:60]}...")
            print("\n智谱 AI 图像生成已就绪!")
        else:
            print(f"\n⚠️ API 返回异常: {result}")
            
except urllib.error.HTTPError as e:
    error_body = e.read().decode('utf-8')
    print(f"\n❌ HTTP 错误 {e.code}: {error_body}")
except Exception as e:
    print(f"\n❌ 请求失败: {str(e)}")

print("=" * 60)
