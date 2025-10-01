# -*- coding: utf-8 -*-
"""
版本 1：基本的財務知識庫 QA 系統

這是最簡單的問答系統，只使用知識庫來回答財務相關問題。
沒有工具，也沒有 Agent 邏輯。
"""

# 導入必要的模組
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate

def main():
    print("🤖 版本 1：基本的財務知識庫 QA 系統")
    print("=" * 60)
    print("📊 這個系統只能回答知識庫中的財務問題")

    # 載入 PDF 文件
    print("📚 載入財務知識庫...")
    loader = PyPDFLoader("202502_6625_AI1_20250924_142829.pdf")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    doc_split = loader.load_and_split(text_splitter=splitter)

    # 建立向量資料庫
    print("🔍 建立財務知識向量資料庫...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(documents=doc_split, embedding=embeddings)
    retriever = vectorstore.as_retriever()

    # 初始化 LLM
    print("🧠 初始化財務分析模型...")
    llm = ChatOllama(model="gemma3:1b", temperature=0.1)

    # 建立財務分析對話模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一個專業的財經分析助手。請根據提供的財務文件內容回答問題。只回答知識庫中有的資訊。"),
        ("user", "財務文件內容：{context}\n\n問題：{question}")
    ])

    print("\n✅ 系統準備完成！現在可以開始問財務問題了。")
    print("=" * 60)
    print("💡 這個版本只能回答知識庫中的問題，無法查詢即時資訊。")
    print()
    print("範例問題：")
    print("• 「必應整體是賺錢的嗎？」")
    print("• 「這家公司主要的業務是什麼？」")
    print("• 「公司的財務狀況如何？」")

    while True:
        try:
            question = input("\n❓ 請輸入財務問題（輸入 'exit' 結束）：")

            if question.lower() == 'exit':
                print("👋 再見！")
                break

            if question.strip():
                print(f"\n🔍 搜尋財務知識庫...")
                # 取得相關文件
                relevant_docs = retriever.get_relevant_documents(question)
                context = relevant_docs[0].page_content if relevant_docs else "沒有找到相關財務資訊"

                # 產生財務分析回答
                response = llm.invoke(prompt.format_messages(
                    context=context[:2000],  # 限制上下文長度
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
