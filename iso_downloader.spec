# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['iso_downloader.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
plist = {
    'CFBundleName': 'ISO Downloader Pro',
    'CFBundleDisplayName': 'ISO Downloader Pro',
    'CFBundleVersion': '1.0',
    'CFBundleShortVersionString': '1.0',
    'CFBundleIdentifier': 'com.benjaminstoica.isodownloaderpro',
    'NSHumanReadableCopyright': '© 2024 Benjamin Stoica',
}
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ISO Downloader Pro',
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
    icon='icon.png',
)

app = BUNDLE(
    exe,
    name='ISO Downloader Pro.app',
    icon='icon.png',
    bundle_identifier='com.benjaminstoica.isodownloaderpro',
    info_plist=plist,
)