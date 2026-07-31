from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from config import settings

MEMORY_FILE = settings.data_dir / "memory.json"
MAX_ENTRIES = 50


def _load() -> Dict[str, Any]:
    try:
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"history": []}


def _save(data: Dict[str, Any]) -> None:
    MEMORY_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def add_entry(user_text: str, plan: Dict[str, Any], results: List[str]) -> None:
    data = _load()
    data.setdefault("history", []).append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "user": user_text,
        "plan": plan,
        "results": results,
    })
    data["history"] = data["history"][-MAX_ENTRIES:]
    _save(data)


def recent_summary(limit: int = 5) -> str:
    history = _load().get("history", [])[-limit:]
    if not history:
        return "ยังไม่มีประวัติ"
    lines = []
    for item in history:
        user = item.get("user", "")
        results = "; ".join(item.get("results", []))
        lines.append(f"- ผู้ใช้: {user} | ผลลัพธ์: {results}")
    return "\n".join(lines)
