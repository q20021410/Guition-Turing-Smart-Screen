@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ===================================================
echo     Turing Smart Screen 설정 도구 (Configure)
echo ===================================================

python configure.py
