#!/usr/bin/env python3
"""
Entry point for running the Silver Tier Personal AI Employee API
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.api.main import app
from src.services.init_db import init_database
from src.config.manager import ConfigManager

def main():
    """
    Main entry point for the API
    """
    print("Starting Silver Tier Personal AI Employee API...")

    # Get configuration
    config_manager = ConfigManager()
    config = config_manager.config

    # Initialize the database
    print("Initializing database...")
    init_database(config["database"]["url"])

    # Import and run uvicorn to serve the API
    try:
        import uvicorn

        # Get host and port from config
        host = config["api"]["host"]
        port = config["api"]["port"]

        print(f"Starting API server on {host}:{port}")

        # Run the FastAPI application
        uvicorn.run(
            "src.api.main:app",
            host=host,
            port=port,
            reload=True,  # Enable auto-reload during development
            workers=config["api"]["workers"],
            log_level="info"
        )

    except ImportError:
        print("Error: uvicorn is not installed.")
        print("Please install it with: pip install uvicorn")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting API server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()