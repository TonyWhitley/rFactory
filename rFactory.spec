# -*- mode: python -*-

block_cipher = None


a = Analysis(['rFactory.py'],
             pathex=['../ScriptedJsonEditor/ScriptedJsonEditor', 
             '../rF2_serverNotify/steps',
             '.',
             'env/Lib/site-packages'],
             binaries=[],
             datas=[('resources\\rfactory.ico', 'resources'),
               ('faq.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='rFactory',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          icon='resources\\rFactory.ico',
          console=True )
