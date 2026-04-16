#!/usr/bin/env python3
"""
Script to run the FastAPI backend server
"""
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    reload = os.getenv("DEBUG", "False").lower() == "true"

    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )