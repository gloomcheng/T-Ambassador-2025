"""
LangChain agent example
"""

import datetime
from langchain_ollama import OllamaLLM
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import tool


llm = OllamaLLM(
    model="gemma3:1b",
    temperature=0.3,
)

@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = llm.predict(f"Calculate the following expression: {expression}")
        return result
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
        result = llm.predict(f"What's the current weather in {location}?")
        return result
    except Exception as e:
        return str(e)

tools = [calculate, get_current_time, get_weather]

template = """你是一位有用的助手，能夠使用以下工具來回答問題：

{tools}

工具名稱: {tool_names}
當前日期和時間: {current_time}
使用以下格式來回答問題：
問題: 需要回答的問題
思考: 你需要做什麼來回答這個問題？
工具: 你將使用哪個工具？請只提供工具名稱。
工具輸入: 你將提供給工具的輸入。
工具輸出: 工具的結果將在這裡顯示。
思考: 你還需要做什麼來回答這個問題？（如果需要更多工具，請重複使用工具部分）
最終答案: 你最終的答案是什麼？

注意：每次只能使用一個工具，並且在提供最終答案之前，必須至少使用一個工具。

開始！
用戶問題: {input}
思考過程: {agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template)

agent = create_react_agent(
  llm=llm,
  prompt=prompt,
  tools=tools,
)
agent_executor = AgentExecutor(
  agent=agent,
  tools=tools,
  verbose=True,
  handle_parsing_errors=True,
  max_iterations=5,
)

if __name__ == "__main__":
    question = "請計算 15 * 3 並告訴我現在的時間，然後告訴我紐約的天氣如何？"
    response = agent_executor.run(question)
    print(response)
