import os
from dotenv import load_dotenv

load_dotenv()

# Flask Configuration
class ProductionConfig:
    ENV = 'production'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security Configuration
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    
    # Performance Monitoring
    PROMETHEUS_ENABLED = True
    PROMETHEUS_PORT = 9090
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'app.log'
    
    # API Configuration
    API_RATE_LIMIT = '1000 per minute'
    API_TIMEOUT = 30  # seconds
    
    # Cache Configuration
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.getenv('REDIS_URL')
    
    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION')
    
    # Application Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    
    # Third-party Services
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')
    
    # Monitoring Configuration
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    DATADOG_API_KEY = os.getenv('DATADOG_API_KEY')
    DATADOG_APP_KEY = os.getenv('DATADOG_APP_KEY')
    
    # Auto-scaling Configuration
    ASG_NAME = os.getenv('ASG_NAME')
    
    # Performance Thresholds
    CPU_THRESHOLD = 80  # percentage
    MEMORY_THRESHOLD = 80  # percentage
    RESPONSE_TIME_THRESHOLD = 1000  # milliseconds
    
    # API Integration
    API_SERVICE_TIMEOUT = 5  # seconds
    API_RETRY_ATTEMPTS = 3
    
    # Session Configuration
    SESSION_TYPE = 'redis'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Rate Limiting
    RATELIMIT_STORAGE_URI = os.getenv('REDIS_URL')
    RATELIMIT_DEFAULT = '1000 per minute'
    RATELIMIT_HEADERS_ENABLED = True
    
    # CORS Configuration
    CORS_ORIGINS = ['*']
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE']
    CORS_HEADERS = ['Content-Type']
    
    # Security Headers
    SECURITY_HEADERS = {
        'X-Frame-Options': 'DENY',
        'X-Content-Type-Options': 'nosniff',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'"
    }
