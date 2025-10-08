"""
LangChain agent example with Long-term Memory
長期記憶版本
"""

import datetime
import json
import os
from langchain_ollama import OllamaLLM
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.memory import BaseMemory
from langchain_core.messages import HumanMessage, AIMessage
from langchain.tools import tool

# 記憶檔案路徑
MEMORY_FILE = "agent_memory.json"

llm = OllamaLLM(
    model="gemma3:1b",
    temperature=0.3,
)

# 自定義持久化記憶類別
class PersistentMemory(BaseMemory):
    """自定義持久化記憶類別"""

    memory_key: str = "chat_history"
    return_messages: bool = True
    chat_memory: ChatMessageHistory = ChatMessageHistory()

    def __init__(self, **kwargs):
        # 初始化 chat_memory 並載入資料
        object.__setattr__(self, 'chat_memory', ChatMessageHistory())
        super().__init__(**kwargs)
        self._load_from_file()

    def _load_from_file(self):
        """從檔案載入記憶"""
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 重建訊息物件
                for msg_data in data.get("chat_history", []):
                    msg_type = msg_data.get("type")
                    content = msg_data.get("content")

                    if msg_type == "HumanMessage":
                        self.chat_memory.add_message(HumanMessage(content=content))
                    elif msg_type == "AIMessage":
                        self.chat_memory.add_message(AIMessage(content=content))

            except Exception as e:
                print(f"載入記憶失敗: {e}")

    def _save_to_file(self):
        """儲存記憶到檔案"""
        try:
            # 將訊息轉換為可序列化的格式
            chat_history = []
            for msg in self.chat_memory.messages:
                chat_history.append({
                    "type": msg.__class__.__name__,
                    "content": msg.content
                })

            data = {"chat_history": chat_history}

            with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"儲存記憶失敗: {e}")

    def clear(self):
        """清除記憶"""
        self.chat_memory.clear()
        self._save_to_file()

    @property
    def memory_variables(self):
        return [self.memory_key]

    def load_memory_variables(self, inputs):
        if self.return_messages:
            return {self.memory_key: self.chat_memory.messages}
        else:
            return {self.memory_key: "\n".join([msg.content for msg in self.chat_memory.messages])}

    def save_context(self, inputs, outputs):
        """儲存對話上下文"""
        if "input" in inputs:
            self.chat_memory.add_message(HumanMessage(content=inputs["input"]))

        if "output" in outputs:
            self.chat_memory.add_message(AIMessage(content=outputs["output"]))

        self._save_to_file()


# 載入記憶
def load_memory():
    """從檔案載入記憶"""
    return PersistentMemory(memory_key="chat_history", return_messages=True)


# 儲存記憶
def save_memory(memory):
    """儲存記憶到檔案"""
    if isinstance(memory, PersistentMemory):
        memory._save_to_file()


@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = llm.invoke(
            f"Calculate the following expression: {expression}")
        return result.content if hasattr(result, 'content') else str(result)
    except Exception as e:
        return str(e)


@tool
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def get_weather(location: str) -> str:
    """Get the current weather for a given location."""
    try:
        result = llm.invoke(f"What's the current weather in {location}?")
        return result.content if hasattr(result, 'content') else str(result)
    except Exception as e:
        return str(e)


@tool
def remember_fact(fact: str) -> str:
    """Store an important fact or information in memory. Input: the fact you want to remember."""
    # 這個工具會在 agent 執行後被處理，用於記憶事實
    return f"__MEMORY_ADD__:{fact}"


@tool
def recall_facts(query: str = "") -> str:
    """Retrieve all previously stored facts from memory. Input: any text to trigger recall."""
    try:
        # 載入記憶並提取所有事實
        current_memory = load_memory()
        messages = current_memory.chat_memory.messages
        facts = []
        for msg in messages:
            # 檢查 AI 訊息中是否包含"已記住"的內容
            if hasattr(msg, '__class__') and msg.__class__.__name__ == "AIMessage" and "已記住:" in msg.content:
                fact = msg.content.replace("已記住:", "").strip()
                facts.append(fact)
        if facts:
            return "Stored facts:\n" + "\n".join(f"- {fact}" for fact in facts)
        else:
            return "No facts stored in memory yet"
    except Exception as e:
        return f"Recall failed: {str(e)}"


tools = [calculate, get_current_time, get_weather, remember_fact, recall_facts]


template = """你是一位有用的助手，能夠使用以下工具來回答問題。你有長期記憶功能，可以記住重要的事實。

{tools}

工具名稱: {tool_names}

長期記憶中的對話歷史:
{chat_history}

請使用以下格式回答問題：

Question: 需要回答的問題
Thought: 我需要做什麼來回答這個問題？
Action: 工具名稱
Action Input: 工具輸入
Observation: 工具輸出
... (重複以上格式)
Thought: 我現在知道最終答案了
Final Answer: 最終答案

Question: {input}
Thought: {agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template)


# 全域記憶變數
memory = load_memory()

agent = create_react_agent(
  llm=llm,
  prompt=prompt,
  tools=tools,
)


agent_executor = AgentExecutor(
  agent=agent,
  tools=tools,
  memory=memory,  # 添加記憶
  verbose=True,
  handle_parsing_errors=True,
  max_iterations=5,
)


def chat_loop():
    """互動式對話循環"""
    print("🤖 AI Agent with Long-term Memory")
    print("你可以問我問題，我會記住重要的資訊！")
    print("輸入 'exit' 結束對話")
    print("-" * 50)

    # 載入全域記憶供 agent 使用
    global memory

    while True:
        try:
            user_input = input("\n你: ").strip()
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("再見！已儲存對話記憶。")
                save_memory(memory)
                break

            if user_input:
                response = agent_executor.invoke({
                    "input": user_input,
                    "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                # 處理記憶標記
                output = response['output']
                if "__MEMORY_ADD__:" in output:
                    # 提取要記住的事實
                    memory_parts = output.split("__MEMORY_ADD__:")
                    if len(memory_parts) > 1:
                        fact = memory_parts[1].strip()
                        # 儲存到記憶
                        memory.save_context({"input": f"記住: {fact}"}, {"output": f"已記住: {fact}"})
                        output = f"🤖 Agent: 已記住事實: {fact}"

                print(f"\n{output}")

                # 儲存正常的對話上下文
                if not "__MEMORY_ADD__:" in response['output']:
                    memory.save_context({"input": user_input}, {"output": response['output']})

        except KeyboardInterrupt:
            print("\n\n再見！已儲存對話記憶。")
            save_memory(memory)
            break
        except Exception as e:
            print(f"發生錯誤: {e}")


def test_memory():
    """測試記憶功能"""
    print("🧪 測試長期記憶功能")
    print("-" * 30)

    # 清除舊的記憶檔案
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)

    # 初始化記憶
    memory = load_memory()

    # 測試記住功能 (通過 agent)
    print("測試 1: 記住功能")
    try:
        response = agent_executor.invoke({
            "input": "記住我最喜歡的顏色是藍色",
            "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        output = response['output']
        print(f"Agent 輸出: {output}")

        # 處理記憶標記
        if "__MEMORY_ADD__:" in output:
            memory_parts = output.split("__MEMORY_ADD__:")
            if len(memory_parts) > 1:
                fact = memory_parts[1].strip()
                memory.save_context({"input": f"記住: {fact}"}, {"output": f"已記住: {fact}"})
                print(f"✅ 已處理記憶: {fact}")
        else:
            print("❌ 沒有找到記憶標記")

    except Exception as e:
        print(f"錯誤: {e}")

    # 測試回想功能
    print("\n測試 2: 回想功能")
    try:
        response = agent_executor.invoke({
            "input": "回想所有記住的事實",
            "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"結果: {response['output']}")
    except Exception as e:
        print(f"錯誤: {e}")

    # 測試計算功能
    print("\n測試 3: 計算功能")
    try:
        response = agent_executor.invoke({
            "input": "計算 15 + 27",
            "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"結果: {response['output']}")
    except Exception as e:
        print(f"錯誤: {e}")

    # 測試時間功能
    print("\n測試 4: 時間功能")
    try:
        response = agent_executor.invoke({
            "input": "現在幾點",
            "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"結果: {response['output']}")
    except Exception as e:
        print(f"錯誤: {e}")

    print("\n✅ 記憶功能測試完成！")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_memory()
    else:
        chat_loop()
