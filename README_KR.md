# Guition 3.5" IPS USB-C 스마트 스크린 - 튜링 모니터 & 고속 커스텀 펌웨어

**한국어** | [English (README.md)](README.md)

**Guition 3.5인치 IPS USB Type-C 보조 모니터**를 위한 고속 커스텀 펌웨어 및 파이썬 무설치 올인원 시스템 모니터링 패키지입니다.

**80MHz SPI DMA** 하드웨어 가속 펌웨어와 단독 실행 가능한 Windows 실행 파일(`main.exe`, `configure.exe`, `theme-editor.exe`)을 통해 파이썬 설치 없이, **화면 깜빡임/밀림 현상 0%, 최신 AMD 라이젠(Zen 3 / Zen 4) 및 인텔 CPU 완벽 지원**으로 PC 하드웨어 상태를 실시간 모니터링할 수 있습니다.

> [!NOTE]
> **프로젝트 원 출처 안내 (Upstream Project)**:
> 본 패키지의 PC 시스템 모니터링 프로그램 원 출처는 **[mathoudebine/turing-smart-screen-python](https://github.com/mathoudebine/turing-smart-screen-python)** (원작자: Matthieu Houdebine) 오픈소스 프로젝트입니다. Guition 3.5인치 ESP32-C3 하드웨어 호환 및 전송 최적화를 거쳐 포터블 단독 실행 패키지로 구성되었습니다.

---

## 📷 실제 구동 사진 & 인터페이스 미리보기

<div align="center">

| 🖥️ 실시간 모니터링 구동 화면 (Landscape) | ⏳ 펌웨어 대기 화면 (Standby) |
| :---: | :---: |
| <img src="img/after.jpg" height="340" alt="실제 모니터링 구동 화면" /> | <img src="img/standby.jpg" height="340" alt="커스텀 펌웨어 대기 화면" /> |
| **실시간 시스템 모니터링 (480x320 가로 모드)**<br/><sub>AMD 라이젠 CPU 온도, 클럭, 점유율 및 RTX GPU 상태를 실시간 표시</sub> | **고속 커스텀 펌웨어 대기 모드 (320x480)**<br/><sub>ESP32-C3 80MHz SPI DMA 펌웨어 부팅 후 PC 시리얼 연결 대기 상태</sub> |

</div>

<br/>

### ⚙️ GUI 설정 마법사 (`configure.exe`)

> 별도의 복잡한 텍스트 파일 수정 없이, 그래픽 화면에서 73종 테마 썸네일을 실시간으로 미리보며 COM 포트 및 하드웨어 센서를 한눈에 제어할 수 있습니다.

<p align="center">
  <img src="img/config.png" width="85%" alt="GUI 설정 마법사 configure.exe" />
</p>

---

## ⚠️ 사용상 주의사항 및 작업 전 필수 경고

> [!CAUTION]
> ### 1. 작업 전 순정 펌웨어 백업 필수 권장 (안전장치)
> 본 배포 패키지에는 출고 순정 4MB 풀 덤프(`firmware/Backup_Firmware.bin`)가 기본 포함되어 있으나, 알리익스프레스 제조 시기 및 액정 패널 리비전에 따라 미세한 하드웨어 차이가 있을 수 있습니다.
> **따라서 새로운 펌웨어를 올리기 전에 현재 본인 기기의 4MB 펌웨어를 먼저 백업해 두는 것을 강력히 권장합니다.**
> - **원클릭 자동 백업**: Python 및 esptool 환경이 있는 경우 `firmware/0_Backup_Current_Firmware.bat` 실행
> - **esptool 수동 명령어**:
>   ```bash
>   esptool --chip esp32c3 --port COM8 --baud 921600 read_flash 0x0 0x400000 My_Original_Backup.bin
>   ```

> [!WARNING]
> ### 2. 플래싱 주소(Offset) 엄격 준수 (벽돌 방지)
> * **새 커스텀 펌웨어 (`new_Firmware.bin`)**: 반드시 **`0x10000`** 주소에 플래싱해야 합니다!
>   * *절대로 `0x0`에 쓰지 마세요. `0x0`에 덮어쓰면 ESP32-C3 부트로더 및 파티션 테이블이 손상됩니다.*
> * **순정 백업 펌웨어 복원 (`Backup_Firmware.bin`)**: 반드시 **`0x0`** 주소에 플래싱해야 합니다!
>   * *4MB 플래시 전체 덤프 파일이므로 0번지부터 덮어써야 원래대로 복원됩니다.*

> [!IMPORTANT]
> ### 3. 플래싱 전 반드시 실행 중인 모니터 프로그램 종료 (`액세스 거부 방지`)
> `main.exe`나 순정 제조사 프로그램(`GUITION Smart screen.exe`), 아두이노 IDE, 시리얼 모니터 등이 화면 포트(예: COM8)를 사용 중인 상태에서는 웹 플래셔 연결 시 `PermissionError(13, '액세스가 거부되었습니다')` 에러가 발생합니다. 플래싱 작업 전에는 모니터 프로그램을 완전히 종료하세요.

> [!NOTE]
> ### 4. 하드웨어 드라이버 설치 시 관리자 권한 및 보안
> * `1_Install_Driver_PawnIO.bat`는 반드시 우클릭 후 **[관리자 권한으로 실행]**해야 드라이버가 등록됩니다.
> * 구형 튜링 스크린 프로그램에서 사용하던 `WinRing0.sys`는 보안 취약점 차단 목록에 등록되어 윈도우에서 경고가 뜰 수 있습니다. 본 패키지에 포함된 마이크로소프트 정식 서명 **PawnIO** 드라이버만 사용하시기 바랍니다.

---

## 🛒 제품 정보 및 구매처

* **제품명**: Guition 3.5" IPS USB-C 보조 모니터 / 스마트 스크린
* **메인 컨트롤러**: ESP32-C3 (RISC-V 싱글코어 @ 160MHz, 4MB Flash)
* **디스플레이 패널**: 3.5인치 IPS LCD (320x480 해상도, ST7796S 컨트롤러)
* **연결 방식**: USB Type-C 단일 케이블 (전원 공급 + 고속 시리얼 통신)
* **구매처 링크**: [알리익스프레스 - Guition 3.5" IPS USB 보조 모니터 구매처](https://ko.aliexpress.com/item/1005006622935422.html)
* **관련 원본 이슈**: [mathoudebine/turing-smart-screen-python#426](https://github.com/mathoudebine/turing-smart-screen-python/issues/426)

---

## ✨ 핵심 특징

1. **파이썬 설치가 전혀 필요 없음 (무설치 포터블)**
   * 단독 실행 바이너리(`main.exe`, `configure.exe`, `theme-editor.exe`)가 모든 종속 라이브러리와 함께 컴파일되어 있어, 윈도우 PC에서 다운로드 후 바로 실행 가능합니다.
2. **초고속 커스텀 펌웨어 (80MHz SPI DMA + 16KB 청크 패킷 프로토콜)**
   * ESP32-C3 USB CDC 버퍼 오버플로우와 대각선 밀림/깨짐 현상을 완전히 해결했습니다.
   * 초당 2프레임 수준의 부드럽고 잔상 없는 320x480 풀프레임 그래픽 전송을 지원합니다.
3. **안전한 AMD 라이젠 & 인텔 센서 수집**
   * 마이크로소프트 정식 서명된 **PawnIO** 커널 드라이버(`v2.2.0`)와 최신 **LibreHardwareMonitorLib** 탑재.
   * 보안 취약점이 있는 구형 `WinRing0.sys` 없이 AMD 라이젠 SMU(Zen 3 5000번대, Zen 4 7000번대)와 CPU Package 온도를 안전하고 정확하게 수집합니다.
4. **73종 테마 & 편리한 GUI 설정기**
   * `configure.exe`를 통해 73종의 프리셋 테마를 실시간 미리보며 원클릭으로 변경할 수 있습니다.
   * `theme-editor.exe`로 테마 좌표와 위젯 배치를 실시간으로 시뮬레이션하고 편집할 수 있습니다.
5. **100% 안전한 순정 펌웨어 복원 지원**
   * 출고 당시의 4MB 풀 플래시 원본 덤프(`Backup_Firmware.bin`)가 함께 제공되어, 언제든지 100% 초기 공장 상태로 원복할 수 있습니다.

---

## ⚡ 빠른 시작 방법

### 1. 새 커스텀 펌웨어 설치 (최초 1회)

프로그램 설치 없이 웹 브라우저에서 바로 플래싱할 수 있습니다:

1. 크롬(Chrome) 또는 엣지(Edge) 브라우저로 **[https://esptool.spacehuhn.com/](https://esptool.spacehuhn.com/)** 에 접속합니다 (또는 `firmware/Web_Flasher_Shortcut.url` 바로가기 더블 클릭).
2. **[Connect]**를 클릭하고 화면 장치 포트(예: `COM8` / `USB JTAG/serial debug unit`)를 선택합니다.
3. 파일 및 주소(Offset) 설정:
   * **파일**: `firmware/new_Firmware.bin` 선택
   * **Offset**: `0x10000` 입력 *(주의: 반드시 0x10000 입력)*
4. **[Program]** 버튼을 누르면 업로드가 시작됩니다.
5. 100% 완료 후 USB 케이블을 분리했다가 다시 연결하면 검은색 대기 화면이 표시됩니다!

*(참고: PC에 파이썬 및 esptool이 구성되어 있는 경우 `firmware/1_Flash_New_Firmware.bat`를 더블 클릭해도 됩니다)*

### 2. 센서 드라이버 설치 (최초 1회)

1. **`1_Install_Driver_PawnIO.bat`** 파일을 우클릭하여 **[관리자 권한으로 실행]**합니다.
2. 서명된 PawnIO 드라이버가 등록되어 라이젠 CPU 온도를 안전하게 읽어올 수 있게 됩니다.

### 3. 시스템 모니터 실행

* **`start_turing.bat`** (또는 `main.exe`)를 더블 클릭합니다.
* 모니터 프로그램이 화면에 즉시 연결되며 실시간 시스템 정보 표시가 시작됩니다!

---

## 🎨 테마 및 환경설정

### GUI 설정 마법사 (`configure.exe`)
`configure.exe`를 실행하여 직관적으로 설정을 제어할 수 있습니다:
* 73종 테마 썸네일 미리보기 및 선택
* COM 포트 변경 및 센서 제공자 선택
* **[Save]** 또는 **[Save & Run]** 클릭으로 즉시 적용

### 실시간 테마 에디터 (`theme-editor.exe`)
* `theme-editor.exe`를 더블 클릭하면 현재 설정된 테마의 시뮬레이터 창이 열립니다.
* 마우스 드래그로 위젯 좌표를 확인하고, `theme.yaml`을 수정하면 저장 즉시 화면이 자동 갱신됩니다.

### 설정 파일 직접 수정 (`config.yaml`)
메모장으로 `config.yaml`을 직접 편집할 수도 있습니다:
```yaml
config:
  COM_PORT: COM8          # 화면이 연결된 포트 번호
  THEME: LandscapeEarth   # 테마 폴더명 지정
  HW_SENSORS: LHM         # 센서 제공자 (LHM 권장)
```

---

## 🔄 공장 순정 펌웨어 복원 (원복)

기기를 초기 출고 순정 상태로 되돌리고 싶은 경우:
1. 크롬/엣지 브라우저로 **[https://esptool.spacehuhn.com/](https://esptool.spacehuhn.com/)** 접속
2. **[Connect]** 클릭 후 포트 연결
3. 파일 및 주소 설정:
   * **파일**: `firmware/Backup_Firmware.bin`
   * **Offset**: `0x0` *(주의: 4MB 풀 덤프이므로 반드시 0x0 입력)*
4. **[Program]** 클릭 -> 100% 완료 시 초기 순정 상태로 100% 복원됩니다.

---

## 📁 폴더 구조 안내

```text
Guition Turing/
 ├── start_turing.bat              # 모니터 실행용 배치파일
 ├── main.exe                      # 시스템 모니터 메인 실행 파일
 ├── configure.exe                 # 테마 선택 및 GUI 설정 마법사
 ├── theme-editor.exe              # 실시간 테마 시뮬레이터 및 편집기
 ├── 1_Install_Driver_PawnIO.bat   # 센서 드라이버 원클릭 설치기
 ├── PawnIO_setup.exe              # 서명된 PawnIO 드라이버 설치 파일
 ├── config.yaml                   # 환경 설정 파일
 ├── README.md                     # 영문 안내문 (English)
 ├── README_KR.md                  # 한글 안내문 (Korean)
 │
 ├── firmware/                     # 펌웨어 및 웹 플래셔 가이드
 │     ├── 0_Backup_Current_Firmware.bat # 1클릭 순정 백업 스크립트 (0x0)
 │     ├── 1_Flash_New_Firmware.bat# 자동 플래시 스크립트 (0x10000)
 │     ├── 2_Restore_Backup_Firmware.bat # 순정 복원 스크립트 (0x0)
 │     ├── new_Firmware.bin        # 80MHz SPI DMA 고속 펌웨어 (0x10000)
 │     ├── Backup_Firmware.bin     # 출고 순정 4MB 풀 덤프 백업본 (0x0)
 │     ├── Web_Flasher_Shortcut.url# 웹 플래셔 무설치 바로가기
 │     └── README_Firmware_Guide.txt# 펌웨어 상세 설명서
 │
 ├── img/                          # 실제 구동 사진 및 스크린샷
 ├── res/                          # 73종 테마, 배경, 폰트, 아이콘 리소스
 ├── external/                     # LibreHardwareMonitor 센서 라이브러리
 └── _internal/                    # 독립 실행형 내장 런타임
```

---

## 📚 사용 라이브러리 및 오픈소스 출처 (Credits)

본 프로젝트는 아래의 훌륭한 오픈소스 프로젝트, 라이브러리 및 도구들을 기반으로 개발되었습니다:

### 1. 원작 프로젝트 및 임베디드 펌웨어
| 구성 요소 | 제작자 / 프로젝트 링크 | 역할 및 설명 | 라이선스 |
| :--- | :--- | :--- | :--- |
| **turing-smart-screen-python** | [@mathoudebine](https://github.com/mathoudebine/turing-smart-screen-python) | 파이썬 시스템 모니터 아키텍처 및 73종 테마 렌더링 엔진 | GPL-3.0 |
| **LovyanGFX** | [@lovyan03](https://github.com/lovyan03/LovyanGFX) | ESP32-C3 80MHz 고속 SPI DMA 디스플레이 드라이버 라이브러리 | FreeBSD / BSD |
| **Arduino-ESP32** | [Espressif Systems](https://github.com/espressif/arduino-esp32) | ESP32-C3용 공식 아두이노 프레임워크 코어 | LGPL-2.1 |
| **PlatformIO** | [PlatformIO Labs](https://platformio.org/) | 임베디드 펌웨어 빌드 및 크로스 컴파일 프레임워크 | Apache-2.0 |
| **ESPTool & Web Flasher** | [Espressif](https://github.com/espressif/esptool) & [@Spacehuhn](https://esptool.spacehuhn.com/) | 크롬/엣지 웹 브라우저 무설치 시리얼 플래셔 도구 | GPL-2.0 / MIT |

### 2. 하드웨어 센서 & 커널 드라이버 아키텍처
| 구성 요소 | 제작자 / 프로젝트 링크 | 역할 및 설명 | 라이선스 |
| :--- | :--- | :--- | :--- |
| **PawnIO** | [@namazso](https://github.com/namazso/PawnIO) | 취약한 `WinRing0.sys`를 대체하는 MS 정식 서명된 드라이버 (라이젠 SMU/온도 접근) | GPL-3.0 |
| **LibreHardwareMonitor** | [LibreHardwareMonitor Team](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor) | Windows 하드웨어 센서(CPU, GPU, RAM, 디스크, 메인보드) 수집 라이브러리 | MPL-2.0 |
| **pythonnet** | [Python.NET Community](https://github.com/pythonnet/pythonnet) | 파이썬에서 C# .NET CLR 어셈블리를 직접 호출하는 브릿지 | MIT |

### 3. 그래픽 렌더링 및 GUI 환경
| 구성 요소 | 제작자 / 프로젝트 링크 | 역할 및 설명 | 라이선스 |
| :--- | :--- | :--- | :--- |
| **Pillow (PIL)** | [Alex Clark & Pillow Contributors](https://github.com/python-pillow/Pillow) | 폰트 래스터라이징, 게이지 바 생성, 비트맵 이미지 처리 엔진 | HPND |
| **sv-ttk** | [@rdbende](https://github.com/rdbende/Sun-Valley-ttk-theme) | Tkinter용 Sun Valley 현대적인 Windows 11 플루언트 다크/라이트 테마 | MIT |
| **tkinter-tooltip** | [@rdbende](https://github.com/rdbende/tkinter-tooltip) | GUI 설정창 내 마우스 호버 도움말 툴팁 위젯 | MIT |
| **darkdetect** | [@albertosottile](https://github.com/albertosottile/darkdetect) | 윈도우 OS 다크/라이트 모드 자동 감지 라이브러리 | BSD-3-Clause |
| **pystray** | [@moses-palmer](https://github.com/moses-palmer) | 윈도우 시스템 트레이 아이콘 및 백그라운드 최소화 구동 | LGPL-3.0 |

### 4. 시스템 유틸리티, 통신 및 패키징
| 구성 요소 | 제작자 / 프로젝트 링크 | 역할 및 설명 | 라이선스 |
| :--- | :--- | :--- | :--- |
| **psutil** | [@giampaolo](https://github.com/giampaolo/psutil) | 크로스 플랫폼 프로세스 및 하드웨어 지표(CPU 로드, 메모리, 네트워크 트래픽) | BSD-3-Clause |
| **pyserial** | [pySerial Team](https://github.com/pyserial/pyserial) | 화면 장치와의 고속 USB CDC 시리얼 통신 계층 | BSD-3-Clause |
| **pywin32** | [@mhammond](https://github.com/mhammond/pywin32) | Windows Win32 API 바인딩 (관리자 권한 상승, 프로세스 관리) | PSF |
| **Babel** | [Babel Team](https://github.com/python-babel/babel) | 국가별 로케일 기반 날짜 및 시각 국제화 포맷터 | BSD-3-Clause |
| **ruamel.yaml / PyYAML** | [YAML Community](https://yaml.readthedocs.io/) | 테마 및 설정 파일용 YAML 파서 및 직렬화 엔진 | MIT |
| **ping3** | [@kyan001](https://github.com/kyan001/ping3) | 네트워크 핑 지연시간(Latency) 측정 ICMP 유틸리티 | MIT |
| **PyInstaller** | [PyInstaller Development Team](https://github.com/pyinstaller/pyinstaller) | 파이썬 무설치 독립 실행형 바이너리 컴파일러 | GPL-2.0 |

---

## ⚖️ License

* 본 프로젝트의 클라이언트 코드 및 모니터 프로그램은 [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html) 라이선스를 따릅니다.
* 테마, 폰트, 외부 라이브러리는 각각의 고유 라이선스를 유지합니다.
