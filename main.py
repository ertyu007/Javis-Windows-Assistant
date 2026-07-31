from __future__ import annotations

import logging
import sys
from dataclasses import asdict

from brain import plan
from config import settings
from executor import execute_plan
from memory import add_entry
from safety import needs_confirmation
from speech import normalize_wake_word, speech_input
from tts import speak

logging.basicConfig(
    level=getattr(logging, settings.log_level, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(settings.log_dir / "javis.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)


def read_command() -> str:
    mode = settings.input_mode
    if mode == "voice":
        return speech_input.listen()
    if mode == "text":
        return input("คุณ > ").strip()

    typed = input("พิมพ์คำสั่ง หรือกด Enter เพื่อพูด > ").strip()
    return typed or speech_input.listen()


def confirmed() -> bool:
    answer = input("ยืนยันคำสั่ง? (y/n) > ").strip().lower()
    return answer in {"y", "yes", "ใช่", "ยืนยัน"}


def main() -> None:
    print("\n🤖 Javis Windows Assistant")
    print("พิมพ์ exit เพื่อออก\n")
    speak("สวัสดีครับ จาวิสพร้อมทำงาน")

    while True:
        try:
            raw = read_command()
            if not raw:
                continue
            if raw.lower() in {"exit", "quit", "ออก", "ปิดจาวิส"}:
                break

            command = normalize_wake_word(raw)
            if command is None:
                print(f"รอคำปลุก '{settings.wake_word}'")
                continue
            if not command:
                continue

            current_plan = plan(command)
            if current_plan.reply:
                print(f"Javis > {current_plan.reply}")
                speak(current_plan.reply)

            if needs_confirmation(current_plan) and not confirmed():
                print("ยกเลิกแล้ว")
                continue

            results = execute_plan(current_plan)
            for result in results:
                print(f"✓ {result}")
            if results:
                speak(results[-1])
            add_entry(command, asdict(current_plan), results)

        except KeyboardInterrupt:
            break
        except Exception as exc:
            logging.getLogger(__name__).exception("Main error: %s", exc)
            print(f"เกิดข้อผิดพลาด: {exc}")

    print("ปิด Javis แล้ว")


if __name__ == "__main__":
    main()
