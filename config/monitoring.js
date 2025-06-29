const dotenv = require('dotenv');
dotenv.config();

module.exports = {
    sentry: {
        enabled: process.env.SENTRY_ENABLED === 'true',
        dsn: process.env.SENTRY_DSN,
        environment: process.env.NODE_ENV || 'development',
        sampleRate: parseFloat(process.env.SENTRY_SAMPLE_RATE) || 1.0
    },
    datadog: {
        enabled: process.env.DATADOG_ENABLED === 'true',
        apiKey: process.env.DATADOG_API_KEY,
        appKey: process.env.DATADOG_APP_KEY,
        tags: {
            environment: process.env.NODE_ENV || 'development',
            service: 'spiral-app',
            version: process.env.APP_VERSION || '1.0.0'
        }
    },
    performance: {
        thresholds: {
            network: {
                maxResponseTime: 2000, // 2 seconds
                maxContentSize: 1024 * 1024 // 1MB
            },
            api: {
                maxResponseTime: 1500, // 1.5 seconds
                errorThreshold: 0.05 // 5% error rate
            },
            memory: {
                maxHeapUsed: 1024 * 1024 * 500, // 500MB
                maxExternal: 1024 * 1024 * 100 // 100MB
            },
            dom: {
                maxElements: 1000,
                maxEventListeners: 500,
                maxStyleSheets: 20,
                maxImages: 50,
                maxScripts: 20
            },
            audio: {
                maxLatency: 0.1, // 100ms
                minSampleRate: 44100
            },
            websocket: {
                maxConnectionTime: 5000, // 5 seconds
                maxErrorRate: 0.1 // 10% error rate
            }
        },
        monitoringInterval: {
            dom: 5000, // 5 seconds
            memory: 10000, // 10 seconds
            audio: 1000, // 1 second
            websocket: 2000 // 2 seconds
        },
        alertThresholds: {
            warning: 0.8, // 80% of threshold
            critical: 0.95 // 95% of threshold
        }
    }
};
