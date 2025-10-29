#!/usr/bin/env python3
"""
DRISHTI-SHIELD System Test Script
Tests the complete full-stack application
"""

import requests
import json
import os
from pathlib import Path

def test_api_health():
    """Test if the API server is running"""
    try:
        response = requests.get("http://127.0.0.1:8000/")
        if response.status_code == 200:
            print("✅ API Health Check: PASSED")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ API Health Check: FAILED (Status: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API Health Check: FAILED (Connection Error)")
        print("   Make sure the FastAPI server is running: python api_server.py")
        return False

def test_analyze_endpoint():
    """Test the main analysis endpoint with dummy files"""
    try:
        # Check if test images exist
        before_image = Path("/Users/srijeetbanerjee/DS_FINAL/test_images/satellite_before.png")
        after_image = Path("/Users/srijeetbanerjee/DS_FINAL/test_images/satellite_after.png")
        
        if not before_image.exists() or not after_image.exists():
            print("❌ Analysis Test: FAILED (Test images not found)")
            print("   Make sure dummy_before.png and dummy_after.png exist")
            return False
        
        # Prepare files for upload
        files = {
            'image_before': ('before.png', open(before_image, 'rb'), 'image/png'),
            'image_after': ('after.png', open(after_image, 'rb'), 'image/png')
        }
        
        print("🔄 Testing analysis endpoint...")
        response = requests.post("http://127.0.0.1:8000/api/v1/analyze", files=files)
        
        # Close files
        files['image_before'][1].close()
        files['image_after'][1].close()
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis Endpoint: PASSED")
            print(f"   Success: {result.get('success', False)}")
            print(f"   Risk Score: {result.get('risk_score', 'N/A')}")
            print(f"   Anomalies: {len(result.get('anomalies_geojson', {}).get('features', []))} detected")
            return True
        else:
            print(f"❌ Analysis Endpoint: FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Analysis Endpoint: FAILED (Exception: {e})")
        return False

def test_static_files():
    """Test if static files are being served"""
    try:
        response = requests.get("http://127.0.0.1:8000/static/change_mask_demo.png")
        if response.status_code == 200:
            print("✅ Static Files: PASSED")
            return True
        else:
            print(f"❌ Static Files: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Static Files: FAILED (Exception: {e})")
        return False

def test_frontend_files():
    """Test if frontend files exist"""
    frontend_file = Path("/Users/srijeetbanerjee/DS_FINAL/frontend/index.html")
    if frontend_file.exists():
        print("✅ Frontend Files: PASSED")
        print(f"   Frontend available at: file://{frontend_file.absolute()}")
        return True
    else:
        print("❌ Frontend Files: FAILED")
        print("   Frontend index.html not found")
        return False

def main():
    """Run all tests"""
    print("🛡️ DRISHTI-SHIELD System Test")
    print("=" * 50)
    
    tests = [
        ("API Health Check", test_api_health),
        ("Analysis Endpoint", test_analyze_endpoint), 
        ("Static Files", test_static_files),
        ("Frontend Files", test_frontend_files)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! DRISHTI-SHIELD is ready for demo!")
        print("\n🚀 Quick Start:")
        print("1. Backend: python api_server.py")
        print("2. Frontend: Open frontend/index.html in browser")
        print("3. API Docs: http://127.0.0.1:8000/docs")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    main()
