# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['C:\\Users\\tony_\\source\\repos\\rFactory\\\\rFactoryModManager.py'],
             pathex=['env\\Lib\\site-packages'],
             binaries=[],
             datas=[('ModMaker.bat', '.'), ('resources\\rfactory.ico', 'resources'), ('rFactoryModManagerFaq.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=['dummyRF2', 'tabFavouriteServers', 'tabGearshift', 'tabGraphics', 'tabJsonEditor', 'tabOpponents', 'tabServers', 'tabSessions', 'executeRF2'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=True)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [('v', None, 'OPTION')],
          name='rFactoryModManager',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='resources\\rfactory.ico')
