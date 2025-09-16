#!/usr/bin/env python3
"""
Windows-specific build script for Microsearch Driver Capture
Provides alternative build methods for Windows users
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if required tools are available"""
    print("Checking build requirements...")
    
    # Check Python
    python_version = sys.version_info
    if python_version < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    print(f"Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check Kivy
    try:
        import kivy
        print(f"Kivy {kivy.__version__}")
    except ImportError:
        print("Kivy not installed")
        return False
    
    # Check PyMySQL
    try:
        import pymysql
        print("PyMySQL available")
    except ImportError:
        print("PyMySQL not installed")
        return False
    
    return True

def create_portable_app():
    """Create a portable Python application"""
    print("\nCreating portable Python application...")
    
    # Create dist directory
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    # Copy application files
    app_files = [
        "main.py",
        "storage.py", 
        "syncer.py",
        "dropdown_manager.py",
        "dropdown_widget.py",
        "config.json",
        "dropdown_config.json",
        "launch.py",
        "launch.bat",
        "launch.ps1"
    ]
    
    for file in app_files:
        if Path(file).exists():
            shutil.copy2(file, dist_dir)
            print(f"Copied {file}")
        else:
            print(f"{file} not found")
    
    # Create requirements.txt
    requirements = [
        "kivy>=2.0.0",
        "pymysql>=1.0.0",
        "jnius>=1.1.0"
    ]
    
    with open(dist_dir / "requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    print("Created requirements.txt")
    
    # Create run script
    run_script = """@echo off
echo Microsearch Driver Capture - Portable Version
echo ============================================
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting application...
python main.py
pause
"""
    
    with open(dist_dir / "run.bat", "w") as f:
        f.write(run_script)
    print("Created run.bat")
    
    print(f"\nPortable app created in {dist_dir.absolute()}")
    print("To run: cd dist && run.bat")
    
    return True

def create_android_instructions():
    """Create instructions for Android build"""
    instructions = """
# Android Build Instructions

## Option 1: Use WSL (Windows Subsystem for Linux)

1. Install WSL2:
   ```cmd
   wsl --install
   ```

2. Install Ubuntu in WSL:
   ```cmd
   wsl --install -d Ubuntu
   ```

3. In WSL, install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv git zip unzip openjdk-8-jdk
   pip3 install buildozer
   ```

4. Copy project to WSL and build:
   ```bash
   cp -r /mnt/d/Driver_App_2 ~/driver_app
   cd ~/driver_app
   buildozer android debug
   ```

## Option 2: Use GitHub Actions (Cloud Build)

1. Push code to GitHub repository
2. Create `.github/workflows/build.yml`:
   ```yaml
   name: Build Android APK
   on: [push]
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: 3.9
         - name: Install dependencies
           run: |
             pip install buildozer
             sudo apt-get update
             sudo apt-get install -y openjdk-8-jdk
         - name: Build APK
           run: buildozer android debug
         - name: Upload APK
           uses: actions/upload-artifact@v2
           with:
             name: app-debug.apk
             path: bin/*.apk
   ```

## Option 3: Use Docker

1. Create Dockerfile:
   ```dockerfile
   FROM ubuntu:20.04
   RUN apt-get update && apt-get install -y \\
       python3 python3-pip python3-venv \\
       git zip unzip openjdk-8-jdk \\
       build-essential libssl-dev libffi-dev \\
       python3-dev
   RUN pip3 install buildozer
   WORKDIR /app
   COPY . .
   CMD ["buildozer", "android", "debug"]
   ```

2. Build with Docker:
   ```bash
   docker build -t driver-app .
   docker run -v $(pwd)/bin:/app/bin driver-app
   ```

## Option 4: Use Online Build Services

- **AppVeyor**: Free for open source
- **GitHub Actions**: Free for public repos
- **GitLab CI**: Free tier available
- **Bitrise**: Free tier available

## Manual APK Creation (Advanced)

If you have Android Studio:

1. Create new Android project
2. Add Python/Kivy support using Chaquopy plugin
3. Copy Python files to assets
4. Build APK in Android Studio
"""
    
    with open("ANDROID_BUILD_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)
    
    print("Created ANDROID_BUILD_INSTRUCTIONS.md")
    print("See the file for detailed Android build options")

def create_desktop_version():
    """Create a desktop version for testing"""
    print("\nCreating desktop version...")
    
    # Create desktop launcher
    desktop_script = """#!/usr/bin/env python3
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Kivy window size for desktop
os.environ['KIVY_WINDOW'] = 'pygame'
os.environ['KIVY_WINDOW_SIZE'] = '800x600'

try:
    from main import MicrosearchApp
    MicrosearchApp().run()
except Exception as e:
    print(f"Error starting app: {e}")
    input("Press Enter to exit...")
"""
    
    with open("run_desktop.py", "w") as f:
        f.write(desktop_script)
    
    print("Created run_desktop.py")
    print("To run desktop version: python run_desktop.py")

def main():
    """Main build function"""
    print("Microsearch Driver Capture - Windows Build Helper")
    print("=" * 50)
    
    if not check_requirements():
        print("\nRequirements check failed")
        return
    
    print("\nSelect build option:")
    print("1. Create portable Python app")
    print("2. Show Android build instructions")
    print("3. Create desktop version")
    print("4. All of the above")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        create_portable_app()
    elif choice == "2":
        create_android_instructions()
    elif choice == "3":
        create_desktop_version()
    elif choice == "4":
        create_portable_app()
        create_android_instructions()
        create_desktop_version()
    else:
        print("Invalid choice")
        return
    
    print("\nBuild process completed!")
    print("\nNext steps:")
    print("1. Test the portable app: cd dist && run.bat")
    print("2. Read ANDROID_BUILD_INSTRUCTIONS.md for Android build")
    print("3. Run desktop version: python run_desktop.py")

if __name__ == "__main__":
    main()
