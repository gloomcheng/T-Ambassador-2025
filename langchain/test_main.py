#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 main.py 是否能正常運行
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """測試必要的模組導入"""
    try:
        from langchain_community.document_loaders import PyPDFLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_community.vectorstores import Chroma
        from langchain_community.chat_models import ChatOllama
        from langchain_community.embeddings.ollama import OllamaEmbeddings
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        from langchain_core.tools import tool
        from langchain.agents import create_tool_calling_agent, AgentExecutor
        print("✅ 所有模組載入成功")
        return True
    except ImportError as e:
        print(f"❌ 模組載入失敗：{e}")
        return False

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

def test_tools():
    """測試工具函數"""
    try:
        from main import get_stock_price, get_financial_news, financial_analysis

        # 測試股票價格查詢
        result = get_stock_price("AAPL")
        print(f"📈 股票測試：{result}")

        # 測試新聞查詢
        result = get_financial_news("科技股")
        print(f"📰 新聞測試：{result[:100]}...")

        # 測試財務分析
        result = financial_analysis("蘋果公司")
        print(f"💼 分析測試：{result}")

        print("✅ 所有工具測試成功")
        return True
    except Exception as e:
        print(f"❌ 工具測試失敗：{e}")
        return False

def main():
    print("🧪 測試 LangChain AI Agent")
    print("=" * 50)

    tests = [
        ("模組載入", test_imports),
        ("Agent 創建", test_agent_creation),
        ("工具測試", test_tools)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 執行測試：{test_name}")
        success = test_func()
        results.append((test_name, success))

    print("\n" + "=" * 50)
    print("📊 測試結果總結：")
    for test_name, success in results:
        status = "✅ 通過" if success else "❌ 失敗"
        print(f"{test_name}: {status}")

    all_passed = all(success for _, success in results)
    if all_passed:
        print("\n🎉 所有測試通過！程式準備好進行 demo")
    else:
        print("\n⚠️  某些測試失敗，請檢查錯誤訊息")

    return all_passed

if __name__ == "__main__":
    main()
