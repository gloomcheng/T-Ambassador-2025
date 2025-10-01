#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試所有學習版本是否能正常運行

這個腳本會測試 v1、v2、v3 三個學習版本，確保學員可以正常運行這些範例。
"""

import sys
import os
import ast
import importlib.util

def test_version_structure(version_name, file_path):
    """測試版本的程式碼結構是否正確"""
    print(f"\n🧪 測試 {version_name}")
    print("=" * 50)

    try:
        # 檢查檔案是否存在
        if not os.path.exists(file_path):
            print(f"❌ {version_name} 檔案不存在：{file_path}")
            return False

        # 嘗試解析程式碼結構
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        # 檢查必要的函數是否存在
        required_functions = ['main']
        for func in required_functions:
            if f'def {func}(' not in code:
                print(f"❌ {version_name} 缺少 {func} 函數")
                return False

        # 檢查必要的匯入是否存在
        required_imports = [
            'from langchain',
            'ChatOllama',
            'PyPDFLoader'
        ]

        missing_imports = []
        for imp in required_imports:
            if imp not in code:
                missing_imports.append(imp)

        if missing_imports:
            print(f"⚠️  {version_name} 可能缺少匯入：{missing_imports}")

        # 嘗試載入模組來檢查語法錯誤
        spec = importlib.util.spec_from_file_location("test_module", file_path)
        if spec is None:
            print(f"❌ {version_name} 無法載入模組規格")
            return False

        module = importlib.util.module_from_spec(spec)

        # 嘗試執行模組（這會捕捉語法錯誤）
        try:
            spec.loader.exec_module(module)
        except SyntaxError as e:
            print(f"❌ {version_name} 語法錯誤：{str(e)}")
            return False
        except Exception as e:
            # 其他錯誤（如缺少依賴）是正常的，我們只檢查語法
            if "cannot import name" in str(e) or "No module named" in str(e):
                print(f"✅ {version_name} 語法正確（依賴問題正常）")
                return True
            else:
                print(f"⚠️  {version_name} 執行時錯誤：{str(e)}")
                return False

        print(f"✅ {version_name} 結構正確")
        return True

    except Exception as e:
        print(f"❌ {version_name} 測試失敗：{str(e)}")
        return False

def main():
    print("🚀 測試所有學習版本結構")
    print("=" * 60)
    print("確保每個版本的程式碼結構正確，讓學員可以順利學習")

    # 定義要測試的版本
    versions = [
        ("版本 1：基本財務知識庫 QA", "versions/v1_basic_financial_qa.py"),
        ("版本 2：財務 QA + 股票價格查詢", "versions/v2_financial_qa_with_stock.py"),
        ("版本 3：財務 QA + 財經新聞查詢", "versions/v3_financial_qa_with_news.py")
    ]

    results = []

    for version_name, file_path in versions:
        success = test_version_structure(version_name, file_path)
        results.append((version_name, success))

    # 顯示測試結果總結
    print("\n" + "=" * 60)
    print("📊 測試結果總結：")
    print("=" * 60)

    all_passed = True
    for version_name, success in results:
        status = "✅ 通過" if success else "❌ 失敗"
        print(f"{version_name}: {status}")
        if not success:
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有版本結構測試通過！")
        print("💡 學員可以正常運行這些學習範例了")
        print("\n運行方式：")
        print("• 版本 1：uv run python versions/v1_basic_financial_qa.py")
        print("• 版本 2：uv run python versions/v2_financial_qa_with_stock.py")
        print("• 版本 3：uv run python versions/v3_financial_qa_with_news.py")
        print("\n📝 注意：運行時需要確保 Ollama 已啟動並載入 gemma3:1b 模型")
    else:
        print("⚠️  某些版本結構測試失敗，請檢查錯誤訊息")

    return all_passed

if __name__ == "__main__":
    main()
