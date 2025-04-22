from setuptools import setup

APP = ['iso_downloader.py']
DATA_FILES = ['icon.png']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.png',
    'packages': ['PyQt6', 'requests'],
    'plist': {
        'CFBundleName': 'ISO Downloader Pro',
        'CFBundleDisplayName': 'ISO Downloader Pro',
        'CFBundleVersion': '1.0',
        'CFBundleShortVersionString': '1.0',
        'CFBundleIdentifier': 'com.benjaminstoica.isodownloaderpro',
        'NSHumanReadableCopyright': '© 2024 Benjamin Stoica',
        'NSHighResolutionCapable': True,
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    name='ISO Downloader Pro',
    version='1.0',
    author='Benjamin Stoica',
    description='Applicazione per scaricare facilmente le ISO dei sistemi operativi più popolari'
)