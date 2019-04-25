# -*- mode: python -*-

block_cipher = None


a = Analysis(['alien_invasion.py',
'E:\\project_Python\\learn\\alien_invasion\\src\\functions\\alien.py',
'E:\\project_Python\\learn\\alien_invasion\\src\\functions\\bullet.py',
'E:\\project_Python\\learn\\alien_invasion\\src\\functions\\button.py',
'E:\\project_Python\\learn\\alien_invasion\\src\\functions\\game_functions.py',
'E:\\project_Python\\learn\\alien_invasion\\src\\functions\\game_stats.py',
'E:\\project_Python\\learn\\alien_invasion\\src\\functions\\scoreboard.py',
'E:\\project_Python\\learn\\alien_invasion\\src\\functions\\settings.py',
'E:\\project_Python\\learn\\alien_invasion\\src\\functions\\ship.py'],
             pathex=['E:\\project_Python\\learn\\alien_invasion\\src'],
             binaries=[],
             datas=[('E:\\project_Python\\learn\\alien_invasion\\images','images'),
             ('E:\\project_Python\\learn\\alien_invasion\\src','src'),
             ('E:\\project_Python\\learn\\alien_invasion\\whl','whl')],
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
          [],
          exclude_binaries=True,
          name='alien_invasion',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='alien_invasion')
