from dotenv import load_dotenv
load_dotenv()
import os
from tools.registry import ToolRegistry
def calculator(expression: str) -> str:
    """
    一个简单的计算器工具，输入数学表达式（如 '2 + 3 * 4'），返回计算结果。
    """
    print(f"正在计算: {expression}")
    try:
        # eval:把字符串当成python代码执行，返回结果
        result = eval(expression)
        return f"计算结果: {expression} = {result}"
    except Exception as e:
        return f"计算错误: {e}"
# # 构造工具
# tool = ToolExecutor()
# tool_description="一个简单的计算器工具，输入数学表达式（如 '2 + 3 * 4'），返回计算结果"
# tool.registerTool("calculator",tool_description,calculator)
# # print(tool.getAvailableTools())
# # 调用
# str="2 + 3 * 4"
# func=tool.getTool("calculator")
# if func:
#     print(func(str))
# else:
#     print(f"没有该工具")