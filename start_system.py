#!/usr/bin/env python3
"""
Startup script for Silver Tier Personal AI Employee System
Runs both the orchestrator and API server
"""
import os
import sys
import subprocess
import threading
import time
from pathlib import Path

def run_orchestrator():
    """Run the orchestrator in a separate process"""
    try:
        # Run the orchestrator
        result = subprocess.run([
            sys.executable, "-c",
            """
import sys
from pathlib import Path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.agents.orchestrator import Orchestrator

# Create default vault structure if it doesn't exist
vault_path = "vault"
vault_dirs = ["Inbox", "Needs_Action", "Plans", "Pending_Approval",
              "Approved", "Rejected", "Done", "Logs", "obsidian_vault"]

vault_root = Path(vault_path)
for dir_name in vault_dirs:
    (vault_root / dir_name).mkdir(parents=True, exist_ok=True)

# Create Dashboard.md if it doesn't exist
dashboard_path = vault_root / "Dashboard.md"
if not dashboard_path.exists():
    dashboard_path.write_text("# AI Employee Dashboard\\n\\nSystem is initializing...")

# Create Company_Handbook.md if it doesn't exist
handbook_path = vault_root / "Company_Handbook.md"
if not handbook_path.exists():
    handbook_content = '''# Company Handbook

## Mission
Our mission is to deliver exceptional value to our customers through innovative AI solutions.

## Values
- Innovation
- Excellence
- Customer Focus
- Integrity
'''
    handbook_path.write_text(handbook_content)

# Start the orchestrator
orchestrator = Orchestrator(vault_path=vault_path)
orchestrator.run()
            """
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Orchestrator exited with error: {e}")
    except KeyboardInterrupt:
        print("Orchestrator stopped by user")

def run_api():
    """Run the API server in a separate process"""
    try:
        result = subprocess.run([sys.executable, "run_api.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"API server exited with error: {e}")
    except KeyboardInterrupt:
        print("API server stopped by user")

def main():
    """Main function to start both services"""
    print("Starting Silver Tier Personal AI Employee System...")

    # Create vault directories if they don't exist
    vault_path = Path("vault")
    vault_dirs = ["Inbox", "Needs_Action", "Plans", "Pending_Approval",
                  "Approved", "Rejected", "Done", "Logs", "obsidian_vault"]

    for dir_name in vault_dirs:
        (vault_path / dir_name).mkdir(parents=True, exist_ok=True)

    print("Vault directories created.")

    # Start orchestrator in a separate thread
    orchestrator_thread = threading.Thread(target=run_orchestrator, daemon=True)
    orchestrator_thread.start()

    # Give the orchestrator a moment to start
    time.sleep(2)

    # Start API server in a separate thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    print("Both orchestrator and API server started.")
    print("Press Ctrl+C to stop the system.")

    try:
        # Wait for both threads
        orchestrator_thread.join()
        api_thread.join()
    except KeyboardInterrupt:
        print("\\nShutting down Silver Tier system...")
        sys.exit(0)

if __name__ == "__main__":
    main()