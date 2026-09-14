@echo off
chcp 65001 >nul
title Restore Factory Backup Firmware (Guition 3.5" - 4MB Full Flash)
cd /d "%~dp0"

echo ==========================================================
echo   Restore Original Factory Firmware (COM8)
echo ==========================================================
echo.
echo Writing Backup_Firmware.bin to COM8 at offset 0x0 (Full 4MB)...
esptool --chip esp32c3 --port COM8 --baud 921600 write_flash 0x0 "%~dp0Backup_Firmware.bin"
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Original factory firmware successfully restored!
) else (
    echo.
    echo [ERROR] Restore failed! Please check COM port and connection.
    echo TIP: You can also use https://esptool.spacehuhn.com/ via Chrome/Edge!
)
echo.
pause
