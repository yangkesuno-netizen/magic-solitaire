#!/usr/bin/env python3
"""搜索网页版 Solitaire 市场数据"""

import os
import sys
import io
sys.path.insert(0, 'active_skills/tavily/scripts')
from tavily_search import search

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

api_key = os.environ.get('TAVILY_API_KEY', '')

print('=' * 70)
print('网页版 Solitaire 市场调研')
print('=' * 70)

# 查询 1: 网页版 Solitaire 流量和规模
query1 = 'web based solitaire games traffic users revenue 2025 2026 browser games'

print('\n查询 1: 网页版 Solitaire 流量和规模\n')
result1 = search(
    query=query1,
    api_key=api_key,
    search_depth='advanced',
    max_results=12
)

if result1.get('success'):
    print('AI 摘要:')
    print(result1.get('answer', 'N/A'))
    print('\n详细搜索结果:')
    for i, item in enumerate(result1.get('results', [])[:8], 1):
        print(f'\n{i}. {item.get("title", "N/A")}')
        print(f'   URL: {item.get("url", "N/A")}')
        print(f'   内容：{item.get("content", "N/A")[:350]}...')

# 查询 2: Solitaire Grand Harvest 网页版
query2 = 'Solitaire Grand Harvest web version Facebook browser play online'

print('\n' + '=' * 70)
print('查询 2: Solitaire Grand Harvest 网页版信息\n')

result2 = search(
    query=query2,
    api_key=api_key,
    search_depth='advanced',
    max_results=10
)

if result2.get('success'):
    print('AI 摘要:')
    print(result2.get('answer', 'N/A'))
    print('\n详细搜索结果:')
    for i, item in enumerate(result2.get('results', [])[:6], 1):
        print(f'\n{i}. {item.get("title", "N/A")}')
        print(f'   URL: {item.get("url", "N/A")}')
        print(f'   内容：{item.get("content", "N/A")[:350]}...')

# 查询 3: 网页游戏变现模式
query3 = 'web browser games monetization 2025 advertising subscription IAP revenue'

print('\n' + '=' * 70)
print('查询 3: 网页游戏变现模式\n')

result3 = search(
    query=query3,
    api_key=api_key,
    search_depth='advanced',
    max_results=10
)

if result3.get('success'):
    print('AI 摘要:')
    print(result3.get('answer', 'N/A'))
    print('\n详细搜索结果:')
    for i, item in enumerate(result3.get('results', [])[:6], 1):
        print(f'\n{i}. {item.get("title", "N/A")}')
        print(f'   URL: {item.get("url", "N/A")}')
        print(f'   内容：{item.get("content", "N/A")[:350]}...')

# 查询 4: 网页游戏 vs 手游对比
query4 = 'web games vs mobile games market size traffic 2025 comparison'

print('\n' + '=' * 70)
print('查询 4: 网页游戏 vs 手游对比\n')

result4 = search(
    query=query4,
    api_key=api_key,
    search_depth='advanced',
    max_results=10
)

if result4.get('success'):
    print('AI 摘要:')
    print(result4.get('answer', 'N/A'))
    print('\n详细搜索结果:')
    for i, item in enumerate(result4.get('results', [])[:6], 1):
        print(f'\n{i}. {item.get("title", "N/A")}')
        print(f'   URL: {item.get("url", "N/A")}')
        print(f'   内容：{item.get("content", "N/A")[:350]}...')

print('\n' + '=' * 70)
print('调研完成')
print('=' * 70)
