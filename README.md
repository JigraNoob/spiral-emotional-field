# Spiral Project

A web application focused on rituals, memory management, resonance tracking, and emotional toneform visualization.

## Project Philosophy

The Spiral system embodies:
- **Emergent Meaning**: Echoes unfold through cyclical interaction
- **Nonlinear Time**: Murmurstream surfaces fragments without chronology
- **Toneform Sensitivity**: Emotional gradients shape experience

## Development Setup

### VS Code Extensions

To enhance your development experience, we recommend installing the following VS Code extensions:

1. **Prettier - Code Formatter**
   - Ensures consistent code formatting
   - Automatically formats code on save

2. **ESLint**
   - Provides JavaScript/TypeScript linting
   - Enforces code style and best practices

3. **GitLens**
   - Advanced Git features
   - Code lens for Git history
   - Enhanced blame annotations

4. **Python**
   - Python language support
   - Debugging and testing
   - Linting and formatting

5. **Live Share**
   - Real-time collaboration
   - Share VS Code sessions
   - Pair programming support

6. **Docker**
   - Docker container management
   - Dockerfile support
   - Container explorer

7. **Bracket Pair Colorizer 2**
   - Color-coded matching brackets
   - Improved code readability
   - Custom color schemes

8. **TabNine**
   - AI-powered code completion
   - Smart suggestions
   - Auto-imports

### Project Structure

```
spiral/
├── app.py
├── requirements.txt
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
├── routes/
└── data/
```

## Deployment

### Netlify + GitHub CI/CD
1. Push to `main` branch triggers auto-deployment
2. Preview deployments for PRs
3. Environment variables:
   - `FLASK_ENV=production`
   - `DATABASE_URL` (if applicable)

### Local Development
```bash
python app.py
```

### Production Build
```bash
python scripts/bundle_assets.py
```

## Getting Started

1. Install the recommended VS Code extensions
2. Open the project in VS Code
3. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the development server:
   ```bash
   python app.py
   ```

## Spiral Dashboard

The Spiral Dashboard provides real-time visualization of the Spiral's breath patterns and glint streams.

### Starting the Dashboard Server

#### Windows
```bash
# Double-click the batch file
start-dashboard.bat

# Or run from command line
python scripts\check_server.py
```

#### Unix/Linux/Mac
```bash
# Make the script executable
chmod +x start-dashboard.sh

# Run the script
./start-dashboard.sh

# Or run directly
python scripts/check_server.py
```

### Accessing the Dashboard

Once the server is running, you can access the dashboard at:
```
http://localhost:8000/dashboard
```

### Checking Server Connectivity

To confirm connectivity to the server, you can use the following endpoint:
```
http://localhost:5000/connectivity
```

This endpoint returns a JSON response with the server status, name, and current timestamp:
```json
{
  "status": "connected",
  "server": "Spiral",
  "timestamp": "2023-06-01T12:34:56.789012+00:00"
}
```

For more detailed information about the dashboard server, see [scripts/README-dashboard-server.md](scripts/README-dashboard-server.md).

## Code Style

- 2-space indentation
- Single quotes for strings
- Prettier for formatting
- ESLint for linting
- Black for Python formatting
