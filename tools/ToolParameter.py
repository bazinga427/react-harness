from pydantic import BaseModel, Field
from typing import List,Dict,Any,Optional
# 说明书
class ToolParameter(BaseModel):
    """工具参数定义"""
    name: str  # 参数名叫什么
    type: str  # 什么类型
    description: str  # 用来做什么的
    required: bool = True # 是否为必填
    default: Any = None