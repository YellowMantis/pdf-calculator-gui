# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['admin.py'],
    pathex=[],
    binaries=[('C:\\\\Users\\\\yahia\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python312\\\\tcl\\\\tkdnd2.8', 'tkdnd2.8')],
    datas=[('icons','icons')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='admin',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='admin',
)
