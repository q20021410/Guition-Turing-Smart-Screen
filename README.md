# Guition 3.5" IPS USB-C Smart Screen - PC Monitor Software

**English** | [한국어 안내 (README_KR.md)](README_KR.md)

Open-source PC system monitor software for the **Guition 3.5" IPS USB Type-C Secondary Display** (ESP32-C3 + ST7796).

> ⚡ **Firmware Repository**: **[q20021410/Guition-ESP32-C3-Fimrware](https://github.com/q20021410/Guition-ESP32-C3-Fimrware)**  
> Looking for ESP32-C3 80MHz SPI DMA firmware source, pre-compiled `.bin` files, or Web Flasher instructions? Visit the dedicated firmware repository.
>
> 📦 **Pre-compiled Releases**: **[Download Guition.Turing.zip (v1.0.0)](https://github.com/q20021410/Guition-Turing-Smart-Screen/releases/latest)**  
> Run immediately without installing Python or any dependencies.

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
2. (First time only) Right-click **`1_Install_Driver_PawnIO.bat`** and select **Run as administrator** to enable CPU temperature and power sensors.
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

## 📂 Program Directory Structure

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
 │     ├── 1_Flash_New_Firmware.bat# One-click firmware flashing script
 │     ├── 2_Restore_Backup_Firmware.bat # Stock factory restore script
 │     ├── new_Firmware.bin        # Pre-built 80MHz SPI DMA firmware (0x10000)
 │     └── Backup_Firmware.bin     # Stock 4MB factory flash backup (0x0)
 │
 ├── build_main.spec               # PyInstaller build spec for main.exe
 └── build_all.spec                # PyInstaller build spec for all executables
```

---

## 📚 Credits & License

- **Upstream Project**: Based on [mathoudebine/turing-smart-screen-python](https://github.com/mathoudebine/turing-smart-screen-python) by Matthieu Houdebine (GPL-3.0).
- **Firmware**: [Guition-ESP32-C3-Fimrware](https://github.com/q20021410/Guition-ESP32-C3-Fimrware) powered by [LovyanGFX](https://github.com/lovyan03/LovyanGFX).
- **Hardware Sensors**: [LibreHardwareMonitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor) & [PawnIO](https://github.com/namazso/PawnIO).
- **License**: GNU General Public License v3.0 ([GPL-3.0](LICENSE)).
