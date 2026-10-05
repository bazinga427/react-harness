import re
from core.message import Message
from datetime import datetime
from core.llm import HelloAgentsLLM
from tools.registry import ToolRegistry
from agents.base import Agent

# ReAct 提示词模板
REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。
当前日期:{current_date}
可用工具如下:
{tools}

请严格按照以下格式进行回应:

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一:
- `{{tool_name}}[{{tool_input}}]`:调用一个可用工具。
- `Finish[最终答案]`:当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在Action:字段后使用 Finish[最终答案] 来输出最终答案。

现在，请开始解决以下问题:
Question: {question}
History: {history}
"""

class ReActAgent(Agent):
    def __init__(self, name, llm, tool_registry, max_steps=5, system_prompt=None):
        super().__init__(name=name, llm=llm, system_prompt=system_prompt)
        self.tool_registry = tool_registry
        self.max_steps = max_steps

    def run(self, question: str):
        """
        运行 ReAct 智能体来回答一个问题。
        """
        # self.history = []  # 每次运行时重置历史记录
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"--- 第 {current_step} 步 ---")

            # 1. 格式化提示词
            tools_desc = self.tool_registry.getAvailableTools()
            history_str = "\n".join([f"{m.role}: {m.content}" for m in self._history])
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tools_desc,
                question=question,
                history=history_str,
                current_date = datetime.now().strftime("%Y-%m-%d")
            )

            # 2. 调用LLM进行思考
            messages = [{"role": "user", "content": prompt}]
            # 【本次修改 3】原来的写法是 self.llm_client，可是这个属性根本不存在：
            # 基类 Agent 里保存大模型客户端用的是 self.llm（见 agents/base.py 里 self.llm = llm 那一行），
            # 所以这里必须写成 self.llm。之前即使前面两个错误都修好，走到这一步也会报
            # AttributeError: ReActAgent object has no attribute llm_client。
            response_text = self.llm.think(messages=messages)

            if not response_text:
                print("错误:LLM未能返回有效响应。")
                break
            # 3. 解析LLM的输出
            thought, action = self._parse_output(response_text)

            if thought:
                print(f"思考: {thought}")

            if not action:
                print("警告:未能解析出有效的Action，流程终止。")
                break

            # 4. 执行Action
            if action.startswith("Finish"):
                # 如果是Finish指令，提取最终答案并结束
                final_answer = re.match(r"Finish\[(.*)\]", action).group(1)
                print(f"最终答案: {final_answer}")
                return final_answer

            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                # ... 处理无效Action格式 ...
                continue

            print(f"行动: {tool_name}[{tool_input}]")

            tool_function = self.tool_registry.getTool(tool_name)
            if not tool_function:
                observation = f"错误:未找到名为 '{tool_name}' 的工具。"
            else:
                observation = tool_function(tool_input)  # 调用真实工具
                # (这段逻辑紧随工具调用之后，在 while 循环的末尾)
                print(f" 观察: {observation}")

                # 将本轮的Action和Observation添加到历史记录中
                self._history.append(Message(content=f"Action: {action}", role="assistant"))
                self._history.append(Message(content=f"Observation: {observation}", role="user"))

                # 循环结束
        print("已达到最大步数，流程终止。")
        return None

        # (这些方法是 ReActAgent 类的一部分)
    def _parse_output(self, text: str):
            """解析LLM的输出，提取Thought和Action。
            """
            # Thought: 匹配到 Action: 或文本末尾
            thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
            # Action: 匹配到文本末尾
            action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)
            thought = thought_match.group(1).strip() if thought_match else None
            action = action_match.group(1).strip() if action_match else None
            return thought, action

    def _parse_action(self, action_text: str):
            """解析Action字符串，提取工具名称和输入。
            """
            match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
            if match:
                return match.group(1), match.group(2)
            return None, None
