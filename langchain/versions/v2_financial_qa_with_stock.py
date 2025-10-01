# -*- coding: utf-8 -*-
"""
版本 2：財務 QA 系統 + 股票價格查詢

這個版本展示了如何添加第一個財務相關工具：股票價格查詢。
現在系統不僅能回答知識庫問題，還能查詢即時股票價格。
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate

def get_stock_price(symbol: str) -> str:
    """查詢股票價格（模擬）"""
    # 模擬的股票數據庫
    stock_data = {
        "AAPL": {"price": 150.25, "change": "+2.5%", "volume": "50M"},
        "GOOGL": {"price": 2750.80, "change": "-1.2%", "volume": "1.2M"},
        "MSFT": {"price": 305.50, "change": "+1.8%", "volume": "25M"},
        "TSLA": {"price": 245.75, "change": "-3.1%", "volume": "80M"},
        "台積電": {"price": 520.0, "change": "+1.5%", "volume": "30M"},
        "鴻海": {"price": 95.5, "change": "+0.8%", "volume": "45M"},
        "聯發科": {"price": 850.0, "change": "-0.5%", "volume": "12M"}
    }

    symbol_upper = symbol.upper()

    if symbol_upper in stock_data:
        data = stock_data[symbol_upper]
        return f"{symbol} 股價：${data['price']} ({data['change']}) 成交量：{data['volume']}"
    else:
        return (
            f"抱歉，我沒有 {symbol} 的股價資訊。"
            "支援的股票：AAPL, GOOGL, MSFT, TSLA, 台積電, 鴻海, 聯發科"
        )

def detect_stock_query(question: str) -> tuple[bool, str | None]:
    """偵測是否為股票查詢，並提取股票代號"""
    question_lower = question.lower()

    # 股票查詢關鍵字
    stock_keywords = ['股價', '股票價格', '股票', '市值', '成交量']

    # 股票代號模式
    stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', '台積電', '鴻海', '聯發科']

    needs_stock = any(keyword in question_lower for keyword in stock_keywords)

    # 嘗試提取股票代號
    found_symbol = None
    for symbol in stock_symbols:
        if symbol in question or symbol.lower() in question_lower:
            found_symbol = symbol
            break

    return needs_stock, found_symbol

def main():
    print("🤖 版本 2：財務 QA 系統 + 股票價格查詢")
    print("=" * 60)
    print("📈 新功能：現在可以查詢股票價格了！")
    print("💡 這個版本結合了知識庫查詢和即時股價查詢")

    # 初始化財務知識庫（與版本 1 相同，帶錯誤處理）
    try:
        loader = PyPDFLoader("202502_6625_AI1_20250924_142829.pdf")
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        doc_split = loader.load_and_split(text_splitter=splitter)

        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = Chroma.from_documents(documents=doc_split, embedding=embeddings)
        retriever = vectorstore.as_retriever()
        print("✅ 知識庫載入成功")
    except Exception as e:
        print(f"⚠️ 知識庫載入失敗，使用預設知識：{str(e)}")
        # 創建一個空的檢索器，如果沒有 PDF 檔案
        from langchain_core.retrievers import BaseRetriever
        from langchain_core.documents import Document

        class EmptyRetriever(BaseRetriever):
            def get_relevant_documents(self, query):
                return [Document(page_content="這是一個財務知識庫的預設回應。由於沒有載入 PDF 文件，這裡提供基本的財務知識。")]

        retriever = EmptyRetriever()

    llm = ChatOllama(model="gemma3:1b", temperature=0.1)

    # 財務知識庫查詢模板
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一個專業的財經分析助手。請根據財務文件內容回答問題。只回答知識庫中有的資訊。"),
        ("user", "財務文件內容：{context}\n\n問題：{question}")
    ])

    print("\n✅ 系統準備完成！現在可以開始問問題了。")
    print("=" * 60)
    print("範例問題：")
    print("• 「必應整體是賺錢的嗎？」（知識庫查詢）")
    print("• 「蘋果股價多少？」或 「AAPL 股價」（股票查詢）")
    print("• 「台積電股價怎麼樣？」（股票查詢）")
    print("• 「比較蘋果和谷歌的股價」（混合查詢）")

    while True:
        try:
            question = input("\n❓ 請輸入問題（輸入 'exit' 結束）：")

            if question.lower() == 'exit':
                print("👋 再見！")
                break

            if question.strip():
                print(f"\n🔍 分析問題：{question}")

                # 偵測是否需要股票查詢
                needs_stock, stock_symbol = detect_stock_query(question)

                if needs_stock and stock_symbol:
                    print(f"📈 查詢股票價格：{stock_symbol}")
                    stock_result = get_stock_price(stock_symbol)
                    print(f"💹 {stock_result}")

                elif needs_stock and not stock_symbol:
                    print("❌ 無法識別股票代號，請明確指出股票名稱")

                else:
                    # 使用知識庫查詢
                    print("📚 搜尋財務知識庫...")
                    relevant_docs = retriever.get_relevant_documents(question)
                    context = relevant_docs[0].page_content if relevant_docs else "沒有找到相關財務資訊"

                    response = llm.invoke(qa_prompt.format_messages(
                        context=context[:2000],
                        question=question
                    ))

                    print(f"\n🤖 財務分析回答：{response.content}")

        except KeyboardInterrupt:
            print("\n\n👋 用戶中斷，再見！")
            break
        except Exception as e:
            print(f"❌ 發生錯誤：{str(e)}")

if __name__ == "__main__":
    main()
