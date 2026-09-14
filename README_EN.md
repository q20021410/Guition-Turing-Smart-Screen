# Guition 3.5" IPS USB-C Smart Screen - Turing Monitor & Custom Firmware

**English** | [한국어 안내 (README_KR.md)](README_KR.md)

A standalone, portable system monitoring package and high-speed custom firmware for the **Guition 3.5" IPS USB Type-C Secondary Display**.

Powered by an **80MHz SPI DMA** custom firmware and pre-compiled Windows binaries, this package lets you monitor CPU, GPU, RAM, temperatures, power draw, and network stats with **zero screen tearing, zero Python dependencies, and full support for both Intel Core & AMD Ryzen (Zen 3 / Zen 4) CPUs**.

> [!NOTE]
> **Upstream Project & Source**:
> The PC system monitoring client in this project is based on the open-source project **[mathoudebine/turing-smart-screen-python](https://github.com/mathoudebine/turing-smart-screen-python)** by Matthieu Houdebine. It has been refactored and packaged to work seamlessly with the Guition 3.5" ESP32-C3 hardware and high-speed custom firmware.
>
> **Dedicated Firmware Repository**:
> Custom ESP32-C3 firmware source and pre-built binaries are hosted at **[q20021410/Guition-ESP32-C3-Fimrware](https://github.com/q20021410/Guition-ESP32-C3-Fimrware)**.

---

## 📷 Screenshots & Hardware Showcase

<div align="center">

| 🖥️ Live Monitoring in Action (Landscape) | ⏳ Custom Firmware Standby Screen |
| :---: | :---: |
| <img src="img/after.jpg" height="340" alt="Guition 3.5 Monitor in Action" /> | <img src="img/standby.jpg" height="340" alt="Custom Firmware Standby Screen" /> |
| **Real-Time System Monitoring (480x320 Landscape)**<br/><sub>Live CPU Package temp, clock, usage & RTX GPU metrics</sub> | **80MHz Custom Firmware Standby (320x480)**<br/><sub>ESP32-C3 SPI DMA firmware booted and awaiting PC serial connection</sub> |

</div>

<br/>

### ⚙️ GUI Configuration Wizard (`configure.exe`)

> Easily preview all 73 pre-installed themes with real-time thumbnails and configure your active COM port and sensor options in a modern fluent interface.

<p align="center">
  <img src="img/config.png" width="85%" alt="GUI Configuration Wizard" />
</p>

---

## ⚠️ Important Precautions & Pre-Flashing Warnings

> [!CAUTION]
> ### 1. Backup Your Original Factory Firmware First!
> While this repository includes a clean 4MB factory flash dump (`firmware/Backup_Firmware.bin`), manufacturing batches or LCD revisions from AliExpress sellers may occasionally vary.
> **We strongly recommend backing up your own device's factory flash (4MB) before flashing new firmware!**
> - **1-Click Auto Backup**: If Python & esptool are installed, simply double-click `firmware/0_Backup_Current_Firmware.bat`.
> - **Manual Command**:
>   ```bash
>   esptool --chip esp32c3 --port COM8 --baud 921600 read_flash 0x0 0x400000 My_Original_Backup.bin
>   ```

> [!WARNING]
> ### 2. Strictly Follow Flash Offset Addresses (Prevent Bricking)
> * **New Custom Firmware (`new_Firmware.bin`)**: Must be flashed at offset **`0x10000`**!
>   * *Never flash `new_Firmware.bin` at `0x0`, as that would overwrite the ESP32-C3 bootloader and partition tables.*
> * **Factory Restore Image (`Backup_Firmware.bin`)**: Must be flashed at offset **`0x0`**!
>   * *Because it is a full 4MB raw dump of the entire flash.*

> [!IMPORTANT]
> ### 3. Close All Serial Monitor Programs Before Flashing (Avoid Access Denied)
> If `main.exe`, `GUITION Smart screen.exe`, Arduino IDE, or a serial monitor is currently running on the display's COM port, the flasher will fail with `PermissionError 13 (Access is denied)`. Always quit any monitoring software before flashing.

> [!NOTE]
> ### 4. Driver Privileges & Security (Intel & AMD)
> * Right-click `1_Install_Driver_PawnIO.bat` and select **[Run as administrator]** once.
> * Avoid older Turing screen packages using vulnerable drivers (`WinRing0.sys`). This project uses the Microsoft-signed **PawnIO** driver (`v2.2.0`), which is fully compatible with Windows 10/11 Core Isolation and Memory Integrity (HVCI) for both **Intel** and **AMD** CPUs.

---

## 🛒 Product Information & Purchase Link

* **Device**: Guition 3.5" IPS USB-C Secondary Monitor / Smart Screen
* **Controller**: ESP32-C3 (RISC-V single-core @ 160MHz, 4MB Flash)
* **Display Panel**: 3.5-inch IPS LCD (320x480 resolution, ST7796S driver)
* **Connectivity**: Single USB Type-C cable (Power + High-speed Serial)
* **Purchase Link**: [AliExpress - Guition 3.5" IPS USB Secondary Screen](https://aliexpress.com/item/1005006622935422.html)
* **Upstream Issue**: [mathoudebine/turing-smart-screen-python#426](https://github.com/mathoudebine/turing-smart-screen-python/issues/426)

---

## ✨ Key Features

1. **No Python Required (Portable Standalone)**
   * Pre-compiled standalone binaries (`main.exe`, `configure.exe`, `theme-editor.exe`) are bundled with all dependencies. Works out of the box on any Windows 10/11 PC.
2. **High-Speed Custom Firmware (80MHz SPI DMA + 16KB Chunking)**
   * Eliminates USB CDC buffer overflow and diagonal tearing glitches.
   * Delivers smooth, artifact-free 320x480 full-frame rendering.
3. **Safe Intel & AMD Hardware Monitoring via PawnIO**
   * Uses the Microsoft-signed **PawnIO** driver (`v2.2.0`) and updated **LibreHardwareMonitorLib**.
   * Reliably reads Intel Core & AMD Ryzen (Zen 3 5000 series, Zen 4 7000 series) CPU Package temperatures and power draw (W) under Windows 11 HVCI.
4. **73+ Themes & New High-Density Theme (`LandscapePastelGirl`)**
   * Non-intrusive left-side layout preserving character illustration.
   * Real-time CPU & GPU Power draw (W).
   * Real-time Network upload/download speed with directional arrows (▼ / ▲).
   * Accurate C: drive storage gauge (Total, Used, Free).
5. **GUI Configuration & Live Theme Editor**
   * Graphical settings wizard (`configure.exe`) with real-time theme previews.
   * Interactive theme editor (`theme-editor.exe`) with visual zone positioning and coordinate debugging.
6. **100% Reversible Factory Restore**
   * Includes the original 4MB full raw flash dump (`Backup_Firmware.bin`). You can restore the factory stock firmware at any time.

---

## ⚡ Quick Start

### 1. Flash Custom Firmware (One-time only)

You can flash the firmware directly inside your web browser without installing any tools:

1. Open the Web Flasher: **[https://esptool.spacehuhn.com/](https://esptool.spacehuhn.com/)** in Google Chrome or Microsoft Edge (or double-click `firmware/Web_Flasher_Shortcut.url`).
2. Click **[Connect]** and select your display device port (e.g. `COM8` / `USB JTAG/serial debug unit`).
3. Set File and Offset:
   * **File**: Select `firmware/new_Firmware.bin`
   * **Offset**: `0x10000` *(IMPORTANT: Must be 0x10000)*
4. Click **[Program]**.
5. Once 100% complete, unplug and reconnect the USB-C cable. The display will show the clean black standby screen!

*(Alternative: If you have Python & esptool installed, double-click `firmware/1_Flash_New_Firmware.bat`)*

### 2. Install Hardware Sensor Driver (First time only - Intel & AMD)

1. Right-click **`1_Install_Driver_PawnIO.bat`** and select **[Run as administrator]**.
2. This registers the signed PawnIO kernel driver, unlocking direct Intel and AMD Ryzen CPU temperature, power (W), and clock sensors under Windows 10/11.

### 3. Start System Monitoring

* Double-click **`main.exe`** (or `start_turing.bat`).
* The monitor connects to the screen immediately and begins real-time performance display!

---

## 🎨 Theme & Setting Customization

### GUI Wizard (`configure.exe`)
Double-click `configure.exe` to launch the graphical configuration wizard:
* Preview 73 pre-installed themes.
* Select active COM port and hardware sensor provider.
* Click **[Save]** or **[Save & Run]**.

### Live Theme Editor (`theme-editor.exe`)
* Double-click `theme-editor.exe` to open the real-time simulator.
* Displays live coordinates when clicking or dragging on the screen preview.

---

## 📂 Project Structure

```text
Guition-Turing-Smart-Screen/
 ├── main.exe                      # Standalone system monitor engine
 ├── configure.exe                 # Graphical theme & COM port configuration wizard
 ├── theme-editor.exe              # Visual theme editor & coordinate debugger
 ├── start_turing.bat              # Helper launch batch file
 ├── 1_Install_Driver_PawnIO.bat   # PawnIO kernel driver installer (Run as Admin)
 ├── config.yaml                   # Active configuration file
 ├── PawnIO_setup.exe              # Microsoft-signed PawnIO kernel driver installer
 │
 ├── firmware/                     # Firmware tools & pre-built binaries
 │     ├── 0_Backup_Current_Firmware.bat # Factory flash dump backup script (0x0)
 │     ├── 1_Flash_New_Firmware.bat      # High-speed firmware flasher script (0x10000)
 │     ├── 2_Restore_Backup_Firmware.bat # Factory stock restore script (0x0)
 │     ├── new_Firmware.bin        # 80MHz SPI DMA custom firmware binary (0x10000)
 │     ├── Backup_Firmware.bin     # Original 4MB factory raw flash backup (0x0)
 │     ├── Web_Flasher_Shortcut.url# Web flasher browser shortcut
 │     └── README_Firmware_Guide.txt# Detailed firmware guide
 │
 ├── img/                          # Screenshots and preview photos
 ├── res/                          # 73 themes, backgrounds, fonts, and icons
 ├── external/                     # LibreHardwareMonitor DLL libraries
 └── _internal/                    # Standalone compiled runtime environment
```

---

## 📚 Libraries & Third-Party Credits

This project builds upon and integrates several outstanding open-source projects, libraries, and tools:

### 1. Upstream Project & Firmware Base
| Component | Author / Source | Role & Description | License |
| :--- | :--- | :--- | :--- |
| **turing-smart-screen-python** | [@mathoudebine](https://github.com/mathoudebine/turing-smart-screen-python) | Base Python system monitor architecture and theme engine | GPL-3.0 |
| **LovyanGFX** | [@lovyan03](https://github.com/lovyan03/LovyanGFX) | Ultra-fast SPI/DMA graphics library used for 80MHz ESP32-C3 rendering | FreeBSD / BSD |
| **Arduino-ESP32** | [Espressif Systems](https://github.com/espressif/arduino-esp32) | Official Arduino core for ESP32-C3 microcontroller | LGPL-2.1 |
| **PlatformIO** | [PlatformIO Labs](https://platformio.org/) | Embedded build and firmware compilation framework | Apache-2.0 |
| **ESPTool & Web Flasher** | [Espressif](https://github.com/espressif/esptool) & [@Spacehuhn](https://esptool.spacehuhn.com/) | Chrome/Edge browser-based WebSerial firmware flashing tool | GPL-2.0 / MIT |

### 2. Hardware Sensors & Driver Architecture
| Component | Author / Source | Role & Description | License |
| :--- | :--- | :--- | :--- |
| **PawnIO** | [@namazso](https://github.com/namazso/PawnIO) | Microsoft-signed kernel driver replacing vulnerable `WinRing0.sys` for secure Intel/AMD sensor access | GPL-3.0 |
| **LibreHardwareMonitor** | [LibreHardwareMonitor Team](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor) | Core Windows sensor library for CPU, GPU, RAM, disk, and motherboard monitoring | MPL-2.0 |
| **pythonnet** | [Python.NET Community](https://github.com/pythonnet/pythonnet) | C# .NET CLR runtime bridge enabling Python to call LibreHardwareMonitorLib | MIT |

### 3. Graphical Interface & Theming
| Component | Author / Source | Role & Description | License |
| :--- | :--- | :--- | :--- |
| **Pillow (PIL)** | [Alex Clark & Pillow Contributors](https://github.com/python-pillow/Pillow) | High-performance bitmap generation, font rasterization, and image processing | HPND |
| **sv-ttk** | [@rdbende](https://github.com/rdbende/Sun-Valley-ttk-theme) | Sun Valley modern Windows 11 fluent dark/light theme for Tkinter | MIT |
| **tkinter-tooltip** | [@rdbende](https://github.com/rdbende/tkinter-tooltip) | Interactive mouse hover tooltip widgets for configuration GUI | MIT |
| **darkdetect** | [@albertosottile](https://github.com/albertosottile/darkdetect) | Automatic OS light/dark mode detection on Windows | BSD-3-Clause |
| **pystray** | [@moses-palmer](https://github.com/moses-palmer) | System tray icon and background minimized operation | LGPL-3.0 |

### 4. Utilities, Serialization & Packaging
| Component | Author / Source | Role & Description | License |
| :--- | :--- | :--- | :--- |
| **psutil** | [@giampaolo](https://github.com/giampaolo/psutil) | Cross-platform hardware metrics (CPU load, memory, disk, network throughput) | BSD-3-Clause |
| **pyserial** | [pySerial Team](https://github.com/pyserial/pyserial) | USB CDC serial communication layer with display | BSD-3-Clause |
| **pywin32** | [@mhammond](https://github.com/mhammond/pywin32) | Windows API integration, UAC administrative privilege elevation, and process handling | PSF |
| **Babel** | [Babel Team](https://github.com/python-babel/babel) | Localized international date and time formatting | BSD-3-Clause |
| **ruamel.yaml / PyYAML** | [YAML Community](https://yaml.readthedocs.io/) | Parsing and preserving YAML theme files and configuration | MIT |
| **ping3** | [@kyan001](https://github.com/kyan001/ping3) | ICMP ping latency monitor | MIT |
| **PyInstaller** | [PyInstaller Development Team](https://github.com/pyinstaller/pyinstaller) | Standalone Windows executable packager | GPL-2.0 |

---

## ⚖️ License

* Client scripts and monitor application are distributed under the [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html).
* Theme assets, fonts, and third-party libraries retain their respective licenses as detailed above.
