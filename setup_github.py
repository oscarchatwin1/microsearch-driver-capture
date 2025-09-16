#!/usr/bin/env python3
"""
GitHub Setup Script for Microsearch Driver Capture
Helps set up Git repository and push to GitHub
"""

import os
import subprocess
import sys
from pathlib import Path

def check_git():
    """Check if Git is installed"""
    try:
        result = subprocess.run(['git', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"Git available: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Git not found. Please install Git from https://git-scm.com/")
        return False

def init_git_repo():
    """Initialize Git repository"""
    print("\nInitializing Git repository...")
    
    try:
        # Initialize git repo
        subprocess.run(['git', 'init'], check=True)
        print("Git repository initialized")
        
        # Create .gitignore
        gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Buildozer
.bin/
.buildozer/

# Android
bin/
*.apk

# Database
*.db
*.sqlite3

# Logs
*.log

# Config (keep templates, ignore actual credentials)
# config.json
# dropdown_config.json
"""
        
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("Created .gitignore")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error initializing Git: {e}")
        return False

def create_readme():
    """Create comprehensive README for GitHub"""
    readme_content = """# Microsearch Driver Capture

An Android app for capturing driver sample data offline and syncing to MySQL when connected to allowed WiFi networks or Ethernet.

## Quick Start

### Download APK (Easiest)
1. Go to [Releases](../../releases) or [Actions](../../actions)
2. Download the latest APK
3. Install on Android 5+ device

### Build from Source
```bash
# Using WSL (Windows)
wsl --install
wsl
sudo apt install python3 python3-pip openjdk-8-jdk
pip3 install buildozer
buildozer android debug

# Using Docker
docker build -t microsearch-driver .
docker run --rm -v $(pwd)/bin:/app/bin microsearch-driver
```

## Features

- **Offline Capture**: Store sample data locally in SQLite database
- **Connection-Gated Sync**: Only sync when connected to allowed WiFi SSIDs or Ethernet
- **Direct MySQL Sync**: Upload data directly to on-site MySQL database
- **Validation**: Client-side validation for temperatures, dates, and required fields
- **Auto-increment**: Per-day sample number auto-increment with duplicate prevention
- **Dropdown Fields**: Configurable dropdown fields populated from database

## Development

### Prerequisites
- Python 3.7+
- Kivy
- PyMySQL
- Buildozer (for Android builds)

### Setup
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/microsearch-driver-capture.git
cd microsearch-driver-capture

# Install dependencies
pip install kivy pymysql

# Run desktop version
python main.py

# Setup MySQL database
python launch.py --setup-mysql

# Setup dropdown tables
python launch.py --setup-dropdowns
```

### Configuration
Edit `config.json`:
```json
{
  "allowed_ssids": ["MicrosearchOps", "MicrosearchGuest"],
  "allow_ethernet": true,
  "mysql": {
    "host": "192.168.1.10",
    "port": 3306,
    "user": "mobile",
    "password": "your_password",
    "db": "microsearch"
  }
}
```

## Data Model

### Sample Fields
- `id`: UUID (client-generated, primary key)
- `description`: Sample description (required)
- `size_kg`: Weight in kilograms
- `use_by_date`: Expiry date (YYYY-MM-DD)
- `pack_code`: Package/batch code
- `bird_temp_c`: Bird temperature (-5.0 to 20.0°C)
- `customer`: Customer name
- `retailer`: Retailer name (required)
- `supplier`: Supplier name (default: Flixton)
- `code`: Product code (default: GB S011)
- `sample_number`: Sample number (auto-increment per day)
- `price_gbp`: Price in GBP (>= 0)
- `van_temp_c`: Van temperature (-5.0 to 20.0°C)
- `device_id`: Device identifier
- `driver_id`: Driver identifier

## Build Options

### Android APK
- **Minimum**: Android 5.0 (API 21)
- **Target**: Android 9.0 (API 28)
- **Architecture**: ARM (armeabi-v7a)

### Desktop Version
- Windows, Linux, macOS
- Same functionality as Android
- Perfect for testing

## Documentation

- [Installation Guide](ANDROID_INSTALL.md)
- [Build Guide](ANDROID_BUILD_GUIDE.md)
- [SQL Setup](SQL_SETUP.md)

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Check [Issues](../../issues) for known problems
- Create new issue for bugs or feature requests
- See [ANDROID_INSTALL.md](ANDROID_INSTALL.md) for troubleshooting

## Architecture

```
/mobile
  main.py              # Kivy app (screens, navigation)
  storage.py           # SQLite init + CRUD + validation
  syncer.py            # SSID check + MySQL upsert
  dropdown_manager.py  # Dropdown field management
  dropdown_widget.py   # Custom dropdown widget
  config.json          # SSIDs + MySQL creds + defaults
  dropdown_config.json # Dropdown field configuration
  buildozer.spec       # Android build config
  launch.py            # Launcher script
  *.sql               # Database setup scripts
```
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    print("Updated README.md for GitHub")

def create_license():
    """Create MIT License file"""
    license_content = """MIT License

Copyright (c) 2024 Microsearch Driver Capture

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    with open('LICENSE', 'w') as f:
        f.write(license_content)
    
    print("Created LICENSE file")

def show_git_commands():
    """Show Git commands for pushing to GitHub"""
    print("\n" + "="*60)
    print("GITHUB SETUP COMMANDS")
    print("="*60)
    print()
    print("1. Create a new repository on GitHub:")
    print("   - Go to https://github.com/new")
    print("   - Repository name: microsearch-driver-capture")
    print("   - Description: Android app for driver sample data capture")
    print("   - Make it Public or Private")
    print("   - Don't initialize with README (we already have one)")
    print()
    print("2. Add files to Git:")
    print("   git add .")
    print()
    print("3. Commit files:")
    print("   git commit -m 'Initial commit: Microsearch Driver Capture app'")
    print()
    print("4. Add GitHub remote (replace YOUR_USERNAME):")
    print("   git remote add origin https://github.com/YOUR_USERNAME/microsearch-driver-capture.git")
    print()
    print("5. Push to GitHub:")
    print("   git branch -M main")
    print("   git push -u origin main")
    print()
    print("6. After pushing, GitHub Actions will automatically build the APK!")
    print("   - Go to Actions tab to see the build")
    print("   - Download APK from the artifacts")
    print()
    print("="*60)

def main():
    """Main setup function"""
    print("Microsearch Driver Capture - GitHub Setup")
    print("=" * 45)
    
    if not check_git():
        return
    
    print("\nSetting up repository...")
    
    # Initialize Git repo
    if not init_git_repo():
        return
    
    # Create GitHub-specific files
    create_readme()
    create_license()
    
    print("\nRepository setup complete!")
    show_git_commands()
    
    print("\nNext steps:")
    print("1. Create repository on GitHub")
    print("2. Run the Git commands shown above")
    print("3. GitHub Actions will build your APK automatically!")

if __name__ == "__main__":
    main()


