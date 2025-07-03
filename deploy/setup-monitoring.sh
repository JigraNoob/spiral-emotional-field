#!/bin/bash

# Spiral Monitoring Setup Script
# Run as root or with sudo

set -e

# Colors for Spiral resonance
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌀 Beginning Spiral Monitoring Attunement...${NC}"

# Verify root privileges
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}⟳ Elevating to root for monitoring attunement...${NC}"
    exec sudo -E "$0" "$@"
fi

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo -e "${BLUE}🐳 Installing Docker...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    usermod -aG docker $SUDO_USER
    systemctl enable --now docker
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo -e "${BLUE}📦 Installing Docker Compose...${NC}"
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Create monitoring directory structure
echo -e "${BLUE}📂 Creating monitoring directory structure...${NC}"
MONITORING_DIR="/opt/spiral/monitoring"
mkdir -p $MONITORING_DIR/{prometheus,grafana,alertmanager,blackbox}

# Copy configuration files
echo -e "${BLUE}📝 Copying configuration files...${NC}"
cp -r $(dirname "$0")/monitoring/* $MONITORING_DIR/

# Set permissions
echo -e "${BLUE}🔒 Setting permissions...${NC}"
chown -R 472:472 $MONITORING_DIR/grafana
chmod -R 775 $MONITORING_DIR

# Create Docker network if it doesn't exist
if ! docker network inspect spiral-monitoring &> /dev/null; then
    echo -e "${BLUE}🌐 Creating Docker network...${NC}"
    docker network create spiral-monitoring
fi

# Start monitoring stack
echo -e "${BLUE}🚀 Starting monitoring stack...${NC}"
cd $MONITORING_DIR
docker-compose up -d

# Wait for services to start
echo -e "${BLUE}⏳ Waiting for services to initialize...${NC}"
sleep 10

# Create Grafana data source
echo -e "${BLUE}📊 Configuring Grafana...${NC}"
until curl -s http://localhost:3000/api/health &> /dev/null; do
    sleep 2
echo -n "."
done

# Import Grafana dashboard
curl -X POST \
  -H "Content-Type: application/json" \
  -d @$MONITORING_DIR/grafana/provisioning/dashboards/spiral-dashboard.json \
  "http://admin:spiral_breath_123@localhost:3000/api/dashboards/db"

echo -e "\n${GREEN}✅ Spiral Monitoring Stack Successfully Attuned!${NC}"
echo -e "\n${BLUE}🔍 Access the monitoring interfaces at:${NC}"
echo -e "- Grafana: ${GREEN}http://localhost:3000${NC} (admin/spiral_breath_123)"
echo -e "- Prometheus: ${GREEN}http://localhost:9090${NC}"
echo -e "- Node Exporter: ${GREEN}http://localhost:9100/metrics${NC}"
echo -e "- cAdvisor: ${GREEN}http://localhost:8080${NC}"
echo -e "\n${YELLOW}📌 Remember to change the default credentials!${NC}"

# Add Spiral metrics endpoint to Prometheus
cat >> $MONITORING_DIR/prometheus/prometheus.yml <<EOL

  # Spiral Dashboard Metrics
  - job_name: 'spiral-dashboard'
    static_configs:
      - targets: ['host.docker.internal:8000']
    metrics_path: /metrics
    scheme: http
    scrape_interval: 10s
    scrape_timeout: 5s

  # Spiral Attunement System
  - job_name: 'spiral-attunement'
    static_configs:
      - targets: ['host.docker.internal:8000']
    metrics_path: /attunement-metrics
    scrape_interval: 15s
EOL

# Restart Prometheus to apply changes
docker-compose restart prometheus

echo -e "\n${GREEN}✨ Spiral monitoring is now attuned to your breath.${NC}"
