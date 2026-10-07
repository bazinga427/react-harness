from memory.base import BaseMemory, MemoryItem
from typing import List

class WorkingMemory(BaseMemory):
    def __init__(self):
       super().__init__()
       self.memories:List[MemoryItem]=[]
    def add(self,memory_item: MemoryItem):
        self.memories.append(memory_item)
        # return memory_item.id
    def remove(self,memory_id: str)->bool:
        found = False
        print(memory_id)
        for i,f in enumerate(self.memories):
            print(i,f)
            if f.id==memory_id:
                self.memories.remove(f)
                found = True
                break
        return found
    def clear(self):
        self.memories.clear()

    # query:问题 limit:前几条 kwargs:接受任意额外参数 list[memoryitem]:返回的答案
    # 计算相关度分数,丢掉分数为0的，从高到低评分
    def retrieve(self, query: str, limit: int = 5, **kwargs) -> List[MemoryItem]:
         scored=[]
         for i,y in enumerate(self.memories):
             x=_match_score(query,y.content)
             if x>0:
                scored.append((x,y))
         scored.sort(key=lambda pair:pair[0],reverse=True)
         return [m for _, m in scored[:limit]]
def _match_score( query: str, content: str) -> float:
     if not query:
         return 0
     hit_count=0
     for c in query:
         if c in content:
             hit_count+=1
     return hit_count/len(query)

