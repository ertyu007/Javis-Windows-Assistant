from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, List

from tools.base_tool import BaseTool

HOME = Path.home()
SEARCH_ROOTS = [HOME / "Desktop", HOME / "Downloads", HOME / "Documents", HOME / "Pictures", HOME / "Videos", HOME / "Music"]
SKIP_DIRS = {"node_modules", ".git", "__pycache__", "venv", ".venv", "windows", "appdata"}


class FileTool(BaseTool):
    name = "file"
    actions = frozenset({"open", "find"})

    def run(self, action: str, target: str = "") -> str:
        self.validate(action)
        matches = self._find(target, limit=5)
        if not matches:
            return f"ไม่พบไฟล์ '{target}'"
        if action == "find":
            return "พบไฟล์:\n" + "\n".join(str(path) for path in matches)
        os.startfile(str(matches[0]))  # type: ignore[attr-defined]
        return f"เปิดไฟล์ {matches[0].name} แล้ว"

    def _find(self, keyword: str, limit: int) -> List[Path]:
        direct = Path(os.path.expandvars(os.path.expanduser(keyword)))
        if direct.is_file():
            return [direct]

        needle = keyword.lower().strip()
        results: List[Path] = []
        for root in SEARCH_ROOTS:
            if not root.exists():
                continue
            for current, dirs, files in os.walk(root):
                dirs[:] = [d for d in dirs if d.lower() not in SKIP_DIRS]
                for filename in files:
                    if needle in filename.lower():
                        results.append(Path(current) / filename)
                        if len(results) >= limit:
                            return results
        return results
