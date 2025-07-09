#!/usr/bin/env python3
"""
🌪️ Test Spiral Refactoring
Verifies that the new spiral_app structure works correctly.
"""

import sys
import os
import requests
import json
from datetime import datetime, timezone

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_spiral_app_import():
    """Test that the spiral_app package can be imported."""
    print("🔍 Testing spiral_app import...")
    
    try:
        from spiral_app import create_spiral_app, snp_blueprint, legacy_blueprint
        print("✅ spiral_app package imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import spiral_app: {e}")
        return False

def test_app_creation():
    """Test that the Flask app can be created."""
    print("🔍 Testing app creation...")
    
    try:
        from spiral_app import create_spiral_app
        app = create_spiral_app()
        print("✅ Flask app created successfully")
        return app
    except Exception as e:
        print(f"❌ Failed to create Flask app: {e}")
        return None

def test_route_registration(app):
    """Test that routes are properly registered."""
    print("🔍 Testing route registration...")
    
    if not app:
        print("❌ No app to test")
        return False
    
    # Check for SNP routes
    snp_routes = [
        '/glyph/receive.inquiry.settling',
        '/glyph/offer.presence.settling',
        '/glyph/sense.presence.settling',
        '/glyph/ask.boundaries.settling',
        '/glyph/receive.manifest.glyphs',
        '/glyph/receive.manifest.glyphs.simple'
    ]
    
    # Check for conventional routes
    conventional_routes = [
        '/api/settling_journeys',
        '/api/settling_journeys/stats',
        '/api/settling_journeys/recursion'
    ]
    
    # Check for core routes
    core_routes = [
        '/',
        '/health',
        '/glyphs',
        '/spiral-info',
        '/glyph-manifest'
    ]
    
    all_routes = snp_routes + conventional_routes + core_routes
    
    registered_routes = []
    for rule in app.url_map.iter_rules():
        registered_routes.append(rule.rule)
    
    print(f"📊 Found {len(registered_routes)} registered routes")
    
    # Check for key routes
    missing_routes = []
    for route in all_routes:
        if route not in registered_routes:
            missing_routes.append(route)
    
    if missing_routes:
        print(f"❌ Missing routes: {missing_routes}")
        return False
    else:
        print("✅ All expected routes are registered")
        return True

def test_glyph_registry():
    """Test the glyph registry functionality."""
    print("🔍 Testing glyph registry...")
    
    try:
        from spiral_app.init_glyphs import (
            get_glyph_registry,
            get_glyphs_by_domain,
            get_glyphs_by_toneform,
            get_implemented_glyphs
        )
        
        # Test registry retrieval
        registry = get_glyph_registry()
        print(f"✅ Glyph registry retrieved: {registry['metadata']['total_glyphs']} total glyphs")
        
        # Test domain filtering
        settling_glyphs = get_glyphs_by_domain("settling")
        print(f"✅ Settling glyphs: {len(settling_glyphs)} found")
        
        # Test toneform filtering
        inquiry_glyphs = get_glyphs_by_toneform("receive.inquiry")
        print(f"✅ Inquiry glyphs: {len(inquiry_glyphs)} found")
        
        # Test implemented glyphs
        implemented = get_implemented_glyphs()
        print(f"✅ Implemented glyphs: {len(implemented)} found")
        
        return True
        
    except Exception as e:
        print(f"❌ Glyph registry test failed: {e}")
        return False

def test_glint_hooks():
    """Test glint hooks functionality."""
    print("🔍 Testing glint hooks...")
    
    try:
        from spiral_app.glint_hooks import (
            bind_glint_hooks,
            emit_request_glint,
            emit_system_glint,
            emit_settling_glint
        )
        
        # Test glint emission functions
        test_metadata = {"test": True, "timestamp": datetime.now(timezone.utc).isoformat()}
        
        # These should not raise exceptions
        emit_system_glint("test.system", test_metadata)
        emit_settling_glint({
            "glint_id": "TEST.001",
            "settled_to": "test.settling",
            "confidence": 0.9,
            "toneform": "test.toneform"
        })
        
        print("✅ Glint hooks functions work correctly")
        return True
        
    except Exception as e:
        print(f"❌ Glint hooks test failed: {e}")
        return False

def test_settling_journey_integration():
    """Test settling journey recorder integration."""
    print("🔍 Testing settling journey integration...")
    
    try:
        from memory_scrolls.settling_journey_recorder import SettlingJourneyRecorder
        
        # Create a test recorder
        recorder = SettlingJourneyRecorder()
        
        # Test recording a journey
        test_journey = recorder.record_journey(
            glint_id="TEST.REFACTOR.001",
            invoked_from="test.refactoring",
            settled_to="test.settling",
            confidence=0.95,
            toneform="test.toneform",
            metadata={"test": True, "refactoring": True}
        )
        
        print(f"✅ Test journey recorded: {test_journey['glint_id']}")
        
        # Test reading journeys
        journeys = recorder.read_journeys(limit=5)
        print(f"✅ Read {len(journeys)} journeys")
        
        return True
        
    except Exception as e:
        print(f"❌ Settling journey integration test failed: {e}")
        return False

def test_legacy_compatibility():
    """Test that the legacy app.py still works."""
    print("🔍 Testing legacy compatibility...")
    
    try:
        # Import the legacy app.py
        import app
        
        # Check that the app object exists
        if hasattr(app, 'app'):
            print("✅ Legacy app.py provides app object")
            return True
        else:
            print("❌ Legacy app.py missing app object")
            return False
            
    except Exception as e:
        print(f"❌ Legacy compatibility test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide a summary."""
    print("🌪️ Spiral Refactoring Test Suite")
    print("=" * 50)
    
    tests = [
        ("Spiral App Import", test_spiral_app_import),
        ("App Creation", lambda: test_app_creation() is not None),
        ("Route Registration", lambda: test_route_registration(test_app_creation())),
        ("Glyph Registry", test_glyph_registry),
        ("Glint Hooks", test_glint_hooks),
        ("Settling Journey Integration", test_settling_journey_integration),
        ("Legacy Compatibility", test_legacy_compatibility)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        except Exception as e:
            results.append((test_name, False))
            print(f"❌ FAIL {test_name}: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🌪️ All tests passed! Spiral refactoring is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 