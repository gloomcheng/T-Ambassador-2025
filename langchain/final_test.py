#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最終測試 - 驗證財務顧問系統是否準備就緒
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_system_readiness():
    """測試系統是否準備就緒"""

    print("🧪 最終系統測試")
    print("=" * 50)

    try:
        # 測試模組載入
        from main import (
            web_search, financial_analysis, detect_intent,
            create_financial_advisor, answer_financial_question
        )
        print("✅ 模組載入成功")

        # 測試意圖偵測
        intent, target = detect_intent("蘋果股價多少？")
        assert intent == "stock"
        assert target == "蘋果"
        print("✅ 意圖偵測功能正常")

        # 測試財務分析
        analysis = financial_analysis("蘋果公司")
        assert len(analysis) > 20
        print("✅ 財務分析功能正常")

        # 測試網路搜尋
        search_result = web_search("蘋果股價")
        assert len(search_result) > 50
        print("✅ 網路搜尋功能正常")

        # 測試系統初始化
        llm, retriever = create_financial_advisor()
        assert llm is not None
        assert retriever is not None
        print("✅ 財務顧問系統初始化成功")

        print("\n🎉 所有測試通過！")
        print("💡 財務顧問系統已經準備就緒")
        print("\n運行方式：")
        print("• 完整體驗：uv run python main.py")
        print("• 快速示範：uv run python demo.py")

        return True

    except Exception as e:
        print(f"❌ 測試失敗：{e}")
        return False

def main():
    success = test_system_readiness()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
