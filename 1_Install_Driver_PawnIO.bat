@echo off
chcp 65001 >nul
title PawnIO Hardware Driver Installer
cd /d "%~dp0"

echo ========================================================
echo   PawnIO Hardware Sensor Driver Installer
echo   (Signed kernel driver for LibreHardwareMonitor)
echo   Supports both Intel Core and AMD Ryzen Processors
echo ========================================================
echo.

:: Check Administrator rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo [INFO] Installing PawnIO hardware driver...
if exist "%~dp0PawnIO_setup.exe" (
    "%~dp0PawnIO_setup.exe" -install -silent
    if %errorlevel% equ 0 (
        echo [SUCCESS] PawnIO driver installed successfully!
        echo [SUCCESS] Intel/AMD CPU temperature, power (W), and motherboard sensors are now fully accessible.
    ) else (
        echo [ERROR] Installer returned error code %errorlevel%.
    )
) else (
    echo [ERROR] PawnIO_setup.exe not found in %~dp0
)

echo.
pause
