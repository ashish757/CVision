#!/usr/bin/env python3
"""
API Test script for CVision AI Analysis Service
"""
import requests
import json
import os
import time

BASE_URL = "http://localhost:8003"

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        print("🏥 Testing Health Endpoint")
        print("=" * 30)

        response = requests.get(f"{BASE_URL}/api/v1/analyze/health")

        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")
        return False

def test_analyze_endpoint():
    """Test the analyze endpoint"""
    try:
        print("\n🧠 Testing Analyze Endpoint")
        print("=" * 35)

        # Create test file path
        test_file = os.path.join(os.getcwd(), "test_resume.pdf")

        if not os.path.exists(test_file):
            print(f"❌ Test file not found: {test_file}")
            return False

        # Prepare request
        payload = {
            "file_path": test_file
        }

        print(f"📁 Testing with file: {test_file}")
        print("⏳ Sending analyze request...")

        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/api/v1/analyze",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()

        print(f"🕒 Request took: {end_time - start_time:.2f} seconds")

        if response.status_code == 200:
            print("✅ Analysis completed successfully!")
            result = response.json()

            print("\n📊 Analysis Results:")
            print("-" * 30)
            print(f"Skills: {', '.join(result['skills'])}")
            print(f"Experience: {result['experience_years']} years")
            print(f"Education: {result['education']}")
            print(f"Score: {result['score']}/100")
            print(f"Processing Time: {result['processing_time_seconds']}s")

            return True
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error testing analyze endpoint: {e}")
        return False

def test_invalid_file():
    """Test with invalid file"""
    try:
        print("\n🚫 Testing Invalid File")
        print("=" * 30)

        payload = {
            "file_path": "/nonexistent/file.pdf"
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/analyze",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 404:
            print("✅ Correctly handled invalid file")
            print(f"Error response: {response.json()}")
            return True
        else:
            print(f"❌ Unexpected response for invalid file: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error testing invalid file: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        print("\n🏠 Testing Root Endpoint")
        print("=" * 25)

        response = requests.get(f"{BASE_URL}/")

        if response.status_code == 200:
            print("✅ Root endpoint works")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error testing root endpoint: {e}")
        return False

if __name__ == "__main__":
    print("🚀 CVision AI Analysis Service API Tests")
    print("=" * 50)

    # Wait a moment for server to start
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)

    success_count = 0
    total_tests = 4

    # Run tests
    if test_root_endpoint():
        success_count += 1

    if test_health_endpoint():
        success_count += 1

    if test_analyze_endpoint():
        success_count += 1

    if test_invalid_file():
        success_count += 1

    # Summary
    print(f"\n📋 Test Summary")
    print("=" * 20)
    print(f"✅ Passed: {success_count}/{total_tests}")
    print(f"❌ Failed: {total_tests - success_count}/{total_tests}")

    if success_count == total_tests:
        print("\n🎉 All tests passed! Your API is working correctly.")
    else:
        print(f"\n⚠️  Some tests failed. Please check the output above.")
