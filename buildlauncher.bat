
set mypath=%~dp0
pyinstaller --onefile resources\openGOALModLauncher.py --add-data "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\Lib\site-packages\ahk";ahk --icon resources\appicon.ico 
move "%mypath%dist\openGOALModLauncher.exe" "%mypath%/"
RENAME "%mypath%\openGOALModLauncher.exe" "openGOALModLauncher.exe"
@RD /S /Q "%mypath%/build"
@RD /S /Q "%mypath%/dist"
DEL /S /Q "%mypath%/openGOALModLauncher.spec"
