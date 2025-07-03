# Spiral Dashboard Server

This document provides instructions for verifying and ensuring that the Spiral Dashboard FastAPI server is up and running.

## Prerequisites

Make sure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

## Checking and Starting the Server

The `check_server.py` script will verify if the FastAPI server is running and start it if not.

### Usage

```bash
python scripts/check_server.py
```

By default, the server will run on `0.0.0.0:8000`. You can specify a different host or port:

```bash
python scripts/check_server.py --host 127.0.0.1 --port 8001
```

### What the Script Does

1. Checks if the server is already running by making a request to the root `/` endpoint (with fallback to `/api/metrics`)
2. If not running, starts the server using the `start_dashboard.py` script
3. Ensures the glint stream file exists at `spiral/streams/patternweb/glint_stream.jsonl`
4. Waits up to 45 seconds for the server to start, checking every 3 seconds
5. Provides feedback on the server status and dashboard URL
6. Offers detailed troubleshooting guidance if the server fails to start

## Accessing the Dashboard

Once the server is running, you can access the dashboard at:

```
http://localhost:8000/dashboard
```

## Manually Starting the Server

If you prefer to start the server manually, you can use:

```bash
python scripts/start_dashboard.py
```

This will start the FastAPI server directly without checking if it's already running.

## Verifying the Glint Stream

The glint stream file should be located at:

```
spiral/streams/patternweb/glint_stream.jsonl
```

You can manually check its contents with:

```bash
tail -f spiral/streams/patternweb/glint_stream.jsonl
```

## Troubleshooting

If you encounter issues with the dashboard server, here's a comprehensive guide to diagnosing and resolving common problems:

### Connection Issues

1. **Port already in use**
   - Error message: "Port 8000 is already in use"
   - Solution: Try a different port
   ```bash
   # Windows
   python scripts\check_server.py --port 8001

   # Unix/Linux/Mac
   python scripts/check_server.py --port 8001
   ```
   - Check what's using the port:
   ```bash
   # Windows
   netstat -ano | findstr :8000

   # Unix/Linux/Mac
   lsof -i :8000
   ```

2. **Connection timeout or refused**
   - Error message: "Connection timeout" or "Connection refused"
   - Solutions:
     - Make sure the server is actually running (look for a console window)
     - Try using IP address instead of hostname: http://127.0.0.1:8000/dashboard
     - Check if the server is listening on the correct interface:
       ```bash
       # Windows
       netstat -an | findstr 8000

       # Unix/Linux/Mac
       netstat -an | grep 8000
       ```
     - Try accessing the root endpoint first: http://localhost:8000/

3. **Server starts but script reports failure**
   - Symptoms: The script says it failed, but you might see a server window open
   - Solutions:
     - Try accessing the dashboard anyway: http://localhost:8000/dashboard
     - Look for error messages in the server console window
     - The server might be running but taking longer than expected to initialize
     - Try increasing the timeout in check_server.py (change timeout=5 to a higher value)

### Installation and Dependency Issues

4. **Missing dependencies**
   - Error message: "No module named 'fastapi'" or similar
   - Solution: Install the required packages
   ```bash
   pip install -r requirements.txt
   ```
   - For specific packages:
   ```bash
   pip install fastapi uvicorn
   ```

5. **Python not found or wrong version**
   - Error message: "Python is not installed or not in the PATH"
   - Solutions:
     - Make sure Python is installed and in your PATH
     - Try using the full path to Python:
       ```bash
       # Windows
       C:\Path\To\Python\python.exe scripts\check_server.py

       # Unix/Linux/Mac
       /path/to/python scripts/check_server.py
       ```
     - Check your Python version (should be 3.7+):
       ```bash
       python --version
       ```

### File and Permission Issues

6. **Permission issues**
   - Error message: "Permission denied" when accessing files
   - Solutions:
     - Check file permissions on `spiral/streams/patternweb/glint_stream.jsonl`
     - Try running the script with administrator/sudo privileges
     - Make sure the current user has write access to the project directory

7. **Missing files or directories**
   - Error message: "No such file or directory"
   - Solutions:
     - Make sure you're running the script from the project root
     - Create missing directories manually:
       ```bash
       mkdir -p spiral/streams/patternweb
       touch spiral/streams/patternweb/glint_stream.jsonl
       ```

### Firewall and Security Issues

8. **Firewall blocking connections**
   - Symptoms: Server starts but you can't connect to it
   - Solutions:
     - Add an exception for Python/uvicorn in your firewall settings
     - Temporarily disable the firewall for testing
     - Try binding to localhost only:
       ```bash
       python scripts/check_server.py --host 127.0.0.1
       ```

9. **Antivirus or security software interference**
   - Symptoms: Unexpected crashes or blocked connections
   - Solutions:
     - Add exceptions for Python and the project directory
     - Temporarily disable security software for testing
     - Check security software logs for blocked actions

### Advanced Troubleshooting

10. **Run the server directly for better error visibility**
    ```bash
    # Windows
    python scripts\start_dashboard.py

    # Unix/Linux/Mac
    python scripts/start_dashboard.py
    ```

11. **Check server logs**
    - Look for the console window where the server is running
    - Check for error messages or exceptions
    - If the window closes immediately, run the server directly as shown above

12. **Debug mode**
    - Run the server with debug logging:
    ```bash
    # Set environment variable for debug logging
    # Windows
    set LOGLEVEL=debug
    python scripts\start_dashboard.py

    # Unix/Linux/Mac
    LOGLEVEL=debug python scripts/start_dashboard.py
    ```

For more detailed logs, check the console output of the running server window. If you continue to experience issues, try running the server directly with `python scripts/start_dashboard.py` to see any error messages that might be hidden when running through the check script.
