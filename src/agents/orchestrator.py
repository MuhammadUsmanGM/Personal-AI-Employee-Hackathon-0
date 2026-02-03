import subprocess
import threading
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import os
from datetime import datetime
from typing import Optional

# Add the project root to the Python path so imports work correctly
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.claude_skills.ai_employee_skills.processor import TaskProcessor
from src.utils.logger import setup_logger, log_activity
from src.services.calendar_service import CalendarService
from src.services.predictive_analytics_service import PredictiveAnalyticsService
from src.services.adaptive_learning_service import AdaptiveLearningService
from src.services.database import init_db, SessionLocal
from src.config.manager import ConfigManager

class TaskTriggerHandler(FileSystemEventHandler):
    """
    Handles file system events to trigger Claude Code when new tasks arrive
    """
    def __init__(self, processor, callback):
        super().__init__()
        self.processor = processor
        self.callback = callback
        self.logger = setup_logger("orchestrator.filesystem")

        # Initialize Silver Tier services
        from src.config.manager import ConfigManager
        config_manager = ConfigManager()
        self.config = config_manager.config
        self.calendar_service = None
        self.analytics_service = None
        self.learning_service = None

        if self.config.get("silver_tier_features", {}).get("enable_learning", False):
            self._initialize_silver_services()

    def _initialize_silver_services(self):
        """Initialize Silver Tier services"""
        try:
            # Initialize database
            init_db(self.config["database"]["url"])

            # Create session for services
            db_session = SessionLocal()

            if self.config["silver_tier_features"]["enable_learning"]:
                self.learning_service = AdaptiveLearningService(db_session)

            if self.config["silver_tier_features"]["enable_analytics"]:
                self.analytics_service = PredictiveAnalyticsService(db_session)

            if self.config["integrations"]["calendar_enabled"]:
                self.calendar_service = CalendarService(db_session)

            log_activity("SILVER_SERVICES_INITIALIZED",
                        "Silver Tier services initialized successfully",
                        self.config["vault_path"])

        except Exception as e:
            log_activity("SILVER_SERVICES_INIT_ERROR",
                        f"Error initializing Silver Tier services: {str(e)}",
                        self.config["vault_path"])

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
    def __init__(self, vault_path="obsidian_vault"):
        self.vault_path = Path(vault_path)
        self.needs_action_path = self.vault_path / 'Needs_Action'
        self.inbox_path = self.vault_path / 'Inbox'
        self.processor = TaskProcessor(vault_path=vault_path)
        self.running_watchers = []
        self.logger = setup_logger("orchestrator.main")

        # Initialize Silver Tier configuration
        from src.config.manager import ConfigManager
        config_manager = ConfigManager()
        self.config = config_manager.config

        # Initialize Silver Tier services if enabled
        self.calendar_service = None
        self.analytics_service = None
        self.learning_service = None
        self.silver_services_initialized = False

        # Create necessary directories if they don't exist
        self.needs_action_path.mkdir(parents=True, exist_ok=True)
        self.inbox_path.mkdir(parents=True, exist_ok=True)

        if self.config.get("silver_tier_features", {}).get("enable_learning", False):
            self._initialize_silver_services()

    def _initialize_silver_services(self):
        """Initialize Silver Tier services"""
        try:
            # Initialize database
            init_db(self.config["database"]["url"])

            # Create session for services
            db_session = SessionLocal()

            if self.config["silver_tier_features"]["enable_learning"]:
                self.learning_service = AdaptiveLearningService(db_session)

            if self.config["silver_tier_features"]["enable_analytics"]:
                self.analytics_service = PredictiveAnalyticsService(db_session)

            if self.config["integrations"]["calendar_enabled"]:
                self.calendar_service = CalendarService(db_session)

            self.silver_services_initialized = True
            log_activity("SILVER_SERVICES_INITIALIZED",
                        "Silver Tier services initialized successfully",
                        str(self.vault_path))

        except Exception as e:
            self.logger.error(f"Error initializing Silver Tier services: {e}")
            log_activity("SILVER_SERVICES_INIT_ERROR",
                        f"Error initializing Silver Tier services: {str(e)}",
                        str(self.vault_path))

    def start_watchers(self):
        """
        Start various watcher processes
        """
        self.logger.info("Starting orchestrator...")

        # Set up file system monitoring for new tasks
        self.setup_task_monitoring()

        # Start Silver Tier services if enabled
        if self.silver_services_initialized:
            self._start_silver_services()

    def _start_silver_services(self):
        """Start Silver Tier services"""
        try:
            # Start calendar sync if enabled
            if self.config["integrations"]["calendar_enabled"] and self.calendar_service:
                # In a real implementation, this would start a periodic sync
                # For now, we'll just log that it's enabled
                self.logger.info("Calendar integration enabled")

            # Start learning processes if enabled
            if self.config["silver_tier_features"]["enable_learning"] and self.learning_service:
                self.logger.info("Learning service enabled")

            # Start analytics if enabled
            if self.config["silver_tier_features"]["enable_analytics"] and self.analytics_service:
                self.logger.info("Analytics service enabled")

        except Exception as e:
            self.logger.error(f"Error starting Silver Tier services: {e}")

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

            # Apply Silver Tier features if enabled
            if self.silver_services_initialized:
                self._apply_silver_tier_features(processed_count)

        except Exception as e:
            self.logger.error(f"Error in Claude Code trigger: {e}")
            log_activity("ERROR", f"Error processing tasks: {e}", str(self.vault_path))

    def _apply_silver_tier_features(self, processed_count: int):
        """
        Apply Silver Tier features after task processing
        """
        try:
            # Run predictive analytics if enabled
            if self.config["silver_tier_features"]["enable_analytics"] and self.analytics_service:
                # Generate predictions and recommendations
                recommendations = self.analytics_service.generate_personalized_recommendations(
                    user_id="default_user"
                )
                self.logger.info(f"Generated {len(recommendations)} personalized recommendations")

            # Run learning updates if enabled
            if self.config["silver_tier_features"]["enable_learning"] and self.learning_service:
                # Apply learning to task processing
                self.learning_service.learn_from_user_behavior(user_id="default_user")

            # Sync calendar if enabled
            if self.config["integrations"]["calendar_enabled"] and self.calendar_service:
                # Sync calendar events if configured
                if self.config["calendar"]["sync_enabled"]:
                    success = self.calendar_service.sync_calendar_events(
                        user_id="default_user",
                        provider=self.config["calendar"]["default_provider"]
                    )
                    if success:
                        self.logger.info("Calendar events synced successfully")

        except Exception as e:
            self.logger.error(f"Error applying Silver Tier features: {e}")
            log_activity("SILVER_FEATURE_ERROR",
                        f"Error applying Silver Tier features: {str(e)}",
                        str(self.vault_path))

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