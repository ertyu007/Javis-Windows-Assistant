from __future__ import annotations

from llm import llm_client
from tools.base_tool import BaseTool


class ChatTool(BaseTool):
    name = "chat"
    actions = frozenset({"answer"})

    def run(self, action: str, target: str = "") -> str:
        self.validate(action)
        if not llm_client.available():
            return "ยังไม่ได้ตั้งค่า Groq API หรือ Ollama"
        return llm_client.complete([
            {"role": "system", "content": "คุณคือ Javis ตอบภาษาไทยสั้น ชัดเจน"},
            {"role": "user", "content": target},
        ])
