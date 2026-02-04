import asyncio
import time
import requests
import os
from typing import Dict, Any, Optional

from .base_handler import BaseResponseHandler, CommunicationChannel, ResponseStatus


class WhatsAppResponseHandler(BaseResponseHandler):
    """
    Response handler for sending WhatsApp messages via WhatsApp Business API
    """
    def __init__(self, access_token: Optional[str] = None, phone_number_id: Optional[str] = None):
        super().__init__(CommunicationChannel.WHATSAPP)
        self.access_token = access_token or os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = phone_number_id or os.getenv('WHATSAPP_PHONE_NUMBER_ID')

        if not self.access_token or not self.phone_number_id:
            raise ValueError(
                "WhatsApp credentials not found. Please set WHATSAPP_ACCESS_TOKEN and WHATSAPP_PHONE_NUMBER_ID."
            )

        self.base_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}"
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def validate_recipient(self, recipient_identifier: str) -> bool:
        """
        Validate that the recipient identifier is a valid WhatsApp number
        Expected format: international format without '+' (e.g., '1234567890')

        Args:
            recipient_identifier: WhatsApp number to validate

        Returns:
            True if valid, False otherwise
        """
        import re
        # Basic validation: digits only, 10-15 digits
        pattern = r'^\d{10,15}$'
        return re.match(pattern, recipient_identifier) is not None

    def format_response(self, content: str, response_format: Optional[str] = None) -> str:
        """
        Format the response content appropriately for WhatsApp messages

        Args:
            content: Raw content to format
            response_format: Format type (ignored for WhatsApp)

        Returns:
            Formatted content string
        """
        # WhatsApp messages are plain text with limited formatting
        # Max length is 4096 characters
        formatted = content.strip()
        if len(formatted) > 4000:  # Leave room for potential prefixes
            self.logger.warning("WhatsApp message content truncated to fit character limit")
            formatted = formatted[:4000] + "... [truncated]"

        return formatted

    async def send_response(self, recipient_identifier: str, content: str, **kwargs) -> Dict[str, Any]:
        """
        Send a WhatsApp message response to the specified recipient

        Args:
            recipient_identifier: WhatsApp number of the recipient (international format without '+')
            content: Content of the response message
            **kwargs: Additional parameters

        Returns:
            Dictionary containing response details and status
        """
        try:
            # Validate recipient
            if not self.validate_recipient(recipient_identifier):
                return await self.handle_error(
                    ValueError(f"Invalid WhatsApp number: {recipient_identifier}. Expected international format without '+'."),
                    recipient_identifier,
                    content
                )

            # Format the content
            formatted_content = self.format_response(content)

            # Send the message
            response = await self._send_whatsapp_message(recipient_identifier, formatted_content)

            if response and response.get('success'):
                # Log success
                self.log_response_attempt(recipient_identifier, content, ResponseStatus.SENT)

                return {
                    "status": ResponseStatus.SENT.value,
                    "recipient": recipient_identifier,
                    "timestamp": time.time(),
                    "provider_message_id": response.get('message_id', f"wa_msg_{int(time.time())}")
                }
            else:
                error_msg = response.get('error', 'Unknown error') if response else 'Failed to send message'
                return await self.handle_error(
                    Exception(f"WhatsApp API error: {error_msg}"),
                    recipient_identifier,
                    content
                )

        except Exception as error:
            return await self.handle_error(error, recipient_identifier, content)

    async def _send_whatsapp_message(self, recipient_number: str, content: str) -> Dict[str, Any]:
        """
        Actually send the WhatsApp message via the WhatsApp Business API

        Args:
            recipient_number: WhatsApp number in international format (without '+')
            content: Content to send

        Returns:
            Dictionary with response from the API
        """
        try:
            # Prepare the message payload
            payload = {
                "messaging_product": "whatsapp",
                "to": recipient_number,
                "type": "text",
                "text": {
                    "body": content
                }
            }

            # Make the API request
            response = requests.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=payload
            )

            if response.status_code == 200:
                response_data = response.json()
                message_id = response_data.get('messages', [{}])[0].get('id', None)
                return {
                    "success": True,
                    "message_id": message_id
                }
            else:
                # Try to get error details from response
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', f"HTTP {response.status_code}")
                except:
                    error_msg = f"HTTP {response.status_code}: {response.text[:200]}..."

                return {
                    "success": False,
                    "error": error_msg
                }

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error sending WhatsApp message: {e}")
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            self.logger.error(f"Unexpected error sending WhatsApp message: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def send_template_message(self, recipient_number: str, template_name: str, language: str = "en_US", components: list = None) -> Dict[str, Any]:
        """
        Send a WhatsApp template message (for predefined message types)

        Args:
            recipient_number: WhatsApp number in international format (without '+')
            template_name: Name of the template to use
            language: Language code for the template
            components: List of components to populate the template

        Returns:
            Dictionary with response from the API
        """
        try:
            payload = {
                "messaging_product": "whatsapp",
                "to": recipient_number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": language
                    }
                }
            }

            if components:
                payload["template"]["components"] = components

            response = requests.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=payload
            )

            if response.status_code == 200:
                response_data = response.json()
                message_id = response_data.get('messages', [{}])[0].get('id', None)
                return {
                    "success": True,
                    "message_id": message_id
                }
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', f"HTTP {response.status_code}")
                return {
                    "success": False,
                    "error": error_msg
                }

        except Exception as e:
            self.logger.error(f"Error sending WhatsApp template message: {e}")
            return {
                "success": False,
                "error": str(e)
            }