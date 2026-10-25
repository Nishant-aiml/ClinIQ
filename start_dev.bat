@echo off
:: ============================================================
:: ClinIQ - Local Dev Launcher (No Ngrok)
:: Frontend: http://localhost:3056
:: Backend:  http://127.0.0.1:8056
:: ============================================================
title ClinIQ Dev Servers

cd /d %~dp0

:: Start Backend in new window
start "ClinIQ Backend :8056" cmd /k "cd /d %~dp0backend && venv\Scripts\python -m uvicorn app.main:app --port 8056 --host 127.0.0.1 --reload"

:: Wait briefly for backend to init
timeout /t 3 /nobreak >nul

:: Start Frontend in new window
start "ClinIQ Frontend :3056" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ============================================================
echo  ClinIQ Dev Servers Started
echo  Frontend:  http://localhost:3056
echo  Backend:   http://127.0.0.1:8056
echo  API Docs:  http://127.0.0.1:8056/docs
echo ============================================================
echo.
pause
