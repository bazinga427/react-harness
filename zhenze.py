import re
s="""Thought: 我需要检索社保法条
Action:内容检索[社保]"""

# 1.分离thought
# Thought:开始，非贪婪匹配，遇到\nAction:或者结尾就停止
# re.DOTALL,让re里的.可以匹配\n
thought=re.search(r"Thought:\s*(.*?)(?=\nAction:|$)",s,re.DOTALL)
print(thought.group(1))

# 2.分离action
action=re.search(r"Action:(.*)",s,re.DOTALL)
print(action.group(1))

# 分离工具名，参数
# (\w+) : 捕获工具 get_parameter这种的
match=re.search(r"(\w+)\[(.*)\]",s,re.DOTALL)
print(match.group(1))
print(match.group(2))