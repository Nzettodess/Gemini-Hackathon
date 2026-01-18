@echo off
:: Ensure we are in the correct directory (optional, but good practice)
cd /d "%~dp0"

:: Set environment variables
set PYTHONPATH=%~dp0src
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

:: Run the server using the python executable in .venv
:: Quotes around the executable path handle spaces in the path
".venv\Scripts\python.exe" -u -m data_governance.server
