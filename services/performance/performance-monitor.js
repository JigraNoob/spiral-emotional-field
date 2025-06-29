const axios = require('axios');
const memoryUsage = require('memory-usage');
const performance = require('performance-now');
const { PerformanceObserver, performance: perf } = require('perf_hooks');
const sentry = require('@sentry/node');
const datadog = require('datadog-metrics');

// Initialize monitoring tools
sentry.init({
    dsn: process.env.SENTRY_DSN,
    tracesSampleRate: 1.0
});

datadog.initialize({
    apiKey: process.env.DATADOG_API_KEY,
    appKey: process.env.DATADOG_APP_KEY
});

class PerformanceMonitor {
    constructor() {
        this.metrics = {
            network: {},
            api: {},
            memory: {},
            cpu: {},
            dom: {},
            js: {},
            websocket: {},
            audio: {}
        };
        
        // Initialize performance observer
        this.performanceObserver = new PerformanceObserver((entryList) => {
            entryList.getEntries().forEach(entry => {
                this.metrics.js[entry.name] = {
                    duration: entry.duration,
                    startTime: entry.startTime,
                    type: entry.entryType
                };
            });
        });
        
        this.performanceObserver.observe({
            entryTypes: ['measure', 'mark']
        });
    }

    // Network monitoring
    async measureNetworkRequest(url, method = 'GET', data = null) {
        const startTime = performance.now();
        try {
            const response = await axios({
                method,
                url,
                data,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const duration = performance.now() - startTime;
            this.metrics.network[url] = {
                duration,
                status: response.status,
                size: response.headers['content-length']
            };
            
            datadog.gauge('network.request.duration', duration, {
                url,
                method,
                status: response.status
            });
            
            return response;
        } catch (error) {
            sentry.captureException(error);
            throw error;
        }
    }

    // API monitoring
    measureApiCall(endpoint, data = null) {
        const startTime = performance.now();
        
        return axios.post(endpoint, data)
            .then(response => {
                const duration = performance.now() - startTime;
                this.metrics.api[endpoint] = {
                    duration,
                    status: response.status,
                    success: true
                };
                
                datadog.gauge('api.response.duration', duration, {
                    endpoint,
                    status: response.status
                });
                
                return response;
            })
            .catch(error => {
                const duration = performance.now() - startTime;
                this.metrics.api[endpoint] = {
                    duration,
                    status: error.response?.status || 500,
                    success: false
                };
                
                sentry.captureException(error);
                
                datadog.gauge('api.response.duration', duration, {
                    endpoint,
                    status: error.response?.status || 500
                });
                
                throw error;
            });
    }

    // Memory monitoring
    trackMemoryUsage() {
        const usage = memoryUsage();
        this.metrics.memory = {
            heapUsed: usage.heapUsed,
            heapTotal: usage.heapTotal,
            external: usage.external
        };
        
        datadog.gauge('memory.heap.used', usage.heapUsed);
        datadog.gauge('memory.heap.total', usage.heapTotal);
        datadog.gauge('memory.external', usage.external);
    }

    // DOM monitoring
    trackDOMMetrics() {
        const metrics = {
            elements: document.getElementsByTagName('*').length,
            listeners: this.countEventListeners(),
            styleSheets: document.styleSheets.length,
            images: document.images.length,
            scripts: document.scripts.length
        };
        
        this.metrics.dom = metrics;
        
        Object.entries(metrics).forEach(([key, value]) => {
            datadog.gauge(`dom.${key}`, value);
        });
    }

    // Event listener counter
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

    // Audio monitoring
    trackAudioPerformance(audioContext) {
        const audioMetrics = {
            latency: audioContext.getOutputTimestamp().contextTime,
            sampleRate: audioContext.sampleRate,
            currentTime: audioContext.currentTime
        };
        
        this.metrics.audio = audioMetrics;
        
        Object.entries(audioMetrics).forEach(([key, value]) => {
            datadog.gauge(`audio.${key}`, value);
        });
    }

    // WebSocket monitoring
    trackWebSocketPerformance(socket) {
        const startTime = performance.now();
        socket.onopen = () => {
            const duration = performance.now() - startTime;
            this.metrics.websocket.connection = {
                duration,
                success: true
            };
            
            datadog.gauge('websocket.connection.duration', duration);
        };
        
        socket.onerror = (error) => {
            this.metrics.websocket.connection = {
                duration: performance.now() - startTime,
                success: false,
                error: error.message
            };
            
            sentry.captureException(error);
            datadog.gauge('websocket.connection.duration', this.metrics.websocket.connection.duration);
        };
    }

    // Start monitoring
    startMonitoring() {
        // Track DOM metrics every 5 seconds
        setInterval(() => this.trackDOMMetrics(), 5000);
        
        // Track memory usage every 10 seconds
        setInterval(() => this.trackMemoryUsage(), 10000);
        
        // Track JavaScript performance
        this.performanceObserver.observe({
            entryTypes: ['measure', 'mark']
        });
    }

    // Get all metrics
    getMetrics() {
        return this.metrics;
    }
}

module.exports = PerformanceMonitor;
