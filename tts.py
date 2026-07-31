from __future__ import annotations

import io
import logging
import time

from config import settings

logger = logging.getLogger(__name__)


def speak(text: str) -> None:
    if not settings.tts_enabled or not text:
        return
    try:
        import pygame
        from gtts import gTTS

        audio = io.BytesIO()
        gTTS(text=text, lang=settings.tts_lang, slow=False).write_to_fp(audio)
        audio.seek(0)
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(audio, "mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.05)
    except Exception as exc:
        logger.warning("TTS ใช้งานไม่ได้: %s", exc)
