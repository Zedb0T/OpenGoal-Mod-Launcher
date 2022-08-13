
set mypath=%~dp0
python -c "import sysconfig; print(sysconfig.get_path('purelib') + '\\ahk')" > tmpFile
set /p PYSITEPKG_DIR= < tmpFile
DEL tmpFile
pyinstaller --onefile resources\openGOALModLauncher.py --add-data %PYSITEPKG_DIR%;ahk --icon resources\appicon.ico 
move "%mypath%dist\openGOALModLauncher.exe" "%mypath%/"
RENAME "%mypath%\openGOALModLauncher.exe" "openGOALModLauncher.exe"
@RD /S /Q "%mypath%/build"
@RD /S /Q "%mypath%/dist"
DEL /S /Q "%mypath%/openGOALModLauncher.spec"
