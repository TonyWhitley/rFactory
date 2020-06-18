# -*- mode: python -*-

block_cipher = None


a = Analysis(['rFactoryModManager.py'],
             pathex=['.', 'env/Lib/site-packages'],
             binaries=[],
             datas=[('ModMaker.bat', '.'), ('resources\\rfactory.ico', 'resources'), ('rFactoryModManagerFaq.txt', '.')],
             hiddenimports=['pkg_resources.py2_warn'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['dummyRF2', 'tabFavouriteServers', 'tabGearshift', 'tabGraphics', 'tabJsonEditor', 'tabOpponents', 'tabServers', 'tabSessions', 'executeRF2'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='rFactoryModManager',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          icon='resources\\rFactory.ico',
          console=True )
