from pydantic import BaseModel,Field
import uuid
from typing import Dict,Any
import re

class Chunk(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content:str
    metadata:Dict[str, Any] = Field(default_factory=dict) # 存来源文件名source和序号index

def chunk_file(
       file_path: str,
       chunk_size: int=100,
       overlap:int=20
) -> list[Chunk]:
    if overlap >= chunk_size:
        raise ValueError(f"overlap({overlap}) 必须小于 chunk_size({chunk_size})")
    with open(file_path,"r",encoding='utf-8') as f:
        text=f.read()
    chunks:list[Chunk] = []
    # 按字数划分
    # start=0
    # index=0
    # while start<len(text):
    #     cur=text[start:start+chunk_size]
    #     chunks.append(Chunk(content=cur, metadata={"source": file_path, "index": index}))
    #     #     start+=chunk_size-overlap
    #     index+=1

    # 按法条划分
    # "第"匹配+非贪婪+前瞻 bug:匹配所有“第”
    # pattern=r"(第(.*?)(?=第|$))"
    # chunks=re.findall(pattern,text,re.DOTALL)

    pattern = r"(?=^\s*第\s*[\d一二三四五六七八九十百]+\s*条)"
    # multiline:匹配每个\n后面的位置  ^+multiline 匹配每一行的开头
    ls = re.split(pattern, text,flags=re.MULTILINE) # list[str]
    chunks=[Chunk(content=c.strip(), metadata={"source": file_path, "index": index}) for index,c
            in enumerate(ls) if c.strip()]
    return chunks
# chunks=chunk_file("../text.txt")
# print(chunks)
