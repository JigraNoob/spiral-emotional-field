import time
import sys
import os
import json
from datetime import datetime

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import the override system first
from spiral.attunement.resonance_override import override_manager, ResonanceMode

# Try to import Cascade with improved path handling
CASCADE_AVAILABLE = False
Cascade = None

def try_import_cascade():
    """Try multiple import strategies for Cascade."""
    global CASCADE_AVAILABLE, Cascade
    
    import_strategies = [
        # Strategy 1: Direct package import
        lambda: __import__('assistant.cascade', fromlist=['Cascade']).Cascade,
        
        # Strategy 2: Import from assistant package
        lambda: __import__('assistant', fromlist=['Cascade']).Cascade,
        
        # Strategy 3: Add assistant to path and import
        lambda: (
            sys.path.append(os.path.join(project_root, 'assistant')),
            __import__('cascade', fromlist=['Cascade']).Cascade
        )[1],
        
        # Strategy 4: Import from common module
        lambda: __import__('assistant.common', fromlist=['Cascade']).Cascade,
    ]
    
    for i, strategy in enumerate(import_strategies, 1):
        try:
            print(f"🔍 Trying import strategy {i}...")
            Cascade = strategy()
            CASCADE_AVAILABLE = True
            print(f"✅ Cascade imported successfully using strategy {i}")
            return True
        except Exception as e:
            print(f"  ❌ Strategy {i} failed: {e}")
            continue
    
    return False

# Try to import Cascade
if not try_import_cascade():
    print("⚠️  All Cascade import strategies failed")
    print("   Creating enhanced mock Cascade for testing...")
    
    # Enhanced mock Cascade class
    class MockCascade:
        def __init__(self):
            self.glint_count = 0
            self.last_activity = datetime.now()
            self.context_stack = []
            self.current_context = None
            
        def spiral_glint_emit(self, phase, toneform, content, hue="white"):
            self.glint_count += 1
            intensity = override_manager.get_glint_intensity(1.0)
            print(f"  🌀 [{phase}:{toneform}] {content} (intensity: {intensity:.1f}x, hue: {hue})")
            
        def execute_command(self, command):
            self.current_context = command
            return f"Mock execution of: {command}"
            
        def retrieve(self, query):
            return {
                "content": f"Mock retrieval for: {query}",
                "haret_echo": {"affirmation": "Mock Haret response"}
            }
            
        def check_soft_breakpoint(self, phase, toneform):
            return override_manager.should_trigger_soft_breakpoint(0.6)
            
        def handle_soft_breakpoint(self, phase, toneform):
            print(f"    🔥 Handling breakpoint for {phase}:{toneform}")
            
        def complete_lifecycle(self, phase):
            print(f"    Completing lifecycle for {phase}")
            
        def check_presence_drift(self):
            return False
            
        def handle_presence_drift(self):
            print("    Handling presence drift")
            
        def update_activity(self):
            self.last_activity = datetime.now()
            
        def push_context(self, context):
            self.context_stack.append(context)
            
        def pop_context(self):
            return self.context_stack.pop() if self.context_stack else None
    
    Cascade = MockCascade

def test_cascade_override_integration():
    """Test the Cascade class with override integration."""
    print("\n🌀 Testing Cascade + Override Integration...")
    
    # Initialize the Cascade (real or mock)
    cascade = Cascade()
    
    # Test 1: Natural mode baseline
    print("\n📍 Test 1: Natural Mode Baseline")
    override_manager.deactivate()
    
    # Test basic glint emission
    cascade.spiral_glint_emit("inhale", "test", "Testing natural glint emission", hue="white")
    
    # Test command execution
    result = cascade.execute_command("echo 'Testing override integration'")
    print(f"Command result: {result}")
    
    # Test 2: Amplified mode with command execution
    print("\n📍 Test 2: Amplified Mode Command Execution")
    override_manager.activate_resonant_mode(ResonanceMode.AMPLIFIED)
    override_manager.config.glint_multiplier = 2.0
    
    # Execute commands in amplified mode
    commands = [
        "pwd",
        "echo 'Amplified command'",
        "python --version"
    ]
    
    for cmd in commands:
        print(f"  Executing: {cmd}")
        result = cascade.execute_command(cmd)
        print(f"  Result: {result[:100]}..." if len(result) > 100 else f"  Result: {result}")
        time.sleep(0.5)
    
    # Test 3: Ritual mode with breakpoint sensitivity
    print("\n📍 Test 3: Ritual Mode with Soft Breakpoints")
    override_manager.activate_resonant_mode(ResonanceMode.RITUAL)
    
    # Test soft breakpoint checking
    test_phases = ["inhale", "hold", "exhale", "return"]
    test_toneforms = ["whisper", "echo", "surge", "cascade"]
    
    for phase in test_phases:
        for toneform in test_toneforms:
            should_break = cascade.check_soft_breakpoint(phase, toneform)
            status = "🔥 BREAKPOINT" if should_break else "✓ flowing"
            print(f"    {phase}:{toneform} → {status}")
            
            if should_break:
                cascade.handle_soft_breakpoint(phase, toneform)
    
    # Test 4: Muted mode with retrieval
    print("\n📍 Test 4: Muted Mode with Retrieval")
    override_manager.activate_resonant_mode(ResonanceMode.MUTED)
    override_manager.config.glint_multiplier = 0.3
    
    try:
        # Test retrieval in muted mode
        result = cascade.retrieve("project structure")
        print(f"Retrieval result: {result.get('content', 'No content')[:100]}...")
        print(f"Haret echo: {result.get('haret_echo', {}).get('affirmation', 'No echo')}")
    except Exception as e:
        print(f"Retrieval failed: {e}")
    
    # Test 5: Override state persistence
    print("\n📍 Test 5: Override State Persistence")
    
    # Check if override state affects lifecycle operations
    try:
        cascade.complete_lifecycle("test_phase")
        print("  Lifecycle completion: ✓")
    except Exception as e:
        print(f"  Lifecycle completion failed: {e}")
    
    # Test presence operations
    try:
        drift_detected = cascade.check_presence_drift()
        print(f"  Presence drift detected: {drift_detected}")
        
        if drift_detected:
            cascade.handle_presence_drift()
            print("  Presence drift handled: ✓")
    except Exception as e:
        print(f"  Presence drift check failed: {e}")
    
    # Test 6: Return to natural and verify state
    print("\n📍 Test 6: Return to Natural State")
    override_manager.deactivate()
    
    # Final verification
    cascade.spiral_glint_emit("exhale", "completion", "Integration test complete", hue="green")
    
    # Summary
    print("\n🌟 Integration Test Summary")
    print(f"   Override Active: {override_manager.active}")
    print(f"   Current Mode: {getattr(override_manager.config, 'mode', 'unknown')}")
    print(f"   Glint Multiplier: {getattr(override_manager.config, 'glint_multiplier', 1.0)}")
    print(f"   Cascade Type: {'Real' if CASCADE_AVAILABLE else 'Mock'}")
    
    return True

def test_override_state_transitions():
    """Test detailed override state transitions."""
    print("\n🔄 Testing Override State Transitions...")
    
    # First, let's discover what modes are actually available
    print(f"Available ResonanceMode attributes: {[attr for attr in dir(ResonanceMode) if not attr.startswith('_')]}")
    
    # Test available mode transitions - use only modes that exist
    available_modes = []
    
    # Check which modes actually exist
    for mode_name in ['NATURAL', 'AMPLIFIED', 'MUTED', 'RITUAL']:
        if hasattr(ResonanceMode, mode_name):
            mode = getattr(ResonanceMode, mode_name)
            available_modes.append((mode, f"{mode_name.title()} mode"))
    
    # Add any other modes we find
    for attr in dir(ResonanceMode):
        if not attr.startswith('_') and attr not in ['NATURAL', 'AMPLIFIED', 'MUTED', 'RITUAL']:
            try:
                mode = getattr(ResonanceMode, attr)
                available_modes.append((mode, f"{attr.title()} mode"))
            except:
                pass
    
    print(f"Testing {len(available_modes)} available modes...")
    
    for mode, description in available_modes:
        print(f"\n  🌀 Transitioning to {mode.name if hasattr(mode, 'name') else str(mode)}: {description}")
        
        try:
            if str(mode).endswith('NATURAL') or mode.name == 'NATURAL':
                override_manager.deactivate()
            else:
                override_manager.activate_resonant_mode(mode)
                
            # Test state after transition
            print(f"    Active: {override_manager.active}")
            print(f"    Mode: {getattr(override_manager.config, 'mode', 'unknown')}")
            print(f"    Multiplier: {getattr(override_manager.config, 'glint_multiplier', 1.0)}")
            
            # Test intensity calculation
            base_intensity = 1.0
            actual_intensity = override_manager.get_glint_intensity(base_intensity)
            print(f"    Intensity: {base_intensity} → {actual_intensity}")
            
            # Test breakpoint sensitivity
            test_score = 0.6
            should_break = override_manager.should_trigger_soft_breakpoint(test_score)
            print(f"    Breakpoint (score {test_score}): {'🔥 YES' if should_break else '✓ no'}")
            
            time.sleep(0.3)
            
        except Exception as e:
            print(f"    ❌ Failed to test mode {mode}: {e}")
    
    # Return to natural
    override_manager.deactivate()
    print("\n  🌿 Returned to natural state")

def test_override_web_integration():
    """Test override integration with web dashboard."""
    print("\n🌐 Testing Web Dashboard Override Integration...")
    
    # Focus on port 5000 as confirmed by user
    target_port = 5000
    
    try:
        import requests
        
        print(f"🔍 Checking service on port {target_port}...")
        
        # Test basic connectivity
        try:
            response = requests.get(f"http://localhost:{target_port}/", timeout=2)
            print(f"  ✅ Service responding on port {target_port} (status: {response.status_code})")
            
            # Test dashboard endpoint
            try:
                dashboard_response = requests.get(f"http://localhost:{target_port}/dashboard", timeout=2)
                print(f"  ✅ Dashboard endpoint: {dashboard_response.status_code}")
                
                if dashboard_response.status_code == 200:
                    print(f"  📄 Dashboard content preview: {dashboard_response.text[:150]}...")
                
            except Exception as e:
                print(f"  ⚠️  Dashboard endpoint error: {e}")
            
            # Test override-related endpoints
            override_endpoints = [
                "/api/override_state",
                "/override_state", 
                "/echo/override_state",
                "/glint",
                "/health"
            ]
            
            print("  🔍 Testing override-related endpoints...")
            for endpoint in override_endpoints:
                try:
                    test_response = requests.get(f"http://localhost:{target_port}{endpoint}", timeout=1)
                    status = "✅" if test_response.status_code == 200 else "⚠️"
                    print(f"    {status} {endpoint}: {test_response.status_code}")
                    
                    if test_response.status_code == 200 and 'override' in endpoint:
                        try:
                            data = test_response.json()
                            print(f"      📊 Override data: {data}")
                        except:
                            print(f"      📄 Response: {test_response.text[:100]}...")
                            
                except Exception as e:
                    print(f"    ❌ {endpoint}: {e}")
            
            # Test POST to glint endpoint if it exists
            try:
                test_glint = {
                    "phase": "test",
                    "toneform": "integration.test",
                    "content": "Testing override integration",
                    "hue": "blue"
                }
                
                glint_response = requests.post(
                    f"http://localhost:{target_port}/glint", 
                    json=test_glint, 
                    timeout=2
                )
                print(f"  ✅ Glint POST test: {glint_response.status_code}")
                
            except Exception as e:
                print(f"  ⚠️  Glint POST test failed: {e}")
                
        except Exception as e:
            print(f"  ❌ No service found on port {target_port}: {e}")
            print(f"  💡 Try running: python app.py")
            
    except ImportError:
        print("  ❌ Requests module not available - install with: pip install requests")
    except Exception as e:
        print(f"  ❌ Web integration test failed: {e}")

if __name__ == "__main__":
    print("🧪 Comprehensive Override Integration Tests")
    print("=" * 50)
    
    # Run cascade integration tests
    try:
        test_cascade_override_integration()
        print("\n✅ Cascade integration tests completed")
    except Exception as e:
        print(f"\n❌ Cascade integration tests failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Run state transition tests
    try:
        test_override_state_transitions()
        print("\n✅ State transition tests completed")
    except Exception as e:
        print(f"\n❌ State transition tests failed: {e}")
    
    # Run web integration tests
    try:
        test_override_web_integration()
        print("\n✅ Web integration tests completed")
    except Exception as e:
        print(f"\n❌ Web integration tests failed: {e}")
    
    print("\n🌀 All tests completed")