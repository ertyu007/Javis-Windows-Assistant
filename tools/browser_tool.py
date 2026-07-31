from __future__ import annotations

import re
import urllib.parse
import webbrowser

from tools.base_tool import BaseTool

SHORTCUTS = {
    "youtube": "https://youtube.com",
    "ยูทูบ": "https://youtube.com",
    "google": "https://google.com",
    "กูเกิล": "https://google.com",
    "facebook": "https://facebook.com",
    "เฟซบุ๊ก": "https://facebook.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
    "gemini": "https://gemini.google.com",
}


class BrowserTool(BaseTool):
    name = "browser"
    actions = frozenset({"open", "search"})

    def run(self, action: str, target: str = "") -> str:
        self.validate(action)
        return self._open(target) if action == "open" else self._search(target)

    def _open(self, target: str) -> str:
        value = target.strip()
        url = SHORTCUTS.get(value.lower())
        if not url:
            if value.startswith(("http://", "https://")):
                url = value
            elif re.fullmatch(r"[\w.-]+\.[a-zA-Z]{2,}(?:/.*)?", value):
                url = "https://" + value
            else:
                return self._search(value)
        webbrowser.open(url)
        return f"เปิด {url} แล้ว"

    def _search(self, query: str) -> str:
        url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)
        webbrowser.open(url)
        return f"ค้นหา '{query}' แล้ว"
