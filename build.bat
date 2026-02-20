@echo off
setlocal EnableExtensions

set "ROOT=%~dp0"
cd /d "%ROOT%"

echo [INFO] Building Windows EXE (requires installed Python + internet)...
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

echo [INFO] Installing dependencies...
python -m pip install -r requirements.txt pyinstaller

echo [INFO] Building EXE with PyInstaller...
python -m PyInstaller --noconfirm --onefile --windowed --name "MaFileManager" --icon "assets\app.ico" --add-data "assets\app.ico;assets" main.py

echo [OK] Done! EXE: dist\MaFileManager.exe
pause
