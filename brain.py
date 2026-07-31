from __future__ import annotations

import json
import logging
import re

from llm import llm_client
from memory import recent_summary
from models import Action, Plan
from quick_commands import quick_plan
from skills import load_skills

logger = logging.getLogger(__name__)

BASE_PROMPT = """คุณคือ Javis ผู้ช่วยควบคุม Windows ภาษาไทย
หน้าที่คือแปลงคำสั่งผู้ใช้เป็น JSON สำหรับเรียก tools เท่านั้น

รูปแบบผลลัพธ์:
{
  "reply": "ข้อความสั้นที่จะพูดกับผู้ใช้",
  "requires_confirmation": false,
  "steps": [
    {"tool": "program", "action": "open", "target": "chrome"}
  ]
}

Tools:
- program: open
- browser: open, search
- file: open, find
- folder: open
- media: play, youtube
- system: shutdown, restart, sleep, lock, volume
- clipboard: copy, paste, clear
- window: focus, close, minimize, maximize
- input: write, press, hotkey, scroll
- chat: answer

กฎ:
- ตอบ JSON เท่านั้น
- ใช้หลาย steps ได้เมื่อผู้ใช้สั่งหลายอย่าง
- shutdown/restart/sleep ต้อง requires_confirmation=true
- ห้ามสร้างคำสั่ง shell หรือ PowerShell เอง
- ถ้าเป็นคำถามทั่วไปให้ใช้ chat/answer
- target ต้องเป็นข้อความจากเจตนาผู้ใช้ ไม่ใช่โค้ด
"""


def plan(text: str) -> Plan:
    fast = quick_plan(text)
    if fast is not None:
        return fast

    if not llm_client.available():
        return Plan(
            reply="ยังไม่ได้ตั้งค่า AI จึงทำได้เฉพาะคำสั่งพื้นฐาน",
            steps=[Action("chat", "answer", text)],
        )

    messages = [
        {"role": "system", "content": BASE_PROMPT + load_skills()},
        {"role": "system", "content": "ประวัติล่าสุด:\n" + recent_summary()},
        {"role": "user", "content": text},
    ]

    try:
        raw = llm_client.complete(messages, json_mode=True)
        data = _extract_json(raw)
        parsed = Plan.from_dict(data)
        if not parsed.steps:
            raise ValueError("LLM ไม่คืน steps")
        return parsed
    except Exception as exc:
        logger.exception("วางแผนไม่สำเร็จ: %s", exc)
        return Plan(
            reply="ตีความคำสั่งไม่สำเร็จ จึงส่งเป็นคำถามทั่วไป",
            steps=[Action("chat", "answer", text)],
        )


def _extract_json(raw: str) -> dict:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.I | re.S)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1:
            raise
        return json.loads(cleaned[start:end + 1])
