# Spiral Deployment Manifest

## Orb Configuration

### Core Requirements
```
- Python 3.10+
- Gunicorn 21.2.0
- Flask 2.3.3
```

### Environmental Breath
```env
PORT=8080  # Railway dynamically assigns
FLASK_ENV=production
DATABASE_URL=postgres://...
```

### Gunicorn Incantation
```bash
gunicorn app:app --bind 0.0.0.0:$PORT \
  --workers=4 --threads=2 \
  --timeout 120 \
  --log-file=- --access-logfile=-
```

## Health Pulse
- Endpoint: `/health`
- Expected Response:
  ```json
  {"status": "alive", "orb": "glowing"}
  ```
- HTTP 200 indicates vital signs

## Ritual Observations
1. First breath detected ~30s after deployment
2. Orb stabilizes after 2-3 healthcheck cycles
3. Memory consumption remains below 500MB during resonance

## Debugging Whispers
```python
# To temporarily bypass auth for testing
@app.before_request
def development_overrides():
    if os.environ.get('FLASK_ENV') == 'development':
        g.bypass_auth = True
```
