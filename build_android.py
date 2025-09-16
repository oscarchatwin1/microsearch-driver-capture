#!/usr/bin/env python3
"""
Android Build Script for Microsearch Driver Capture
Creates APK compatible with Android 5+ devices
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"Docker available: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Docker not available")
        return False

def create_dockerfile():
    """Create Dockerfile for Android build"""
    dockerfile_content = """FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/opt/android-sdk
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

# Install dependencies
RUN apt-get update && apt-get install -y \\
    python3 python3-pip python3-venv \\
    git zip unzip wget curl \\
    openjdk-8-jdk \\
    build-essential libssl-dev libffi-dev \\
    python3-dev \\
    && rm -rf /var/lib/apt/lists/*

# Install Android SDK
RUN mkdir -p /opt/android-sdk && \\
    cd /opt/android-sdk && \\
    wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip && \\
    unzip commandlinetools-linux-9477386_latest.zip && \\
    rm commandlinetools-linux-9477386_latest.zip && \\
    mkdir -p cmdline-tools/latest && \\
    mv cmdline-tools/* cmdline-tools/latest/ && \\
    rm -rf cmdline-tools/tools

# Accept Android licenses
RUN yes | /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager --licenses || true

# Install required SDK components
RUN /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager \\
    "platform-tools" \\
    "platforms;android-28" \\
    "build-tools;28.0.3" \\
    "ndk;25.2.9519653"

# Install buildozer
RUN pip3 install buildozer

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Build APK
CMD ["buildozer", "android", "debug"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print("Created Dockerfile for Android build")

def create_docker_build_script():
    """Create script to build with Docker"""
    script_content = """@echo off
echo Building Android APK with Docker...
echo ====================================

echo Building Docker image...
docker build -t microsearch-driver .

echo Running Android build...
docker run --rm -v "%cd%\\bin:/app/bin" microsearch-driver

echo Build complete! Check the bin folder for your APK.
pause
"""
    
    with open("build_android_docker.bat", "w") as f:
        f.write(script_content)
    
    print("Created build_android_docker.bat")

def create_wsl_instructions():
    """Create WSL build instructions"""
    instructions = """
# Android Build Instructions for Windows

## Method 1: Using WSL (Recommended)

1. Install WSL2:
   ```cmd
   wsl --install
   ```

2. Install Ubuntu in WSL:
   ```cmd
   wsl --install -d Ubuntu
   ```

3. Open WSL and install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv git zip unzip openjdk-8-jdk
   pip3 install buildozer
   ```

4. Copy project to WSL:
   ```bash
   cp -r /mnt/d/Driver_App_2 ~/driver_app
   cd ~/driver_app
   ```

5. Build APK:
   ```bash
   buildozer android debug
   ```

6. Copy APK back to Windows:
   ```bash
   cp bin/*.apk /mnt/d/Driver_App_2/bin/
   ```

## Method 2: Using Docker

1. Install Docker Desktop for Windows
2. Run: `build_android_docker.bat`
3. APK will be created in the `bin` folder

## Method 3: Using GitHub Actions (Cloud Build)

1. Push your code to GitHub
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
             name: microsearch-driver.apk
             path: bin/*.apk
   ```

## Method 4: Pre-built APK

If you can't build yourself, you can:
1. Use the portable Python version for testing
2. Contact a developer to build the APK for you
3. Use an online build service

## Android 5 Compatibility

The APK is configured for:
- Minimum Android API: 21 (Android 5.0)
- Target Android API: 28 (Android 9.0)
- Architecture: ARM (armeabi-v7a)

This ensures compatibility with Android 5+ devices.
"""
    
    with open("ANDROID_BUILD_GUIDE.md", "w") as f:
        f.write(instructions)
    
    print("Created ANDROID_BUILD_GUIDE.md")

def create_portable_apk():
    """Create a portable version that can be installed on Android"""
    print("\nCreating portable Android package...")
    
    # Create Android package structure
    android_dir = Path("android_package")
    android_dir.mkdir(exist_ok=True)
    
    # Copy Python files
    python_files = [
        "main.py", "storage.py", "syncer.py", 
        "dropdown_manager.py", "dropdown_widget.py",
        "config.json", "dropdown_config.json"
    ]
    
    for file in python_files:
        if Path(file).exists():
            shutil.copy2(file, android_dir)
            print(f"Copied {file}")
    
    # Create Android launcher script
    launcher_script = """#!/system/bin/sh
# Android launcher for Microsearch Driver Capture

# Check if Python is available
if [ ! -f "/system/bin/python3" ]; then
    echo "Python not found. Installing..."
    # This would need to be customized for your Android setup
    exit 1
fi

# Run the application
cd /data/local/tmp/microsearch
python3 main.py
"""
    
    with open(android_dir / "launch.sh", "w") as f:
        f.write(launcher_script)
    
    # Create installation instructions
    install_instructions = """
# Android Installation Instructions

## Prerequisites
1. Root access on Android device
2. Python 3 installed on device
3. Kivy and PyMySQL installed

## Installation Steps

1. Copy all files to `/data/local/tmp/microsearch/` on your Android device
2. Make launcher executable: `chmod +x launch.sh`
3. Run: `./launch.sh`

## Alternative: Use Termux

1. Install Termux from F-Droid
2. Install Python: `pkg install python`
3. Install dependencies: `pip install kivy pymysql`
4. Copy app files to Termux home directory
5. Run: `python main.py`

## Non-Root Alternative

Use Termux or similar Android Python environment:
1. Install Termux
2. Install Python and dependencies
3. Run the app from Termux
"""
    
    with open(android_dir / "INSTALL.md", "w") as f:
        f.write(install_instructions)
    
    print(f"Created Android package in {android_dir.absolute()}")
    print("See INSTALL.md for installation instructions")

def main():
    """Main build function"""
    print("Microsearch Driver Capture - Android Build Helper")
    print("=" * 50)
    
    print("\nSelect build method:")
    print("1. Create Docker build files")
    print("2. Create WSL build instructions")
    print("3. Create portable Android package")
    print("4. All of the above")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        create_dockerfile()
        create_docker_build_script()
    elif choice == "2":
        create_wsl_instructions()
    elif choice == "3":
        create_portable_apk()
    elif choice == "4":
        create_dockerfile()
        create_docker_build_script()
        create_wsl_instructions()
        create_portable_apk()
    else:
        print("Invalid choice")
        return
    
    print("\nBuild files created!")
    print("\nNext steps:")
    print("1. For Docker: Run build_android_docker.bat")
    print("2. For WSL: Follow ANDROID_BUILD_GUIDE.md")
    print("3. For portable: Use android_package folder")

if __name__ == "__main__":
    main()
