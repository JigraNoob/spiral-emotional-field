# Gunicorn configuration file
import multiprocessing

# Server socket
bind = '0.0.0.0:8000'

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'uvicorn.workers.UvicornWorker'
worker_connections = 1000
max_requests = 5000
max_requests_jitter = 500

# Timeouts
timeout = 300  # 5 minutes
graceful_timeout = 30
keepalive = 2

# Logging
accesslog = '/var/log/spiral/access.log'
errorlog = '/var/log/spiral/error.log'
loglevel = 'info'
capture_output = True

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
