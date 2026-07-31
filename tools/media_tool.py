from __future__ import annotations

import os
import urllib.parse
import webbrowser
from pathlib import Path
from typing import Optional

from tools.base_tool import BaseTool

EXTENSIONS = {".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".wma"}
ROOTS = [Path.home() / "Music", Path.home() / "Downloads", Path.home() / "Desktop"]


class MediaTool(BaseTool):
    name = "media"
    actions = frozenset({"play", "youtube"})

    def run(self, action: str, target: str = "") -> str:
        self.validate(action)
        if action == "youtube":
            return self._youtube(target)
        local = self._local(target)
        if local:
            os.startfile(str(local))  # type: ignore[attr-defined]
            return f"กำลังเล่น {local.name}"
        return self._youtube(target)

    def _local(self, keyword: str) -> Optional[Path]:
        needle = keyword.lower()
        for root in ROOTS:
            if not root.exists():
                continue
            for current, _, files in os.walk(root):
                for filename in files:
                    path = Path(current) / filename
                    if path.suffix.lower() in EXTENSIONS and needle in path.stem.lower():
                        return path
        return None

    def _youtube(self, keyword: str) -> str:
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(keyword)
        webbrowser.open(url)
        return f"ค้นหาเพลง '{keyword}' บน YouTube แล้ว"
