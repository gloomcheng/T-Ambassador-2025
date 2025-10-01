#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最終測試 - 驗證財務顧問 AI Agent 是否能正常運行
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_agent_creation():
    """測試 Agent 創建"""
    try:
        from main import create_financial_agent
        print("🔧 創建財務顧問 Agent...")
        agent = create_financial_agent()
        print("✅ Agent 創建成功")
        return True
    except Exception as e:
        print(f"❌ Agent 創建失敗：{e}")
        return False

def test_web_search():
    """測試網路搜尋工具"""
    try:
        from main import web_search
        print("🔍 測試網路搜尋工具...")

        # 測試搜尋功能
        result = web_search("蘋果公司介紹")
        if len(result) > 100:  # 確保有搜尋結果
            print("✅ 網路搜尋工具正常運作")
            print(f"搜尋結果預覽：{result[:200]}...")
            return True
        else:
            print("⚠️ 網路搜尋結果可能有問題")
            return False
    except Exception as e:
        print(f"❌ 網路搜尋測試失敗：{e}")
        return False

def test_financial_analysis():
    """測試財務分析工具"""
    try:
        from main import financial_analysis
        print("💼 測試財務分析工具...")

        result = financial_analysis("蘋果公司")
        if len(result) > 20:  # 確保有分析結果
            print("✅ 財務分析工具正常運作")
            print(f"分析結果：{result}")
            return True
        else:
            print("⚠️ 財務分析結果可能有問題")
            return False
    except Exception as e:
        print(f"❌ 財務分析測試失敗：{e}")
        return False

def main():
    print("🧪 最終測試：財務顧問 AI Agent")
    print("=" * 60)

    tests = [
        ("Agent 創建", test_agent_creation),
        ("網路搜尋", test_web_search),
        ("財務分析", test_financial_analysis)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 執行測試：{test_name}")
        success = test_func()
        results.append((test_name, success))

    print("\n" + "=" * 60)
    print("📊 測試結果總結：")
    for test_name, success in results:
        status = "✅ 通過" if success else "❌ 失敗"
        print(f"{test_name}: {status}")

    all_passed = all(success for _, success in results)
    if all_passed:
        print("\n🎉 所有測試通過！財務顧問 AI Agent 準備就緒")
        print("\n💡 現在你可以運行以下指令來體驗 Agent：")
        print("   uv run python main.py")
    else:
        print("\n⚠️  某些測試失敗，請檢查錯誤訊息並修正問題")

    return all_passed

if __name__ == "__main__":
    main()
