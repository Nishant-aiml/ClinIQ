@echo off
:: ============================================================
:: ClinIQ - Full Stack + Ngrok Launcher
:: Frontend:       http://localhost:3056
:: Backend:        http://127.0.0.1:8056
:: Ngrok Inspector: http://127.0.0.1:4056
:: ============================================================
title ClinIQ Full Stack

cd /d %~dp0

echo.
echo ============================================================
echo  ClinIQ - Starting All Services
echo ============================================================
echo.

:: 1. Start Backend
start "ClinIQ Backend :8056" cmd /k "cd /d %~dp0backend && venv\Scripts\python -m uvicorn app.main:app --port 8056 --host 127.0.0.1 --reload"

:: 2. Wait for backend to start
timeout /t 4 /nobreak >nul

:: 3. Start Frontend
start "ClinIQ Frontend :3056" cmd /k "cd /d %~dp0frontend && npm run dev"

:: 4. Wait for frontend to start
timeout /t 5 /nobreak >nul

:: 5. Start Ngrok with project-isolated config
start "ClinIQ Ngrok :4056" cmd /k "ngrok start cliniq --config %~dp0ngrok.yml"

echo.
echo ============================================================
echo  All ClinIQ services launched!
echo  Frontend:        http://localhost:3056
echo  Backend API:     http://127.0.0.1:8056
echo  API Docs:        http://127.0.0.1:8056/docs
echo  Ngrok Inspector: http://127.0.0.1:4056
echo ============================================================
echo.
pause
