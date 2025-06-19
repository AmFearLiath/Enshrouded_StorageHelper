@echo off
setlocal

:: Name des Scripts
set SCRIPT=updater.py

:: Python-Interpreter prüfen
where python >nul 2>&1
if errorlevel 1 (
    echo [FEHLER] Python ist nicht installiert oder nicht im PATH.
    pause
    exit /b 1
)

:: Virtualenv verwenden, falls vorhanden
if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
)

:: Start GUI
echo [INFO] Starte Updater-GUI...
python %SCRIPT%

endlocal
pause
