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
        result = llm.invoke(f"Calculate the following expression: {expression}. Return only the final number.")
        content = result.content if hasattr(result, 'content') else str(result)
        # 嘗試提取數字
        import re
        numbers = re.findall(r'\d+', content)
        if numbers:
            return numbers[-1]  # 返回最後一個數字
        return content.strip()
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

tools = [calculate, get_current_time, get_weather]

template = """You are a helpful assistant with access to tools. Use the tools to answer questions.

{tools}

Available tools: {tool_names}

Format:
Question: [question]
Thought: [reasoning]
Action: [tool name]
Action Input: [tool input]
Observation: [tool result]
...repeat as needed...
Thought: [final reasoning]
Final Answer: [answer]

Question: {input}
Thought: {agent_scratchpad}
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
    # 測試簡單問題
    print("=== 測試簡單問題 ===")
    question1 = "請計算 15 * 3"
    print(f"問題: {question1}")
    response1 = agent_executor.invoke({"input": question1})
    print(f"答案: {response1['output']}")
    print()

    # 測試另一個簡單問題
    print("=== 測試時間問題 ===")
    question2 = "現在幾點鐘？"
    print(f"問題: {question2}")
    response2 = agent_executor.invoke({"input": question2})
    print(f"答案: {response2['output']}")
    print()

    # 測試複雜問題
    print("=== 測試複雜問題 ===")
    question3 = "請計算 15 * 3 並告訴我現在的時間，然後告訴我紐約的天氣如何？"
    print(f"問題: {question3}")
    response3 = agent_executor.invoke({"input": question3})
    print(f"答案: {response3['output']}")
    print()
