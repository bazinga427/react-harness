from pydantic import BaseModel, Field
from typing import Literal, Optional,Dict,Any,List
from datetime import datetime
import uuid
from abc import ABC, abstractmethod

# pydantic:帮你定义数据类，自动做校验，转换的python库
# BaseModel:数据模型基类，继承pydantic的能力
# Field:字段配置工具(给字段加描述，加默认值，加约束)  第一个参数为默认值，...表示无默认值但必填
# uuid:通用唯一识别码
# default_factory：要一个函数

class MemoryItem(BaseModel):
    content: str = Field(..., description="记忆内容")
    memory_type: Literal["working", "episodic", "semantic", "perceptual"] = Field(
        "working", description="记忆类型"
    )
    importance: float = Field(0.5, description="重要性，0-1 之间")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="唯一 ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="创建时间")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="附加元数据")

# 抽象基类：接口说明书
class BaseMemory(ABC):

    @abstractmethod
    def add(self,memory_item: MemoryItem)->str:
        pass

    @abstractmethod
    def retrieve(self, query: str, limit: int = 5, **kwargs) -> List[MemoryItem]:
        pass

    @abstractmethod
    def remove(self, memory_id: str) -> bool :
        pass

    @abstractmethod
    def clear(self)->None:
        pass