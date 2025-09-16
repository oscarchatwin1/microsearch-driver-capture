#!/bin/bash
# Microsearch Driver Capture - Linux/Mac Launcher
# Shell script to run the Python launcher

echo "Microsearch Driver Capture - Linux/Mac Launcher"
echo "=============================================="

# Function to find Python executable
find_python() {
    local python_cmd=""
    
    # Try different Python commands
    for cmd in python3 python py; do
        if command -v "$cmd" >/dev/null 2>&1; then
            local version=$($cmd --version 2>&1)
            if [[ $? -eq 0 ]]; then
                echo "Found Python: $cmd ($version)"
                python_cmd="$cmd"
                break
            fi
        fi
    done
    
    echo "$python_cmd"
}

# Find Python
PYTHON_CMD=$(find_python)

if [[ -z "$PYTHON_CMD" ]]; then
    echo "ERROR: Python is not installed or not in PATH"
    echo "Please install Python 3.7+ and try again"
    echo ""
    echo "On Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "On macOS: brew install python3"
    echo "Or download from: https://www.python.org/downloads/"
    read -p "Press Enter to exit"
    exit 1
fi

# Check if required files exist
REQUIRED_FILES=("main.py" "storage.py" "syncer.py" "config.json" "launch.py")
MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [[ ! -f "$file" ]]; then
        MISSING_FILES+=("$file")
    fi
done

if [[ ${#MISSING_FILES[@]} -gt 0 ]]; then
    echo "ERROR: Missing required files:"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "Please run this script from the project directory"
    read -p "Press Enter to exit"
    exit 1
fi

echo "All required files found"
echo ""

# Make the script executable
chmod +x "$0"

# Run the Python launcher
echo "Starting launcher..."
$PYTHON_CMD launch.py "$@"

# Keep window open if no arguments provided (interactive mode)
if [[ $# -eq 0 ]]; then
    echo ""
    read -p "Press Enter to exit"
fi
