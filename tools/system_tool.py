from __future__ import annotations

import ctypes
import subprocess

import pyautogui

from tools.base_tool import BaseTool


class SystemTool(BaseTool):
    name = "system"
    actions = frozenset({"shutdown", "restart", "sleep", "lock", "volume", "abort"})

    def run(self, action: str, target: str = "") -> str:
        self.validate(action)
        if action == "shutdown":
            subprocess.Popen(["shutdown", "/s", "/t", "5"])
            return "จะปิดเครื่องใน 5 วินาที"
        if action == "restart":
            subprocess.Popen(["shutdown", "/r", "/t", "5"])
            return "จะรีสตาร์ทใน 5 วินาที"
        if action == "abort":
            subprocess.Popen(["shutdown", "/a"])
            return "ยกเลิกการปิดเครื่องแล้ว"
        if action == "sleep":
            subprocess.Popen(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
            return "กำลังพักเครื่อง"
        if action == "lock":
            ctypes.windll.user32.LockWorkStation()
            return "ล็อกหน้าจอแล้ว"
        return self._volume(target)

    def _volume(self, target: str) -> str:
        value = target.lower().strip()
        if value == "up":
            pyautogui.press("volumeup", presses=3)
            return "เพิ่มเสียงแล้ว"
        if value == "down":
            pyautogui.press("volumedown", presses=3)
            return "ลดเสียงแล้ว"
        if value == "mute":
            pyautogui.press("volumemute")
            return "สลับปิดเสียงแล้ว"
        return "ระดับเสียงรองรับ up, down หรือ mute"
