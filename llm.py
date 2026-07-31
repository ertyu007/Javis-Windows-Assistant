from __future__ import annotations

import logging
from typing import Dict, List, Optional

import requests

from config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    def available(self) -> bool:
        return self._pick_backend() is not None

    def complete(self, messages: List[Dict[str, str]], json_mode: bool = False) -> str:
        backend = self._pick_backend()
        if backend == "ollama":
            try:
                return self._ollama(messages, json_mode)
            except Exception as exc:
                logger.warning("Ollama ใช้งานไม่ได้: %s", exc)
                if settings.llm_mode == "auto" and settings.groq_api_key:
                    return self._groq(messages)
                raise
        if backend == "groq":
            return self._groq(messages)
        raise RuntimeError("ไม่มี LLM ที่ใช้งานได้ กรุณาตั้งค่า Groq หรือเปิด Ollama")

    def _pick_backend(self) -> Optional[str]:
        mode = settings.llm_mode
        if mode == "groq":
            return "groq" if settings.groq_api_key else None
        if mode == "ollama":
            return "ollama" if self._ollama_online() else None
        if self._ollama_online():
            return "ollama"
        if settings.groq_api_key:
            return "groq"
        return None

    def _ollama_online(self) -> bool:
        try:
            response = requests.get(f"{settings.ollama_base_url}/api/tags", timeout=2)
            return response.ok
        except requests.RequestException:
            return False

    def _ollama(self, messages: List[Dict[str, str]], json_mode: bool) -> str:
        payload = {
            "model": settings.ollama_model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.1 if json_mode else 0.6},
        }
        if json_mode:
            payload["format"] = "json"
        response = requests.post(
            f"{settings.ollama_base_url}/api/chat",
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["message"]["content"].strip()

    def _groq(self, messages: List[Dict[str, str]]) -> str:
        response = requests.post(
            f"{settings.groq_base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.groq_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.groq_model,
                "messages": messages,
                "temperature": 0.1,
                "max_tokens": 1200,
            },
            timeout=35,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()


llm_client = LLMClient()
