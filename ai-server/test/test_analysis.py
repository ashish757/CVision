#!/usr/bin/env python3
"""
Test script for CVision AI Analysis Service
"""
import asyncio
import json
import tempfile
import os
from app.services.analysis_service import AnalysisService
from app.models.analysis import AnalyzeRequest, AnalyzeResponse


async def test_analysis_service():
    """Test the analysis service with a mock file"""

    # Create a temporary test file (PDF simulation)
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
        tmp_file.write(b"Mock PDF content for testing")
        temp_file_path = tmp_file.name

    try:
        print("🧪 Testing CVision AI Analysis Service")
        print("=" * 50)

        # Test the analysis service
        print(f"📁 Testing with file: {os.path.basename(temp_file_path)}")

        result = await AnalysisService.analyze_resume(temp_file_path)

        print("✅ Analysis completed successfully!")
        print("\n📊 Results:")
        print("-" * 30)
        print(f"Skills: {', '.join(result.skills)}")
        print(f"Experience: {result.experience_years} years")
        print(f"Education: {result.education}")
        print(f"Score: {result.score}/100")
        print(f"Processing Time: {result.processing_time_seconds}s")

        # Test JSON serialization
        print("\n🔍 JSON Output:")
        print(json.dumps(result.model_dump(), indent=2))

        # Test file validation
        print("\n🔐 Testing Validation:")
        print(f"File type valid: {AnalysisService.validate_file_type(temp_file_path)}")
        print(f"File size: {AnalysisService.get_file_size_mb(temp_file_path)} MB")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        # Clean up
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        print("\n🧹 Cleanup completed")


def test_invalid_file():
    """Test with invalid file types"""
    print("\n🚫 Testing Invalid File Types:")
    print("-" * 35)

    invalid_files = [
        "/tmp/test.txt",
        "/tmp/test.jpg",
        "/tmp/test.doc",  # Note: we only support .docx
    ]

    for file_path in invalid_files:
        is_valid = AnalysisService.validate_file_type(file_path)
        print(f"{file_path}: {'✅ Valid' if is_valid else '❌ Invalid'}")


if __name__ == "__main__":
    print("🚀 Starting CVision AI Analysis Service Tests\n")

    # Run async test
    asyncio.run(test_analysis_service())

    # Run sync tests
    test_invalid_file()

    print("\n✨ All tests completed!")
