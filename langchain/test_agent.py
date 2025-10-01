#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡單測試腳本 - 測試 AI Agent 的各項功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import create_ai_agent

def test_tools():
    """測試各個工具的功能"""
    print("🧪 測試 AI Agent 工具功能")
    print("=" * 40)

    # 創建 Agent
    agent = create_ai_agent()

    # 測試案例
    test_cases = [
        "計算 15 * 7 + 3",
        "台北的天氣怎麼樣？",
        "把 'hello' 翻譯成中文",
        "今天是星期幾？",
        "必應整體是賺錢的嗎？"
    ]

    for i, question in enumerate(test_cases, 1):
        print(f"\n📋 測試案例 {i}: {question}")
        print("-" * 50)

        try:
            response = agent.invoke({"input": question})
            print(f"🤖 回答: {response['output']}")
        except Exception as e:
            print(f"❌ 錯誤: {str(e)}")

        print("-" * 50)

    print("\n✅ 測試完成！")

if __name__ == "__main__":
    test_tools()
