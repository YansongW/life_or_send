from typing import List, Dict
from ragflow import RAGFlow
from config.config import settings

class VectorService:
    def __init__(self):
        self.rag_flow = RAGFlow(**settings.RAGFLOW_CONFIG)
    
    async def add_conversation(self, user_id: str, question: str, answer: str):
        """添加对话到向量数据库"""
        conversation = f"Q: {question}\nA: {answer}"
        metadata = {
            "user_id": user_id,
            "type": "conversation",
            "timestamp": str(datetime.utcnow())
        }
        await self.rag_flow.add_documents([{
            "page_content": conversation,
            "metadata": metadata
        }])
    
    async def search_similar_conversations(
        self,
        user_id: str,
        query: str,
        limit: int = 5
    ) -> List[Dict]:
        """搜索相似对话"""
        results = await self.rag_flow.similarity_search(
            query,
            filter={"user_id": user_id},
            k=limit
        )
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in results
        ] 