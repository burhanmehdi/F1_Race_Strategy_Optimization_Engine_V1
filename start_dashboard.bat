@echo off
cd /d "%~dp0"

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" (
  set "PYTHON_EXE=%CD%\.venv\Scripts\python.exe"
) else (
  set "PYTHON_EXE=py"
)

start "F1 Strategy Engine" cmd /k call "%PYTHON_EXE%" "%CD%\run_dashboard.py"

echo.
echo F1 Strategy Engine is starting in a new terminal window.
echo Open http://127.0.0.1:8000/ once the server finishes booting.
echo.
