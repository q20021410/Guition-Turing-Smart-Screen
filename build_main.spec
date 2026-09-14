# -*- mode: python ; coding: utf-8 -*-

import sys
import os

runtime_dll = os.path.join(
    os.environ.get('LOCALAPPDATA', ''),
    r'Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\pythonnet\runtime\Python.Runtime.dll'
)

binaries = []
if os.path.exists(runtime_dll):
    binaries.append((runtime_dll, '.'))

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=binaries,
    datas=[
        ('config.yaml', '.'),
    ],
    hiddenimports=[
        'clr',
        'pythonnet',
        'PIL',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
        'psutil',
        'serial',
        'serial.tools.list_ports',
        'yaml',
        'pystray',
        'win32api',
        'win32con',
        'win32gui',
        'requests',
        'ping3',
        'mmap',
        'xml.etree.ElementTree',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['unittest', 'test', 'tkinter.test'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['res\\icons\\monitor-icon-17865\\icon.ico'] if os.path.exists('res\\icons\\monitor-icon-17865\\icon.ico') else None,
    contents_directory='_internal',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Guition_Monitor',
)
