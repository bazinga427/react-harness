from rag.retriever import *
from tools.tool import *
class rag_tool(Tool):
    def __init__(self,retriever:Retriever):
        super().__init__(
            name="内容检索",description="从知识库检索内容"
        )
        self.retriever=retriever

    def run(self, parameters: Dict[str, Any])->str:
        query=parameters["query"]
        results=self.retriever.search(query)
        if not results:
            return "没有找到相关记录"
        else:
            return "\n".join(i.content for i in results)
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="query",
                type="str",
                description="从知识库检索内容",
                required=False
            )
        ]
# chunk=chunk_file("../text.txt")
# retriever=Retriever(chunk)
# rg=rag_tool(retriever)
# ls=rg.run({"query":"慢了"})
# print(ls)