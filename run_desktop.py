#!/usr/bin/env python3
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
