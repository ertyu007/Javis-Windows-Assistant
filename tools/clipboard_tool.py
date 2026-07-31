from __future__ import annotations

import pyperclip

from tools.base_tool import BaseTool


class ClipboardTool(BaseTool):
    name = "clipboard"
    actions = frozenset({"copy", "paste", "clear"})

    def run(self, action: str, target: str = "") -> str:
        self.validate(action)
        if action == "copy":
            pyperclip.copy(target)
            return "คัดลอกข้อความแล้ว"
        if action == "clear":
            pyperclip.copy("")
            return "ล้างคลิปบอร์ดแล้ว"
        return pyperclip.paste()
