@echo off
:: ============================================================
:: ClinIQ - Ngrok Tunnel Launcher
:: Ports: Frontend 3056 | Backend 8056 | Ngrok Inspector 4056
:: ============================================================
title ClinIQ Ngrok Tunnel

cd /d %~dp0

:: Use project-level ngrok.yml (isolated from other projects)
set CONFIG=%~dp0ngrok.yml

echo.
echo ============================================================
echo  ClinIQ Ngrok Tunnel
echo  Inspector: http://127.0.0.1:4056
echo  Config:    %CONFIG%
echo ============================================================
echo.

:: Start the tunnel using this project's isolated config
ngrok start cliniq --config "%CONFIG%"

pause
