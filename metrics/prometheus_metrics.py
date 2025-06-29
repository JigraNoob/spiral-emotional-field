from flask import request
import time
from prometheus_client import Counter, Histogram, Gauge

# API Metrics
REQUEST_COUNT = Counter(
    'spiral_request_count',
    'App Request Count',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'spiral_request_latency_seconds',
    'Request Latency',
    ['endpoint']
)

ERROR_COUNT = Counter(
    'spiral_error_count',
    'App Error Count',
    ['type', 'endpoint']
)

# Resource Metrics
MEMORY_USAGE = Gauge('spiral_memory_usage_bytes', 'Memory Usage in Bytes')
CPU_USAGE = Gauge('spiral_cpu_usage_percent', 'CPU Usage Percent')


def start_timer():
    return time.time()


def record_metrics(response, endpoint, start_time):
    latency = time.time() - start_time
    REQUEST_LATENCY.labels(endpoint).observe(latency)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        http_status=response.status_code
    ).inc()
    
    if response.status_code >= 400:
        ERROR_COUNT.labels(
            type='http_error',
            endpoint=endpoint
        ).inc()
    
    return response
