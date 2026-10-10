import jieba
from rank_bm25 import BM25Okapi
from rag.chunker import *
class Retriever:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self.tokenized_chunks = [list(jieba.cut(chunk.content)) for chunk in chunks]
        self.bm25 = BM25Okapi(self.tokenized_chunks)
    def _score(self, query: str) -> list[float]:
        # 返回每一个chunk的分数列表
        tokenized_query = list(jieba.cut(query))
        return self.bm25.get_scores(tokenized_query)


    def search(self, query: str, top_k: int = 2) -> list[Chunk]:
        scores=self._score(query)
        scored=list(zip(scores,self.chunks))
        scored = [item for item in scored if item[0] > 0]
        if not scored:
            return []
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _,c in scored[:min(top_k,len(scored))]]


# chunks=chunk_file("../text.txt")
# retriever=Retriever(chunks)
# print(retriever.search("慢了"))