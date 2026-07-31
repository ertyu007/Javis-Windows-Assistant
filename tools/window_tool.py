from __future__ import annotations

import pygetwindow as gw

from tools.base_tool import BaseTool


class WindowTool(BaseTool):
    name = "window"
    actions = frozenset({"focus", "close", "minimize", "maximize"})

    def run(self, action: str, target: str = "") -> str:
        self.validate(action)
        windows = [w for w in gw.getWindowsWithTitle(target) if w.title]
        if not windows:
            return f"ไม่พบหน้าต่าง '{target}'"
        window = windows[0]
        if action == "focus":
            if window.isMinimized:
                window.restore()
            window.activate()
        elif action == "close":
            window.close()
        elif action == "minimize":
            window.minimize()
        elif action == "maximize":
            window.maximize()
        return f"{action} หน้าต่าง {window.title} แล้ว"
