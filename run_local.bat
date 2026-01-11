@echo off
REM Local execution script for AI Code Review Assistant (Windows)
REM Usage: run_local.bat <pr_number>

echo AI Code Review Assistant - Local Runner
echo ========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found
    echo Please create .env file from .env.example
    exit /b 1
)

REM Check if PR number is provided as argument
if not "%1"=="" (
    set GITHUB_PR_NUMBER=%1
)

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Creating...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Run the reviewer
echo Starting code review...
echo.
python -m src.main

REM Check exit code
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Review completed successfully
) else (
    echo.
    echo Review failed
    exit /b 1
)
