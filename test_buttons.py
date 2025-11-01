"""
Simple test script to verify button functionality
"""
import requests
import os
from urllib.parse import urljoin

def test_flask_app():
    base_url = "http://127.0.0.1:5000"
    
    # Test 1: Check if the main page loads
    try:
        response = requests.get(base_url)
        print(f"✅ Main page status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Main page loads successfully")
        else:
            print("❌ Main page failed to load")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Flask app is not running! Please start the app first.")
        return False
    
    # Test 2: Test file upload with a test image
    image_path = "OIP.jpeg"
    if os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as f:
                files = {'image': f}
                response = requests.post(base_url, files=files)
                print(f"✅ Upload test status: {response.status_code}")
                if response.status_code == 200:
                    print("✅ Image upload and processing works!")
                    
                    # Check if the response contains result page content
                    if "Detection Result" in response.text:
                        print("✅ Result page generated successfully")
                        
                        # Check if buttons are present
                        if "Analyze Another Image" in response.text:
                            print("✅ 'Analyze Another Image' button found")
                        if "Download Report" in response.text:
                            print("✅ 'Download Report' button found")
                        if "Share Results" in response.text:
                            print("✅ 'Share Results' button found")
                            
                        return True
                    else:
                        print("❌ Result page content not found")
                        return False
                else:
                    print(f"❌ Upload failed with status: {response.status_code}")
                    print("Response:", response.text[:500])
                    return False
        except Exception as e:
            print(f"❌ Error during upload test: {e}")
            return False
    else:
        print(f"❌ Test image {image_path} not found")
        return False

    # Test 3: Test PDF download endpoint
    try:
        pdf_response = requests.get(urljoin(base_url, "/download_pdf"))
        if pdf_response.status_code == 200:
            print("✅ PDF download endpoint works")
        else:
            print(f"⚠️ PDF download returned status: {pdf_response.status_code}")
    except Exception as e:
        print(f"⚠️ PDF download test failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing Flask app functionality...")
    print("=" * 50)
    test_flask_app()
    print("=" * 50)
    print("✅ Test completed!")