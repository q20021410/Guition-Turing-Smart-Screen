================================================================================
   Guition 3.5" (ESP32-C3) Firmware Guide / 펌웨어 가이드
================================================================================

================================================================================
 [KR] 한국어 안내
================================================================================

1. 개요
   이 폴더에는 Guition 3.5인치 화면용 커스텀 고속 펌웨어와 순정 공장 백업 펌웨어가 들어있습니다.
   별도의 프로그램 설치 없이 크롬(Chrome) 또는 엣지(Edge) 웹 브라우저에서 바로 플래싱할 수 있습니다.

2. 웹 플래셔(Web Flasher) 주소
   - 링크: https://esptool.spacehuhn.com/
   - 또는 이 폴더의 'Web_Flasher_Shortcut.url' 바로가기를 더블 클릭하세요.

3. 새 커스텀 펌웨어 설치 (권장)
   - 파일: 'new_Firmware.bin'
   - 오프셋(Offset): 0x10000  <-- [중요] 반드시 0x10000 입력!
   - 주요 특징:
     * 80MHz SPI DMA 전송 (화면 깜빡임, 밀림 및 지연 완전 해결)
     * 16KB 청크 패킷 분할 전송 (USB CDC 버퍼 오버플로우 방지 및 이미지 깨짐 해결)

   [웹 플래셔 업로드 방법]
   ① 크롬 또는 엣지 브라우저로 https://esptool.spacehuhn.com/ 접속합니다.
   ② [Connect] 버튼을 클릭하고 화면 장치(예: COM8 / USB JTAG/serial debug unit)를 선택합니다.
   ③ 파일 및 주소(Offset) 설정:
      - [Choose File] 클릭 -> 'new_Firmware.bin' 파일 선택
      - Offset 입력란에 '0x10000' 입력 (0이 4개)
   ④ [Program] 버튼을 클릭하여 플래싱을 시작합니다.
   ⑤ 100% 완료 후 USB 케이블을 분리했다가 다시 연결하거나 화면 뒷면 리셋 버튼을 누릅니다.

4. 순정 공장 펌웨어 복원 (원복용)
   - 파일: 'Backup_Firmware.bin'
   - 오프셋(Offset): 0x0  <-- [중요] 4MB 전체 덤프이므로 반드시 0x0 입력!
   - 설명: 제품 출고 시점의 4MB 전체 플래시 원본 백업본입니다.

   [웹 플래셔 복원 방법]
   ① https://esptool.spacehuhn.com/ 접속 후 [Connect] 클릭
   ② [Choose File] 클릭 -> 'Backup_Firmware.bin' 파일 선택
   ③ Offset 입력란에 '0x0' 입력
   ④ [Program] 버튼 클릭 -> 100% 완료 시 공장 출고 순정 상태로 원상복구됩니다.

5. 배치파일을 이용한 커맨드라인 플래시 (Python 환경 사용자용)
   PC에 Python 및 esptool이 설치되어 있는 경우 아래 배치파일을 더블 클릭하여 바로 실행할 수 있습니다:
   - '0_Backup_Current_Firmware.bat'   : [권장] 작업 전 현재 기기 4MB 펌웨어 1클릭 백업
   - '1_Flash_New_Firmware.bat'        : 새 고속 펌웨어 자동 플래시 (0x10000)
   - '2_Restore_Backup_Firmware.bat'   : 순정 백업 자동 복원 (0x0)

6. 작업 전 필수 주의사항 및 경고 (안전 가이드)
   - [필수 백업] 알리익스프레스 생산 배치별 미세 하드웨어 차이에 대비해 작업 전 본인 기기의 4MB 펌웨어를 먼저 백업해두세요.
   - [오프셋 주소 준수]
     * 새 펌웨어('new_Firmware.bin')는 반드시 '0x10000' (0이 4개)에 올려야 합니다. (0x0에 쓰면 부트로더 손상)
     * 순정 복원('Backup_Firmware.bin')은 반드시 '0x0'에 올려야 합니다.
   - [프로그램 종료] 'main.exe'나 제조사 프로그램이 켜져 있으면 '액세스 거부(PermissionError 13)'가 발생하므로 플래싱 전 반드시 종료하세요.
   - [케이블 분리 금지] 플래싱 진행 중에는 USB 케이블을 뽑지 마세요.


================================================================================
 [EN] English Guide
================================================================================

1. Overview
   This folder contains custom high-speed firmware and original factory backup firmware for Guition 3.5" display.
   You can flash firmware directly via Google Chrome or Microsoft Edge browser without installing any software.

2. Web Flasher URL
   - Link: https://esptool.spacehuhn.com/
   - Or double-click 'Web_Flasher_Shortcut.url' in this folder.

3. Flash Custom High-Speed Firmware (Recommended)
   - File: 'new_Firmware.bin'
   - Offset: 0x10000  <-- [IMPORTANT] Must enter 0x10000!
   - Features:
     * 80MHz SPI DMA high-speed transfer (zero tearing and low latency)
     * 16KB chunk packet protocol (prevents USB CDC buffer overflow and glitched rendering)

   [Web Flasher Steps]
   1. Open https://esptool.spacehuhn.com/ in Google Chrome or Microsoft Edge.
   2. Click [Connect] and select your display device (e.g. COM8 / USB JTAG/serial debug unit).
   3. Configure file and offset:
      - Click [Choose File] -> Select 'new_Firmware.bin'
      - In the Offset box, type: 0x10000
   4. Click [Program] to begin flashing.
   5. Once 100% complete, unplug and re-plug the USB-C cable or press the reset button on the back of the screen.

4. Restore Factory Backup Firmware (Stock Restore)
   - File: 'Backup_Firmware.bin'
   - Offset: 0x0  <-- [IMPORTANT] Full 4MB dump, must enter 0x0!
   - Features:
     * Complete 4MB raw flash dump extracted directly from factory state.

   [Web Flasher Steps]
   1. Open https://esptool.spacehuhn.com/ and click [Connect].
   2. Click [Choose File] -> Select 'Backup_Firmware.bin'
   3. In the Offset box, type: 0x0
   4. Click [Program]. Once 100% complete, the display is restored to factory stock firmware.

5. Command Line Batch Flasher (For Python Users)
   If your PC has Python and esptool installed, you can simply double-click the batch files:
   - '0_Backup_Current_Firmware.bat'   : [Recommended] 1-Click 4MB raw backup of current firmware (0x0)
   - '1_Flash_New_Firmware.bat'        : Flash custom firmware (0x10000)
   - '2_Restore_Backup_Firmware.bat'   : Restore factory backup (0x0)

6. Important Precautions & Safety Warnings
   - [Always Backup First] To guard against hardware variations between AliExpress batches, back up your original 4MB firmware before flashing.
   - [Strictly Observe Offsets]
     * New custom firmware ('new_Firmware.bin') must be flashed at '0x10000' (DO NOT flash at 0x0).
     * Factory stock restore ('Backup_Firmware.bin') must be flashed at '0x0'.
   - [Quit Monitor Programs] Close 'main.exe', vendor apps, or serial monitors before flashing to avoid 'PermissionError 13 (Access denied)'.
   - [Do Not Disconnect] Never unplug the USB cable while flashing is in progress.
