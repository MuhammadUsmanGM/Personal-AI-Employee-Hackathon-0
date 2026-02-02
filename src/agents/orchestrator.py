import subprocess
import threading
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import os

# Add the project root to the Python path so imports work correctly
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.claude_skills.ai_employee_skills.processor import TaskProcessor
from src.utils.logger import setup_logger, log_activity

class TaskTriggerHandler(FileSystemEventHandler):
    """
    Handles file system events to trigger Claude Code when new tasks arrive
    """
    def __init__(self, processor, callback):
        self.processor = processor
        self.callback = callback
        self.logger = setup_logger("orchestrator.filesystem")

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.md'):
            return
        if 'Needs_Action' in event.src_path or 'Inbox' in event.src_path:
            self.logger.info(f"New task detected: {event.src_path}")
            log_activity("TRIGGER", f"New task detected: {event.src_path}", str(Path(event.src_path).parent.parent))
            self.callback()

class Orchestrator:
    """
    Coordinates all agents and manages the overall workflow
    """
    def __init__(self, vault_path="vault"):
        self.vault_path = Path(vault_path)
        self.needs_action_path = self.vault_path / 'Needs_Action'
        self.inbox_path = self.vault_path / 'Inbox'
        self.processor = TaskProcessor(vault_path=vault_path)
        self.running_watchers = []
        self.logger = setup_logger("orchestrator.main")

        # Create necessary directories if they don't exist
        self.needs_action_path.mkdir(parents=True, exist_ok=True)
        self.inbox_path.mkdir(parents=True, exist_ok=True)

    def start_watchers(self):
        """
        Start various watcher processes
        """
        self.logger.info("Starting orchestrator...")

        # Set up file system monitoring for new tasks
        self.setup_task_monitoring()

    def setup_task_monitoring(self):
        """
        Set up file system monitoring to trigger processing when new tasks arrive
        """
        event_handler = TaskTriggerHandler(self.processor, self.trigger_claude)
        observer = Observer()
        observer.schedule(event_handler, str(self.needs_action_path), recursive=True)
        observer.schedule(event_handler, str(self.inbox_path), recursive=True)
        observer.start()

        self.running_watchers.append(observer)
        self.logger.info(f"Monitoring {self.needs_action_path} and {self.inbox_path} for new tasks")

    def trigger_claude(self):
        """
        Trigger Claude Code to process new tasks
        """
        self.logger.info("Triggering Claude Code to process new tasks...")
        try:
            # Process tasks immediately
            processed_count = self.processor.process_pending_tasks()
            self.logger.info(f"Claude Code processed {processed_count} tasks")

            # Also process any approval requests
            self.processor.process_approval_requests()

        except Exception as e:
            self.logger.error(f"Error in Claude Code trigger: {e}")
            log_activity("ERROR", f"Error processing tasks: {e}", str(self.vault_path))

    def run(self):
        """
        Main run loop for the orchestrator
        """
        self.logger.info("Starting orchestrator main loop...")
        log_activity("SYSTEM", "Orchestrator started", str(self.vault_path))

        self.start_watchers()

        # Run the processor continuously in a separate thread
        processor_thread = threading.Thread(
            target=self.processor.run_continuous_processing,
            daemon=True
        )
        processor_thread.start()

        try:
            # Keep orchestrator running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Orchestrator shutting down...")
            log_activity("SYSTEM", "Orchestrator stopped", str(self.vault_path))
            self.cleanup()

    def cleanup(self):
        """
        Clean up resources
        """
        for watcher in self.running_watchers:
            if hasattr(watcher, 'stop'):
                watcher.stop()
            elif hasattr(watcher, 'terminate'):
                watcher.terminate()

        for watcher in self.running_watchers:
            if hasattr(watcher, 'join'):
                watcher.join()

if __name__ == "__main__":
    # Create default vault structure if it doesn't exist
    vault_path = "vault"
    vault_dirs = ["Inbox", "Needs_Action", "Plans", "Pending_Approval",
                  "Approved", "Rejected", "Done", "Logs"]

    vault_root = Path(vault_path)
    for dir_name in vault_dirs:
        (vault_root / dir_name).mkdir(parents=True, exist_ok=True)

    # Create Dashboard.md if it doesn't exist
    dashboard_path = vault_root / "Dashboard.md"
    if not dashboard_path.exists():
        dashboard_path.write_text("# AI Employee Dashboard\n\nSystem is initializing...")

    # Create Company_Handbook.md if it doesn't exist
    handbook_path = vault_root / "Company_Handbook.md"
    if not handbook_path.exists():
        from utils.handbook_parser import HandbookParser
        parser = HandbookParser(str(handbook_path))

    # Start the orchestrator
    orchestrator = Orchestrator(vault_path=vault_path)
    orchestrator.run()