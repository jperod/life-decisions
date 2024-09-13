@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Set variables
SET "VENV_DIR=.venv"
SET "PYTON_VERSION=python3.12"
SET "ORCHESTRATION_SCRIPT=orchestrator.py"
SET "POETRY_INSTALL_CMD=poetry install"

IF EXIST "%VENV_DIR%" (
    echo Deleting existing virtual environment...
    rmdir /s /q "%VENV_DIR%"
)

echo Creating virtual environment...
%PYTHON_VERSION% -m venv %VENV_DIR%

echo Activate virtual environment
CALL %VENV_DIR%\Scripts\activate

echo Installing Poetry and dependencies...
pip install poetry
poetry install

echo Running orchestration script...
python %ORCHESTRATION_SCRIPT%


echo Done.
ENDLOCAL
pause