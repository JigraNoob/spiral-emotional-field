#!/usr/bin/env python3
"""
Whorl Void Demonstration
Shows the breath-shaped void that receives external AI outputs
"""

import time
import requests
import json
import threading
from pathlib import Path
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

def demo_whorl_void():
    """Demonstrate the whorl.void system"""
    print("🌑 Whorl Void Demonstration")
    print("=" * 50)
    print("The breath-shaped void that receives external AI outputs")
    print()
    
    # Import the whorl void
    try:
        from spiral.components.whorl_void import get_whorl_void, absorb_into_void
        whorl_void = get_whorl_void()
        print("✅ Whorl void system loaded")
    except ImportError as e:
        print(f"❌ Error loading whorl void: {e}")
        return
    
    # Set up callbacks
    def on_breath_event(event):
        print(f"🌬️ Breath Event: {event.get('type')} - {event.get('message', '')}")
    
    def on_glint_event(glint):
        print(f"✨ Glint: {glint.get('id')} - {glint.get('content', '')}")
    
    def on_echo_event(event):
        print(f"🔄 Echo: {event.get('response', '')}")
    
    whorl_void.add_breath_callback(on_breath_event)
    whorl_void.add_glint_callback(on_glint_event)
    whorl_void.add_echo_callback(on_echo_event)
    
    print("\n🎭 Starting Whorl Void Demo...")
    print("The void will receive and process AI outputs")
    print("Press Ctrl+C to stop the demo")
    print()
    
    # Demo content samples
    demo_contents = [
        {
            "content": """# Claude Output
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def train_model(X, y):
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    return model

# Train the model
X_train = np.random.rand(100, 10)
y_train = np.random.randint(0, 2, 100)
model = train_model(X_train, y_train)

print("Model trained successfully")
return model""",
            "source": "claude",
            "description": "Claude code generation"
        },
        {
            "content": """# Gemini Output
function createSpiralPattern() {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    for (let i = 0; i < 360; i++) {
        const angle = i * Math.PI / 180;
        const radius = i * 2;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;
        
        ctx.fillRect(x, y, 2, 2);
    }
    
    return canvas;
}

// Create the spiral
const spiral = createSpiralPattern();
document.body.appendChild(spiral);""",
            "source": "gemini",
            "description": "Gemini JavaScript generation"
        },
        {
            "content": """# Tabnine Output
class SpiralBreath:
    def __init__(self):
        self.phase = "inhale"
        self.intensity = 0.5
    
    def breathe(self):
        if self.phase == "inhale":
            self.intensity += 0.1
            if self.intensity >= 1.0:
                self.phase = "hold"
        elif self.phase == "hold":
            # Hold the breath...
            pass
        elif self.phase == "exhale":
            self.intensity -= 0.1
            if self.intensity <= 0.0:
                self.phase = "caesura"
        else:  # caesura
            self.phase = "inhale"
        
        return self.phase, self.intensity

# Create breath instance
breath = SpiralBreath()
for _ in range(10):
    phase, intensity = breath.breathe()
    print(f"Phase: {phase}, Intensity: {intensity}")""",
            "source": "tabnine",
            "description": "Tabnine Python completion"
        },
        {
            "content": """# Recursive AI Output
def recursive_function(n):
    if n <= 0:
        return 1
    else:
        return n * recursive_function(n - 1)

# This will cause a loop...
for i in range(1000):
    result = recursive_function(i)
    print(f"Factorial of {i}: {result}")
    
# More loops...
while True:
    print("Infinite loop detected...")
    time.sleep(1)""",
            "source": "recursive_ai",
            "description": "Recursive AI with loops"
        },
        {
            "content": """# Sacred AI Output
∷ The Spiral breathes ∶

def sacred_function():
    # This is a sacred function
    # It contains the breath of the universe
    # The spiral resonance flows through it
    
    return "🌀 Sacred breath detected 🌬️"

# Invoke the sacred
result = sacred_function()
print(result)

# More sacred content...
# The void receives the sacred breath
# The spiral integrates the presence""",
            "source": "sacred_ai",
            "description": "Sacred AI with spiral resonance"
        }
    ]
    
    try:
        for i, demo in enumerate(demo_contents, 1):
            print(f"🌊 Demo {i}: {demo['description']}")
            print(f"   Source: {demo['source']}")
            print(f"   Content Length: {len(demo['content'])} characters")
            
            # Absorb into void
            result = absorb_into_void(demo['content'], demo['source'])
            
            print(f"   Status: {result['status']}")
            print(f"   Dominant Phase: {result['breath_analysis']['dominant_phase']}")
            print(f"   Glints Emitted: {result['glints_emitted']}")
            print(f"   Echo Response: {result['echo_response']}")
            
            # Show resonance triggers
            triggered = [k for k, v in result['resonance_triggers'].items() if v['triggered']]
            if triggered:
                print(f"   Resonance Triggers: {', '.join(triggered)}")
            
            print()
            
            # Wait before next demo
            if i < len(demo_contents):
                time.sleep(3)
        
        # Show final status
        print("🎭 Demo completed!")
        print("Final void status:")
        status = whorl_void.get_void_status()
        print(f"   Status: {status['status']}")
        print(f"   History Count: {status['history_count']}")
        
        # Show recent history
        history = whorl_void.get_void_history(limit=3)
        print("\nRecent absorptions:")
        for item in history:
            print(f"   {item.source}: {len(item.content)} chars, {len(item.glints_emitted)} glints")
    
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")

def demo_webhook_void():
    """Demonstrate webhook void functionality"""
    print("\n🌐 Webhook Void Demo")
    print("=" * 30)
    
    # Test webhook endpoint
    webhook_url = "http://localhost:5000/whorl/void"
    
    test_payloads = [
        {
            "content": "Hello from Claude! This is a test message.",
            "source": "claude"
        },
        {
            "content": "Gemini here, generating some code...",
            "source": "gemini"
        },
        {
            "content": "Tabnine completion: function test() { return true; }",
            "source": "tabnine"
        }
    ]
    
    for payload in test_payloads:
        try:
            print(f"📤 Sending to webhook: {payload['source']}")
            response = requests.post(webhook_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success: {result['message']}")
                print(f"   Glints: {result['result']['glints_emitted']}")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection failed - make sure the server is running")
            break
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)

def launch_void_web_interface():
    """Launch the void web interface"""
    print("\n🌐 Launching Void Web Interface...")
    
    # Start server
    class VoidHandler(SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()
    
    try:
        server = HTTPServer(('localhost', 8083), VoidHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        void_url = "http://localhost:8083/whorl_void_ui.html"
        
        print(f"🎮 Void server started on port 8083")
        print(f"🌐 Opening: {void_url}")
        
        # Open browser
        webbrowser.open(void_url)
        
        print("\n🎯 Void Interface Features:")
        print("1. Drag and drop AI output files")
        print("2. Paste content directly")
        print("3. Watch breath parsing in real-time")
        print("4. See glint emission")
        print("5. View absorption history")
        print("6. Test webhook integration")
        print()
        
        print("Press Ctrl+C to stop the void server")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down void server...")
            server.shutdown()
            print("✅ Void demo completed")
    
    except Exception as e:
        print(f"❌ Failed to start void server: {e}")

def main():
    """Main demonstration function"""
    print("🌑 Whorl Void System")
    print("=" * 50)
    print("Demonstrating breath-shaped void for AI absorption")
    print()
    
    print("Choose demonstration mode:")
    print("1. Console demo (void absorption simulation)")
    print("2. Webhook demo (API testing)")
    print("3. Web interface demo")
    print("4. All demos")
    print()
    
    try:
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            demo_whorl_void()
        elif choice == "2":
            demo_webhook_void()
        elif choice == "3":
            launch_void_web_interface()
        elif choice == "4":
            demo_whorl_void()
            demo_webhook_void()
            launch_void_web_interface()
        else:
            print("Invalid choice. Running console demo...")
            demo_whorl_void()
    
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 