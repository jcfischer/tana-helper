# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.hooks import copy_metadata

title = 'Tana Helper'
name = 'tanahelper'

start_datas = []
start_binaries = []
start_hiddenimports = []
start_datas += copy_metadata('opentelemetry-sdk')

tmp_ret = collect_all('chromadb')
start_datas += tmp_ret[0]
start_binaries += tmp_ret[1]
start_hiddenimports += tmp_ret[2]

start_hiddenimports += collect_submodules('service')
start_hiddenimports += ['hnswlib']

start_datas += [('service/dist', 'service/dist'), 
    ('icons', 'icons'), 
    ('service/bin', 'service/bin'),
     ('service/scripts', 'service/scripts')]

start_a = Analysis(
    ['start.py'],
    pathex=['service'],
    binaries=start_binaries,
    datas=start_datas,
    hiddenimports=start_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

start_pyz = PYZ(start_a.pure)

start_exe = EXE(
    start_pyz,
    start_a.scripts,
    [],
    exclude_binaries=True,
    name='start',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='universal2',
    codesign_identity=None,
    entitlements_file=None,
)

helper_a = Analysis(
    ['tanahelper.py'],
    pathex=[],
    binaries=[],
    datas = [('icons','icons')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
helper_pyz = PYZ(helper_a.pure)

helper_exe = EXE(
    helper_pyz,
    helper_a.scripts,
    [],
    exclude_binaries=True,
    name=name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='universal2',
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT( 
    helper_exe,
    start_exe,
    helper_a.binaries,
    helper_a.zipfiles,
    helper_a.datas,
    start_a.binaries,
    start_a.zipfiles,
    start_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=name,
)

app = BUNDLE(
    coll,
    target_arch='universal2',
    name=f'{title}.app',
    icon=f'icons/{title}.icns',
    bundle_identifier=None,
)