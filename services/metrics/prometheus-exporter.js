const promClient = require('prom-client');
const { PerformanceObserver, performance } = require('perf_hooks');
const memoryUsage = require('memory-usage');

// Initialize Prometheus metrics
const register = new promClient.Registry();

// Add default metrics
promClient.collectDefaultMetrics({ register });

// Custom metrics
const networkRequestDuration = new promClient.Histogram({
    name: 'network_request_duration_seconds',
    help: 'Duration of network requests in seconds',
    labelNames: ['endpoint', 'method', 'status'],
    buckets: [0.1, 0.5, 1, 2, 5]
});

const apiResponseDuration = new promClient.Histogram({
    name: 'api_response_duration_seconds',
    help: 'Duration of API responses in seconds',
    labelNames: ['endpoint', 'status'],
    buckets: [0.1, 0.5, 1, 2, 5]
});

const memoryUsageMetrics = new promClient.Gauge({
    name: 'memory_usage_bytes',
    help: 'Memory usage in bytes',
    labelNames: ['type']
});

const domMetrics = new promClient.Gauge({
    name: 'dom_complexity',
    help: 'DOM complexity metrics',
    labelNames: ['type']
});

const audioLatency = new promClient.Histogram({
    name: 'audio_processing_latency_seconds',
    help: 'Audio processing latency in seconds',
    buckets: [0.01, 0.05, 0.1, 0.5, 1]
});

const websocketMetrics = new promClient.Gauge({
    name: 'websocket_connections',
    help: 'WebSocket connection metrics',
    labelNames: ['type']
});

class PrometheusExporter {
    constructor() {
        // Register all metrics
        register.registerMetric(networkRequestDuration);
        register.registerMetric(apiResponseDuration);
        register.registerMetric(memoryUsageMetrics);
        register.registerMetric(domMetrics);
        register.registerMetric(audioLatency);
        register.registerMetric(websocketMetrics);

        // Start metrics collection
        this.startMetricsCollection();
    }

    // Track network requests
    trackNetworkRequest(endpoint, method, duration, status) {
        networkRequestDuration.labels(endpoint, method, status).observe(duration);
    }

    // Track API responses
    trackApiResponse(endpoint, duration, status) {
        apiResponseDuration.labels(endpoint, status).observe(duration);
    }

    // Track memory usage
    trackMemoryUsage() {
        const usage = memoryUsage();
        memoryUsageMetrics.labels('heap_used').set(usage.heapUsed);
        memoryUsageMetrics.labels('heap_total').set(usage.heapTotal);
        memoryUsageMetrics.labels('external').set(usage.external);
    }

    // Track DOM complexity
    trackDOMMetrics() {
        const metrics = {
            elements: document.getElementsByTagName('*').length,
            listeners: this.countEventListeners(),
            styleSheets: document.styleSheets.length,
            images: document.images.length,
            scripts: document.scripts.length
        };

        Object.entries(metrics).forEach(([key, value]) => {
            domMetrics.labels(key).set(value);
        });
    }

    // Count event listeners
    countEventListeners() {
        let count = 0;
        const walk = (node) => {
            if (node.nodeType === 1) {
                const eventListeners = Object.getOwnPropertyNames(node).filter(
                    prop => prop.startsWith('on')
                );
                count += eventListeners.length;
                
                node.childNodes.forEach(walk);
            }
        };
        
        walk(document);
        return count;
    }

    // Track audio performance
    trackAudioPerformance(audioContext) {
        const latency = audioContext.getOutputTimestamp().contextTime;
        audioLatency.observe(latency);
    }

    // Track WebSocket connections
    trackWebSocketConnection(type, count) {
        websocketMetrics.labels(type).set(count);
    }

    // Start metrics collection
    startMetricsCollection() {
        // Track DOM metrics every 5 seconds
        setInterval(() => this.trackDOMMetrics(), 5000);
        
        // Track memory usage every 10 seconds
        setInterval(() => this.trackMemoryUsage(), 10000);
    }

    // Get all metrics
    async getMetrics() {
        return await register.metrics();
    }
}

module.exports = PrometheusExporter;
