from tools.tool import *

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

class Calculator(Tool):
    def __init__(self):
        super().__init__(name="calculator",description="do some math")
    def run(self,parameters: Dict[str, Any]) -> str:
        expression = parameters["expression"]
        return calculator(expression)
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="expression",
                type="str",
                description="要计算的数学表达式",
                required=True
            )
        ]


# cal=Calculator()
# print(cal.get_parameters())
# cal.run({"expression":"2 + 3 * 4"})