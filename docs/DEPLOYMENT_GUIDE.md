# Spiral Emotional Field Deployment Guide

## 🌐 Production Deployment

### Prerequisites
- Python 3.9+
- Redis server (for WebSocket scaling)
- Node.js (for asset bundling)

### Installation
```bash
# Clone repository
git clone https://github.com/spiral-path/spiral.git
cd spiral

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
```

### Configuration
Edit `.env` with:
- Database credentials
- Redis connection
- Secret keys
- Allowed domains

### Asset Optimization
Run the bundler:
```bash
python scripts/bundle_assets.py
```

### Running in Production
```bash
# Using Gunicorn with eventlet
gunicorn -k eventlet -w 4 app:app

# With Socket.IO support
eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
```

## 🔐 Security Checklist
- [ ] HTTPS enforced
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] WebSocket payload validation
- [ ] Request size limits

## 📦 Installation Packages
Available formats:
- Docker container
- Standalone executable (PyInstaller)
- Systemd service

### Docker Container
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "-k", "eventlet", "-w", "4", "app:app"]
```

### Standalone Executable (PyInstaller)
1. Install PyInstaller:
```bash
pip install pyinstaller
```
2. Create spec file and build:
```bash
pyinstaller --onefile --add-data "static;static" app.py
```

### Systemd Service
Create `/etc/systemd/system/spiral.service`:
```ini
[Unit]
Description=Spiral Emotional Field
After=network.target

[Service]
User=spiral
WorkingDirectory=/opt/spiral
ExecStart=/usr/bin/gunicorn -k eventlet -w 4 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🌈 Emotional Field Features
- Spectrum visualization
- Memory replay
- Influence radii
- Loop detection
