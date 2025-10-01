# -*- coding: utf-8 -*-
"""
版本 3：財務 QA 系統 + 財經新聞查詢

這個版本展示了如何添加財經新聞查詢工具。
現在系統可以查詢最新的財經新聞資訊。
"""

import random
from datetime import datetime, timedelta
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate

def get_financial_news(topic: str | None = None) -> str:
    """查詢財經新聞（模擬）"""
    # 模擬的財經新聞數據庫
    news_data = {
        "科技股": [
            "蘋果公司宣佈推出新款 iPhone，市場預期銷售將創新高",
            "谷歌母公司 Alphabet 股價上漲 3%，受惠於雲端服務業務成長",
            "微軟 Azure 雲端服務訂閱用戶突破 1 億大關",
            "特斯拉上海超級工廠產能提升，預計年產能達 100 萬輛"
        ],
        "台股": [
            "台積電股價突破 600 元大關，外資連續買超",
            "鴻海集團宣佈投資電動車電池技術，市場看好前景",
            "聯發科 5G 晶片出貨量持續成長，股價創今年新高",
            "國泰金控獲利優於預期，股息發放率達 70%"
        ],
        "經濟指標": [
            "美國聯準會維持利率不變，市場預期下半年可能降息",
            "台灣 GDP 成長率優於預期，達 3.2%",
            "中國經濟數據疲軟，影響亞洲股市表現",
            "歐洲央行暗示可能進一步升息以對抗通膨"
        ]
    }

    if topic and topic in news_data:
        news_list = news_data[topic]
        # 隨機選擇 2-3 條新聞
        selected_news = random.sample(news_list, min(2, len(news_list)))
        return f"📈 {topic}相關新聞：\n" + "\n".join(f"• {news}" for news in selected_news)
    else:
        # 返回所有類別的最新新聞
        all_news = []
        for category, news_list in news_data.items():
            latest_news = random.choice(news_list)
            all_news.append(f"📊 {category}：{latest_news}")

        return "📰 最新財經新聞：\n" + "\n".join(all_news)

def detect_news_query(question: str) -> tuple[bool, str | None]:
    """偵測是否為新聞查詢，並提取主題"""
    question_lower = question.lower()

    # 新聞查詢關鍵字
    news_keywords = ['新聞', '最新消息', '市場動態', '財經新聞', '經濟新聞']

    needs_news = any(keyword in question_lower for keyword in news_keywords)

    # 嘗試提取新聞主題
    topics = ["科技股", "台股", "經濟指標"]
    found_topic = None

    for topic in topics:
        if topic in question:
            found_topic = topic
            break

    return needs_news, found_topic

def main():
    print("🤖 版本 3：財務 QA 系統 + 財經新聞查詢")
    print("=" * 60)
    print("📰 新功能：現在可以查詢財經新聞了！")
    print("💡 這個版本整合了知識庫、股票價格和新聞查詢")

    # 初始化財務知識庫（帶錯誤處理）
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
    print("• 「蘋果股價多少？」（股票查詢）")
    print("• 「最近的財經新聞？」（新聞查詢）")
    print("• 「台股最新消息？」（新聞查詢）")
    print("• 「分析蘋果公司的投資價值」（綜合分析）")

    while True:
        try:
            question = input("\n❓ 請輸入問題（輸入 'exit' 結束）：")

            if question.lower() == 'exit':
                print("👋 再見！")
                break

            if question.strip():
                print(f"\n🔍 分析問題：{question}")

                # 偵測是否需要新聞查詢
                needs_news, news_topic = detect_news_query(question)

                if needs_news:
                    print(f"📰 查詢財經新聞...")
                    if news_topic:
                        print(f"🎯 主題：{news_topic}")
                    news_result = get_financial_news(news_topic)
                    print(f"\n{news_result}")

                else:
                    # 檢查是否為股票查詢（重複檢查邏輯）
                    needs_stock, stock_symbol = detect_stock_query(question)

                    if needs_stock and stock_symbol:
                        print(f"📈 查詢股票價格：{stock_symbol}")
                        stock_result = get_stock_price(stock_symbol)
                        print(f"💹 {stock_result}")
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

def detect_stock_query(question: str) -> tuple[bool, str]:
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
        return f"抱歉，我沒有 {symbol} 的股價資訊。支援的股票：AAPL, GOOGL, MSFT, TSLA, 台積電, 鴻海, 聯發科"

if __name__ == "__main__":
    main()
