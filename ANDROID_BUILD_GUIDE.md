
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
