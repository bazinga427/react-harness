from memory.working import WorkingMemory
from memory.base import MemoryItem

wm = WorkingMemory()
wm.add(MemoryItem(content="张三是一名Python开发者"))
wm.add(MemoryItem(content="张三是前端工程师"))
_id=wm.add(MemoryItem(content="张三喜欢喝咖啡"))

# print(wm.remove(_id))

# print(len(wm.memories))
results = wm.retrieve(query="张三是", limit=5)

print(f"找到 {len(results)} 条相关记忆：")
for m in results:
    print(f"  - {m.content}")