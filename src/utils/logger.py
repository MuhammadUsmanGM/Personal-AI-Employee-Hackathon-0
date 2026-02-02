import logging
from pathlib import Path
from datetime import datetime
import os

def setup_logger(name, log_file=None, level=logging.INFO):
    """
    Set up a logger with both file and console handlers
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if log_file is provided)
    if log_file:
        # Ensure log directory exists
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def log_activity(activity_type, message, vault_path):
    """
    Log an activity to the vault's log directory with timestamp
    """
    log_dir = Path(vault_path) / "Logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"

    with open(log_file, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {activity_type.upper()}: {message}\n")

def get_recent_logs(vault_path, days=1):
    """
    Get recent log entries from the log directory
    """
    log_dir = Path(vault_path) / "Logs"
    if not log_dir.exists():
        return []

    log_entries = []
    for day_offset in range(days):
        date_str = (datetime.now() - datetime.timedelta(days=day_offset)).strftime('%Y-%m-%d')
        log_file = log_dir / f"{date_str}.log"

        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                log_entries.extend(f.readlines())

    return log_entries