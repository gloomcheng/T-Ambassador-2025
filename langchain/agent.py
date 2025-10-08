"""
Chrome DevTools MCP 訂票 Agent
使用 MCP (Model Context Protocol) 控制 Chrome 瀏覽器進行自動訂票
"""

from langchain_ollama import OllamaLLM
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import tool
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json

# 初始化 Ollama 模型
llm = OllamaLLM(
    model="gemma3:1b",
    temperature=0.3,  # 較低溫度以確保準確性
)

# MCP 客戶端管理類


class ChromeMCPClient:

    def __init__(self):
        self.session = None
        self.browser_connected = False

    async def connect(self):
        """連接到 Chrome DevTools MCP 伺服器"""
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "chrome-devtools-mcp"],
            env=None
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                self.session = session
                await session.initialize()
                self.browser_connected = True
                return session

    async def navigate(self, url: str):
        """導航到指定網址"""
        if not self.session:
            raise Exception("MCP session not initialized")

        result = await self.session.call_tool(
            "navigate_page",
            arguments={"url": url}
        )
        return result

    async def click_element(self, uid: str):
        """點擊頁面元素"""
        result = await self.session.call_tool(
            "click",
            arguments={"uid": uid}
        )
        return result

    async def input_text(self, uid: str, text: str):
        """在輸入框中輸入文字"""
        result = await self.session.call_tool(
            "fill",
            arguments={"uid": uid, "value": text}
        )
        return result

    async def get_page_content(self):
        """獲取當前頁面內容"""
        result = await self.session.call_tool(
            "take_snapshot",
            arguments={}
        )
        return result

    async def screenshot(self, path: str = "screenshot.png"):
        """截取當前頁面畫面"""
        result = await self.session.call_tool(
            "take_screenshot",
            arguments={"filePath": path}
        )
        return result

    async def execute_script(self, script: str):
        """執行 JavaScript 代碼"""
        result = await self.session.call_tool(
            "evaluate_script",
            arguments={"function": script}
        )
        return result


# 全局 MCP 客戶端實例
mcp_client = ChromeMCPClient()


# 定義訂票工具
@tool
def navigate_to_booking_site(url: str) -> str:
    """導航到訂票網站。輸入應該是完整的 URL"""
    try:
        asyncio.run(mcp_client.navigate(url))
        return f"成功導航到: {url}"
    except Exception as e:
        return f"導航失敗: {str(e)}"


@tool
def fill_booking_form(form_data: str) -> str:
    """填寫訂票表單。輸入應該是 JSON 格式，包含 uid 和 value
    例如: {"name_uid": "element123", "name_value": "張三",
           "date_uid": "element456", "date_value": "2025-10-15"}
    """
    try:
        data = json.loads(form_data)
        results = []

        # 處理每個欄位
        for key, value in data.items():
            if key.endswith("_uid"):
                field_name = key.replace("_uid", "")
                value_key = f"{field_name}_value"
                if value_key in data:
                    uid = value
                    text = data[value_key]
                    asyncio.run(mcp_client.input_text(uid, text))
                    results.append(f"{field_name}: 已填入 {text}")

        return "表單填寫完成: " + ", ".join(results)
    except Exception as e:
        return f"填寫表單失敗: {str(e)}"


@tool
def click_booking_button(uid: str) -> str:
    """點擊訂票按鈕。輸入應該是元素 UID"""
    try:
        asyncio.run(mcp_client.click_element(uid))
        return f"成功點擊按鈕: {uid}"
    except Exception as e:
        return f"點擊失敗: {str(e)}"


@tool
def check_booking_status() -> str:
    """檢查當前頁面內容，確認訂票狀態"""
    try:
        page_content = asyncio.run(mcp_client.get_page_content())
        # 簡化內容分析
        content = str(page_content)[:500]  # 只取前500字元
        return f"頁面內容: {content}"
    except Exception as e:
        return f"檢查狀態失敗: {str(e)}"


@tool
def take_screenshot(filename: str = "booking_screenshot.png") -> str:
    """截取當前頁面畫面以確認訂票結果"""
    try:
        asyncio.run(mcp_client.screenshot(filename))
        return f"截圖已儲存: {filename}"
    except Exception as e:
        return f"截圖失敗: {str(e)}"


@tool
def select_dropdown_option(script: str) -> str:
    """選擇下拉選單選項。輸入應該是 JavaScript 代碼
    例如: document.querySelector('#ticket-type').value = 'adult'
    """
    try:
        asyncio.run(mcp_client.execute_script(script))
        return "已執行選擇操作"
    except Exception as e:
        return f"選擇失敗: {str(e)}"

# 組織工具列表


tools = [
    navigate_to_booking_site,
    fill_booking_form,
    click_booking_button,
    check_booking_status,
    take_screenshot,
    select_dropdown_option
]


# 定義 ReAct prompt 模板
template = """你是一個專業的訂票助手 agent，能夠使用 Chrome 瀏覽器工具來自動化訂票流程。

你可以使用以下工具:
{tools}

工具名稱: {tool_names}

訂票流程應該遵循以下步驟:
1. 導航到訂票網站
2. 填寫必要的表單資訊（姓名、日期、票種等）
3. 選擇下拉選單選項（如果需要）
4. 點擊提交/訂票按鈕
5. 檢查訂票狀態
6. 截圖保存確認

請使用以下格式:

Question: 需要完成的訂票任務
Thought: 你應該思考下一步要做什麼
Action: 要採取的行動，應該是 [{tool_names}] 中的一個
Action Input: 行動的輸入
Observation: 行動的結果
... (這個循環可以重複多次)
Thought: 我現在知道訂票結果了
Final Answer: 訂票任務的最終結果

開始!

Question: {input}
Thought: {agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template)


# 創建 agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)


# 創建 agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10  # 訂票流程可能需要更多步驟
)


# 訂票範例
async def main():
    """主程式：執行訂票任務"""

    # 初始化 MCP 連接
    print("正在連接 Chrome DevTools MCP...")
    await mcp_client.connect()
    print("MCP 連接成功！\n")

    print("=== Chrome DevTools MCP 訂票 Agent ===\n")

    # 範例 1: 高鐵訂票
    print("範例: 高鐵訂票流程")
    booking_request = """
    請幫我在高鐵網站訂票:
    - 網址: https://www.thsrc.com.tw
    - 出發站: 台北
    - 到達站: 台中
    - 日期: 2025-10-15
    - 時間: 上午10點
    - 票數: 2張成人票

    請執行以下步驟:
    1. 導航到高鐵網站
    2. 選擇訂票功能
    3. 填寫出發站和到達站
    4. 選擇日期和時間
    5. 選擇票種和數量
    6. 搜尋車次
    7. 選擇合適的車次
    8. 確認訂票資訊
    9. 截圖保存確認

    完成後請截圖確認。
    """

    result = agent_executor.invoke({
        "input": booking_request
    })

    print(f"\n訂票結果: {result['output']}\n")


# 獨立函數版本（不使用 asyncio.run 在主程式中）
def run_booking_agent(booking_details: str):
    """執行訂票 agent"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()


async def test_mcp_connection():
    """測試 MCP 連接"""
    try:
        print("正在連接 MCP...")
        await mcp_client.connect()
        print("MCP 連接成功！")

        # 測試導航
        print("測試導航功能...")
        await mcp_client.navigate("https://example.com")
        print("導航測試成功！")

        return True
    except Exception as e:
        print(f"MCP 連接測試失敗: {str(e)}")
        return False


if __name__ == "__main__":
    print("""
    ============================================
    Chrome DevTools MCP 訂票 Agent
    ============================================

    使用前準備:
    1. 安裝 MCP Chrome DevTools 伺服器:
       npm install -g chrome-devtools-mcp

    2. 啟動 Chrome 並開啟 DevTools

    3. 運行此程式
    ============================================
    """)

    # 測試 MCP 連接
    print("測試 MCP 連接...")
    try:
        result = asyncio.run(test_mcp_connection())
        if result:
            print("所有測試通過！程式準備就緒。")
        else:
            print("測試失敗，請檢查設定。")
    except Exception as e:
        print(f"測試時發生錯誤: {str(e)}")

    print("\n提示: 取消註解 run_booking_agent() 來執行訂票任務")


# 啟用訂票測試
async def run_booking_test():
    """執行訂票測試"""
    await main()
