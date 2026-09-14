# -*- mode: python ; coding: utf-8 -*-

import sys
import os
import _tkinter
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

runtime_dll = os.path.join(
    os.environ.get('LOCALAPPDATA', ''),
    r'Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\pythonnet\runtime\Python.Runtime.dll'
)

binaries = []
if os.path.exists(runtime_dll):
    binaries.append((runtime_dll, '.'))

dll_dir = os.path.dirname(_tkinter.__file__)
python_base = os.path.dirname(dll_dir)
tcl_dir = os.path.join(python_base, 'tcl')

if os.path.exists(os.path.join(dll_dir, '_tkinter.pyd')):
    binaries.append((os.path.join(dll_dir, '_tkinter.pyd'), '.'))
if os.path.exists(os.path.join(dll_dir, 'tcl86t.dll')):
    binaries.append((os.path.join(dll_dir, 'tcl86t.dll'), '.'))
if os.path.exists(os.path.join(dll_dir, 'tk86t.dll')):
    binaries.append((os.path.join(dll_dir, 'tk86t.dll'), '.'))

common_datas = [('config.yaml', '.')]
if os.path.exists(tcl_dir):
    common_datas.append((tcl_dir, 'tcl'))

dist_info_path = os.path.join(
    os.environ.get('LOCALAPPDATA', ''),
    r'Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\tkinter_tooltip-3.1.2.dist-info'
)
if os.path.exists(dist_info_path):
    common_datas.append((dist_info_path, 'tkinter_tooltip-3.1.2.dist-info'))

try:
    common_datas += collect_data_files('sv_ttk')
except Exception:
    pass
try:
    common_datas += collect_data_files('tktooltip')
except Exception:
    pass
try:
    common_datas += collect_data_files('babel')
except Exception:
    pass

common_hidden = [
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
    'sv_ttk',
    'darkdetect',
    'babel',
    'tktooltip',
]
try:
    common_hidden += collect_submodules('ruamel.yaml')
except Exception:
    pass

# Analysis for configure.py (GUI Configurator)
configure_a = Analysis(
    ['configure.py'],
    pathex=['.'],
    binaries=binaries,
    datas=common_datas,
    hiddenimports=common_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['unittest', 'test', 'tkinter.test'],
    noarchive=False,
    optimize=0,
)
configure_pyz = PYZ(configure_a.pure)
configure_exe = EXE(
    configure_pyz,
    configure_a.scripts,
    [],
    exclude_binaries=True,
    name='configure',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['res\\icons\\monitor-icon-17865\\icon.ico'] if os.path.exists('res\\icons\\monitor-icon-17865\\icon.ico') else None,
    contents_directory='_internal',
)

# Analysis for main.py (System Monitor)
main_a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=binaries,
    datas=common_datas,
    hiddenimports=common_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['unittest', 'test', 'tkinter.test'],
    noarchive=False,
    optimize=0,
)
main_pyz = PYZ(main_a.pure)
main_exe = EXE(
    main_pyz,
    main_a.scripts,
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

# Analysis for theme-editor.py (Theme Editor GUI)
theme_editor_a = Analysis(
    ['theme-editor.py'],
    pathex=['.'],
    binaries=binaries,
    datas=common_datas,
    hiddenimports=common_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['unittest', 'test', 'tkinter.test'],
    noarchive=False,
    optimize=0,
)
theme_editor_pyz = PYZ(theme_editor_a.pure)
theme_editor_exe = EXE(
    theme_editor_pyz,
    theme_editor_a.scripts,
    [],
    exclude_binaries=True,
    name='theme-editor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['res\\icons\\monitor-icon-17865\\icon.ico'] if os.path.exists('res\\icons\\monitor-icon-17865\\icon.ico') else None,
    contents_directory='_internal',
)

# Collect all into one folder
coll = COLLECT(
    main_exe,
    main_a.binaries,
    main_a.datas,
    configure_exe,
    configure_a.binaries,
    configure_a.datas,
    theme_editor_exe,
    theme_editor_a.binaries,
    theme_editor_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Guition_Monitor',
)
