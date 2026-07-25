@echo off
cd /d "%~dp0"

echo =====================================
echo   Starting PetApp2 (Portable Mode)
echo =====================================

rem ffmpeg を PATH に追加
set PATH=%CD%\ffmpeg;%PATH%

rem Python 実行（カレントディレクトリを維持）
portable\python_embed\python.exe "%CD%\main.py"

echo.
echo --- App finished or crashed ---
pause
