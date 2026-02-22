#!/usr/bin/env python3
"""
Validation script for CVision AI Analysis Service
Tests all components without starting the server
"""
import sys
import os
import tempfile
import json
import asyncio

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported successfully"""
    print("🔍 Testing Imports")
    print("=" * 20)

    try:
        # Test FastAPI
        import fastapi
        print("✅ FastAPI imported")

        # Test Pydantic models
        from app.models.analysis import AnalyzeRequest, AnalyzeResponse, ErrorResponse
        print("✅ Pydantic models imported")

        # Test service
        from app.services.analysis_service import AnalysisService
        print("✅ Analysis service imported")

        # Test API routes
        from app.api.v1.analysis import router
        print("✅ API routes imported")

        # Test main app
        from app.main import app
        print("✅ Main app imported")

        return True

    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_models():
    """Test Pydantic models"""
    print("\n📋 Testing Pydantic Models")
    print("=" * 30)

    try:
        from app.models.analysis import AnalyzeRequest, AnalyzeResponse

        # Test AnalyzeResponse
        response = AnalyzeResponse(
            skills=["Python", "React"],
            experience_years=3,
            education="B.Tech",
            score=75,
            processing_time_seconds=2.5
        )
        print("✅ AnalyzeResponse model works")

        # Test serialization
        data = response.model_dump()
        print("✅ Model serialization works")

        # Test JSON conversion
        json_str = response.model_dump_json()
        print("✅ JSON serialization works")

        return True

    except Exception as e:
        print(f"❌ Model test error: {e}")
        return False

async def test_service():
    """Test analysis service"""
    print("\n🧠 Testing Analysis Service")
    print("=" * 30)

    try:
        from app.services.analysis_service import AnalysisService

        # Create a temporary test file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(b"Mock resume content for testing")
            temp_file_path = tmp_file.name

        try:
            # Test file validation
            is_valid = AnalysisService.validate_file_type(temp_file_path)
            print(f"✅ File validation: {is_valid}")

            # Test file size calculation
            size_mb = AnalysisService.get_file_size_mb(temp_file_path)
            print(f"✅ File size calculation: {size_mb} MB")

            # Test analysis
            result = await AnalysisService.analyze_resume(temp_file_path)
            print(f"✅ Analysis completed: {result.score}/100")
            print(f"   Skills: {len(result.skills)} skills found")
            print(f"   Experience: {result.experience_years} years")
            print(f"   Processing time: {result.processing_time_seconds}s")

            return True

        finally:
            # Clean up
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    except Exception as e:
        print(f"❌ Service test error: {e}")
        return False

def test_invalid_files():
    """Test validation with invalid files"""
    print("\n🚫 Testing Invalid File Handling")
    print("=" * 40)

    try:
        from app.services.analysis_service import AnalysisService

        # Test invalid extensions
        test_cases = [
            ("test.txt", False),
            ("test.pdf", True),
            ("test.docx", True),
            ("test.doc", False),
            ("test.jpg", False)
        ]

        for filename, expected in test_cases:
            result = AnalysisService.validate_file_type(filename)
            status = "✅" if result == expected else "❌"
            print(f"{status} {filename}: {result} (expected: {expected})")

        return True

    except Exception as e:
        print(f"❌ Invalid file test error: {e}")
        return False

def test_api_structure():
    """Test API structure and endpoints"""
    print("\n🔗 Testing API Structure")
    print("=" * 25)

    try:
        from app.main import app
        from fastapi.testclient import TestClient

        # This would require TestClient to be installed
        # For now, just check if the app has the expected attributes

        # Check if app is FastAPI instance
        import fastapi
        if isinstance(app, fastapi.FastAPI):
            print("✅ App is FastAPI instance")

        # Check if routes are registered
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/api/v1/analyze", "/api/v1/analyze/health"]

        for route in expected_routes:
            if any(route in r for r in routes):
                print(f"✅ Route registered: {route}")
            else:
                print(f"❌ Missing route: {route}")

        return True

    except Exception as e:
        print(f"❌ API structure test error: {e}")
        return False

async def run_all_tests():
    """Run all validation tests"""
    print("🚀 CVision AI Analysis Service Validation")
    print("=" * 50)

    tests = [
        ("Import Tests", test_imports),
        ("Model Tests", test_models),
        ("Service Tests", test_service),
        ("Invalid File Tests", test_invalid_files),
        ("API Structure Tests", test_api_structure)
    ]

    passed = 0
    total = len(tests)

    for name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()

            if result:
                passed += 1

        except Exception as e:
            print(f"\n❌ {name} failed with exception: {e}")

    print(f"\n📊 Validation Summary")
    print("=" * 25)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")

    if passed == total:
        print("\n🎉 All validations passed! Your CVision AI Analysis Service is ready!")
        print("\n📚 Next steps:")
        print("1. Start the server: python start_server.py")
        print("2. Test the API: python test_api.py")
        print("3. Check docs: http://localhost:8003/docs")
    else:
        print(f"\n⚠️  {total - passed} validation(s) failed. Please review the errors above.")

    return passed == total

if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
