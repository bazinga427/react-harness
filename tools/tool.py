from abc import ABC, abstractmethod
from typing import List,Dict,Any,Optional
from tools.ToolParameter import *

class Tool(ABC):
    # ABC:abstract base class(抽象基类),自己不能被实例化，只能被继承
    """工具基类"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod # 子类必须自己实现
    # 工具执行
    def run(self, parameters: Dict[str, Any]) -> str:
        """执行工具"""
        pass

    @abstractmethod
    # 工具报出需要什么参数
    def get_parameters(self) -> List[ToolParameter]:
        """获取工具参数定义"""
        pass