from __future__ import annotations

import os
from pathlib import Path

from tools.base_tool import BaseTool

HOME = Path.home()
SHORTCUTS = {
    "desktop": HOME / "Desktop", "เดสก์ท็อป": HOME / "Desktop",
    "downloads": HOME / "Downloads", "ดาวน์โหลด": HOME / "Downloads",
    "documents": HOME / "Documents", "เอกสาร": HOME / "Documents",
    "pictures": HOME / "Pictures", "รูปภาพ": HOME / "Pictures",
    "music": HOME / "Music", "เพลง": HOME / "Music",
    "videos": HOME / "Videos", "วิดีโอ": HOME / "Videos",
}


class FolderTool(BaseTool):
    name = "folder"
    actions = frozenset({"open"})

    def run(self, action: str, target: str = "") -> str:
        self.validate(action)
        raw = target.strip()
        path = SHORTCUTS.get(raw.lower(), Path(os.path.expandvars(os.path.expanduser(raw))))
        if not Path(path).is_dir():
            return f"ไม่พบโฟลเดอร์ '{target}'"
        os.startfile(str(path))  # type: ignore[attr-defined]
        return f"เปิดโฟลเดอร์ {path} แล้ว"
