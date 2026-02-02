# AGENTS.md - Personal AI Employee Hackathon 0

## Architecture Overview

The Personal AI Employee is a multi-agent system consisting of five core agent types that work together to create an autonomous digital employee:

1. **Claude Code Agent** - The primary reasoning engine
2. **Watcher Agents** - Sensory input collectors
3. **MCP Servers** - External action executors
4. **Orchestrator Agent** - Process coordinator
5. **Watchdog Agent** - Health monitor and recovery

## 1. Claude Code Agent

### Role
Primary reasoning and decision-making agent that processes tasks, makes decisions, and orchestrates actions.

### Technical Specifications
- **Type**: LLM-based reasoning agent
- **Platform**: Claude Code (Anthropic)
- **Execution Mode**: Interactive with Ralph Wiggum persistence loop
- **File System Access**: Full read/write access to Obsidian vault
- **MCP Integration**: Configured to use multiple MCP servers

### Core Capabilities
```
Input Processing → Reasoning → Decision Making → Action Planning → Output Generation
```

### File Operations
- Reads from: `/Needs_Action/`, `/Vault/`, `Company_Handbook.md`, `Business_Goals.md`
- Writes to: `/Plans/`, `/Done/`, `/Pending_Approval/`, `Dashboard.md`, `/Logs/`
- Creates: Plan.md files, Approval request files, Status updates

### Decision Logic Flow
1. Monitor `/Needs_Action/` folder for new tasks
2. Read `Company_Handbook.md` for rules and guidelines
3. Process input according to defined workflows
4. Create plan in `/Plans/` with status tracking
5. Execute or request approval for actions
6. Update `Dashboard.md` with status
7. Move processed items to `/Done/`

### Persistence Mechanism (Ralph Wiggum Loop)
- Continues execution until all tasks in `/Needs_Action/` are processed
- Uses stop hook to prevent early termination
- Monitors completion criteria before allowing exit

## 2. Watcher Agents

### 2.1 Base Watcher Class (Python)

```python
# base_watcher.py
import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod

class BaseWatcher(ABC):
    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process"""
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder"""
        pass

    def run(self):
        self.logger.info(f'Starting {self.__class__.__name__}')
        while True:
            try:
                items = self.check_for_updates()
                for item in items:
                    action_file = self.create_action_file(item)
                    self.logger.info(f'Created action file: {action_file}')
            except Exception as e:
                self.logger.error(f'Error in {self.__class__.__name__}: {e}')
            time.sleep(self.check_interval)
```

### 2.2 Gmail Watcher Agent

**Purpose**: Monitors Gmail for important/unread messages

**Dependencies**:
- `google-api-python-client`
- `google-auth-oauthlib`
- OAuth credentials file

**Implementation**:
```python
# gmail_watcher.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from base_watcher import BaseWatcher
from datetime import datetime

class GmailWatcher(BaseWatcher):
    def __init__(self, vault_path: str, credentials_path: str):
        super().__init__(vault_path, check_interval=120)  # 2 minutes
        self.creds = Credentials.from_authorized_user_file(credentials_path)
        self.service = build('gmail', 'v1', credentials=self.creds)
        self.processed_ids = set()

    def check_for_updates(self) -> list:
        results = self.service.users().messages().list(
            userId='me', q='is:unread is:important'
        ).execute()
        messages = results.get('messages', [])
        return [m for m in messages if m['id'] not in self.processed_ids]

    def create_action_file(self, message) -> Path:
        msg = self.service.users().messages().get(
            userId='me', id=message['id']
        ).execute()

        # Extract headers
        headers = {h['name']: h['value'] for h in msg['payload']['headers']}

        content = f'''---
type: email
from: {headers.get('From', 'Unknown')}
subject: {headers.get('Subject', 'No Subject')}
received: {datetime.now().isoformat()}
priority: high
status: pending
---

## Email Content
{msg.get('snippet', '')}

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
'''
        filepath = self.needs_action / f'EMAIL_{message["id"]}.md'
        filepath.write_text(content)
        self.processed_ids.add(message['id'])
        return filepath
```

### 2.3 WhatsApp Watcher Agent

**Purpose**: Monitors WhatsApp for urgent messages

**Dependencies**:
- `playwright`
- WhatsApp Web session data

**Implementation**:
```python
# whatsapp_watcher.py
from playwright.sync_api import sync_playwright
from base_watcher import BaseWatcher
from pathlib import Path
import json

class WhatsAppWatcher(BaseWatcher):
    def __init__(self, vault_path: str, session_path: str):
        super().__init__(vault_path, check_interval=30)  # 30 seconds
        self.session_path = Path(session_path)
        self.keywords = ['urgent', 'asap', 'invoice', 'payment', 'help']

    def check_for_updates(self) -> list:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                self.session_path, headless=True
            )
            page = browser.pages[0]
            page.goto('https://web.whatsapp.com')
            page.wait_for_selector('[data-testid="chat-list"]')

            # Find unread messages
            unread = page.query_selector_all('[aria-label*="unread"]')
            messages = []
            for chat in unread:
                text = chat.inner_text().lower()
                if any(kw in text for kw in self.keywords):
                    messages.append({'text': text, 'chat': chat})
            browser.close()
            return messages
```

### 2.4 File System Watcher Agent

**Purpose**: Monitors file system for new files dropped in designated folders

**Dependencies**:
- `watchdog`

**Implementation**:
```python
# filesystem_watcher.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import shutil

class DropFolderHandler(FileSystemEventHandler):
    def __init__(self, vault_path: str):
        self.needs_action = Path(vault_path) / 'Needs_Action'

    def on_created(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)
        dest = self.needs_action / f'FILE_{source.name}'
        shutil.copy2(source, dest)
        self.create_metadata(source, dest)

    def create_metadata(self, source: Path, dest: Path):
        meta_path = dest.with_suffix('.md')
        meta_path.write_text(f'''---
type: file_drop
original_name: {source.name}
size: {source.stat().st_size}
---

New file dropped for processing.
''')

class FileSystemWatcher:
    def __init__(self, watch_path: str, vault_path: str):
        self.watch_path = watch_path
        self.event_handler = DropFolderHandler(vault_path)
        self.observer = Observer()

    def start(self):
        self.observer.schedule(self.event_handler, self.watch_path, recursive=False)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()
```

## 3. MCP (Model Context Protocol) Servers

### 3.1 Email MCP Server

**Purpose**: Handle email sending, drafting, and management

**Capabilities**:
- `send_email(to: str, subject: str, body: str, attachments: list[str]?)`
- `draft_email(to: str, subject: str, body: str)`
- `search_emails(query: str)`

**Configuration**:
```json
{
  "name": "email-mcp",
  "command": "node",
  "args": ["/path/to/email-mcp-server/index.js"],
  "env": {
    "GMAIL_CREDENTIALS_PATH": "/secure/path/credentials.json"
  }
}
```

### 3.2 Browser MCP Server

**Purpose**: Handle web navigation, form filling, and payment processing

**Capabilities**:
- `navigate_to(url: str)`
- `click_element(selector: str)`
- `fill_form(fields: dict[str, str])`
- `extract_data_from_page(selectors: dict[str, str])`

**Configuration**:
```json
{
  "name": "browser-mcp",
  "command": "npx",
  "args": ["@anthropic/browser-mcp"],
  "env": {
    "HEADLESS": "true"
  }
}
```

### 3.3 Filesystem MCP Server

**Purpose**: Handle file operations within the vault

**Capabilities**:
- `read_file(path: str)`
- `write_file(path: str, content: str)`
- `list_directory(path: str)`
- `move_file(source: str, destination: str)`

**Configuration**: Built-in to Claude Code

## 4. Orchestrator Agent

### Purpose
Coordinates all agents and manages the overall workflow

### Responsibilities
- Starts and manages watcher processes
- Monitors folder changes
- Triggers Claude Code when new tasks arrive
- Manages scheduling for periodic tasks

### Implementation
```python
# orchestrator.py
import subprocess
import threading
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class TaskTriggerHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.md'):
            return
        if 'Needs_Action' in event.src_path:
            self.callback()

class Orchestrator:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action_path = self.vault_path / 'Needs_Action'
        self.running_watchers = []

    def start_watchers(self):
        # Start Gmail watcher
        gmail_process = subprocess.Popen(['python', 'gmail_watcher.py'])
        self.running_watchers.append(gmail_process)

        # Start file system watcher
        fs_watcher = FileSystemWatcher('/watch/folder', str(self.vault_path))
        fs_watcher.start()
        self.running_watchers.append(fs_watcher)

    def setup_task_monitoring(self):
        event_handler = TaskTriggerHandler(self.trigger_claude)
        observer = Observer()
        observer.schedule(event_handler, str(self.needs_action_path), recursive=True)
        observer.start()

    def trigger_claude(self):
        """Trigger Claude Code to process new tasks"""
        subprocess.run(['claude', '--prompt', f'Process all items in {self.needs_action_path}'])

    def run(self):
        self.setup_task_monitoring()
        self.start_watchers()

        # Keep orchestrator running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        for watcher in self.running_watchers:
            if hasattr(watcher, 'stop'):
                watcher.stop()
            elif hasattr(watcher, 'terminate'):
                watcher.terminate()
```

## 5. Watchdog Agent

### Purpose
Monitors system health and automatically restarts failed processes

### Responsibilities
- Monitors process health
- Restarts failed processes
- Logs system health metrics
- Sends alerts on critical failures

### Implementation
```python
# watchdog.py
import subprocess
import time
from pathlib import Path

PROCESSES = {
    'orchestrator': 'python orchestrator.py',
    'gmail_watcher': 'python gmail_watcher.py',
    'file_watcher': 'python filesystem_watcher.py'
}

def is_process_running(pid_file: Path) -> bool:
    if not pid_file.exists():
        return False
    try:
        pid = int(pid_file.read_text().strip())
        # Check if process exists (cross-platform)
        import psutil
        return psutil.pid_exists(pid)
    except:
        return False

def check_and_restart():
    for name, cmd in PROCESSES.items():
        pid_file = Path(f'/tmp/{name}.pid')
        if not is_process_running(pid_file):
            print(f'{name} not running, restarting...')
            proc = subprocess.Popen(cmd.split())
            pid_file.write_text(str(proc.pid))

if __name__ == "__main__":
    while True:
        check_and_restart()
        time.sleep(60)  # Check every minute
```

## Bronze Tier Implementation Plan

### Phase 1: Claude Code Setup
1. Install Claude Code CLI
2. Configure MCP servers in `~/.config/claude-code/mcp.json`
3. Set up Obsidian vault structure

### Phase 2: Basic Watcher Implementation
1. Implement `BaseWatcher` class
2. Create `FileSystemWatcher` for file drops
3. Test file monitoring functionality

### Phase 3: Obsidian Integration
1. Create `Dashboard.md` template
2. Create `Company_Handbook.md` with business rules
3. Set up folder structure:
   ```
   /Vault/
   ├── Dashboard.md
   ├── Company_Handbook.md
   ├── /Needs_Action/
   ├── /Plans/
   └── /Done/
   ```

### Phase 4: Basic MCP Integration
1. Configure filesystem MCP (built-in)
2. Test Claude Code file operations
3. Implement basic approval workflow

### Security Implementation
- Human-in-the-loop for sensitive actions
- File-based approval system
- Credential isolation in environment variables
- Audit logging for all actions

## File Format Specifications

### Action Item Format (`/Needs_Action/*.md`)
```yaml
---
type: email | whatsapp | file_drop | finance
from: sender_identifier
priority: low | medium | high | critical
status: pending
created: ISO_TIMESTAMP
---
```

### Plan Format (`/Plans/*.md`)
```yaml
---
created: ISO_TIMESTAMP
status: pending_approval | in_progress | completed
related_to: REFERENCE_ID
---

## Objective
[Clear objective statement]

## Steps
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Approval Required
[Description of required approvals]
```

### Approval Request Format (`/Pending_Approval/*.md`)
```yaml
---
type: approval_request
action: send_email | make_payment | execute_action
amount: DECIMAL_AMOUNT (if financial)
recipient: TARGET_RECIPIENT
reason: REASON_FOR_ACTION
created: ISO_TIMESTAMP
expires: EXPIRATION_TIMESTAMP
status: pending
---

## Action Details
- Description of the action to be approved

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder.
```