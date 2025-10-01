#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
財務顧問系統示範

這個腳本展示了智慧財務顧問系統如何：
1. 自動偵測用戶意圖並決定搜尋資訊
2. 整合知識庫和網路搜尋結果
3. 提供專業的財務建議
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import create_financial_advisor, answer_financial_question

def demo_questions():
    """示範幾個問題來展示系統的功能"""

    print("🎯 智慧財務顧問系統功能示範")
    print("=" * 60)

    # 創建財務顧問系統
    llm, retriever = create_financial_advisor()

    demo_questions_list = [
        "蘋果股價多少？",
        "分析蘋果公司的投資價值",
        "最近科技股有什麼新聞？",
        "我想投資電動車產業，你有什麼建議？",
        "台積電股價怎麼樣？"
    ]

    for i, question in enumerate(demo_questions_list, 1):
        print(f"\n🔥 問題 {i}: {question}")
        print("-" * 50)

        try:
            answer = answer_financial_question(question, llm, retriever)
            print(f"💼 財務顧問回答：{answer}")
        except Exception as e:
            print(f"❌ 錯誤：{str(e)}")

        print("-" * 50)

    print("\n🎉 示範完成！")
    print("\n💡 現在你可以試試自己的問題了：")
    print("   uv run python main.py")

def main():
    demo_questions()

if __name__ == "__main__":
    main()
