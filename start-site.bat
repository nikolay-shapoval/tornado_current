@echo off
cd /d "%~dp0"
if exist docs\index.html goto open
py source\build_site.py
if errorlevel 1 (
    echo Could not build the website. Run: python3 source/build_site.py
    pause
    exit /b 1
)
:open
start "" "%~dp0docs\index.html"
