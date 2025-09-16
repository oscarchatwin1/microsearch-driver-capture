# Microsearch Driver Capture - PowerShell Launcher
# PowerShell script to run the Python launcher with better error handling

Write-Host "Microsearch Driver Capture - PowerShell Launcher" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Function to find Python executable
function Find-Python {
    # First try the specific Python path
    $pythonPath = "C:\Users\oscarchatwin\AppData\Local\Programs\Python\Python313\python.exe"
    if (Test-Path $pythonPath) {
        try {
            $version = & $pythonPath --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Found Python: $pythonPath ($version)" -ForegroundColor Green
                return $pythonPath
            }
        }
        catch {
            # Continue to fallback
        }
    }
    
    # Fallback to PATH
    $pythonCommands = @('python', 'python3', 'py')
    
    foreach ($cmd in $pythonCommands) {
        try {
            $version = & $cmd --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Found Python: $cmd ($version)" -ForegroundColor Green
                return $cmd
            }
        }
        catch {
            continue
        }
    }
    
    return $null
}

# Find Python
$pythonCmd = Find-Python

if (-not $pythonCmd) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.7+ and try again" -ForegroundColor Red
    Write-Host ""
    Write-Host "You can download Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if required files exist
$requiredFiles = @('main.py', 'storage.py', 'syncer.py', 'config.json', 'launch.py')
$missingFiles = @()

foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "ERROR: Missing required files:" -ForegroundColor Red
    foreach ($file in $missingFiles) {
        Write-Host "  - $file" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Please run this script from the project directory" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "All required files found" -ForegroundColor Green
Write-Host ""

# Parse command line arguments
$args = $args -join ' '

# Run the Python launcher
try {
    Write-Host "Starting launcher..." -ForegroundColor Yellow
    & $pythonCmd launch.py $args
}
catch {
    Write-Host "ERROR: Failed to run launcher: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Keep window open if no arguments provided (interactive mode)
if ($args -eq '') {
    Write-Host ""
    Read-Host "Press Enter to exit"
}
