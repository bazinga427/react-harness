from multiprocessing import resource_sharer

from joblib import Memory

from memory.working import *
from tools.tool import *


# 修改1：Memory_Tool的run只留一个retrieve(agent只会用到这一个),其他的调用workingmemory实现
class Memory_tool(Tool):
    def __init__(self,memory:WorkingMemory):
        # 传入memory对象
        super().__init__(name="memory",description="查询关于用户本人或过往对话的记忆，当问题涉及用户个人信息、偏好、之前说过的事情时使用") # 调用父类
        # 保存memory
        self.memory = memory
    def run(self, parameters: Dict[str, Any])->str:
            query=parameters["query"]
            results=self.memory.retrieve(query)
            if not results:
                return "没有找到相关记忆"
            else:
                return "\n".join(i.content for i in results)

    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="query",
                type="str",
                description="查询关于用户本人或过往对话的记忆，当问题涉及用户个人信息、偏好、之前说过的事情时使用",
                required=False
            )
        ]

# wm=WorkingMemory()
# mem=Memory_tool(wm)
# wm.add(MemoryItem(content="111222"))
# ans=mem.run({"query":"111"})
# print(ans)