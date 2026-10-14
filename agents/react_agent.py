import re
from core.message import Message
from datetime import datetime
from core.llm import HelloAgentsLLM
from tools.registry import ToolRegistry
from agents.base import Agent

# ReAct 提示词模板

# 静态
SYSTEM_CONTENT="""请注意，你是一个有能力调用外部工具的智能助手。
当前日期:{current_date}
可用工具如下:
{tools}

请严格按照以下格式进行回应:

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一:
- `{{tool_name}}[{{tool_input}}]`:调用一个可用工具。
- `Finish[最终答案]`:当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在Action:字段后使用 Finish[最终答案] 来输出最终答案。
"""

# 动态（加到上下文窗口）
USER_CONTENT="""以下是已完成的步骤，仅供你参考，不要重复输出:
{history}

现在轮到你。请只输出一段 Thought 和一行 Action，输出后立即停止。
不要输出 Observation，不要复述历史。
如果历史中的信息已经足以回答，直接输出 Finish[最终答案]。
Question: {question}"""

class ReActAgent(Agent):
    def __init__(self, name, llm, tool_registry, max_steps=5, system_prompt=None,recent_move=None):
        super().__init__(name=name, llm=llm, system_prompt=system_prompt)
        self.tool_registry = tool_registry
        self.max_steps = max_steps
        self.recent_move = []

    def run(self, question: str):
        """
        运行 ReAct 智能体来回答一个问题。
        """
        # self.history = []  # 每次运行时重置历史记录
        self.recent_move = []  # 每次新问题，清空记录
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"--- 第 {current_step} 步 ---")

            # 1. 格式化提示词
            tools_desc = self.tool_registry.getAvailableTools()
            history_str = "\n".join([f"{m.role}: {m.content}" for m in self._history])
            system_content = SYSTEM_CONTENT.format(
                tools=tools_desc,
                current_date = datetime.now().strftime("%Y-%m-%d")
            )
            user_content = USER_CONTENT.format(
                question=question,
                history=history_str
            )

            # 2. 调用LLM进行思考

            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ]
            # print(f"提示词:{messages}")
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
                final_answer = re.match(r"Finish\[(.*)\]", action,re.DOTALL).group(1)
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
                self.recent_move.append([tool_name, tool_input])
                # 检测是否重复

                if len(self.recent_move) >= 2:
                    last_action = self.recent_move[-1]
                    previous_action = self.recent_move[-2]
                    if (last_action[0]==previous_action[0]):
                        print("重复")
                        observation = "你已经重复调用过这个工具了，检索结果没有新增信息。请基于现有信息直接输出 Finish[最终答案]。"
                        self._history.append(Message(content=f"Action: {action}", role="assistant"))
                        self._history.append(Message(
                            content=f"Observation: {observation}", role="user"))
                        continue

            params = {p.name: tool_input for p in tool_function.get_parameters()}
            try:
                observation = tool_function.run(params)
                # (这段逻辑紧随工具调用之后，在 while 循环的末尾)
                print(f" 观察: {observation}")
            except Exception as e:
                observation=f"工具{tool_name}执行失败：{type(e).__name__}:{e}"

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
            # .strip() 去掉字符串首尾的空白字符
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
