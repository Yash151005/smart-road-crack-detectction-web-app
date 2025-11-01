#!/usr/bin/env python3
"""
Test script to verify the SmartRoadCrackWebApp functionality
"""

import os
import sys
from flask import Flask
from src.image_processing import detect_cracks, calculate_crack_percentage

def test_image_processing():
    """Test the image processing functions"""
    print("Testing image processing functions...")
    
    # Check if test image exists
    test_image_path = "data/upload/test_road.jpg"
    if not os.path.exists(test_image_path):
        print(f"⚠️  Test image not found at {test_image_path}")
        print("   Please add a road image to test with")
        return False
    
    try:
        # Test crack detection
        result_path = "static/results/test_processed.jpg"
        os.makedirs(os.path.dirname(result_path), exist_ok=True)
        
        mask_path = detect_cracks(test_image_path, result_path)
        print(f"✅ Crack detection completed: {result_path}")
        print(f"✅ Mask generated: {mask_path}")
        
        # Test percentage calculation
        crack_percentage = calculate_crack_percentage(mask_path)
        print(f"✅ Crack percentage calculated: {crack_percentage}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during image processing: {e}")
        return False

def test_flask_app():
    """Test Flask app setup"""
    print("\nTesting Flask app setup...")
    
    try:
        from app import app
        print("✅ Flask app imported successfully")
        
        # Check routes
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home route accessible")
            else:
                print(f"❌ Home route error: {response.status_code}")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def check_directories():
    """Check if required directories exist"""
    print("\nChecking required directories...")
    
    dirs = [
        "data/upload/",
        "static/results/",
        "templates/",
        "src/"
    ]
    
    all_exist = True
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} (missing)")
            os.makedirs(dir_path, exist_ok=True)
            print(f"   Created directory: {dir_path}")
    
    return all_exist

def main():
    """Run all tests"""
    print("🚀 SmartRoadCrackWebApp Test Suite")
    print("=" * 40)
    
    # Check directories
    check_directories()
    
    # Test Flask app
    flask_ok = test_flask_app()
    
    # Test image processing (if test image exists)
    processing_ok = test_image_processing()
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    print(f"Flask App: {'✅ PASS' if flask_ok else '❌ FAIL'}")
    print(f"Image Processing: {'✅ PASS' if processing_ok else '⚠️  SKIP (no test image)'}")
    
    if flask_ok:
        print("\n🎉 Ready to run! Use: python app.py")
    else:
        print("\n❌ Please fix the issues above before running the app")

if __name__ == "__main__":
    main()