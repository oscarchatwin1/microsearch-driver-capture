# Microsearch Driver Capture

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
