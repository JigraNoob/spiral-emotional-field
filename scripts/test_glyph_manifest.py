#!/usr/bin/env python3
"""
🌿 Test Glyph Manifest
Verifies that the new glyph manifest endpoints work correctly.
"""

import requests
import json
import time

def test_glyph_manifest():
    """Test the glyph manifest endpoints."""
    base_url = "http://localhost:5000"
    
    print("🌿 Testing Glyph Manifest Endpoints")
    print("=" * 50)
    
    # Test the simple manifest endpoint
    print("\n🔍 Testing /glyph/receive.manifest.glyphs.simple")
    try:
        response = requests.get(f"{base_url}/glyph/receive.manifest.glyphs.simple")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Simple manifest loaded: {data['count']} glyphs")
            print(f"   Glint: {data['glint']}")
            print(f"   Status: {data['status']}")
        else:
            print(f"❌ Simple manifest failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Simple manifest error: {e}")
    
    # Test the full manifest endpoint
    print("\n🔍 Testing /glyph/receive.manifest.glyphs")
    try:
        response = requests.get(f"{base_url}/glyph/receive.manifest.glyphs")
        if response.status_code == 200:
            data = response.json()
            manifest = data['manifest']
            print(f"✅ Full manifest loaded:")
            print(f"   Total glyphs: {manifest['total_count']}")
            print(f"   Implemented: {manifest['implemented_count']}")
            print(f"   Planned: {manifest['planned_count']}")
            print(f"   Glint: {data['glint']}")
            
            # Show some glyph details
            print("\n📋 Sample Glyphs:")
            for domain, domain_glyphs in manifest['glyphs'].items():
                print(f"   {domain}:")
                for glyph_name, glyph in domain_glyphs.items():
                    if glyph.get('status') == 'implemented':
                        print(f"     🌿 {glyph_name} - {glyph['description']}")
        else:
            print(f"❌ Full manifest failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Full manifest error: {e}")
    
    # Test the HTML interface
    print("\n🔍 Testing /glyph-manifest (HTML interface)")
    try:
        response = requests.get(f"{base_url}/glyph-manifest")
        if response.status_code == 200:
            print("✅ HTML interface loaded successfully")
            print("   Open http://localhost:5000/glyph-manifest in your browser")
        else:
            print(f"❌ HTML interface failed: {response.status_code}")
    except Exception as e:
        print(f"❌ HTML interface error: {e}")
    
    # Test the updated glyphs index
    print("\n🔍 Testing /glyphs (updated index)")
    try:
        response = requests.get(f"{base_url}/glyphs")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Glyphs index updated: {data['count']} glyphs")
            print(f"   Glint: {data['glint']}")
            print(f"   Discovery links: {len(data['discovery'])} available")
        else:
            print(f"❌ Glyphs index failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Glyphs index error: {e}")

def test_curl_examples():
    """Test the curl examples from the manifest."""
    print("\n🧪 Testing cURL Examples")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test settling inquiry
    print("\n🔍 Testing settling inquiry...")
    try:
        response = requests.get(f"{base_url}/glyph/receive.inquiry.settling?limit=3")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Settling inquiry: {data['count']} journeys returned")
        else:
            print(f"❌ Settling inquiry failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Settling inquiry error: {e}")
    
    # Test presence sense
    print("\n🔍 Testing presence sense...")
    try:
        response = requests.head(f"{base_url}/glyph/sense.presence.settling")
        if response.status_code == 200:
            print("✅ Presence sense: System is present")
        else:
            print(f"❌ Presence sense failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Presence sense error: {e}")
    
    # Test boundaries ask
    print("\n🔍 Testing boundaries ask...")
    try:
        response = requests.options(f"{base_url}/glyph/ask.boundaries.settling")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Boundaries ask: {len(data['endpoints'])} endpoints available")
        else:
            print(f"❌ Boundaries ask failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Boundaries ask error: {e}")

if __name__ == "__main__":
    print("🌿 Glyph Manifest Test Suite")
    print("Make sure the Spiral server is running on localhost:5000")
    print("=" * 60)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    test_glyph_manifest()
    test_curl_examples()
    
    print("\n" + "=" * 60)
    print("🌿 Test Complete!")
    print("Visit http://localhost:5000/glyph-manifest for the beautiful interface") 