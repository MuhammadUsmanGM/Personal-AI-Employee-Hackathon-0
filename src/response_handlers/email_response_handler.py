import asyncio
import base64
import time
from typing import Dict, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .base_handler import BaseResponseHandler, CommunicationChannel, ResponseStatus


class EmailResponseHandler(BaseResponseHandler):
    """
    Response handler for sending email responses via Gmail API
    """
    def __init__(self, credentials_path: Optional[str] = None, token_path: Optional[str] = "./token.json"):
        super().__init__(CommunicationChannel.EMAIL)
        self.credentials_path = credentials_path or os.getenv('GMAIL_CREDENTIALS_PATH')
        self.token_path = token_path
        self.service = self._setup_gmail_service()

    def _setup_gmail_service(self):
        """
        Set up Gmail API service with proper authentication
        """
        creds = None

        # Load existing credentials
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, ['https://www.googleapis.com/auth/gmail.send'])

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self.credentials_path or not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        "Gmail credentials file not found. Please set GMAIL_CREDENTIALS_PATH."
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, ['https://www.googleapis.com/auth/gmail.send']
                )
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def validate_recipient(self, recipient_identifier: str) -> bool:
        """
        Validate that the recipient identifier is a valid email address

        Args:
            recipient_identifier: Email address to validate

        Returns:
            True if valid, False otherwise
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, recipient_identifier) is not None

    def format_response(self, content: str, response_format: Optional[str] = "plain") -> str:
        """
        Format the response content appropriately for email

        Args:
            content: Raw content to format
            response_format: Format type - 'plain' or 'html'

        Returns:
            Formatted content string
        """
        if response_format == "html":
            # Wrap content in basic HTML structure
            return f"<html><body>{content}</body></html>"
        else:
            # Plain text format
            return content.strip()

    async def send_response(self, recipient_identifier: str, content: str, subject: Optional[str] = "Response from AI Employee", **kwargs) -> Dict[str, Any]:
        """
        Send an email response to the specified recipient

        Args:
            recipient_identifier: Email address of the recipient
            content: Content of the response message
            subject: Subject of the email
            **kwargs: Additional parameters (cc, bcc, attachments, etc.)

        Returns:
            Dictionary containing response details and status
        """
        try:
            # Validate recipient
            if not self.validate_recipient(recipient_identifier):
                return await self.handle_error(
                    ValueError(f"Invalid email address: {recipient_identifier}"),
                    recipient_identifier,
                    content
                )

            # Format the content
            formatted_content = self.format_response(content, kwargs.get('format', 'plain'))

            # Create message
            message = self._create_message(
                sender=os.getenv('GMAIL_USER_EMAIL', 'me'),
                to=recipient_identifier,
                subject=subject,
                message_text=formatted_content,
                message_type=kwargs.get('format', 'plain'),
                **kwargs
            )

            # Send the message
            sent_message = self.service.users().messages().send(
                userId="me",
                body=message
            ).execute()

            # Log success
            self.log_response_attempt(recipient_identifier, content, ResponseStatus.SENT)

            return {
                "status": ResponseStatus.SENT.value,
                "message_id": sent_message['id'],
                "recipient": recipient_identifier,
                "timestamp": time.time(),
                "provider_message_id": sent_message['id']
            }

        except HttpError as error:
            return await self.handle_error(error, recipient_identifier, content)
        except Exception as error:
            return await self.handle_error(error, recipient_identifier, content)

    def _create_message(self, sender: str, to: str, subject: str, message_text: str, message_type: str = "plain", **kwargs):
        """
        Create a message for the Gmail API

        Args:
            sender: Sender email address
            to: Recipient email address
            subject: Email subject
            message_text: Email content
            message_type: Type of message ('plain' or 'html')
            **kwargs: Additional parameters

        Returns:
            Message object ready for Gmail API
        """
        if message_type == "html":
            message = MIMEMultipart()
            message.attach(MIMEText(message_text, 'html'))
        else:
            message = MIMEText(message_text)

        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        # Add CC and BCC if provided
        if 'cc' in kwargs and kwargs['cc']:
            message['cc'] = ', '.join(kwargs['cc']) if isinstance(kwargs['cc'], list) else kwargs['cc']

        if 'bcc' in kwargs and kwargs['bcc']:
            message['bcc'] = ', '.join(kwargs['bcc']) if isinstance(kwargs['bcc'], list) else kwargs['bcc']

        # Encode the message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        return {'raw': raw_message}