from __future__ import annotations

import re
from typing import Optional

from models import Action, Plan

WEB_NAMES = {
    "youtube": "youtube",
    "ยูทูบ": "youtube",
    "google": "google",
    "กูเกิล": "google",
    "facebook": "facebook",
    "เฟซบุ๊ก": "facebook",
    "github": "github",
    "chatgpt": "chatgpt",
}


def quick_plan(text: str) -> Optional[Plan]:
    original = text.strip()
    value = original.lower().strip()

    if value in {"เพิ่มเสียง", "เสียงดังขึ้น"}:
        return _one("กำลังเพิ่มเสียง", "system", "volume", "up")
    if value in {"ลดเสียง", "เสียงเบาลง"}:
        return _one("กำลังลดเสียง", "system", "volume", "down")
    if value in {"ปิดเสียง", "mute"}:
        return _one("กำลังปิดเสียง", "system", "volume", "mute")
    if value in {"ล็อกหน้าจอ", "ล็อกเครื่อง"}:
        return _one("กำลังล็อกหน้าจอ", "system", "lock")
    if value in {"ปิดเครื่อง", "shutdown"}:
        return Plan("ต้องยืนยันก่อนปิดเครื่อง", [Action("system", "shutdown")], True)
    if value in {"รีสตาร์ท", "restart", "รีสตาร์ทเครื่อง"}:
        return Plan("ต้องยืนยันก่อนรีสตาร์ท", [Action("system", "restart")], True)
    if value in {"พักเครื่อง", "sleep"}:
        return Plan("ต้องยืนยันก่อนพักเครื่อง", [Action("system", "sleep")], True)

    match = re.match(r"^(?:ค้นหา|เสิร์ช)\s+(.+)$", original, flags=re.I)
    if match:
        query = match.group(1).strip()
        return _one(f"กำลังค้นหา {query}", "browser", "search", query)

    match = re.match(r"^(?:เปิดเว็บ|เข้าเว็บ)\s+(.+)$", original, flags=re.I)
    if match:
        target = match.group(1).strip()
        return _one(f"กำลังเปิด {target}", "browser", "open", target)

    match = re.match(r"^เปิด\s+(.+)$", original, flags=re.I)
    if match:
        target = match.group(1).strip()
        web = WEB_NAMES.get(target.lower())
        if web:
            return _one(f"กำลังเปิด {target}", "browser", "open", web)
        if target.lower().startswith(("โฟลเดอร์ ", "folder ")):
            folder = target.split(" ", 1)[1]
            return _one(f"กำลังเปิดโฟลเดอร์ {folder}", "folder", "open", folder)
        if target.lower().startswith(("ไฟล์ ", "file ")):
            filename = target.split(" ", 1)[1]
            return _one(f"กำลังเปิดไฟล์ {filename}", "file", "open", filename)
        return _one(f"กำลังเปิด {target}", "program", "open", target)

    match = re.match(r"^(?:เล่นเพลง|เปิดเพลง)\s+(.+)$", original, flags=re.I)
    if match:
        keyword = match.group(1).strip()
        return _one(f"กำลังเปิดเพลง {keyword}", "media", "play", keyword)

    match = re.match(r"^(?:พิมพ์|เขียน)\s+(.+)$", original, flags=re.I)
    if match:
        content = match.group(1)
        return _one("กำลังพิมพ์ข้อความ", "input", "write", content)

    match = re.match(r"^กด\s+(.+)$", original, flags=re.I)
    if match:
        key = match.group(1).strip()
        action = "hotkey" if "+" in key else "press"
        return _one(f"กำลังกด {key}", "input", action, key)

    match = re.match(r"^(?:ปิดโปรแกรม|ปิดหน้าต่าง)\s+(.+)$", original, flags=re.I)
    if match:
        target = match.group(1).strip()
        return _one(f"กำลังปิด {target}", "window", "close", target)

    return None


def _one(reply: str, tool: str, action: str, target: str = "") -> Plan:
    return Plan(reply=reply, steps=[Action(tool, action, target)])
