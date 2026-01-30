# Watcher System Specifications

## Overview
The Watcher system consists of lightweight Python scripts that run continuously, monitoring various inputs and creating actionable files for Claude Code to process. These serve as the sensory system for the Personal AI Employee.

## Core Watcher Pattern

### Base Watcher Class
```python
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
        '''Return list of new items to process'''
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        '''Create .md file in Needs_Action folder'''
        pass

    def run(self):
        self.logger.info(f'Starting {self.__class__.__name__}')
        while True:
            try:
                items = self.check_for_updates()
                for item in items:
                    self.create_action_file(item)
            except Exception as e:
                self.logger.error(f'Error: {e}')
            time.sleep(self.check_interval)
```

## Gmail Watcher Specification

### Configuration Requirements
- Google API credentials file
- OAuth 2.0 authentication
- Gmail API access scope
- Check interval: 120 seconds

### Functionality
- Monitor for unread, important emails
- Filter by priority keywords
- Create action files for urgent messages
- Track processed message IDs to avoid duplicates

### Action File Format
```markdown
---
type: email
from: sender@example.com
subject: Email Subject
received: 2026-01-07T10:30:00Z
priority: high
status: pending
---
## Email Content
Email snippet content here...

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
```

## WhatsApp Watcher Specification

### Configuration Requirements
- WhatsApp Web session persistence
- Playwright browser automation
- Keyword monitoring list
- Check interval: 30 seconds

### Functionality
- Monitor WhatsApp Web for unread messages
- Detect urgency keywords (urgent, asap, invoice, payment, help)
- Create action files for important conversations
- Maintain persistent browser session

### Security Considerations
- Comply with WhatsApp Terms of Service
- Use proper session management
- Handle login failures gracefully

## File System Watcher Specification

### Configuration Requirements
- Watched directory path
- File type filters
- Destination folder for action files

### Functionality
- Monitor specified directories for file creation/modification
- Copy files to Needs_Action folder
- Create metadata files with processing instructions
- Support for various file types (documents, images, etc.)

## Finance Watcher Specification

### Configuration Requirements
- Banking API credentials
- Transaction monitoring thresholds
- CSV import capabilities
- Account linking

### Functionality
- Monitor bank transactions
- Flag unusual or large transactions
- Create accounting entries
- Generate financial alerts

## Watcher Management System

### Process Management
- Auto-restart on failure
- Health monitoring
- Resource usage tracking
- Logging and error reporting

### Coordination
- Shared state management
- Conflict resolution
- Priority handling
- Rate limiting

## Error Handling

### Transient Errors
- Network timeouts
- API rate limits
- Temporary service unavailability
- Retry with exponential backoff

### Permanent Errors
- Invalid credentials
- Account suspension
- API deprecation
- Alert user and pause operations

## Performance Requirements

### Resource Usage
- Low CPU consumption (<5%)
- Minimal memory footprint
- Efficient network usage
- Disk space monitoring

### Responsiveness
- Sub-second detection of changes
- Immediate action file creation
- Quick error recovery
- Real-time status updates

## Security Requirements

### Data Protection
- No sensitive data in logs
- Encrypted credential storage
- Secure API communication
- Access control for action files

### Privacy Compliance
- Local processing only
- No data transmission without consent
- Anonymization of personal information
- Compliance with local regulations

## Monitoring and Logging

### Required Logs
- Start/stop events
- Processing statistics
- Error occurrences
- Performance metrics

### Alerting
- Failure notifications
- Performance degradation
- Security incidents
- Configuration changes

## Deployment Considerations

### Local Deployment
- Persistent execution
- System startup integration
- Resource constraints
- Network reliability

### Cloud Deployment (Platinum Tier)
- Containerized execution
- Auto-scaling capabilities
- Load balancing
- High availability