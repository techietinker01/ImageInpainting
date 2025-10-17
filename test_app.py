"""
Simple test script for Image Inpainting app
Tests the Flask endpoints without TensorFlow
"""
import requests
import base64
import json
from PIL import Image, ImageDraw
import io

def create_test_images():
    """Create simple test images for inpainting"""
    # Create a simple colored image
    original = Image.new('RGB', (256, 256), color='lightblue')
    draw = ImageDraw.Draw(original)
    draw.rectangle([50, 50, 200, 200], fill='red')
    
    # Create a mask (white background with black strokes)
    mask = Image.new('RGB', (256, 256), color='white')
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse([100, 100, 150, 150], fill='black')
    
    return original, mask

def image_to_base64(img):
    """Convert PIL Image to base64 data URL"""
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()
    return f'data:image/png;base64,{img_str}'

def test_status_endpoint(base_url='http://localhost:5000'):
    """Test the /api/status endpoint"""
    print("\n🔍 Testing /api/status endpoint...")
    try:
        response = requests.get(f'{base_url}/api/status', timeout=5)
        print(f"✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def test_about_endpoint(base_url='http://localhost:5000'):
    """Test the /about endpoint"""
    print("\n🔍 Testing /about endpoint...")
    try:
        response = requests.get(f'{base_url}/about', timeout=5)
        print(f"✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def test_inpainting_endpoint(base_url='http://localhost:5000'):
    """Test the /upload_mask endpoint with test images"""
    print("\n🔍 Testing /upload_mask endpoint (Image Inpainting)...")
    try:
        # Create test images
        print("   Creating test images...")
        original, mask = create_test_images()
        
        # Convert to base64
        original_b64 = image_to_base64(original)
        mask_b64 = image_to_base64(mask)
        
        # Send request
        print("   Sending inpainting request...")
        response = requests.post(
            f'{base_url}/upload_mask',
            json={'original': original_b64, 'mask': mask_b64},
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✅ Inpainting successful!")
            print(f"   Response type: {response.headers.get('Content-Type')}")
            print(f"   Image size: {len(response.content)} bytes")
            
            # Save the result
            result_img = Image.open(io.BytesIO(response.content))
            result_img.save('test_output.png')
            print(f"   ✅ Result saved to: test_output.png")
            return True
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Image Inpainting App Test Suite")
    print("=" * 60)
    
    base_url = 'http://localhost:5000'
    
    print(f"\n📍 Testing server at: {base_url}")
    print("   Make sure the server is running with: python app2.py")
    print()
    
    results = []
    results.append(("Status Endpoint", test_status_endpoint(base_url)))
    results.append(("About Endpoint", test_about_endpoint(base_url)))
    results.append(("Inpainting Endpoint", test_inpainting_endpoint(base_url)))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)

if __name__ == '__main__':
    main()
