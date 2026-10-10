from tools.calculate import Calculator
from tools.search import Search
from tools.Memory import *
from tools.Rag import *
from core.llm import HelloAgentsLLM
from agents.react_agent import *
# from tools.search import *
from tools.registry import  ToolRegistry



# --- 客户端使用示例 ---
if __name__ == '__main__':

    # 1. 创建 LLM 客户端
    llm_client = HelloAgentsLLM()

    # 2. 创建工具执行器，注册工具
    tool_registry = ToolRegistry()
    tool_registry.registerTool(
        Calculator()
    )
    # tool_registry.registerTool(
    #     Search()
    # )

    wm = WorkingMemory()
    wm.add(MemoryItem(content="我正在找python方向实习"))
    wm.add(MemoryItem(content="我是大二软件工程专业学生"))
    mem=Memory_tool(wm)
    tool_registry.registerTool(mem)

    chunk = chunk_file("text.txt")
    retriever=Retriever(chunk)
    tool_registry.registerTool(rag_tool(retriever))
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
    question = "公司一定要给我交社会保险费吗，请根据知识库找到对应的法条，并返回具体的法条"
    result = agent.run(question)
    print("最终返回:", result)
