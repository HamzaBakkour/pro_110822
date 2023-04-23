import PyInstaller.__main__
import sys
PyInstaller.__main__.run([
    'pro_110822/mainwindow.py',
    '--onefile',
    '--windowed',
    '--name',
    'mainwindow_' + sys.argv[1]
])