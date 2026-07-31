from __future__ import annotations

import logging
from pathlib import Path

from config import settings

logger = logging.getLogger(__name__)


def load_skills(max_chars: int = 14000) -> str:
    """โหลด skills/**/SKILL.md เพื่อเสริม system prompt"""
    chunks = []
    used = 0
    for path in sorted(settings.skills_dir.glob("**/SKILL.md")):
        try:
            text = path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            logger.warning("อ่าน skill ไม่ได้ %s: %s", path, exc)
            continue

        block = f"\n### Skill: {path.parent.name}\n{text}\n"
        if used + len(block) > max_chars:
            break
        chunks.append(block)
        used += len(block)
    return "".join(chunks)
