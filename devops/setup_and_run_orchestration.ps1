# Set the title for the PowerShell window
$host.ui.RawUI.WindowTitle = "ld Orchestration"

# Set variables
$PROJECT_DIR = "C:\Repos\life-decisions"
$VENV_DIR = "$PROJECT_DIR\.venv"
$PYTHON_VERSION = "python3.12"
$ORCHESTRATION_SCRIPT = "$PROJECT_DIR\orchestrator.py"

# Output Python version for debugging
Write-Host "Python version being used: $PYTHON_VERSION"

# Set PYTHONPATH 
$env:PYTHONPATH = "$PROJECT_DIR;$env:PYTHONPATH"

# Change to project directory
Set-Location $PROJECT_DIR

# Check if virtual environment exists and delete if it does
if (Test-Path $VENV_DIR) {
    Write-Host "Deleting existing virtual environment..."
    Remove-Item -Recurse -Force $VENV_DIR
    
    # Wait 5 seconds
    Start-Sleep -Seconds 5
}

# Create virtual environment
Write-Host "Creating virtual environment with $PYTHON_VERSION..."
& $PYTHON_VERSION -m venv $VENV_DIR

# Set PYTHONPATH 
$env:PYTHONPATH = "$PWD;$env:PYTHONPATH"

# Activate virtual environment
Write-Host "Activating virtual environment..."
& "$VENV_DIR\Scripts\Activate.ps1"


# Install Poetry and dependencies
Write-Host "Installing Poetry..."
pip install poetry
Write-Host "Installing project dependencies..."
poetry install

# Run Unit Tests
pytest

# Run orchestration script
Write-Host "Running orchestration script..."
python $ORCHESTRATION_SCRIPT

# Cleanup
Write-Host "Done."