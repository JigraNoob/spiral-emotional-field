const promClient = require('prometheus-client');
const axios = require('axios');
const os = require('os');
const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');
dotenv.config();

// Initialize Prometheus metrics
const register = new promClient.Registry();

// Custom metrics
const diskIoMetrics = new promClient.Gauge({
    name: 'disk_io_operations',
    help: 'Disk I/O operations per second',
    labelNames: ['operation', 'device']
});

const apiRateLimitMetrics = new promClient.Gauge({
    name: 'api_rate_limit_usage',
    help: 'API rate limit usage',
    labelNames: ['service', 'endpoint']
});

const userBehaviorMetrics = new promClient.Gauge({
    name: 'user_behavior',
    help: 'User behavior metrics',
    labelNames: ['metric', 'type']
});

const thirdPartyServiceMetrics = new promClient.Gauge({
    name: 'third_party_service_health',
    help: 'Health of third-party services',
    labelNames: ['service', 'metric']
});

const appDowntimeMetrics = new promClient.Counter({
    name: 'app_downtime_seconds',
    help: 'Total downtime in seconds'
});

class MetricCollector {
    constructor() {
        // Register all metrics
        register.registerMetric(diskIoMetrics);
        register.registerMetric(apiRateLimitMetrics);
        register.registerMetric(userBehaviorMetrics);
        register.registerMetric(thirdPartyServiceMetrics);
        register.registerMetric(appDowntimeMetrics);

        // Start metrics collection
        this.startMetricsCollection();
    }

    // Track disk I/O operations
    async trackDiskIo() {
        const stats = fs.statSync('/');
        const ioStats = {
            read: stats.blksize * stats.blocks,
            write: stats.blksize * stats.blocks
        };

        Object.entries(ioStats).forEach(([operation, value]) => {
            diskIoMetrics.labels(operation, 'root').set(value);
        });
    }

    // Track API rate limits
    async trackApiRateLimits() {
        const services = process.env.API_SERVICES.split(',');
        
        for (const service of services) {
            try {
                const response = await axios.get(`https://${service}/rate-limit`);
                const { limit, remaining, reset } = response.data;
                
                apiRateLimitMetrics.labels(service, 'requests').set(remaining);
                apiRateLimitMetrics.labels(service, 'limit').set(limit);
                apiRateLimitMetrics.labels(service, 'reset').set(reset);
            } catch (error) {
                console.error(`Failed to get rate limit for ${service}:`, error);
            }
        }
    }

    // Track user behavior
    async trackUserBehavior() {
        // Example user behavior metrics
        userBehaviorMetrics.labels('sessions', 'active').set(this.getActiveSessions());
        userBehaviorMetrics.labels('actions', 'per_minute').set(this.getActionsPerMinute());
        userBehaviorMetrics.labels('engagement', 'time').set(this.getAverageSessionDuration());
    }

    // Get active sessions
    getActiveSessions() {
        // Implementation depends on your session management
        return 100; // Example value
    }

    // Get actions per minute
    getActionsPerMinute() {
        // Implementation depends on your action tracking
        return 500; // Example value
    }

    // Get average session duration
    getAverageSessionDuration() {
        // Implementation depends on your session tracking
        return 1800; // Example value in seconds
    }

    // Track third-party services
    async trackThirdPartyServices() {
        const services = process.env.THIRD_PARTY_SERVICES.split(',');
        
        for (const service of services) {
            try {
                const response = await axios.get(`https://${service}/health`);
                const { status, latency, errors } = response.data;
                
                thirdPartyServiceMetrics.labels(service, 'status').set(status === 'healthy' ? 1 : 0);
                thirdPartyServiceMetrics.labels(service, 'latency').set(latency);
                thirdPartyServiceMetrics.labels(service, 'errors').set(errors);
            } catch (error) {
                console.error(`Failed to check health of ${service}:`, error);
                thirdPartyServiceMetrics.labels(service, 'status').set(0);
            }
        }
    }

    // Track app downtime
    async trackAppDowntime() {
        // Implementation depends on your health check
        const isHealthy = await this.checkAppHealth();
        if (!isHealthy) {
            appDowntimeMetrics.inc();
        }
    }

    // Check app health
    async checkAppHealth() {
        try {
            const response = await axios.get('/health');
            return response.data.status === 'healthy';
        } catch (error) {
            return false;
        }
    }

    // Start metrics collection
    startMetricsCollection() {
        // Track disk I/O every 5 seconds
        setInterval(() => this.trackDiskIo(), 5000);
        
        // Track API rate limits every minute
        setInterval(() => this.trackApiRateLimits(), 60000);
        
        // Track user behavior every 30 seconds
        setInterval(() => this.trackUserBehavior(), 30000);
        
        // Track third-party services every minute
        setInterval(() => this.trackThirdPartyServices(), 60000);
        
        // Track app downtime every 10 seconds
        setInterval(() => this.trackAppDowntime(), 10000);
    }

    // Get all metrics
    async getMetrics() {
        return await register.metrics();
    }
}

module.exports = MetricCollector;
