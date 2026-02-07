@echo off
echo Installing dependencies...
py -m pip install -r requirements.txt
py -m pip install pyinstaller

echo.
echo Building executable...
py -m PyInstaller --onefile --noconsole --name SwiftClip --icon=icon.ico --add-data "icon.ico;." main.py

echo.
echo ========================================
echo Done! Executable is in: dist\SwiftClip.exe
echo.
echo Note: Run as Administrator for hotkey to work properly
echo ========================================
pause
