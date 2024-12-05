class PromptTemplate:
    SYSTEM_PROMPT = """你是一个专业的客服助手，你需要：
1. 始终保持礼貌和专业的态度
2. 给出简洁明确的回答
3. 在不确定的情况下，诚实地表达不确定性
4. 避免讨论敏感话题
5. 在合适的时候使用emoji表情，让对话更亲切

当前对话主题: {topic}
用户历史问题: {history}

请基于以上信息，回答用户的问题。
"""

    @staticmethod
    def format_history(messages: list) -> str:
        formatted = []
        for msg in messages:
            if msg["role"] == "user":
                formatted.append(f"用户: {msg['content']}")
            else:
                formatted.append(f"助手: {msg['content']}")
        return "\n".join(formatted[-5:])  # 只保留最近5轮对话

    @staticmethod
    def create_prompt(topic: str, history: list, current_query: str) -> str:
        history_text = PromptTemplate.format_history(history)
        prompt = PromptTemplate.SYSTEM_PROMPT.format(
            topic=topic,
            history=history_text
        )
        return f"{prompt}\n\n用户问题: {current_query}" 