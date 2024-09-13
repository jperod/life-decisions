@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Set variables
SET "VENV_DIR=.venv"
SET "PYTHON_VERSION=python3.12"
SET "ORCHESTRATION_SCRIPT=orchestrator.py"

REM Output Python version for debugging
echo Python version being used: %PYTHON_VERSION%

REM Check if virtual environment exists and delete if it does
IF EXIST "%VENV_DIR%" (
    echo Deleting existing virtual environment...
    rmdir /s /q "%VENV_DIR%"
)

REM Create virtual environment
echo Creating virtual environment with %PYTHON_VERSION%...
%PYTHON_VERSION% -m venv %VENV_DIR%

REM Activate virtual environment
echo Activating virtual environment...
CALL %VENV_DIR%\Scripts\activate

REM Install Poetry and dependencies
echo Installing Poetry...
pip install poetry
echo Installing project dependencies...
poetry install

REM Run orchestration script
echo Running orchestration script...
python %ORCHESTRATION_SCRIPT%

REM Cleanup
echo Done.
ENDLOCAL
pause
