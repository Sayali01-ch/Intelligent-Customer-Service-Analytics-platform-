@echo off
REM Quick Start Script for Windows
REM Intelligent Customer Service Analytics Platform

setlocal enabledelayedexpansion

echo ==================================
echo Analytics Platform - Quick Start (Windows)
echo ==================================
echo.

REM Check if Docker is installed
docker --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Docker not found. Please install Docker Desktop.
    echo Download from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo. [OK] Docker found

REM Check if Docker Compose is installed
docker-compose --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Docker Compose not found. Please install Docker Compose.
    pause
    exit /b 1
)

echo. [OK] Docker Compose found
echo.

echo Select deployment method:
echo 1) Docker (Recommended - All services)
echo 2) Manual (Local development)
echo 3) Exit
echo.
set /p choice="Enter option (1/2/3): "

if "%choice%"=="1" (
    echo.
    echo Starting Docker deployment...
    echo.
    
    echo Building docker images...
    docker-compose build
    
    echo.
    echo [OK] Docker images built
    echo.
    
    echo Starting containers...
    docker-compose up -d
    
    echo.
    echo [OK] Containers started
    echo.
    
    echo Waiting for services to start (30 seconds)...
    timeout /t 30 /nobreak
    
    echo.
    echo Checking service health...
    powershell -Command "try { Invoke-WebRequest -Uri http://localhost:8000/health | Out-Null; Write-Host '[OK] API is running' } catch { Write-Host '[Warning] API not responding yet' }"
    
    echo.
    echo ==================================
    echo. Platform is ready!
    echo ==================================
    echo.
    echo Access the platform:
    echo   Frontend:     http://localhost:3000
    echo   API:          http://localhost:8000
    echo   API Docs:     http://localhost:8000/docs
    echo   Streamlit:    http://localhost:8501
    echo.
    echo Commands:
    echo   Stop services:     docker-compose down
    echo   View logs:         docker-compose logs -f
    echo.
    pause
    
) else if "%choice%"=="2" (
    echo.
    echo Starting manual deployment...
    echo.
    
    REM Check Python
    python --version > nul 2>&1
    if %errorlevel% neq 0 (
        echo Python not found. Please install Python 3.11+
        echo Download from: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo. [OK] Python %PYTHON_VERSION% found
    
    REM Check Node.js
    node --version > nul 2>&1
    if %errorlevel% neq 0 (
        echo Node.js not found. Please install Node.js 18+
        echo Download from: https://nodejs.org/
        pause
        exit /b 1
    )
    
    for /f %%i in ('node --version') do set NODE_VERSION=%%i
    echo. [OK] Node.js %NODE_VERSION% found
    echo.
    
    echo Setting up backend...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    
    if not exist .env (
        copy .env.example .env
        echo. [Warning] .env file created. Please edit with your settings.
    )
    
    echo.
    echo Setting up database...
    python -c "from database import create_tables; create_tables()"
    echo. [OK] Database initialized
    echo.
    
    echo Starting backend server...
    start python run_api.py
    
    echo Setting up frontend...
    cd frontend
    call npm install
    timeout /t 2 /nobreak
    call npm start
    
    echo.
    echo ==================================
    echo. Platform is running!
    echo ==================================
    echo.
    echo Access the platform:
    echo   Frontend:     http://localhost:3000
    echo   API:          http://localhost:8000
    echo   API Docs:     http://localhost:8000/docs
    echo.
    pause
    
) else if "%choice%"=="3" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid option
    exit /b 1
)