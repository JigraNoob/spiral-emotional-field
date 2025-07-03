#!/bin/bash

# SSL Setup Script for Spiral Dashboard
# Run as root or with sudo

set -e

# Check for domain argument
if [ -z "$1" ]; then
    echo "Usage: $0 your-domain.com"
    exit 1
fi

DOMAIN="$1"
EMAIL="admin@$DOMAIN"
NGINX_CONF="/etc/nginx/sites-available/spiral"
TEMP_CONF="/tmp/nginx-temp.conf"

# Update Nginx configuration with domain
sed -i "s/server_name spiral.local;/server_name $DOMAIN;/g" $NGINX_CONF

# Install Certbot
if ! command -v certbot &> /dev/null; then
    echo "Installing Certbot..."
    apt-get update
    apt-get install -y certbot python3-certbot-nginx
fi

# Create a temporary Nginx config for HTTP challenge
cp $NGINX_CONF $TEMP_CONF
sed -i 's/listen 80;/listen 80;\n    listen [::]:80;/' $TEMP_CONF
sed -i 's/listen 443 ssl http2/# &/' $TEMP_CONF
sed -i 's/ssl_/# ssl_/g' $TEMP_CONF

# Request certificate with webroot plugin
echo "Requesting SSL certificate for $DOMAIN..."
certbot certonly --webroot \
    --webroot-path /var/www/html \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    --non-interactive

# Update Nginx configuration with SSL
cat > $NGINX_CONF << EOL
# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name $DOMAIN;

    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/$DOMAIN/chain.pem;
    
    # SSL protocols
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_stapling on;
    ssl_stapling_verify on;

    # HSTS (uncomment after testing)
    # add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;

    # Rest of your Nginx configuration
    $(tail -n +2 $TEMP_CONF)
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN;
    return 301 https://\$host\$request_uri;
}
EOL

# Test and reload Nginx
echo "Testing Nginx configuration..."
nginx -t

systemctl reload nginx

# Set up auto-renewal
echo "0 0,12 * * * root /usr/bin/certbot renew --quiet --deploy-hook 'systemctl reload nginx'" > /etc/cron.d/certbot-renew

# Verify installation
echo "SSL setup complete!"
echo "Testing SSL configuration..."
curl -I https://$DOMAIN

echo "\n✅ SSL certificate for $DOMAIN is now active"
echo "🔒 Auto-renewal is configured via cron"
echo "📝 Certificate location: /etc/letsencrypt/live/$DOMAIN/"

echo "\nNext steps:"
echo "1. Verify your dashboard is accessible at: https://$DOMAIN"
echo "2. Uncomment HSTS header in $NGINX_CONF after confirming SSL works"
echo "3. Monitor certificate renewal: journalctl -u certbot.timer -f"
