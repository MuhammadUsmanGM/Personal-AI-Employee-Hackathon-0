#!/usr/bin/env python3
"""
Startup script for Gold Tier Personal AI Employee System
Initializes and runs the complete Gold Tier system with all advanced features
"""
import os
import sys
import subprocess
import threading
import time
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.init_db import init_database
from src.config.manager import get_config
from src.ml_models.training_pipeline import download_pretrained_models


def initialize_gold_tier_system():
    """Initialize the Gold Tier system with all components"""
    print("Initializing Gold Tier Personal AI Employee System...")

    # Get configuration
    config = get_config()

    # Use existing obsidian vault structure from Bronze/Silver tier
    vault_path = Path("obsidian_vault")

    # Create only enterprise-specific directories without interfering with existing structure
    enterprise_dirs = ["Enterprise", "Analytics", "Models", "Reports", "Strategic_Planning", "Risk_Management", "Compliance"]

    for dir_name in enterprise_dirs:
        (vault_path / dir_name).mkdir(parents=True, exist_ok=True)

    print("Using existing obsidian vault structure from Bronze/Silver tier with enterprise extensions.")

    # Initialize database
    print("Initializing database...")
    init_database(config["database"]["url"])
    print("Database initialized.")

    # Download AI models if needed
    print("Downloading AI models...")
    try:
        download_pretrained_models()
        print("AI models downloaded.")
    except Exception as e:
        print(f"Warning: Could not download AI models: {e}")
        print("   This might be due to network issues or missing dependencies.")

    print("Gold Tier system initialized successfully!")


def run_orchestrator():
    """Run the orchestrator in a separate process"""
    try:
        from src.agents.orchestrator import Orchestrator

        # Start the orchestrator
        orchestrator = Orchestrator(vault_path="vault")
        orchestrator.run()
    except KeyboardInterrupt:
        print("🛑 Orchestrator stopped by user")
    except Exception as e:
        print(f"❌ Orchestrator error: {e}")


def run_api_server():
    """Run the API server in a separate process"""
    try:
        import uvicorn
        from src.api.main import app

        config = get_config()

        print(f"🌐 Starting API server on {config['api']['host']}:{config['api']['port']}")

        uvicorn.run(
            "src.api.main:app",
            host=config["api"]["host"],
            port=config["api"]["port"],
            reload=False,  # Disable reload in production
            workers=config["api"]["workers"],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("🛑 API server stopped by user")
    except Exception as e:
        print(f"❌ API server error: {e}")


def main():
    """Main function to start the Gold Tier system"""
    print("Gold Tier Personal AI Employee System Startup")
    print("=" * 50)

    # Initialize the system
    initialize_gold_tier_system()

    print("\nStarting Gold Tier services...")

    # Start orchestrator in a separate thread
    orchestrator_thread = threading.Thread(target=run_orchestrator, daemon=True)
    orchestrator_thread.start()

    # Give the orchestrator a moment to start
    time.sleep(2)

    # Start API server in a separate thread
    api_thread = threading.Thread(target=run_api_server, daemon=True)
    api_thread.start()

    print("Both orchestrator and API server started.")
    print("API available at: http://localhost:8000/api/docs")
    print("Orchestrator running in background")
    print("\nGold Tier features now available:")
    print("   • Advanced AI capabilities (NLP, prediction, recommendation)")
    print("   • Strategic planning and forecasting")
    print("   • Risk management and assessment")
    print("   • Compliance tracking and reporting")
    print("   • Resource optimization and allocation")
    print("   • Enterprise governance and policies")
    print("   • Business intelligence and analytics")
    print("   • Human-AI collaboration engine")
    print("\nPress Ctrl+C to stop the system.")

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down Gold Tier system...")
        print("Gold Tier system stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()