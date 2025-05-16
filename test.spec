# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['e:\\bezgo_root_main\\version2menu\\test.py'],
    pathex=[],
    binaries=[],
    datas=[('e:\\bezgo_root_main\\version2menu\\layouts', 'layouts'), ('e:\\bezgo_root_main\\version2menu\\logo.png', '.'), ('e:\\bezgo_root_main\\version2menu\\AnekMalayalam-Regular.ttf', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='test',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
