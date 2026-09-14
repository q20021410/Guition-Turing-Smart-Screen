@echo off
title Turing Smart Screen Monitor (Guition 3.5")
cd /d "%~dp0"

echo ===================================================
echo     Turing Smart Screen Monitor (Guition 3.5")
echo ===================================================
echo.
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\PawnIO" >nul 2>&1
if %errorlevel% neq 0 (
    net session >nul 2>&1
    if %errorlevel% equ 0 (
        if exist "%~dp0PawnIO_setup.exe" (
            echo [INFO] Installing PawnIO hardware driver...
            "%~dp0PawnIO_setup.exe" -install -silent
        )
    )
)

python main.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Program stopped with error code %errorlevel%.
    pause
)
