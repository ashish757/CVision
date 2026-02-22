#!/usr/bin/env python3
"""
Simple server startup script for CVision AI Analysis Service
"""
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Starting CVision AI Analysis Service...")
    from app.main import app

    print("App loaded successfully")

    import uvicorn
    print("Starting server on port 4000...")

    if __name__ == "__main__":
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=4000,
            log_level="info",
            reload=True
        )

except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
