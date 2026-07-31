from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Optional

from config import settings
from tools.base_tool import BaseTool

ALIASES: Dict[str, str] = {
    "chrome": "chrome.exe", "โครม": "chrome.exe", "กูเกิล": "chrome.exe",
    "edge": "msedge.exe", "ไมโครซอฟท์ edge": "msedge.exe",
    "vscode": "code.exe", "vs code": "code.exe", "visual studio code": "code.exe",
    "notepad": "notepad.exe", "โน้ตแพด": "notepad.exe",
    "calculator": "calc.exe", "เครื่องคิดเลข": "calc.exe",
    "explorer": "explorer.exe", "file explorer": "explorer.exe",
    "cmd": "cmd.exe", "terminal": "wt.exe", "เทอร์มินัล": "wt.exe",
    "discord": "Discord.exe", "ดิสคอร์ด": "Discord.exe",
    "spotify": "Spotify.exe", "สปอติฟาย": "Spotify.exe",
    "steam": "steam.exe", "สตีม": "steam.exe",
    "word": "WINWORD.EXE", "excel": "EXCEL.EXE", "powerpoint": "POWERPNT.EXE",
}

CACHE_FILE = settings.data_dir / "cache.json"


class ProgramTool(BaseTool):
    name = "program"
    actions = frozenset({"open"})

    def run(self, action: str, target: str = "") -> str:
        self.validate(action)
        if not target.strip():
            return "ไม่ได้ระบุชื่อโปรแกรม"

        keyword = ALIASES.get(target.strip().lower(), target.strip())
        path = self._cached(keyword) or self._which(keyword) or self._find_start_menu(keyword) or self._find_exe(keyword)
        if not path:
            return f"หาโปรแกรม '{target}' ไม่เจอ"

        try:
            os.startfile(path)  # type: ignore[attr-defined]
        except AttributeError:
            subprocess.Popen([path])
        self._remember(keyword, path)
        return f"เปิด {target} แล้ว"

    def _which(self, keyword: str) -> Optional[str]:
        return shutil.which(keyword)

    def _find_start_menu(self, keyword: str) -> Optional[str]:
        needle = Path(keyword).stem.lower()
        roots = [
            Path(os.getenv("APPDATA", "")) / "Microsoft/Windows/Start Menu/Programs",
            Path(os.getenv("PROGRAMDATA", "")) / "Microsoft/Windows/Start Menu/Programs",
        ]
        for root in roots:
            if not root.exists():
                continue
            for link in root.rglob("*.lnk"):
                if needle in link.stem.lower():
                    return str(link)
        return None

    def _find_exe(self, keyword: str) -> Optional[str]:
        needle = Path(keyword).stem.lower()
        roots = [
            Path(os.getenv("LOCALAPPDATA", "")),
            Path(os.getenv("PROGRAMFILES", r"C:\Program Files")),
            Path(os.getenv("PROGRAMFILES(X86)", r"C:\Program Files (x86)")),
        ]
        skip = {"windowsapps", "packages", "temp", "cache", "node_modules"}
        for root in roots:
            if not root.exists():
                continue
            for current, dirs, files in os.walk(root):
                dirs[:] = [d for d in dirs if d.lower() not in skip]
                for filename in files:
                    if filename.lower().endswith(".exe") and needle in Path(filename).stem.lower():
                        return str(Path(current) / filename)
        return None

    def _load_cache(self) -> dict:
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"programs": {}}

    def _cached(self, keyword: str) -> Optional[str]:
        path = self._load_cache().get("programs", {}).get(keyword.lower())
        return path if path and Path(path).exists() else None

    def _remember(self, keyword: str, path: str) -> None:
        data = self._load_cache()
        data.setdefault("programs", {})[keyword.lower()] = path
        CACHE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
