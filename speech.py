from __future__ import annotations

import logging
from typing import Optional

from config import settings

logger = logging.getLogger(__name__)


class SpeechInput:
    def __init__(self) -> None:
        self._recognizer = None
        try:
            import speech_recognition as sr
            self.sr = sr
            self._recognizer = sr.Recognizer()
            self._recognizer.dynamic_energy_threshold = True
            self._recognizer.pause_threshold = 0.8
        except ImportError:
            self.sr = None

    @property
    def available(self) -> bool:
        return self._recognizer is not None

    def listen(self) -> str:
        if not self.available:
            return ""
        try:
            print("[🎤] พูดได้เลย...")
            with self.sr.Microphone(sample_rate=16000) as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=0.35)
                audio = self._recognizer.listen(
                    source,
                    timeout=settings.audio_timeout,
                    phrase_time_limit=settings.phrase_time_limit,
                )
            text = self._recognizer.recognize_google(audio, language="th-TH")
            return text.strip()
        except self.sr.WaitTimeoutError:
            return ""
        except self.sr.UnknownValueError:
            print("[⚠️] ฟังไม่ชัด")
            return ""
        except Exception as exc:
            logger.warning("รับเสียงไม่สำเร็จ: %s", exc)
            print(f"[⚠️] ไมค์ใช้งานไม่ได้: {exc}")
            return ""


def normalize_wake_word(text: str) -> Optional[str]:
    wake = settings.wake_word.strip()
    if not wake:
        return text.strip()
    value = text.strip()
    if not value.lower().startswith(wake.lower()):
        return None
    return value[len(wake):].strip()


speech_input = SpeechInput()
