#!/usr/bin/env python3
"""搜索 Top Solitaire 竞品列表和规模数据"""

import os
import sys
import io
sys.path.insert(0, 'active_skills/tavily/scripts')
from tavily_search import search

# 处理 Windows 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

api_key = os.environ.get('TAVILY_API_KEY', '')

print('=' * 70)
print('Solitaire 竞品规模调研')
print('=' * 70)

# 查询 1: Top 竞品列表
query1 = 'top 10 solitaire mobile games 2025 2026 revenue downloads DAU users market share'

print('\n查询 1: Top Solitaire 竞品列表和规模\n')
result1 = search(
    query=query1,
    api_key=api_key,
    search_depth='advanced',
    max_results=15
)

if result1.get('success'):
    print('AI 摘要:')
    print(result1.get('answer', 'N/A'))
    print('\n详细搜索结果:')
    for i, item in enumerate(result1.get('results', [])[:8], 1):
        print(f'\n{i}. {item.get("title", "N/A")}')
        print(f'   URL: {item.get("url", "N/A")}')
        print(f'   内容：{item.get("content", "N/A")[:300]}...')

# 查询 2: 头部竞品详细数据
query2 = 'Solitaire Grand Harvest revenue 2025 2026 Supercell Playtika income players'

print('\n' + '=' * 70)
print('查询 2: Solitaire Grand Harvest 详细数据\n')

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
    for i, item in enumerate(result2.get('results', [])[:5], 1):
        print(f'\n{i}. {item.get("title", "N/A")}')
        print(f'   URL: {item.get("url", "N/A")}')
        print(f'   内容：{item.get("content", "N/A")[:300]}...')

# 查询 3: 其他主要竞品
query3 = 'Solitaire Triples June Journey Gardenscapes revenue downloads 2025 2026'

print('\n' + '=' * 70)
print('查询 3: 其他主要竞品数据\n')

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
    for i, item in enumerate(result3.get('results', [])[:5], 1):
        print(f'\n{i}. {item.get("title", "N/A")}')
        print(f'   URL: {item.get("url", "N/A")}')
        print(f'   内容：{item.get("content", "N/A")[:300]}...')

# 查询 4: 厂商信息
query4 = 'Playtika Wooga Supercell Solitaire games portfolio revenue 2025'

print('\n' + '=' * 70)
print('查询 4: 主要厂商信息\n')

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
    for i, item in enumerate(result4.get('results', [])[:5], 1):
        print(f'\n{i}. {item.get("title", "N/A")}')
        print(f'   URL: {item.get("url", "N/A")}')
        print(f'   内容：{item.get("content", "N/A")[:300]}...')

print('\n' + '=' * 70)
print('调研完成')
print('=' * 70)
