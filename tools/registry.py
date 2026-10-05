from typing import Dict, Any
from tools.tool import *
# 构建一个通用的工具(支持Tool对象)
class ToolRegistry:
    """
    一个工具执行器，负责管理和执行工具。
    """
    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def registerTool(self, tool: Tool):
        """
        向工具箱中注册一个新工具。
        """
        if tool.name in self.tools:
            print(f"警告:工具 '{tool.name}' 已存在，将被覆盖。")
        self.tools[tool.name] = tool
        print(f"工具 '{tool.name}' 已注册。")

    # -> 返回类型 ->callable:返回可调用的东西（函数）
    def getTool(self, name: str) -> Tool:
        """
        根据名称获取一个工具的执行函数。
        """
        return self.tools.get(name)


    def execute(self, name: str, parameters: dict) -> str:
        """执行某个工具"""
        tool = self.get(name)
        if tool is None:
            return f"错误：未找到工具 '{name}'"
        return tool.run(parameters)

    def getAvailableTools(self) -> str:
        """
        获取所有可用工具的格式化描述字符串。
        """
        return "\n".join([
            f"- {tool.name}: {tool.description}"
            for tool in self.tools.values()
        ])
