#!/usr/bin/env python3
"""
Launcher script for Microsearch Driver Capture app
Provides easy startup options and environment checks
"""

import sys
import os
import subprocess
import json
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['kivy', 'pymysql']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    missing = check_dependencies()
    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
            print("Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install dependencies: {e}")
            return False
    return True

def check_config():
    """Check if config.json exists and is valid"""
    config_path = Path('config.json')
    if not config_path.exists():
        print("❌ config.json not found!")
        return False
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Check required fields
        required_fields = ['allowed_ssids', 'mysql', 'defaults']
        for field in required_fields:
            if field not in config:
                print(f"❌ Missing required field '{field}' in config.json")
                return False
        
        # Check MySQL config
        mysql_config = config['mysql']
        mysql_fields = ['host', 'port', 'user', 'password', 'db']
        for field in mysql_fields:
            if field not in mysql_config:
                print(f"❌ Missing MySQL field '{field}' in config.json")
                return False
        
        print("✅ Configuration file is valid")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config.json: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading config.json: {e}")
        return False

def run_tests():
    """Run the test suite"""
    print("🧪 Running test suite...")
    try:
        result = subprocess.run([sys.executable, 'test_app.py'], 
                              capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Tests timed out")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def run_app():
    """Run the main Kivy application"""
    print("🚀 Starting Microsearch Driver Capture app...")
    try:
        subprocess.run([sys.executable, 'main.py'])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")

def show_menu():
    """Show interactive menu"""
    while True:
        print("\n" + "="*50)
        print("Microsearch Driver Capture - Launcher")
        print("="*50)
        print("1. Run App")
        print("2. Run Tests")
        print("3. Check Dependencies")
        print("4. Install Dependencies")
        print("5. Check Configuration")
        print("6. Setup MySQL Database")
        print("7. Setup Dropdown Tables")
        print("8. Build Android APK")
        print("9. Windows Build Helper")
        print("10. Exit")
        print("-"*50)
        
        choice = input("Select option (1-10): ").strip()
        
        if choice == '1':
            if check_config():
                run_app()
            else:
                print("Please fix configuration issues first")
        
        elif choice == '2':
            run_tests()
        
        elif choice == '3':
            missing = check_dependencies()
            if missing:
                print(f"❌ Missing dependencies: {', '.join(missing)}")
            else:
                print("✅ All dependencies are installed")
        
        elif choice == '4':
            install_dependencies()
        
        elif choice == '5':
            check_config()
        
        elif choice == '6':
            setup_mysql()
        
        elif choice == '7':
            setup_dropdown_tables()
        
        elif choice == '8':
            build_apk()
        
        elif choice == '9':
            windows_build_helper()
        
        elif choice == '10':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please select 1-10.")

def setup_dropdown_tables():
    """Setup dropdown data tables"""
    print("📋 Setting up dropdown tables...")
    
    try:
        result = subprocess.run([sys.executable, '-c', '''
import pymysql
import json

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

mysql_config = config["mysql"]

# Connect to MySQL
connection = pymysql.connect(
    host=mysql_config["host"],
    port=mysql_config["port"],
    user=mysql_config["user"],
    password=mysql_config["password"],
    database=mysql_config["db"],
    charset="utf8mb4"
)

# Read and execute SQL file
with open("create_dropdown_tables.sql", "r") as f:
    sql_script = f.read()

cursor = connection.cursor()
for statement in sql_script.split(";"):
    if statement.strip():
        cursor.execute(statement)

connection.commit()
connection.close()
print("✅ Dropdown tables created successfully")
        '''], capture_output=True, text=True, timeout=60)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Dropdown setup timed out")
        return False
    except Exception as e:
        print(f"❌ Error running dropdown setup: {e}")
        return False

def windows_build_helper():
    """Run Windows build helper"""
    print("🖥️  Running Windows build helper...")
    
    try:
        result = subprocess.run([sys.executable, 'build_windows.py'], 
                              capture_output=True, text=True, timeout=120)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Windows build helper timed out")
        return False
    except Exception as e:
        print(f"❌ Error running Windows build helper: {e}")
        return False

def setup_mysql():
    """Setup MySQL database and tables"""
    print("🗄️ Setting up MySQL database...")
    
    try:
        result = subprocess.run([sys.executable, 'setup_mysql.py'], 
                              capture_output=True, text=True, timeout=60)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ MySQL setup timed out")
        return False
    except Exception as e:
        print(f"❌ Error running MySQL setup: {e}")
        return False

def build_apk():
    """Build Android APK using Buildozer"""
    print("🔨 Building Android APK...")
    
    # Check if buildozer is installed
    try:
        subprocess.run(['buildozer', '--version'], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Buildozer not found. Installing...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'buildozer'])
            print("✅ Buildozer installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Buildozer: {e}")
            return
    
    # Build APK
    try:
        print("Building APK (this may take several minutes)...")
        subprocess.run(['buildozer', 'android', 'debug'], check=True)
        print("✅ APK built successfully!")
        print("APK location: bin/microsearchdriver-1.0-debug.apk")
    except subprocess.CalledProcessError as e:
        print(f"❌ APK build failed: {e}")
    except KeyboardInterrupt:
        print("\n❌ Build cancelled by user")

def main():
    """Main launcher function"""
    print("Microsearch Driver Capture - Launcher Script")
    print("Python version:", sys.version)
    print("Working directory:", os.getcwd())
    
    # Check if we're in the right directory
    required_files = ['main.py', 'storage.py', 'syncer.py', 'config.json']
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please run this script from the project directory")
        return
    
    # Check command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--test', '-t']:
            run_tests()
        elif arg in ['--app', '-a']:
            if check_config():
                run_app()
        elif arg in ['--build', '-b']:
            build_apk()
        elif arg in ['--setup-mysql', '-m']:
            setup_mysql()
        elif arg in ['--setup-dropdowns', '-d']:
            setup_dropdown_tables()
        elif arg in ['--windows-build', '-w']:
            windows_build_helper()
        elif arg in ['--check', '-c']:
            check_dependencies()
            check_config()
        elif arg in ['--install', '-i']:
            install_dependencies()
        elif arg in ['--help', '-h']:
            show_help()
        else:
            print(f"❌ Unknown argument: {arg}")
            show_help()
    else:
        # Interactive mode
        show_menu()

def show_help():
    """Show help message"""
    print("""
Microsearch Driver Capture - Launcher Script

Usage: python launch.py [OPTION]

Options:
  --app, -a            Run the main application
  --test, -t            Run test suite
  --build, -b           Build Android APK
  --setup-mysql, -m     Setup MySQL database and tables
  --setup-dropdowns, -d Setup dropdown data tables
  --windows-build, -w   Windows build helper
  --check, -c           Check dependencies and configuration
  --install, -i         Install missing dependencies
  --help, -h            Show this help message

Interactive mode:
  Run without arguments for interactive menu

Examples:
  python launch.py --app
  python launch.py --test
  python launch.py --setup-mysql
  python launch.py --setup-dropdowns
  python launch.py --windows-build
  python launch.py --build
""")

if __name__ == "__main__":
    main()
