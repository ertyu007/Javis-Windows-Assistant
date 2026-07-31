from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    llm_mode: str = os.getenv("LLM_MODE", "auto").strip().lower()
    groq_api_key: str = os.getenv("GROQ_API_KEY", "").strip().strip('"').strip("'")
    groq_base_url: str = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1").rstrip("/")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

    input_mode: str = os.getenv("INPUT_MODE", "hybrid").strip().lower()
    wake_word: str = os.getenv("WAKE_WORD", "").strip()
    audio_timeout: int = int(os.getenv("AUDIO_TIMEOUT", "5"))
    phrase_time_limit: int = int(os.getenv("PHRASE_TIME_LIMIT", "8"))

    tts_enabled: bool = _bool("TTS_ENABLED", True)
    tts_lang: str = os.getenv("TTS_LANG", "th")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()

    data_dir: Path = BASE_DIR / "data"
    log_dir: Path = BASE_DIR / "logs"
    skills_dir: Path = BASE_DIR / "skills"


settings = Settings()
settings.data_dir.mkdir(exist_ok=True)
settings.log_dir.mkdir(exist_ok=True)
