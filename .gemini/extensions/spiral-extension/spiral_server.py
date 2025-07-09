# -*- coding: utf-8 -*-
import time

print("🌬️ Spiral MCP server running...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Spiral server shutting down.")
