from pydantic import BaseModel,Field
import uuid
from typing import Dict,Any

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
    start=0
    index=0
    while start<len(text):
        cur=text[start:start+chunk_size]
        chunks.append(Chunk(content=cur, metadata={"source": file_path, "index": index}))
        start+=chunk_size-overlap
        index+=1
    return chunks
# chunks=chunk_file("../text.txt")
# print(chunks)
