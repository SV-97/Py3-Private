# -*- mode: python -*-

block_cipher = None


a = Analysis(['P3_043_ANSYSOutputNormalize.py'],
             pathex=['/home/sv-97/GitHub/Py3-Private/P3_043_ANYSYOutputNormalize'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
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
          name='P3_043_ANSYSOutputNormalize',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
