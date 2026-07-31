@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo [1/3] สร้าง virtual environment...
py -m venv venv
if errorlevel 1 goto :error

echo [2/3] ติดตั้งแพ็กเกจ...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 goto :error

echo [3/3] สร้างไฟล์ .env...
if not exist .env copy .env.example .env >nul

echo.
echo ติดตั้งเสร็จ แก้ GROQ_API_KEY ในไฟล์ .env แล้วเปิด run.bat
pause
exit /b 0

:error
echo.
echo ติดตั้งไม่สำเร็จ กรุณาตรวจ Python และข้อความด้านบน
pause
exit /b 1
