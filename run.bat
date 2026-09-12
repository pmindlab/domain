@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo [NameLab] Tworze srodowisko Python...
  python -m venv .venv || goto :error
)
echo [NameLab] Sprawdzam zaleznosci...
.venv\Scripts\python.exe -m pip install -q -r requirements.txt || goto :error
echo [NameLab] Startuje pod http://127.0.0.1:8787
.venv\Scripts\python.exe launcher.py
exit /b 0
:error
echo.
echo Nie udalo sie uruchomic NameLab. Sprawdz Python 3.11+ i polaczenie z internetem.
pause
exit /b 1
