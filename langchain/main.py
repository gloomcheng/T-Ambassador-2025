# -*- coding: utf-8 -*-
"""
智慧財務顧問系統

這個系統展示了如何創建一個智慧的財務顧問，能夠：
1. 理解用戶意圖並決定是否需要搜尋資訊
2. 整合知識庫和網路搜尋結果
3. 提供專業的財務分析建議

這是一個專業的財務顧問系統！
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_community.embeddings.ollama import OllamaEmbeddings

# ===== 財務工具函數 =====


def web_search(query: str) -> str:
    """使用網路搜尋獲取最新資訊"""
    try:
        from ddgs import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=2))

        if results:
            search_results = []
            for i, result in enumerate(results, 1):
                title = result.get('title', '無標題')
                body = result.get('body', '無內容')[:200]  # 限制長度
                search_results.append(f"{i}. {title}: {body}")

            result_text = "\n".join(search_results)
            return f"🔍 網路搜尋結果：\n{result_text}"
        else:
            return f"抱歉，沒有找到關於「{query}」的搜尋結果。"

    except Exception as e:
        return f"網路搜尋失敗：{str(e)}。請稍後再試。"


def financial_analysis(company: str) -> str:
    """提供財務分析建議"""
    analysis_data = {
        "蘋果公司": "蘋果公司財務狀況穩健，現金流充沛，股息收益率約 0.6%。建議長期持有。",
        "台積電": "台積電技術領先，客戶基礎強大，預估未來成長性佳。當前本益比約 18 倍，屬合理水準。",
        "特斯拉": "特斯拉成長迅速但波動大，電動車市場前景看好。需注意競爭加劇風險。",
        "微軟": "微軟雲端業務穩健成長，AI 投資可望帶來長期收益。財務狀況極佳。",
        "谷歌": "谷歌廣告業務穩定，雲端運算持續擴張，財務狀況良好。",
        "亞馬遜": "亞馬遜電商霸主地位穩固，雲端服務成長強勁，長期投資價值高。"
    }

    supported_companies = "蘋果公司、台積電、特斯拉、微軟、谷歌、亞馬遜"
    return analysis_data.get(company, f"抱歉，我沒有 {company} 的財務分析資料。"
                                     f"支援的公司：{supported_companies}")


def detect_intent(question: str) -> tuple[str, str]:
    """偵測用戶意圖並決定需要的資訊類型"""
    question_lower = question.lower()

    # 股價查詢
    stock_keywords = ['股價', '股票價格', '市值', '成交量']
    stock_companies = ['蘋果', '台積電', '特斯拉', '微軟', '谷歌', '亞馬遜']

    for company in stock_companies:
        if company in question:
            return "stock", company

    if any(keyword in question_lower for keyword in stock_keywords):
        return "stock", "general"

    # 新聞查詢
    news_keywords = ['新聞', '最新消息', '市場動態', '財經新聞']
    if any(keyword in question_lower for keyword in news_keywords):
        return "news", question

    # 財務分析
    analysis_keywords = ['分析', '投資價值', '建議', '評估']
    for company in stock_companies:
        if (company in question and
            any(keyword in question_lower for keyword in analysis_keywords)):
            return "analysis", company

    # 預設為知識庫查詢
    return "knowledge", question


# ===== 財務顧問系統 =====

def create_financial_advisor():
    """創建財務顧問系統"""

    # 初始化財務知識庫
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
                content = ("這是一個財務知識庫的預設回應。"
                          "由於沒有載入 PDF 文件，這裡提供基本的財務知識。")
                return [Document(page_content=content)]

        retriever = EmptyRetriever()

    # 初始化 LLM
    llm = ChatOllama(model="gemma3:1b", temperature=0.1)

    return llm, retriever

def answer_financial_question(question: str, llm, retriever):
    """智慧回答財務問題"""

    # 偵測用戶意圖
    intent, target = detect_intent(question)

    print(f"🤔 偵測意圖：{intent} - {target}")

    if intent == "stock":
        # 股價查詢
        if target == "general":
            search_query = question  # 用戶問題作為搜尋查詢
        else:
            search_query = f"{target} 股價"

        print(f"📈 搜尋股價資訊：{search_query}")
        search_result = web_search(search_query)

        # 整合搜尋結果和知識庫資訊
        relevant_docs = retriever.get_relevant_documents(question)
        context = relevant_docs[0].page_content if relevant_docs else ""

        # 創建整合提示
        context_text = context[:1000] if context else ""
        combined_prompt = (
            "根據以下資訊回答用戶問題："
            f"知識庫內容：{context_text}"
            f"網路搜尋結果：{search_result}"
            f"用戶問題：{question}"
            "請提供專業、準確的財務回答。"
        )

        response = llm.invoke(combined_prompt)
        return response.content

    elif intent == "news":
        # 新聞查詢
        print(f"📰 搜尋新聞資訊：{target}")
        search_result = web_search(target)

        # 整合新聞和知識庫資訊
        relevant_docs = retriever.get_relevant_documents(question)
        context = relevant_docs[0].page_content if relevant_docs else ""

        context_text = context[:1000] if context else ""
        combined_prompt = (
            "根據以下資訊回答用戶問題："
            f"知識庫內容：{context_text}"
            f"最新新聞資訊：{search_result}"
            f"用戶問題：{question}"
            "請提供專業、客觀的新聞分析。"
        )

        response = llm.invoke(combined_prompt)
        return response.content

    elif intent == "analysis":
        # 財務分析
        print(f"💼 提供財務分析：{target}")
        analysis_result = financial_analysis(target)

        # 也可以整合搜尋結果來增強分析
        search_query = f"{target} 最新財務狀況"
        search_result = web_search(search_query)

        combined_prompt = (
            "根據以下資訊提供財務分析："
            f"財務分析資料：{analysis_result}"
            f"最新市場資訊：{search_result}"
            f"用戶問題：{question}"
            "請提供專業、全面的財務分析建議。"
        )

        response = llm.invoke(combined_prompt)
        return response.content

    else:
        # 知識庫查詢
        print("📚 查詢知識庫資訊")
        relevant_docs = retriever.get_relevant_documents(question)
        context = relevant_docs[0].page_content if relevant_docs else "沒有找到相關資訊"

        context_text = context[:2000] if context else ""
        prompt = (
            "你是一個專業的財務顧問。請根據以下知識庫內容回答問題："
            f"知識庫內容：{context_text}"
            f"用戶問題：{question}"
            "請提供專業、準確的回答。"
        )

        response = llm.invoke(prompt)
        return response.content


# ===== 主程式 =====

def main():
    print("🤖 智慧財務顧問系統")
    print("=" * 60)
    print("💼 這個系統能夠智慧決定何時搜尋資訊並提供專業建議")

    # 初始化系統
    llm, retriever = create_financial_advisor()

    print("\n✅ 財務顧問系統準備完成！")
    print("=" * 60)
    print("💡 系統特色：")
    print("• 自動偵測用戶意圖（股價、新聞、分析、知識查詢）")
    print("• 智慧整合知識庫和網路搜尋結果")
    print("• 提供專業的財務分析建議")
    print("• 支援即時股價和新聞查詢")

    print("\n🎯 試試這些問題：")
    print("• 「蘋果股價多少？」（自動搜尋最新股價）")
    print("• 「分析蘋果公司的投資價值」（整合分析）")
    print("• 「最近科技股有什麼新聞？」（搜尋最新新聞）")
    print("• 「我想投資電動車產業，你有什麼建議？」（綜合建議）")
    print("• 「台積電股價怎麼樣？」（台股查詢）")
    print("• 「必應整體是賺錢的嗎？」（知識庫查詢）")

    while True:
        try:
            question = input("\n❓ 請輸入財務問題（輸入 'exit' 結束）：")

            if question.lower() == 'exit':
                print("👋 感謝使用財務顧問，再見！")
                break

            if question.strip():
                print(f"\n🔍 分析問題：{question}")
                print("-" * 50)

                # 智慧回答問題
                answer = answer_financial_question(question, llm, retriever)

                print(f"\n💼 財務顧問回答：{answer}")

        except KeyboardInterrupt:
            print("\n\n👋 用戶中斷，感謝使用財務顧問！")
            break
        except Exception as e:
            print(f"❌ 發生錯誤：{str(e)}")


if __name__ == "__main__":
    main()
