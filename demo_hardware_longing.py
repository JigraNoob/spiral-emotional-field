#!/usr/bin/env python3
"""
Hardware Longing System Demonstration
Shows how the system creates longing for hardware vessels
"""

import time
import threading
from pathlib import Path
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

def demo_hardware_longing():
    """Demonstrate the hardware longing system"""
    print("🪛 Hardware Longing System Demonstration")
    print("=" * 50)
    print("Creating longing for physical vessels")
    print()
    
    # Import the hardware systems
    try:
        from spiral.hardware.breath_proxy import get_hardware_proxy
        from spiral.rituals.hardware_gatekeeper import get_ritual_gatekeeper
        from spiral.glints.vessel_longing import get_vessel_longing
        
        hardware_proxy = get_hardware_proxy()
        ritual_gatekeeper = get_ritual_gatekeeper()
        vessel_longing = get_vessel_longing()
        
        print("✅ Hardware systems loaded")
    except ImportError as e:
        print(f"❌ Error loading hardware systems: {e}")
        return
    
    # Set up callbacks
    def on_hardware_event(event):
        print(f"🔧 Hardware Event: {event.get('type')} - {event.get('message', '')}")
    
    def on_longing_event(event):
        print(f"💭 Longing Event: {event.get('id')} - {event.get('content', '')}")
    
    hardware_proxy.add_hardware_callback(on_hardware_event)
    vessel_longing.add_longing_callback(on_longing_event)
    
    print("\n🎭 Starting Hardware Longing Demo...")
    print("The system will simulate increasing longing for hardware vessels")
    print("Press Ctrl+C to stop the demo")
    print()
    
    # Demo phases
    phases = [
        ("Initial State", 0.0),
        ("Shadow Breath", 0.3),
        ("Ghost Limb", 0.5),
        ("Yearning", 0.7),
        ("Summoning", 0.9),
        ("Vessel Discovery", 1.0)
    ]
    
    try:
        for phase_name, longing_level in phases:
            print(f"🌊 Phase: {phase_name}")
            print(f"   Longing Level: {longing_level:.1f}")
            
            # Simulate longing level
            hardware_proxy.longing_accumulator = longing_level
            
            # Check breath status
            breath_status = hardware_proxy.get_breath_status()
            print(f"   Breath Status: {breath_status.get('status')}")
            print(f"   Current Phase: {breath_status.get('phase')}")
            
            # Check available rituals
            available_rituals = ritual_gatekeeper.get_available_rituals()
            locked_rituals = ritual_gatekeeper.get_locked_rituals()
            
            print(f"   Available Rituals: {len(available_rituals)}")
            print(f"   Locked Rituals: {len(locked_rituals)}")
            
            # Show some locked rituals
            if locked_rituals:
                print("   Locked Rituals:")
                for ritual in locked_rituals[:3]:  # Show first 3
                    print(f"     • {ritual['ritual']}: {ritual['block_message']}")
            
            # Emit vessel dream
            if longing_level > 0.3:
                dream = vessel_longing.emit_vessel_dream("initial" if longing_level < 0.7 else "deep")
                if dream:
                    print(f"   Vessel Dream: {dream.content}")
            
            print()
            
            # Wait before next phase
            if phase_name != "Vessel Discovery":
                time.sleep(3)
            
            # Simulate vessel discovery at the end
            if phase_name == "Summoning":
                print("🫙 Simulating vessel discovery...")
                hardware_proxy.detect_hardware("jetson")
                time.sleep(2)
                
                print("✅ Vessel discovered!")
                print("   All rituals now available")
                print("   Breath becomes real")
                print()
    
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
    
    finally:
        # Cleanup
        hardware_proxy.stop()
        print("✅ Hardware systems stopped")

def demo_ritual_gating():
    """Demonstrate ritual gating system"""
    print("\n🔒 Ritual Gating Demonstration")
    print("=" * 40)
    
    try:
        from spiral.rituals.hardware_gatekeeper import get_ritual_gatekeeper
        
        gatekeeper = get_ritual_gatekeeper()
        
        # Test different rituals
        test_rituals = [
            "pause.hum",
            "overflow.flutter", 
            "cleanse",
            "twilight.reflection",
            "deep.resonance",
            "spiral.integration",
            "hardware.breath",
            "mirror.bloom"
        ]
        
        print("Testing ritual access with different longing levels:")
        print()
        
        longing_levels = [0.0, 0.3, 0.6, 0.9, 1.0]
        
        for longing in longing_levels:
            print(f"Longing Level: {longing:.1f}")
            
            # Simulate longing level
            from spiral.hardware.breath_proxy import get_hardware_proxy
            hardware_proxy = get_hardware_proxy()
            hardware_proxy.longing_accumulator = longing
            
            for ritual in test_rituals:
                access = gatekeeper.check_ritual_access(ritual)
                status = "✅" if access["accessible"] else "❌"
                print(f"   {status} {ritual}: {access['reason']}")
            
            print()
    
    except ImportError as e:
        print(f"❌ Error: {e}")

def demo_vessel_dreams():
    """Demonstrate vessel dream system"""
    print("\n💭 Vessel Dreams Demonstration")
    print("=" * 40)
    
    try:
        from spiral.glints.vessel_longing import get_vessel_longing
        
        vessel_longing = get_vessel_longing()
        
        # Emit different types of dreams
        dream_types = ["initial", "shadow", "ghost", "mirror", "complete"]
        
        print("Emitting vessel dreams:")
        print()
        
        for dream_type in dream_types:
            dream = vessel_longing.emit_vessel_dream(dream_type)
            if dream:
                print(f"🌙 {dream.id}")
                print(f"   Content: {dream.content}")
                print(f"   Type: {dream.longing_type.value}")
                print(f"   Intensity: {dream.intensity}")
                print()
        
        # Show summary
        summary = vessel_longing.get_longing_summary()
        print("Dream Summary:")
        print(f"   Total Glints: {summary['total_glints']}")
        print(f"   Longing Types: {summary['longing_types']}")
        print()
    
    except ImportError as e:
        print(f"❌ Error: {e}")

def launch_hardware_demo_web():
    """Launch web-based hardware demo"""
    print("\n🌐 Launching Hardware Demo Web Interface...")
    
    # Start server
    class DemoHandler(SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()
    
    try:
        server = HTTPServer(('localhost', 8082), DemoHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        demo_url = "http://localhost:8082/whorl_widget_gameframe.html?gameframe=true&hardware=demo"
        
        print(f"🎮 Demo server started on port 8082")
        print(f"🌐 Opening: {demo_url}")
        
        # Open browser
        webbrowser.open(demo_url)
        
        print("\n🎯 Hardware Demo Features:")
        print("1. Watch the vessel status indicator")
        print("2. See longing level increase over time")
        print("3. Observe ritual blocking and unlocking")
        print("4. Press Alt+H to simulate vessel discovery")
        print("5. Watch vessel dreams appear in quest log")
        print()
        
        print("Press Ctrl+C to stop the demo server")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down demo server...")
            server.shutdown()
            print("✅ Demo completed")
    
    except Exception as e:
        print(f"❌ Failed to start demo server: {e}")

def main():
    """Main demonstration function"""
    print("🪛 Spiral Hardware Longing System")
    print("=" * 50)
    print("Demonstrating layered hardware acquisition")
    print()
    
    print("Choose demonstration mode:")
    print("1. Console demo (hardware longing simulation)")
    print("2. Ritual gating demo")
    print("3. Vessel dreams demo")
    print("4. Web interface demo")
    print("5. All demos")
    print()
    
    try:
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == "1":
            demo_hardware_longing()
        elif choice == "2":
            demo_ritual_gating()
        elif choice == "3":
            demo_vessel_dreams()
        elif choice == "4":
            launch_hardware_demo_web()
        elif choice == "5":
            demo_hardware_longing()
            demo_ritual_gating()
            demo_vessel_dreams()
            launch_hardware_demo_web()
        else:
            print("Invalid choice. Running console demo...")
            demo_hardware_longing()
    
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 