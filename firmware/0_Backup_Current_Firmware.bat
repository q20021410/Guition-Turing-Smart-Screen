@echo off
chcp 65001 >nul
title Backup Factory Firmware (Guition 3.5" - ESP32-C3)
cd /d "%~dp0"

echo ==========================================================
echo   Backup Current Firmware Dump (4MB)
echo ==========================================================
echo.
echo Reading 4MB flash from COM8 at offset 0x0...
esptool --chip esp32c3 --port COM8 --baud 921600 read_flash 0x0 0x400000 "%~dp0My_Original_Backup.bin"
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Original firmware successfully dumped to:
    echo           %~dp0My_Original_Backup.bin
) else (
    echo.
    echo [ERROR] Backup failed! Please check COM port and connection.
    echo Make sure main.exe or any other serial monitor is closed.
)
echo.
pause
