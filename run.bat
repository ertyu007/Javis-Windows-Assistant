@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not exist venv\Scripts\python.exe (
  echo ยังไม่ได้ติดตั้ง กรุณาเปิด setup.bat ก่อน
  pause
  exit /b 1
)
call venv\Scripts\activate.bat
python main.py
pause
