# SPDX-License-Identifier: GPL-3.0-or-later
#
# turing-smart-screen-python - a Python system monitor and library for USB-C displays like Turing Smart Screen or XuanFang
# https://github.com/mathoudebine/turing-smart-screen-python/
#
# Copyright (C) 2021 Matthieu Houdebine (mathoudebine)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# This file will use LibreHardwareMonitor.dll library to get hardware sensors
# Some metrics are still fetched by psutil when not available on LibreHardwareMonitor
# For Windows platforms only

import ctypes
import math
import os
import sys
import time
from statistics import mean
from typing import Tuple

import clr  # Clr is from pythonnet package. Do not install clr package
import psutil
from win32api import *

import library.sensors.sensors as sensors
from library.log import logger

# Import LibreHardwareMonitor dll to Python
if getattr(sys, 'frozen', False):
    _base_dir = os.path.dirname(sys.executable)
else:
    _base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

lhm_dir = os.path.join(_base_dir, 'external', 'LibreHardwareMonitor')
if not os.path.exists(lhm_dir):
    lhm_dir = os.path.join(os.getcwd(), 'external', 'LibreHardwareMonitor')

lhm_dll = os.path.join(lhm_dir, 'LibreHardwareMonitorLib.dll')
clr.AddReference(lhm_dll)
clr.AddReference(os.path.join(lhm_dir, 'HidSharp.dll'))
# noinspection PyUnresolvedReferences
from LibreHardwareMonitor import Hardware

File_information = GetFileVersionInfo(lhm_dll, "\\")

ms_file_version = File_information['FileVersionMS']
ls_file_version = File_information['FileVersionLS']

logger.debug("Found LibreHardwareMonitorLib %s" % ".".join([str(HIWORD(ms_file_version)), str(LOWORD(ms_file_version)),
                                                            str(HIWORD(ls_file_version)),
                                                            str(LOWORD(ls_file_version))]))

if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    logger.warning("Program is not running as administrator. Run as administrator to enable full CPU temperature readings.")

handle = Hardware.Computer()
handle.IsCpuEnabled = True
handle.IsGpuEnabled = True
handle.IsMemoryEnabled = True
handle.IsMotherboardEnabled = True  # For CPU Fan Speed
handle.IsControllerEnabled = True  # For CPU Fan Speed
handle.IsNetworkEnabled = True
handle.IsStorageEnabled = False
handle.IsPsuEnabled = False
handle.Open()
for hardware in handle.Hardware:
    if hardware.HardwareType == Hardware.HardwareType.Cpu:
        logger.info("Found CPU: %s" % hardware.Name)
    elif hardware.HardwareType == Hardware.HardwareType.Memory:
        logger.info("Found Memory: %s" % hardware.Name)
    elif hardware.HardwareType == Hardware.HardwareType.GpuNvidia:
        logger.info("Found Nvidia GPU: %s" % hardware.Name)
    elif hardware.HardwareType == Hardware.HardwareType.GpuAmd:
        logger.info("Found AMD GPU: %s" % hardware.Name)
    elif hardware.HardwareType == Hardware.HardwareType.GpuIntel:
        logger.info("Found Intel GPU: %s" % hardware.Name)
    elif hardware.HardwareType == Hardware.HardwareType.Storage:
        logger.info("Found Storage: %s" % hardware.Name)
    elif hardware.HardwareType == Hardware.HardwareType.Network:
        logger.info("Found Network interface: %s" % hardware.Name)


def get_hw_and_update(hwtype: Hardware.HardwareType, name: str = None) -> Hardware.Hardware:
    for hardware in handle.Hardware:
        if hardware.HardwareType == hwtype:
            if (name and hardware.Name == name) or name is None:
                hardware.Update()
                return hardware
    return None


def get_gpu_name() -> str:
    # Determine which GPU to use, in case there are multiple : try to avoid using discrete GPU for stats
    hw_gpus = []
    for hardware in handle.Hardware:
        if hardware.HardwareType == Hardware.HardwareType.GpuNvidia \
                or hardware.HardwareType == Hardware.HardwareType.GpuAmd \
                or hardware.HardwareType == Hardware.HardwareType.GpuIntel:
            hw_gpus.append(hardware)

    if len(hw_gpus) == 0:
        # No supported GPU found on the system
        logger.warning("No supported GPU found")
        return ""
    elif len(hw_gpus) == 1:
        # Found one supported GPU
        logger.debug("Found one supported GPU: %s" % hw_gpus[0].Name)
        return str(hw_gpus[0].Name)
    else:
        # Found multiple GPUs, try to determine which one to use
        amd_gpus = 0
        intel_gpus = 0
        nvidia_gpus = 0

        gpu_to_use = ""

        # Count GPUs by manufacturer
        for gpu in hw_gpus:
            if gpu.HardwareType == Hardware.HardwareType.GpuAmd:
                amd_gpus += 1
            elif gpu.HardwareType == Hardware.HardwareType.GpuIntel:
                intel_gpus += 1
            elif gpu.HardwareType == Hardware.HardwareType.GpuNvidia:
                nvidia_gpus += 1

        logger.warning(
            "Found %d GPUs on your system (%d AMD / %d Nvidia / %d Intel). Auto identify which GPU to use." % (
                len(hw_gpus), amd_gpus, nvidia_gpus, intel_gpus))

        if nvidia_gpus >= 1:
            # One (or more) Nvidia GPU: use first available for stats
            gpu_to_use = get_hw_and_update(Hardware.HardwareType.GpuNvidia).Name
        elif amd_gpus == 1:
            # No Nvidia GPU, only one AMD GPU: use it
            gpu_to_use = get_hw_and_update(Hardware.HardwareType.GpuAmd).Name
        elif amd_gpus > 1:
            # No Nvidia GPU, several AMD GPUs found: try to use the real GPU but not the APU integrated in CPU
            for gpu in hw_gpus:
                if gpu.HardwareType == Hardware.HardwareType.GpuAmd:
                    for sensor in gpu.Sensors:
                        if sensor.SensorType == Hardware.SensorType.Load and str(sensor.Name).startswith("GPU Core"):
                            # Found load sensor for this GPU: assume it is main GPU and use it for stats
                            gpu_to_use = gpu.Name
        else:
            # No AMD or Nvidia GPU: there are several Intel GPUs, use first available for stats
            gpu_to_use = get_hw_and_update(Hardware.HardwareType.GpuIntel).Name

        if gpu_to_use:
            logger.debug("This GPU will be used for stats: %s" % gpu_to_use)
        else:
            logger.warning("No supported GPU found (no GPU with load sensor)")

        return gpu_to_use


def get_net_interface_and_update(if_name: str) -> Hardware.Hardware:
    for hardware in handle.Hardware:
        if hardware.HardwareType == Hardware.HardwareType.Network and hardware.Name == if_name:
            hardware.Update()
            return hardware

    logger.warning("Network interface '%s' not found. Check names in config.yaml." % if_name)
    return None


class Cpu(sensors.Cpu):
    @staticmethod
    def percentage(interval: float) -> float:
        cpu = get_hw_and_update(Hardware.HardwareType.Cpu)
        if cpu:
            try:
                for sensor in cpu.Sensors:
                    if sensor.SensorType == Hardware.SensorType.Load and str(sensor.Name).startswith(
                            "CPU Total") and sensor.Value is not None:
                        val = float(sensor.Value)
                        if not math.isnan(val):
                            return val
            except Exception:
                pass

        # Fallback to psutil - 100% reliable on Windows without Admin rights
        try:
            val = float(psutil.cpu_percent(interval=None))
            if not math.isnan(val):
                return val
        except Exception:
            pass

        logger.error("CPU load cannot be read")
        return 0.0

    @staticmethod
    def frequency() -> float:
        frequencies = []
        cpu = get_hw_and_update(Hardware.HardwareType.Cpu)
        try:
            for sensor in cpu.Sensors:
                if sensor.SensorType == Hardware.SensorType.Clock:
                    # Keep only real core clocks, ignore effective core clocks
                    if "Core #" in str(sensor.Name) and "Effective" not in str(
                            sensor.Name) and sensor.Value is not None:
                        val = float(sensor.Value)
                        if val > 0:
                            frequencies.append(val)

            if frequencies:
                # Take mean of all core clock as "CPU clock"
                return mean(frequencies)
        except:
            pass

        # Fallback 1: check "Cores (Average)" or other clock sensors in LHM
        try:
            for sensor in cpu.Sensors:
                if sensor.SensorType == Hardware.SensorType.Clock and "Average" in str(sensor.Name) and sensor.Value is not None:
                    val = float(sensor.Value)
                    if val > 0:
                        return val
        except:
            pass

        # Fallback 2: psutil.cpu_freq() (works 100% on Windows without Admin rights)
        try:
            freq = psutil.cpu_freq()
            if freq and freq.current and freq.current > 0:
                return float(freq.current)
        except:
            pass

        return math.nan

    @staticmethod
    def load() -> Tuple[float, float, float]:  # 1 / 5 / 15min avg (%):
        # Get this data from psutil because it is not available from LibreHardwareMonitor
        return psutil.getloadavg()

    @staticmethod
    def temperature() -> float:
        # 1. Check AIDA64 Shared Memory (Highest accuracy, supports all Ryzen AGESA versions)
        try:
            import mmap
            import xml.etree.ElementTree as ET
            shm = mmap.mmap(-1, 0x20000, "AIDA64_SensorValues", mmap.ACCESS_READ)
            raw = shm.read().split(b'\x00')[0].decode('utf-8', errors='ignore')
            if raw and "<temp>" in raw:
                root = ET.fromstring(f"<root>{raw}</root>")
                # Priority IDs: TCPUDIO (Die), TCPU (CPU), TCC1 (CCD1)
                for target_id in ["TCPUDIO", "TCPU", "TCC1", "TCC2"]:
                    for elem in root.findall("temp"):
                        if elem.findtext("id", "") == target_id:
                            val = float(elem.findtext("val", "0"))
                            if val > 0:
                                return val
                # Any CPU temp
                for elem in root.findall("temp"):
                    label = elem.findtext("label", "").lower()
                    if "cpu" in label:
                        val = float(elem.findtext("val", "0"))
                        if val > 0:
                            return val
        except Exception:
            pass

        # 2. Search LibreHardwareMonitor CPU sensors
        cpu = get_hw_and_update(Hardware.HardwareType.Cpu)
        try:
            for keyword in ["Tctl", "Tdie", "Core Average", "Core Max", "CPU Package", "Package", "Core"]:
                for sensor in cpu.Sensors:
                    if sensor.SensorType == Hardware.SensorType.Temperature and sensor.Value is not None:
                        val = float(sensor.Value)
                        if val > 0 and keyword.lower() in str(sensor.Name).lower():
                            return val

            for sensor in cpu.Sensors:
                if sensor.SensorType == Hardware.SensorType.Temperature and sensor.Value is not None:
                    val = float(sensor.Value)
                    if val > 0:
                        return val
        except:
            pass

        # 3. Fallback to Motherboard CPU sensor
        try:
            mb = get_hw_and_update(Hardware.HardwareType.Motherboard)
            if mb:
                for sensor in mb.Sensors:
                    if sensor.SensorType == Hardware.SensorType.Temperature and sensor.Value is not None:
                        val = float(sensor.Value)
                        if val > 0 and "cpu" in str(sensor.Name).lower():
                            return val
                for sub in mb.SubHardware:
                    sub.Update()
                    for sensor in sub.Sensors:
                        if sensor.SensorType == Hardware.SensorType.Temperature and sensor.Value is not None:
                            val = float(sensor.Value)
                            if val > 0 and "cpu" in str(sensor.Name).lower():
                                return val
        except:
            pass

        return math.nan

    @staticmethod
    def fan_percent(fan_name: str = None) -> float:
        mb = get_hw_and_update(Hardware.HardwareType.Motherboard)
        try:
            for sh in mb.SubHardware:
                sh.Update()
                for sensor in sh.Sensors:
                    if sensor.SensorType == Hardware.SensorType.Control and "#2" in str(
                            sensor.Name) and sensor.Value is not None:  # Is Motherboard #2 Fan always the CPU Fan ?
                        return float(sensor.Value)
        except:
            pass

        # No Fan Speed sensor for this CPU model
        return math.nan

    @staticmethod
    def power() -> float:
        # 1. Check AIDA64 Shared Memory
        try:
            import mmap
            import xml.etree.ElementTree as ET
            shm = mmap.mmap(-1, 0x20000, "AIDA64_SensorValues", mmap.ACCESS_READ)
            raw = shm.read().split(b'\x00')[0].decode('utf-8', errors='ignore')
            if raw and "<pwr>" in raw:
                root = ET.fromstring(f"<root>{raw}</root>")
                for target_id in ["PCPUPKG", "PCPUDIO", "PCPU"]:
                    for elem in root.findall("pwr"):
                        if elem.findtext("id", "") == target_id:
                            val = float(elem.findtext("val", "0"))
                            if val > 0:
                                return val
        except Exception:
            pass

        # 2. Check LHM
        try:
            cpu = get_hw_and_update(Hardware.HardwareType.Cpu)
            if cpu:
                for s in cpu.Sensors:
                    if s.SensorType == Hardware.SensorType.Power and s.Value is not None:
                        val = float(s.Value)
                        if val > 0 and ("package" in str(s.Name).lower() or "total" in str(s.Name).lower() or "cpu" in str(s.Name).lower()):
                            return val
                for s in cpu.Sensors:
                    if s.SensorType == Hardware.SensorType.Power and s.Value is not None:
                        val = float(s.Value)
                        if val > 0:
                            return val
        except Exception:
            pass
        return math.nan


class Gpu(sensors.Gpu):
    # GPU to use is detected once, and its name is saved for future sensors readings
    gpu_name = ""

    # Latest FPS value is backed up in case next reading returns no value
    prev_fps = 0

    # Get GPU to use for sensors, and update it
    @classmethod
    def get_gpu_to_use(cls):
        if not cls.gpu_name:
            cls.gpu_name = get_gpu_name()
        gpu_to_use = get_hw_and_update(Hardware.HardwareType.GpuAmd, cls.gpu_name)
        if gpu_to_use is None:
            gpu_to_use = get_hw_and_update(Hardware.HardwareType.GpuNvidia, cls.gpu_name)
        if gpu_to_use is None:
            gpu_to_use = get_hw_and_update(Hardware.HardwareType.GpuIntel, cls.gpu_name)

        return gpu_to_use

    @classmethod
    def stats(cls) -> Tuple[
        float, float, float, float, float]:  # load (%) / used mem (%) / used mem (Mb) / total mem (Mb) / temp (°C)
        gpu_to_use = cls.get_gpu_to_use()
        if gpu_to_use is None:
            # GPU not supported
            return math.nan, math.nan, math.nan, math.nan, math.nan

        load = math.nan
        used_mem = math.nan
        total_mem = math.nan
        temp = math.nan

        for sensor in gpu_to_use.Sensors:
            if sensor.SensorType == Hardware.SensorType.Load and str(sensor.Name).startswith(
                    "GPU Core") and sensor.Value is not None:
                load = float(sensor.Value)
            elif sensor.SensorType == Hardware.SensorType.Load and str(sensor.Name).startswith("D3D 3D") and math.isnan(
                    load) and sensor.Value is not None:
                # Only use D3D usage if global "GPU Core" sensor is not available, because it is less
                # precise and does not cover the entire GPU: https://www.hwinfo.com/forum/threads/what-is-d3d-usage.759/
                load = float(sensor.Value)
            elif sensor.SensorType == Hardware.SensorType.SmallData and str(sensor.Name).startswith(
                    "GPU Memory Used") and sensor.Value is not None:
                used_mem = float(sensor.Value)
            elif sensor.SensorType == Hardware.SensorType.SmallData and str(sensor.Name).startswith(
                    "D3D") and str(sensor.Name).endswith("Memory Used") and math.isnan(
                used_mem) and sensor.Value is not None:
                # Only use D3D memory usage if global "GPU Memory Used" sensor is not available, because it is less
                # precise and does not cover the entire GPU: https://www.hwinfo.com/forum/threads/what-is-d3d-usage.759/
                used_mem = float(sensor.Value)
            elif sensor.SensorType == Hardware.SensorType.SmallData and str(sensor.Name).startswith(
                    "GPU Memory Total") and sensor.Value is not None:
                total_mem = float(sensor.Value)
            elif sensor.SensorType == Hardware.SensorType.Temperature and str(sensor.Name).startswith(
                    "GPU Core") and sensor.Value is not None:
                temp = float(sensor.Value)

        return load, (used_mem / total_mem * 100.0), used_mem, total_mem, temp

    @classmethod
    def fps(cls) -> int:
        gpu_to_use = cls.get_gpu_to_use()
        if gpu_to_use is None:
            # GPU not supported
            return -1

        try:
            for sensor in gpu_to_use.Sensors:
                if sensor.SensorType == Hardware.SensorType.Factor and "FPS" in str(
                        sensor.Name) and sensor.Value is not None:
                    # If a reading returns a value <= 0, returns old value instead
                    if int(sensor.Value) > 0:
                        cls.prev_fps = int(sensor.Value)
                    return cls.prev_fps
        except:
            pass

        # No FPS sensor for this GPU model
        return -1

    @classmethod
    def fan_percent(cls) -> float:
        gpu_to_use = cls.get_gpu_to_use()
        if gpu_to_use is None:
            # GPU not supported
            return math.nan

        try:
            for sensor in gpu_to_use.Sensors:
                if sensor.SensorType == Hardware.SensorType.Control and sensor.Value is not None:
                    return float(sensor.Value)
        except:
            pass

        # No Fan Speed sensor for this GPU model
        return math.nan

    @classmethod
    def frequency(cls) -> float:
        gpu_to_use = cls.get_gpu_to_use()
        if gpu_to_use is None:
            # GPU not supported
            return math.nan

        try:
            for sensor in gpu_to_use.Sensors:
                if sensor.SensorType == Hardware.SensorType.Clock:
                    # Keep only real core clocks, ignore effective core clocks
                    if "Core" in str(sensor.Name) and "Effective" not in str(sensor.Name) and sensor.Value is not None:
                        return float(sensor.Value)
        except:
            pass

        # No Frequency sensor for this GPU model
        return math.nan

    @classmethod
    def power(cls) -> float:
        try:
            gpu_to_use = cls.get_gpu_to_use()
            if gpu_to_use:
                for s in gpu_to_use.Sensors:
                    if s.SensorType == Hardware.SensorType.Power and s.Value is not None:
                        val = float(s.Value)
                        if val > 0:
                            return val
        except Exception:
            pass
        return math.nan

    @classmethod
    def is_available(cls) -> bool:
        cls.gpu_name = get_gpu_name()
        return bool(cls.gpu_name)


class Memory(sensors.Memory):
    @staticmethod
    def swap_percent() -> float:
        ram = get_hw_and_update(Hardware.HardwareType.Memory, "Total Memory")
        vram = get_hw_and_update(Hardware.HardwareType.Memory, "Virtual Memory")

        virtual_mem_used = math.nan
        mem_used = math.nan
        virtual_mem_available = math.nan
        mem_available = math.nan

        # Get virtual / physical memory stats
        for sensor in ram.Sensors:
            if sensor.SensorType == Hardware.SensorType.Data and str(sensor.Name).startswith(
                    "Memory Used") and sensor.Value is not None:
                mem_used = int(sensor.Value)
            elif sensor.SensorType == Hardware.SensorType.Data and str(sensor.Name).startswith(
                    "Memory Available") and sensor.Value is not None:
                mem_available = int(sensor.Value)

        for sensor in vram.Sensors:
            if sensor.SensorType == Hardware.SensorType.Data and str(sensor.Name).startswith(
                    "Memory Used") and sensor.Value is not None:
                virtual_mem_used = int(sensor.Value)
            elif sensor.SensorType == Hardware.SensorType.Data and str(sensor.Name).startswith(
                    "Memory Available") and sensor.Value is not None:
                virtual_mem_available = int(sensor.Value)

        # Compute swap stats from virtual / physical memory stats
        swap_used = virtual_mem_used - mem_used
        swap_available = virtual_mem_available - mem_available
        swap_total = swap_used + swap_available
        try:
            percent_swap = swap_used / swap_total * 100.0
        except:
            # No swap / pagefile disabled
            percent_swap = 0.0

        return percent_swap

    @staticmethod
    def virtual_percent() -> float:
        ram = get_hw_and_update(Hardware.HardwareType.Memory, "Total Memory")
        for sensor in ram.Sensors:
            if sensor.SensorType == Hardware.SensorType.Load and str(sensor.Name).startswith(
                    "Memory") and sensor.Value is not None:
                return float(sensor.Value)

        return math.nan

    @staticmethod
    def virtual_used() -> int:  # In bytes
        ram = get_hw_and_update(Hardware.HardwareType.Memory, "Total Memory")
        for sensor in ram.Sensors:
            if sensor.SensorType == Hardware.SensorType.Data and str(sensor.Name).startswith(
                    "Memory Used") and sensor.Value is not None:
                return int(sensor.Value * 1000000000.0)

        return 0

    @staticmethod
    def virtual_free() -> int:  # In bytes
        ram = get_hw_and_update(Hardware.HardwareType.Memory, "Total Memory")
        for sensor in ram.Sensors:
            if sensor.SensorType == Hardware.SensorType.Data and str(sensor.Name).startswith(
                    "Memory Available") and sensor.Value is not None:
                return int(sensor.Value * 1000000000.0)

        return 0


def _get_disk_path():
    try:
        import library.config as config
        configured = config.CONFIG_DATA["config"].get("DISK_DRIVE", "")
        if configured:
            return configured
    except Exception:
        pass
    if sys.platform == "win32":
        return os.environ.get('SystemDrive', 'C:') + '\\'
    return "/"


# NOTE: all disk data are fetched from psutil Python library, because LHM does not have it.
# This is because LHM is a hardware-oriented library, whereas used/free/total space is for partitions, not disks
class Disk(sensors.Disk):
    @staticmethod
    def disk_usage_percent() -> float:
        return psutil.disk_usage(_get_disk_path()).percent

    @staticmethod
    def disk_used() -> int:  # In bytes
        return psutil.disk_usage(_get_disk_path()).used

    @staticmethod
    def disk_free() -> int:  # In bytes
        return psutil.disk_usage(_get_disk_path()).free


class Net(sensors.Net):
    # Previous psutil counters, per interface: {interface name: (monotonic timestamp, counters)}
    _psutil_before = {}

    @staticmethod
    def stats(if_name, interval) -> Tuple[
        int, int, int, int]:  # up rate (B/s), uploaded (B), dl rate (B/s), downloaded (B)

        upload_rate = 0
        uploaded = 0
        download_rate = 0
        downloaded = 0

        if if_name != "":
            net_if = get_net_interface_and_update(if_name)
            # LHM does not expose Data/Throughput sensors for every adapter it reports (e.g. some
            # Wi-Fi adapters): all values would silently stay at 0 and the network widgets would
            # display nothing. Read those interfaces from psutil, like disk stats above.
            if net_if is None or not any(
                    sensor.SensorType in (Hardware.SensorType.Data, Hardware.SensorType.Throughput)
                    for sensor in net_if.Sensors):
                return Net._stats_from_psutil(if_name)

            for sensor in net_if.Sensors:
                if sensor.SensorType == Hardware.SensorType.Data and str(sensor.Name).startswith(
                        "Data Uploaded") and sensor.Value is not None:
                    uploaded = int(sensor.Value * 1000000000.0)
                elif sensor.SensorType == Hardware.SensorType.Data and str(sensor.Name).startswith(
                        "Data Downloaded") and sensor.Value is not None:
                    downloaded = int(sensor.Value * 1000000000.0)
                elif sensor.SensorType == Hardware.SensorType.Throughput and str(sensor.Name).startswith(
                        "Upload Speed") and sensor.Value is not None:
                    upload_rate = int(sensor.Value)
                elif sensor.SensorType == Hardware.SensorType.Throughput and str(sensor.Name).startswith(
                        "Download Speed") and sensor.Value is not None:
                    download_rate = int(sensor.Value)

        return upload_rate, uploaded, download_rate, downloaded

    @staticmethod
    def _stats_from_psutil(if_name) -> Tuple[
        int, int, int, int]:  # up rate (B/s), uploaded (B), dl rate (B/s), downloaded (B)

        upload_rate = 0
        uploaded = 0
        download_rate = 0
        downloaded = 0

        counters = psutil.net_io_counters(pernic=True).get(if_name)
        if counters is not None:
            now = time.monotonic()
            before = Net._psutil_before.get(if_name)
            # Rates are computed from the elapsed time, so they stay correct even if this
            # interface was not read on the previous cycle.
            if before is not None and now > before[0]:
                elapsed = now - before[0]
                upload_rate = int(max(0, counters.bytes_sent - before[1].bytes_sent) / elapsed)
                download_rate = int(max(0, counters.bytes_recv - before[1].bytes_recv) / elapsed)
            uploaded = counters.bytes_sent
            downloaded = counters.bytes_recv
            Net._psutil_before[if_name] = (now, counters)

        return upload_rate, uploaded, download_rate, downloaded
