# -*- mode: python -*-

block_cipher = None


a = Analysis(['P3_010_Spannungsteiler.py'],
             pathex=['D:\\Git Repos\\Py3-Private\\P3_010_Spannungsteiler\\P3_010_Spannungsteiler'],
             binaries=[],
             datas=[],
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
          exclude_binaries=True,
          name='P3_010_Spannungsteiler',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='P3_010_Spannungsteiler')
