import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

class FileSystemWatcher(FileSystemEventHandler):
    """
    Watches a specified directory for file changes and creates action files in Needs_Action
    """
    def __init__(self, watch_path: str, vault_path: str):
        self.watch_path = Path(watch_path)
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.logger = logging.getLogger(self.__class__.__name__)
        self.processed_files = set()

        # Create the needs_action directory if it doesn't exist
        self.needs_action.mkdir(parents=True, exist_ok=True)

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path in self.processed_files:
            return

        source = Path(event.src_path)
        self.processed_files.add(str(source))

        # Create action file for the new file
        self.create_action_file(source)
        self.logger.info(f'Created action file for: {source}')

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path in self.processed_files:
            return

        source = Path(event.src_path)
        self.processed_files.add(str(source))

        # Create action file for the modified file
        self.create_action_file(source)
        self.logger.info(f'Created action file for modified: {source}')

    def create_action_file(self, source: Path):
        """
        Create an action file in the Needs_Action folder for the given source file
        """
        # Create a unique name for the action file
        action_filename = f'FILE_{source.name}_{int(time.time())}.md'
        action_path = self.needs_action / action_filename

        # Create the action file content
        content = f'''---
type: file_drop
original_name: {source.name}
full_path: {str(source.absolute())}
size: {source.stat().st_size if source.exists() else 0}
modified: {time.ctime(source.stat().st_mtime) if source.exists() else time.ctime()}
---

## New File Dropped for Processing

A new file has been detected in the monitored directory:

- **Original Name**: {source.name}
- **Full Path**: {str(source.absolute())}
- **Size**: {source.stat().st_size if source.exists() else 0} bytes
- **Modified**: {time.ctime(source.stat().st_mtime) if source.exists() else time.ctime()}

## Suggested Actions
- [ ] Review the file content
- [ ] Determine appropriate processing steps
- [ ] Execute required actions based on Company Handbook rules
'''

        action_path.write_text(content)
        return action_path

    def start_watching(self):
        """
        Start watching the directory for changes
        """
        self.logger.info(f'Starting FileSystemWatcher for: {self.watch_path}')

        self.observer = Observer()
        self.observer.schedule(self, str(self.watch_path), recursive=False)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            self.logger.info('FileSystemWatcher stopped by user')

        self.observer.join()


class DropFolderHandler(FileSystemEventHandler):
    """
    Alternative implementation for handling file drops
    """
    def __init__(self, vault_path: str):
        self.needs_action = Path(vault_path) / 'Needs_Action'
        self.needs_action.mkdir(parents=True, exist_ok=True)

    def on_created(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)
        dest = self.needs_action / f'FILE_{source.name}'

        # Create metadata file with action instructions
        meta_content = f'''---
type: file_drop
original_name: {source.name}
size: {source.stat().st_size if source.exists() else 0}
---

## New File Dropped for Processing

File: {source.name}
Size: {source.stat().st_size if source.exists() else 0} bytes

## Processing Instructions
Review this file and determine appropriate action based on Company Handbook.
'''
        meta_path = dest.with_suffix('.md')
        meta_path.write_text(meta_content)


def run_filesystem_watcher(watch_path: str, vault_path: str):
    """
    Convenience function to run the filesystem watcher
    """
    watcher = FileSystemWatcher(watch_path, Path(vault_path))
    watcher.start_watching()