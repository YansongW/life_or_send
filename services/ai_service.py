import httpx
from config.config import settings
from ragflow import RAGFlow
from ragflow.schema import Document
from .prompt_template import PromptTemplate

class AIService:
    def __init__(self):
        self.ollama_url = settings.OLLAMA_API_URL
        self.model_name = settings.MODEL_NAME
        self.rag_flow = RAGFlow(**settings.RAGFLOW_CONFIG)
        self.prompt_template = PromptTemplate()
    
    async def chat(self, user_id: str, message: str, context: list = None, topic: str = "一般咨询"):
        # 使用RAGFlow检索相关上下文
        relevant_docs = await self.rag_flow.similarity_search(message)
        
        # 构建提示词
        prompt = self.prompt_template.create_prompt(
            topic=topic,
            history=context or [],
            current_query=message
        )
        
        # 调用Ollama API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 2000
                    }
                }
            )
            result = response.json()
            return result["response"]
    
    async def add_to_knowledge_base(self, text: str, metadata: dict = None):
        # 将新的对话内容添加到向量数据库
        doc = Document(page_content=text, metadata=metadata or {})
        await self.rag_flow.add_documents([doc])
    
    def _format_context(self, docs: list[Document]) -> str:
        return "\n".join([f"- {doc.page_content}" for doc in docs]) 