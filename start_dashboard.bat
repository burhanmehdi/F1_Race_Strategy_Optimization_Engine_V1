@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" run_dashboard.py
) else (
  py run_dashboard.py
)
if errorlevel 1 (
  echo.
  echo Dashboard failed to start.
  echo Check that Python dependencies are installed with:
  echo   .venv\Scripts\python.exe -m pip install -r requirements.txt
  echo.
  pause
)
