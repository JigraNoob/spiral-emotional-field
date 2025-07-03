#!/bin/bash

# Test Spiral Alerting Configuration
# Validates alert rules and notification templates

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🔍 Validating Spiral Alerting Configuration...${NC}"

# Check for required tools
command -v promtool >/dev/null 2>&1 || {
    echo -e "${RED}❌ promtool not found. Please install Prometheus first.${NC}"
    exit 1
}

command -v amtool >/dev/null 2>&1 || {
    echo -e "${YELLOW}⚠️  amtool not found. Alertmanager config validation will be skipped.${NC}"
}

# Validate Prometheus alert rules
echo -e "\n${GREEN}✅ Validating Prometheus alert rules...${NC}"
promtool check rules deploy/monitoring/prometheus/alerts/spiral.rules

# Validate Alertmanager config if amtool is available
if command -v amtool >/dev/null 2>&1; then
    echo -e "\n${GREEN}✅ Validating Alertmanager configuration...${NC}"
    amtool check-config deploy/monitoring/alertmanager/config.yml
else
    echo -e "\n${YELLOW}⚠️  Skipping Alertmanager config validation (amtool not found)${NC}"
fi

# Test alert rule syntax
echo -e "\n${GREEN}🧪 Testing alert rules...${NC}"
RULES_FILE="deploy/monitoring/prometheus/alerts/spiral.rules"
ALERT_NAMES=(
    "SilenceProtocolTriggered"
    "DeferralTimeHigh"
    "SaturationApproachingLimit"
    "SaturationCritical"
    "WebSocketHeartbeatMissed"
    "ToneformAnomaly"
    "BreathCycleIrregular"
)

for alert in "${ALERT_NAMES[@]}"; do
    if grep -q "alert: $alert" "$RULES_FILE"; then
        echo -e "${GREEN}✓ Found alert rule: $alert${NC}"
    else
        echo -e "${RED}✗ Missing alert rule: $alert${NC}"
    fi
done

# Check notification templates
echo -e "\n${GREEN}📋 Checking notification templates...${NC}"
TEMPLATE_FILES=(
    "deploy/monitoring/alertmanager/templates/email.default.tmpl"
    "deploy/monitoring/alertmanager/templates/email.rhythm.tmpl"
    "deploy/monitoring/alertmanager/templates/email.resonance.tmpl"
    "deploy/monitoring/alertmanager/templates/email.critical.tmpl"
)

for template in "${TEMPLATE_FILES[@]}"; do
    if [ -f "$template" ]; then
        echo -e "${GREEN}✓ Found template: $template${NC}"
    else
        echo -e "${YELLOW}⚠️  Missing template: $template${NC}"
    fi
done

# Test webhook endpoints if configured
if grep -q "webhook_configs" "deploy/monitoring/alertmanager/config.yml"; then
    echo -e "\n${GREEN}🔌 Found webhook configurations${NC}"
    grep -A 5 "webhook_configs" "deploy/monitoring/alertmanager/config.yml" | grep -v "^--$"
else
    echo -e "\n${YELLOW}⚠️  No webhook configurations found${NC}"
fi

# Check SMTP configuration
if grep -q "smtp_" "deploy/monitoring/alertmanager/config.yml"; then
    echo -e "\n${GREEN}📧 SMTP configuration found${NC}"
    grep -A 5 "smtp_" "deploy/monitoring/alertmanager/config.yml" | grep -v "^--$"
else
    echo -e "\n${YELLOW}⚠️  No SMTP configuration found${NC}"
fi

echo -e "\n${GREEN}✨ Alerting configuration test complete!${NC}"
echo -e "${YELLOW}ℹ️  Remember to replace placeholder values in the configuration files before deployment.${NC}"
