# -*- coding: utf-8 -*-
"""
範例展示如何使用 Ollama 的嵌入模型與 LLM 模型來建立一個簡單的問答系統。
"""
# Google Drive 下載
import gdown
# 資料清整與分段
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 向量資料庫與嵌入模型
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings.ollama import OllamaEmbeddings
# Prompt 模板
from langchain_core.prompts import ChatPromptTemplate

# 下載 PDF 文件
#gdown.download("https://drive.google.com/file/d/1IuPEquZCw19VQxoLOvF6bc1WrfHn84ks/view?usp=sharing", "knowledgebase.pdf", fuzzy=True)
# 載入 PDF 文件
loader = PyPDFLoader("202502_6625_AI1_20250924_142829.pdf")

# 將文件切割成較小的段落
splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=120)
doc_split = loader.load_and_split(text_splitter=splitter)

# 使用 Ollama 的嵌入模型來建立向量資料庫
embeddings = OllamaEmbeddings(
  model="nomic-embed-text"
)
vectorstore = Chroma.from_documents(
  documents=doc_split,
  embedding=embeddings
)
retriever = vectorstore.as_retriever()

# 使用 Ollama 的 LLM 模型來建立問答系統
llm = ChatOllama(
  model="gemma3:1b",
  temperature=0.1
)
# 建立 Prompt 模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位專業的財經分析師，請根據用戶提供的文件內容來回答問題。"),
    ("user", "文件內容: {context}"),
    ("user", "根據上述文件內容，回答以下問題: {question}")
])
question = "必應整體是賺錢的嗎？"
result = llm.invoke(prompt.format_messages(
  context=retriever.get_relevant_documents(question)[0].page_content,
  question=question
))
print(result.content)