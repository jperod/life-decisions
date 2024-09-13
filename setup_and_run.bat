@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Set variables
SET "VENV_DIR=.venv"
SET "ORCHESTRATION_SCRIPT=orchestrator.py"
SET "POETRY_INSTALL_CMD=poetry install"

REM Check if virtual environment exists
IF NOT EXIST "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

echo Activate virtual environment
CALL %VENV_DIR%\Scripts\activate

echo Install Poetry 
pip install poetry
poetry install

echo Running orchestration script...
python %ORCHESTRATION_SCRIPT%


echo Done.
ENDLOCAL
pause