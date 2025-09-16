
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
   RUN apt-get update && apt-get install -y \
       python3 python3-pip python3-venv \
       git zip unzip openjdk-8-jdk \
       build-essential libssl-dev libffi-dev \
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
