# Guition 3.5" IPS USB-C Smart Screen - PC Monitor Software

**English** | [Korean (README_KR.md)](README_KR.md)

Open-source PC system monitor software and custom firmware integration for the **Guition 3.5" IPS USB Type-C Secondary Display**.

> [!NOTE]
> **Upstream Project & Source**:
> The PC system monitoring client in this project is based on the open-source project **[mathoudebine/turing-smart-screen-python](https://github.com/mathoudebine/turing-smart-screen-python)** by Matthieu Houdebine. It has been customized and packaged to work seamlessly with the Guition 3.5" ESP32-C3 hardware and high-speed custom firmware.
>
> ⚡ **Dedicated Firmware Repository**:
> Custom ESP32-C3 firmware source, pre-compiled `.bin` files, and Web Flasher instructions are hosted at **[q20021410/Guition-ESP32-C3-Fimrware](https://github.com/q20021410/Guition-ESP32-C3-Fimrware)**.
>
> 📦 **Pre-compiled Releases**:
> Download standalone Windows executables (no Python needed) at **[Guition.Turing.zip (v1.0.1)](https://github.com/q20021410/Guition-Turing-Smart-Screen/releases/latest)**.

---

## 📷 Showcase

<div align="center">

| 🖥️ Live Monitoring (Landscape) | ⏳ Custom Firmware Standby Screen |
| :---: | :---: |
| <img src="img/after.jpg" height="320" alt="Live Monitoring" /> | <img src="img/standby.jpg" height="320" alt="Standby Screen" /> |
| **Real-Time Monitoring (480x320)**<br/><sub>CPU/GPU temp, power (W), clocks, network & C: drive</sub> | **80MHz SPI DMA Standby (320x480)**<br/><sub>Awaiting PC serial connection</sub> |

</div>

<p align="center">
  <img src="img/config.png" width="80%" alt="GUI Configuration Wizard" />
</p>

---

## 🛒 Product Information & Hardware Verification

To verify that your display hardware matches this software and firmware:

* **Device**: Guition 3.5" IPS USB-C Secondary Monitor / Smart Screen
* **Controller**: ESP32-C3 (RISC-V single-core @ 160MHz, 4MB Flash)
* **Display Panel**: 3.5-inch IPS LCD (320x480 native resolution, ST7796S driver)
* **Connectivity**: Single USB Type-C cable (Power + High-speed Serial)
* **Purchase Link**: [AliExpress - Guition 3.5" IPS USB Secondary Screen](https://aliexpress.com/item/1005006622935422.html)
* **Upstream Discussion**: [mathoudebine/turing-smart-screen-python#426](https://github.com/mathoudebine/turing-smart-screen-python/issues/426)

---

## ⚠️ Important Precautions

> [!CAUTION]
> ### 1. Backup Your Original Factory Firmware First!
> While this repository includes a clean 4MB factory flash dump (`firmware/Backup_Firmware.bin`), slight hardware revisions from AliExpress batches may occur.
> **We strongly recommend backing up your device's current 4MB flash before flashing new firmware!**
> - **1-Click Backup**: If Python & esptool are installed, double-click `firmware/0_Backup_Current_Firmware.bat`.
> - **Manual Command**:
>   ```bash
>   esptool --chip esp32c3 --port COM8 --baud 921600 read_flash 0x0 0x400000 My_Original_Backup.bin
>   ```

> [!WARNING]
> ### 2. Strictly Follow Flash Offset Addresses (Prevent Bricking)
> * **New Custom Firmware (`new_Firmware.bin`)**: Must be flashed at offset **`0x10000`**!
>   * *Never flash `new_Firmware.bin` at `0x0`, as that would overwrite the ESP32-C3 bootloader and partition tables.*
> * **Factory Restore Image (`Backup_Firmware.bin`)**: Must be flashed at offset **`0x0`**!
>   * *Because it is a full 4MB raw dump of the entire flash memory.*

> [!IMPORTANT]
> ### 3. Close All Serial Monitor Programs Before Flashing (Avoid Access Denied)
> If `main.exe`, `GUITION Smart screen.exe`, Arduino IDE, or a serial terminal is currently running on the display's COM port, flashing will fail with `PermissionError 13 (Access is denied)`. Always close all monitoring software before flashing.

> [!NOTE]
> ### 4. Kernel Driver Privileges (Intel & AMD)
> * Right-click `1_Install_Driver_PawnIO.bat` and select **[Run as administrator]** once.
> * This project uses the Microsoft-signed **PawnIO** driver (`v2.2.0`) instead of vulnerable `WinRing0.sys`. It is fully compatible with Windows 10/11 Core Isolation and Memory Integrity (HVCI) for both **Intel** and **AMD** CPUs.

---

## ✨ Features

- **Guition 3.5" ST7796 Support**: Tuned for 80MHz SPI DMA custom firmware with zero screen tearing and low latency.
- **Intel & AMD Ryzen Hardware Monitoring**: Powered by the Microsoft-signed **PawnIO** kernel driver (`v2.2.0`) and **LibreHardwareMonitorLib**, compatible with Windows 10/11 Core Isolation (HVCI).
- **New High-Density Theme (`LandscapePastelGirl`)**:
  - Non-intrusive layout preserving character art on the right.
  - Real-time CPU & GPU Power draw (W).
  - Directional network upload/download speed indicators (▼ / ▲).
  - Accurate C: drive system storage gauge (Total, Used, Free).
- **73+ Pre-installed Themes**: Switch instantly with real-time thumbnail previews via `configure.py`.
- **Visual Theme Editor**: Interactive coordinate inspector and widget placement tool via `theme-editor.py`.

---

## ⚡ Quick Start

### Option 1: Standalone Windows Executable (Recommended)

1. Download **`Guition.Turing.zip`** from [Releases](https://github.com/q20021410/Guition-Turing-Smart-Screen/releases/latest) and extract.
2. (First time only) Right-click **`1_Install_Driver_PawnIO.bat`** and select **Run as administrator** to enable CPU temperature and power sensors for Intel & AMD.
3. Run **`main.exe`** (or `start_turing.bat`).

### Option 2: Run from Python Source

```bash
# Clone repository
git clone https://github.com/q20021410/Guition-Turing-Smart-Screen.git
cd Guition-Turing-Smart-Screen

# Install dependencies
pip install -r requirements.txt

# Run configuration GUI
python configure.py

# Launch system monitor
python main.py
```

---

## 📁 Program Directory Structure

```text
Guition-Turing-Smart-Screen/
 ├── main.py                       # Main application entry point
 ├── configure.py                  # Graphical theme & COM port configuration wizard
 ├── theme-editor.py               # Visual theme designer & coordinate debugger
 ├── config.yaml                   # Active user configuration (COM port, theme, sensors)
 ├── requirements.txt              # Python package dependencies
 ├── start_turing.bat              # Helper launch batch script
 ├── 1_Install_Driver_PawnIO.bat   # Microsoft-signed PawnIO driver installer
 ├── PawnIO_setup.exe              # PawnIO kernel driver installer executable
 │
 ├── library/                      # Core application modules
 │     ├── config.py               # YAML configuration loader & validator
 │     ├── stats.py                # System performance metrics orchestrator
 │     ├── scheduler.py            # Multi-threaded sensor polling scheduler
 │     ├── log.py                  # Logging handler
 │     ├── lcd/                    # Display hardware communication drivers
 │     │     ├── lcd_comm.py       # Serial protocol base abstraction
 │     │     └── lcd_comm_rev_a.py # Turing / Guition 3.5" protocol implementation
 │     └── sensors/                # Hardware sensor backends
 │           ├── sensors.py        # Base sensor interface
 │           ├── sensors_librehardwaremonitor.py # LHM (Windows Ring 0 / PawnIO)
 │           └── sensors_python.py # psutil / WMI sensor fallback
 │
 ├── res/                          # Graphical assets & themes
 │     ├── themes/                 # 73+ pre-installed themes
 │     │     ├── LandscapePastelGirl/ # Custom high-density theme
 │     │     └── LandscapeEarth/      # Classic Earth theme
 │     └── icons/                  # Application tray & window icons
 │
 ├── external/                     # Native libraries and assemblies
 │     └── LibreHardwareMonitor/   # LibreHardwareMonitorLib.dll & dependencies
 │
 ├── firmware/                     # Firmware flasher utilities & binaries
 │     ├── 0_Backup_Current_Firmware.bat # Factory flash dump backup script (0x0)
 │     ├── 1_Flash_New_Firmware.bat      # High-speed firmware flasher script (0x10000)
 │     ├── 2_Restore_Backup_Firmware.bat # Stock factory restore script (0x0)
 │     ├── new_Firmware.bin        # Pre-built 80MHz SPI DMA firmware (0x10000)
 │     └── Backup_Firmware.bin     # Stock 4MB factory flash backup (0x0)
 │
 ├── build_main.spec               # PyInstaller build spec for main.exe
 └── build_all.spec                # PyInstaller build spec for all executables
```

---

## 📚 Credits & License

- **Upstream Project**: Based on [mathoudebine/turing-smart-screen-python](https://github.com/mathoudebine/turing-smart-screen-python) by Matthieu Houdebine (GPL-3.0).
- **Firmware Repository**: [Guition-ESP32-C3-Fimrware](https://github.com/q20021410/Guition-ESP32-C3-Fimrware) powered by [LovyanGFX](https://github.com/lovyan03/LovyanGFX).
- **Hardware Sensors**: [LibreHardwareMonitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor) & [PawnIO](https://github.com/namazso/PawnIO).
- **License**: GNU General Public License v3.0 ([GPL-3.0](LICENSE)).
