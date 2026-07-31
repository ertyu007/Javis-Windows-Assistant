from __future__ import annotations

import pyautogui
import pyperclip

from tools.base_tool import BaseTool


class InputTool(BaseTool):
    name = "input"
    actions = frozenset({"write", "press", "hotkey", "scroll"})

    def run(self, action: str, target: str = "") -> str:
        self.validate(action)
        pyautogui.FAILSAFE = True
        if action == "write":
            pyperclip.copy(target)
            pyautogui.hotkey("ctrl", "v")
            return "พิมพ์ข้อความแล้ว"
        if action == "press":
            pyautogui.press(target.lower().strip())
            return f"กด {target} แล้ว"
        if action == "hotkey":
            keys = [part.strip().lower() for part in target.split("+") if part.strip()]
            if not keys:
                return "ไม่ได้ระบุปุ่มลัด"
            pyautogui.hotkey(*keys)
            return f"กด {target} แล้ว"
        try:
            amount = int(target)
        except ValueError:
            amount = -5 if target.lower().strip() in {"down", "ลง"} else 5
        pyautogui.scroll(amount)
        return "เลื่อนหน้าจอแล้ว"
