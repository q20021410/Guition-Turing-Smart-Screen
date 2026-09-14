@echo off
chcp 65001 >nul
title Flash New Firmware (Guition 3.5" - 80MHz SPI DMA)
cd /d "%~dp0"

echo ==========================================================
echo   Flash Custom High-Speed Firmware (COM8)
echo ==========================================================
echo.
echo Writing new_Firmware.bin to COM8 at offset 0x10000...
esptool --chip esp32c3 --port COM8 --baud 921600 write_flash 0x10000 "%~dp0new_Firmware.bin"
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] New firmware successfully flashed!
) else (
    echo.
    echo [ERROR] Flash failed! Please check COM port and connection.
    echo TIP: You can also use https://esptool.spacehuhn.com/ via Chrome/Edge!
)
echo.
pause
