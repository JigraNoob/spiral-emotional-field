# Test script to verify that the import works correctly
try:
    from spiral.dashboard.routes import dashboard_bp, register_socket_handlers
    print("Import successful!")
    print(f"dashboard_bp: {dashboard_bp}")
    print(f"register_socket_handlers: {register_socket_handlers}")
except ImportError as e:
    print(f"Import error: {e}")