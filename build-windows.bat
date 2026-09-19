@echo off
setlocal

cd /d "%~dp0"

set OUTPUT_DIR=dist

if not exist "assets\nav\appicon.ico" (
    echo ERROR: assets\nav\appicon.ico was not found.
    exit /b 1
)

if exist "%OUTPUT_DIR%" (
    rmdir /s /q "%OUTPUT_DIR%"
)

mkdir "%OUTPUT_DIR%"

python -m nuitka ^
    --mode=onefile ^
    --enable-plugin=pyside6 ^
    --include-qt-plugins=multimedia,networkinformation,platforminputcontexts,imageformats ^
    --include-data-dir=assets=assets ^
    --windows-icon-from-ico=assets\nav\appicon.ico ^
    --output-dir="%OUTPUT_DIR%" ^
    --output-filename=PavPlay-1.0.0-beta-windows-x64.exe ^
    --product-name="PavPlay" ^
    --file-description="Pav Play Media Player" ^
    --product-version="1.0.0.0" ^
    --file-version="1.0.0.0" ^
    --windows-console-mode=disable ^
    src\main.py

if errorlevel 1 (
    echo.
    echo ======================================
    echo Pav Play Windows build FAILED.
    echo ======================================
    exit /b 1
)

echo.
echo ======================================
echo Pav Play Windows build completed.
echo Output:
echo %OUTPUT_DIR%\PavPlay-1.0.0-beta-windows-x64.exe
echo ======================================

endlocal