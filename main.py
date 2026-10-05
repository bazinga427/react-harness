from tools.calculate import calculator
from core.llm import HelloAgentsLLM
from agents.react_agent import *
from tools.search import *
from tools.registry import  ToolRegistry

# --- 客户端使用示例 ---
if __name__ == '__main__':

    # 1. 创建 LLM 客户端
    llm_client = HelloAgentsLLM()

    # 2. 创建工具执行器，注册工具
    tool_registry = ToolRegistry()
    tool_registry.registerTool(
        name="search",
        description="一个网页搜索引擎，输入查询关键词，返回搜索结果摘要。",
        func=search
    )
    tool_registry.registerTool(
        name="calculator",
        description="一个计算器工具，输入数学表达式（如 '2 + 3 * 4'），返回计算结果。",
        func=calculator
    )
    # 3. 创建 ReAct Agent
    agent = ReActAgent(
        name="ReActAgent",
        # 【本次修改 2】创建 Agent 时，括号里的参数名必须和 ReActAgent 定义里的一模一样：
        # 大模型客户端叫 llm（不是 llm_client），工具执行器叫 tool_registry（不是 tool_executor）。
        # 名字对不上，Python 会直接报 TypeError: __init__() got an unexpected keyword argument。
        llm=llm_client,
        tool_registry=tool_registry,
        max_steps=5
    )

    # 4. 运行
    question = "南昌今天的天气怎么样？转华氏度呢"
    result = agent.run(question)
    print("最终返回:", result)
