#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangChain AI Agent 教學範例運行器

這個腳本讓你可以輕鬆運行不同版本的範例來學習進化過程。
"""

import subprocess
import sys
import os

def run_example(version_name, file_path):
    """運行指定版本的範例"""
    print(f"\n{'='*60}")
    print(f"🚀 運行 {version_name}")
    print(f"{'='*60}")

    try:
        # 使用 subprocess 運行 Python 腳本
        result = subprocess.run([
            sys.executable, file_path
        ], cwd=os.path.dirname(file_path))

        return result.returncode == 0

    except KeyboardInterrupt:
        print(f"\n⏹️  {version_name} 被用戶中斷")
        return True
    except Exception as e:
        print(f"❌ 運行 {version_name} 時發生錯誤：{str(e)}")
        return False

def main():
    print("🤖 LangChain AI Agent 教學範例運行器")
    print("=" * 60)
    print("這個工具讓你可以逐步體驗從簡單 QA 到 AI Agent 的進化過程")

    # 定義所有版本
    examples = [
        ("版本 1：基本財務知識庫 QA", "versions/v1_basic_financial_qa.py"),
        ("版本 2：財務 QA + 股票價格查詢", "versions/v2_financial_qa_with_stock.py"),
        ("版本 3：財務 QA + 財經新聞查詢", "versions/v3_financial_qa_with_news.py"),
        ("最終版本：專業財務顧問 AI Agent", "versions/v4_financial_ai_agent.py")
    ]

    print("\n📋 可用範例：")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")

    print("\n💡 建議學習順序：")
    print("1 → 2 → 3 → 4 （每個版本都建立在前一個版本的基礎上）")

    while True:
        try:
            choice = input("
請選擇要運行的版本 (1-4)，或輸入 'all' 運行全部，或 'exit' 結束："            choice = choice.strip().lower()

            if choice == 'exit':
                print("👋 感謝使用，再見！")
                break

            if choice == 'all':
                print("\n🚀 運行所有版本...")
                all_successful = True

                for name, file_path in examples:
                    success = run_example(name, file_path)
                    if not success:
                        all_successful = False

                    # 每個版本後詢問是否繼續
                    if len(examples) > 1:
                        continue_input = input("繼續下一個版本？(y/n): ")
                        if continue_input.lower() != 'y':
                            break

                if all_successful:
                    print("\n✅ 所有版本都運行成功！")
                else:
                    print("\n⚠️  某些版本運行時出現問題，請檢查錯誤訊息")

            elif choice in ['1', '2', '3', '4']:
                index = int(choice) - 1
                name, file_path = examples[index]
                run_example(name, file_path)

            else:
                print("❌ 請輸入 1-4、'all' 或 'exit'")

        except KeyboardInterrupt:
            print("\n\n👋 用戶中斷，感謝使用！")
            break
        except Exception as e:
            print(f"❌ 發生錯誤：{str(e)}")

if __name__ == "__main__":
    main()
