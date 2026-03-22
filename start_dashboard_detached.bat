@echo off
cd /d "%~dp0"

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" (
  set "PYTHON_EXE=.venv\Scripts\python.exe"
) else (
  set "PYTHON_EXE=py"
)

start "F1 Strategy Engine" cmd /k "%PYTHON_EXE% -m uvicorn f1_strategy_engine.api.main:app --app-dir src --host 127.0.0.1 --port 8000"
