#!/bin/bash

# Deployment script for Spiral Dashboard
# Run as root or with sudo

set -e

# Configuration
APP_USER="www-data"
APP_GROUP="www-data"
APP_DIR="/opt/spiral"
LOG_DIR="/var/log/spiral"
ENV_FILE="/etc/default/spiral"

# Create application directory
mkdir -p $APP_DIR
chown -R $APP_USER:$APP_GROUP $APP_DIR

# Create log directory
mkdir -p $LOG_DIR
chown -R $APP_USER:$APP_GROUP $LOG_DIR

# Install system dependencies
apt-get update
apt-get install -y python3-venv python3-pip nginx

# Set up Python virtual environment
sudo -u $APP_USER python3 -m venv $APP_DIR/venv
source $APP_DIR/venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r $APP_DIR/requirements.txt
pip install gunicorn

# Copy application files
cp -r $APP_DIR/* $APP_DIR/
chown -R $APP_USER:$APP_GROUP $APP_DIR

# Set up environment file
cat > $ENV_FILE << EOL
# Spiral Dashboard Environment Variables
PYTHONPATH=$APP_DIR
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)
EOL

# Set up systemd service
cp $APP_DIR/deploy/spiral-dashboard.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable spiral-dashboard
systemctl start spiral-dashboard

# Configure Nginx
cp $APP_DIR/deploy/nginx-spiral.conf /etc/nginx/sites-available/spiral
ln -sf /etc/nginx/sites-available/spiral /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test and restart Nginx
nginx -t
systemctl restart nginx

# Set up firewall
ufw allow 'Nginx Full'
ufw enable

echo "Deployment complete! The Spiral Dashboard should now be accessible at http://your-server-ip"
echo "Next steps:"
echo "1. Set up SSL with Let's Encrypt (recommended)"
echo "2. Configure your domain name in the Nginx configuration"
echo "3. Monitor logs: journalctl -u spiral-dashboard -f"
