#!/usr/bin/env python3
"""
Solitaire 市场调研 - 使用 Tavily AI Search
"""

import os
import sys

# 设置环境变量 (从 MEMORY.md 已知 Tavily key 已配置)
sys.path.insert(0, 'active_skills/tavily/scripts')

from tavily_search import search

# 获取 API key
api_key = os.environ.get('TAVILY_API_KEY', '')

if not api_key:
    print("错误：TAVILY_API_KEY 环境变量未设置")
    print("请设置：export TAVILY_API_KEY='tvly-your-key-here'")
    sys.exit(1)

print(f"Tavily API Key: {api_key[:10]}...{api_key[-4:]}")

# 查询 1: Solitaire Grand Harvest 数据
query1 = "Solitaire Grand Harvest Supercell revenue DAU 2025 2026 players download"

print("=" * 60)
print("Solitaire 市场调研 - 竞品数据分析")
print("=" * 60)

print(f"\n查询 1: {query1}\n")
result1 = search(
    query=query1,
    api_key=api_key,
    search_depth="advanced",
    max_results=10
)

if result1.get("success"):
    print("AI 摘要:")
    print(result1.get("answer", "N/A"))
    print("\n搜索结果:")
    for i, item in enumerate(result1.get("results", [])[:5], 1):
        print(f"\n{i}. {item.get('title', 'N/A')}")
        print(f"   URL: {item.get('url', 'N/A')}")
        print(f"   内容：{item.get('content', 'N/A')[:200]}...")
else:
    print(f"搜索失败：{result1.get('error', 'Unknown error')}")

# 查询 2: Solitaire 市场整体数据
query2 = "mobile solitaire game market size revenue 2025 2026 tri peaks klondike"

print("\n" + "=" * 60)
print(f"查询 2: {query2}\n")

result2 = search(
    query=query2,
    api_key=api_key,
    search_depth="advanced",
    max_results=10
)

if result2.get("success"):
    print("AI 摘要:")
    print(result2.get("answer", "N/A"))
    print("\n搜索结果:")
    for i, item in enumerate(result2.get("results", [])[:5], 1):
        print(f"\n{i}. {item.get('title', 'N/A')}")
        print(f"   URL: {item.get('url', 'N/A')}")
        print(f"   内容：{item.get('content', 'N/A')[:200]}...")
else:
    print(f"搜索失败：{result2.get('error', 'Unknown error')}")

# 查询 3: Top Solitaire 竞品排名
query3 = "top solitaire mobile games 2025 ranking revenue Sensor Tower data.ai"

print("\n" + "=" * 60)
print(f"查询 3: {query3}\n")

result3 = search(
    query=query3,
    api_key=api_key,
    search_depth="advanced",
    max_results=10
)

if result3.get("success"):
    print("AI 摘要:")
    print(result3.get("answer", "N/A"))
    print("\n搜索结果:")
    for i, item in enumerate(result3.get("results", [])[:5], 1):
        print(f"\n{i}. {item.get('title', 'N/A')}")
        print(f"   URL: {item.get('url', 'N/A')}")
        print(f"   内容：{item.get('content', 'N/A')[:200]}...")
else:
    print(f"搜索失败：{result3.get('error', 'Unknown error')}")

# 查询 4: Solitaire 用户画像和付费行为
query4 = "solitaire game player demographics age gender spending habits mobile 2025"

print("\n" + "=" * 60)
print(f"查询 4: {query4}\n")

result4 = search(
    query=query4,
    api_key=api_key,
    search_depth="advanced",
    max_results=10
)

if result4.get("success"):
    print("AI 摘要:")
    print(result4.get("answer", "N/A"))
    print("\n搜索结果:")
    for i, item in enumerate(result4.get("results", [])[:5], 1):
        print(f"\n{i}. {item.get('title', 'N/A')}")
        print(f"   URL: {item.get('url', 'N/A')}")
        print(f"   内容：{item.get('content', 'N/A')[:200]}...")
else:
    print(f"搜索失败：{result4.get('error', 'Unknown error')}")

# 查询 5: Solitaire 买量成本 CPI LTV
query5 = "solitaire game CPI cost per install LTV customer acquisition 2025 mobile"

print("\n" + "=" * 60)
print(f"查询 5: {query5}\n")

result5 = search(
    query=query5,
    api_key=api_key,
    search_depth="advanced",
    max_results=10
)

if result5.get("success"):
    print("AI 摘要:")
    print(result5.get("answer", "N/A"))
    print("\n搜索结果:")
    for i, item in enumerate(result5.get("results", [])[:5], 1):
        print(f"\n{i}. {item.get('title', 'N/A')}")
        print(f"   URL: {item.get('url', 'N/A')}")
        print(f"   内容：{item.get('content', 'N/A')[:200]}...")
else:
    print(f"搜索失败：{result5.get('error', 'Unknown error')}")

print("\n" + "=" * 60)
print("调研完成")
print("=" * 60)
