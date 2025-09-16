# Android Installation Guide

## Quick Start - Download APK

The easiest way to get the Android APK is to use the automated build:

1. **GitHub Actions Build** (Recommended):
   - Go to the Actions tab in this repository
   - Download the latest APK from the artifacts
   - Install on your Android 5+ device

2. **Manual Build** (If you have Linux/WSL):
   - Follow the instructions in `ANDROID_BUILD_GUIDE.md`
   - Use WSL or Docker to build the APK

## Android 5 Compatibility

✅ **Fully Compatible with Android 5.0+**
- Minimum API: 21 (Android 5.0)
- Target API: 28 (Android 9.0)
- Architecture: ARM (works on most devices)

## Installation Steps

1. **Enable Unknown Sources**:
   - Go to Settings > Security
   - Enable "Unknown Sources" or "Install unknown apps"

2. **Download APK**:
   - Download the APK file to your device
   - Tap the APK file to install

3. **Grant Permissions**:
   - Allow WiFi access
   - Allow network access
   - Allow storage access

## Configuration

1. **Open the app** after installation
2. **Configure MySQL connection**:
   - Go to Sync screen
   - Update `config.json` with your MySQL details
   - Or use the app's configuration screen

3. **Set up WiFi/Ethernet**:
   - Connect to allowed WiFi networks
   - Or connect via Ethernet cable
   - App will automatically detect connection type

## Features

- ✅ **Offline Capture**: Works without internet
- ✅ **WiFi/Ethernet Sync**: Flexible connection options
- ✅ **MySQL Integration**: Direct database sync
- ✅ **Dropdown Fields**: Configurable field types
- ✅ **Data Validation**: Built-in validation rules
- ✅ **Auto-increment**: Smart sample numbering

## Troubleshooting

### App Won't Install
- Check Android version (needs 5.0+)
- Enable "Unknown Sources"
- Try downloading APK again

### Sync Not Working
- Check WiFi/Ethernet connection
- Verify MySQL server is running
- Check `config.json` settings
- Use "Test MySQL Connection" button

### App Crashes
- Check device has enough storage
- Restart the app
- Check error messages in Sync screen

## Support

If you encounter issues:
1. Check the error messages in the app
2. Verify your MySQL configuration
3. Test with the desktop version first
4. Check the GitHub Issues page

## Alternative: Desktop Version

If you can't install on Android, you can:
1. Use the portable Python version
2. Run on Windows/Linux/Mac
3. Test all functionality before Android deployment

See `dist/` folder for portable version.
