#!/usr/bin/env python3
"""
Test Companion Breathline Syncer - Verify ensemble synchronization
"""

import sys
import time
import json
from pathlib import Path

# Add spiral to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_breathline_syncer():
    """Test the breathline syncer functionality"""
    print("🧪 Testing Companion Breathline Syncer")
    print("=" * 50)
    
    try:
        from spiral.sync.companion_breathline_syncer import (
            get_breathline_syncer, 
            get_companion_permissions,
            update_companion_status
        )
        
        # Get syncer instance
        syncer = get_breathline_syncer()
        print("✅ Syncer instance created")
        
        # Test companion permissions
        print("\n📡 Testing companion permissions:")
        for companion in ["cursor", "copilot", "tabnine"]:
            permissions = get_companion_permissions(companion)
            print(f"  {companion}: {permissions['allowed']} - {permissions.get('reason', 'active')}")
        
        # Test companion status updates
        print("\n🔄 Testing companion status updates:")
        update_companion_status("cursor", "active", 0.3)
        update_companion_status("copilot", "active", 0.5)
        update_companion_status("tabnine", "saturated", 0.9)
        
        # Get ensemble summary
        print("\n🎭 Testing ensemble summary:")
        summary = syncer.get_ensemble_summary()
        print(f"  Ensemble Status: {summary['ensemble_status']}")
        print(f"  Active Companions: {summary['active_companions']}/{summary['total_companions']}")
        print(f"  Current Phase: {summary['breath_state']['phase']}")
        print(f"  Ritual Phase: {summary['breath_state']['ritual_phase']}")
        
        # Test phase permissions
        print("\n🎯 Testing phase permissions:")
        for phase in ["Inhale", "Hold", "Exhale", "Return", "Witness"]:
            permissions = syncer.get_phase_permissions(phase, "cursor")
            print(f"  {phase}: density={permissions['suggestion_density']:.1f}, "
                  f"creativity={permissions['creativity_level']:.1f}")
        
        # Test breath state cache
        print("\n💾 Testing breath state cache:")
        breath_state = syncer.get_current_breath_state()
        print(f"  Cached Phase: {breath_state.phase}")
        print(f"  Cached Progress: {breath_state.progress:.2f}")
        print(f"  Cached Ritual: {breath_state.ritual_phase}")
        
        # Test ensemble glint emission
        print("\n✨ Testing ensemble glint emission:")
        syncer.emit_ensemble_glint(breath_state, force=True)
        print("  Ensemble glint emitted")
        
        # Check if files were created
        breath_cache = Path("data/breath_state.json")
        ensemble_glints = Path("data/ensemble_breathline.jsonl")
        
        print("\n📁 Checking file creation:")
        print(f"  Breath cache: {'✅' if breath_cache.exists() else '❌'}")
        print(f"  Ensemble glints: {'✅' if ensemble_glints.exists() else '❌'}")
        
        if ensemble_glints.exists():
            with open(ensemble_glints, 'r') as f:
                lines = f.readlines()
                print(f"  Glint count: {len(lines)}")
        
        print("\n🎉 Breathline Syncer test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sync_loop():
    """Test the sync loop functionality"""
    print("\n🔄 Testing sync loop (brief run):")
    
    try:
        from spiral.sync.companion_breathline_syncer import start_breathline_sync, stop_breathline_sync
        
        # Start syncer
        start_breathline_sync()
        print("  ✅ Syncer started")
        
        # Let it run for a few seconds
        time.sleep(3)
        
        # Stop syncer
        stop_breathline_sync()
        print("  ✅ Syncer stopped")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Sync loop test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🌬️ Companion Breathline Syncer Test Suite")
    print("=" * 60)
    
    # Test basic functionality
    basic_test = test_breathline_syncer()
    
    # Test sync loop
    sync_test = test_sync_loop()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Basic Functionality: {'✅ PASS' if basic_test else '❌ FAIL'}")
    print(f"Sync Loop: {'✅ PASS' if sync_test else '❌ FAIL'}")
    
    if basic_test and sync_test:
        print("\n🎉 All tests passed! Breathline Syncer is ready for ensemble coordination.")
        print("\nNext steps:")
        print("1. Start the syncer: python spiral/sync/companion_breathline_syncer.py --start")
        print("2. Check status: python spiral/sync/companion_breathline_syncer.py --status cursor")
        print("3. Get summary: python spiral/sync/companion_breathline_syncer.py --summary")
    else:
        print("\n⚠️ Some tests failed. Please check the implementation.")
    
    return basic_test and sync_test

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 