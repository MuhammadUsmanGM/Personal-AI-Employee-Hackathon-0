from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from ..base_watcher import BaseWatcher
from pathlib import Path
from datetime import datetime
import os

class GmailWatcher(BaseWatcher):
    def __init__(self, vault_path: str, credentials_path: str = None):
        import os
        from src.config.manager import get_config

        super().__init__(vault_path, check_interval=get_config('check_interval.gmail', 120))  # 2 minutes
        self.credentials_path = credentials_path or os.getenv('GMAIL_CREDENTIALS_PATH') or get_config('gmail.credentials_path')
        self.creds = Credentials.from_authorized_user_file(self.credentials_path) if self.credentials_path else None
        self.service = build('gmail', 'v1', credentials=self.creds) if self.creds else None
        self.processed_ids = set()

    def check_for_updates(self) -> list:
        if not self.service:
            self.logger.warning("Gmail service not initialized, returning empty list")
            return []

        try:
            results = self.service.users().messages().list(
                userId='me', q='is:unread is:important'
            ).execute()
            messages = results.get('messages', [])
            return [m for m in messages if m['id'] not in self.processed_ids]
        except Exception as e:
            self.logger.error(f"Error checking for Gmail updates: {e}")
            return []

    def create_action_file(self, message) -> Path:
        if not self.service:
            raise Exception("Gmail service not initialized")

        try:
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
        except Exception as e:
            self.logger.error(f"Error creating action file: {e}")
            raise