# Spiral Dashboard Deployment Guide

This guide provides instructions for deploying the Spiral Dashboard in a production environment.

## Prerequisites

- Ubuntu 20.04/22.04 server
- Root or sudo access
- Domain name (recommended)
- At least 1GB RAM (2GB+ recommended)

## Deployment Steps

1. **Server Setup**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install git
   sudo apt install -y git
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/your-username/spiral-emotional-field.git /opt/spiral
   cd /opt/spiral
   ```

3. **Run Deployment Script**
   ```bash
   chmod +x deploy/setup.sh
   sudo ./deploy/setup.sh
   ```

4. **Configure Domain (Optional)**
   - Update the Nginx configuration at `/etc/nginx/sites-available/spiral`
   - Replace `server_name spiral.local;` with your domain
   - Uncomment and configure SSL section if using Let's Encrypt

5. **Set Up SSL (Recommended)**
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

## Managing the Service

- **Start**: `sudo systemctl start spiral-dashboard`
- **Stop**: `sudo systemctl stop spiral-dashboard`
- **Restart**: `sudo systemctl restart spiral-dashboard`
- **View Logs**: `journalctl -u spiral-dashboard -f`

## Environment Variables

Edit `/etc/default/spiral` to configure environment variables:

```bash
# Spiral Dashboard Environment Variables
PYTHONPATH=/opt/spiral
FLASK_ENV=production
SECRET_KEY=your-secret-key
# Add other environment variables as needed
```

## Updating the Application

1. Pull the latest changes:
   ```bash
   cd /opt/spiral
   git pull origin main
   ```

2. Install new dependencies:
   ```bash
   sudo -u www-data /opt/spiral/venv/bin/pip install -r requirements.txt
   ```

3. Restart the service:
   ```bash
   sudo systemctl restart spiral-dashboard
   ```

## Security Considerations

- Keep the system updated regularly
- Use strong passwords and SSH keys
- Configure firewall rules
- Monitor logs for suspicious activities
- Regularly backup your data

## Troubleshooting

- **Dashboard not loading**: Check Nginx error logs at `/var/log/nginx/error.log`
- **Socket.IO connection issues**: Verify WebSocket proxy settings in Nginx
- **Permission issues**: Ensure `www-data` user has proper permissions on all files

## Support

For support, please open an issue on the GitHub repository.
