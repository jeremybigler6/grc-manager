@echo off
title GRC Agent Server Launcher
echo Launching your Autonomous GRC Agent Microservice...

:: This line tells Windows to open your default browser to the docs page instantly
start http://127.0.0.1:8000/docs

cd "C:\Users\abigl\OneDrive\Desktop\python-risk-register\app"
py -m uvicorn api:app --reload
pause