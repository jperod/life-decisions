# Set variables
$PROJECT_DIR = "C:\Repos\jperod\ld"
$VENV_DIR = "$PROJECT_DIR\.venv"

# Set PYTHONPATH 
$env:PYTHONPATH = "$PWD;$env:PYTHONPATH"

# Activate virtual environment
Write-Host "Activating virtual environment..."
& "$VENV_DIR\Scripts\Activate.ps1"