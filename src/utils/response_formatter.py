from typing import Dict, Any, Optional
from enum import Enum


class ResponseFormat(Enum):
    PLAIN = "plain"
    HTML = "html"
    MARKDOWN = "markdown"


class ResponseFormatter:
    """
    Utility for formatting responses appropriately for different communication channels
    """
    @staticmethod
    def format_for_channel(content: str, channel: str, format_type: ResponseFormat = ResponseFormat.PLAIN,
                          max_length: Optional[int] = None) -> str:
        """
        Format content appropriately for the specified channel

        Args:
            content: Raw content to format
            channel: Communication channel ('email', 'linkedin', 'whatsapp')
            format_type: Desired format type
            max_length: Maximum allowed length (optional)

        Returns:
            Formatted content string
        """
        # Apply channel-specific formatting
        if channel.lower() == 'email':
            formatted_content = ResponseFormatter._format_for_email(content, format_type)
        elif channel.lower() == 'linkedin':
            formatted_content = ResponseFormatter._format_for_linkedin(content)
        elif channel.lower() == 'whatsapp':
            formatted_content = ResponseFormatter._format_for_whatsapp(content)
        else:
            # Default formatting
            formatted_content = content.strip()

        # Apply length limits if specified
        if max_length and len(formatted_content) > max_length:
            formatted_content = formatted_content[:max_length - 3] + "..."

        return formatted_content

    @staticmethod
    def _format_for_email(content: str, format_type: ResponseFormat) -> str:
        """
        Format content specifically for email

        Args:
            content: Raw content to format
            format_type: Desired format type

        Returns:
            Formatted email content
        """
        if format_type == ResponseFormat.HTML:
            # Wrap content in basic HTML structure
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
            </head>
            <body>
                <p>{content.replace('\\n', '<br>')}</p>
            </body>
            </html>
            """
        elif format_type == ResponseFormat.MARKDOWN:
            # Convert markdown to simple text format
            import re
            # Remove markdown formatting
            content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Bold
            content = re.sub(r'\*(.*?)\*', r'\1', content)     # Italic
            content = re.sub(r'#+\s+(.*)', r'\1', content)     # Headers
            content = re.sub(r'-\s+(.*)', r'• \1', content)    # Lists
        else:
            # Plain text - just clean it up
            content = content.replace('\r\n', '\n').replace('\r', '\n')

        return content.strip()

    @staticmethod
    def _format_for_linkedin(content: str) -> str:
        """
        Format content specifically for LinkedIn messages

        Args:
            content: Raw content to format

        Returns:
            Formatted LinkedIn content
        """
        # LinkedIn supports limited formatting
        # Remove complex markdown but preserve simple formatting
        import re

        # Replace bold markers with asterisks (LinkedIn supports these)
        content = re.sub(r'\*\*(.*?)\*\*', r'*\1*', content)

        # Keep simple lists
        content = re.sub(r'-\s+(.*)', r'• \1', content)
        content = re.sub(r'\d+\.\s+(.*)', r'• \1', content)

        # Limit length to LinkedIn's message limit (around 2000 characters)
        if len(content) > 1950:  # Leave room for potential additions
            content = content[:1950] + "... [truncated]"

        return content.strip()

    @staticmethod
    def _format_for_whatsapp(content: str) -> str:
        """
        Format content specifically for WhatsApp messages

        Args:
            content: Raw content to format

        Returns:
            Formatted WhatsApp content
        """
        # WhatsApp supports limited formatting
        # Remove markdown but keep simple symbols
        import re

        # Replace bold markers with asterisks (WhatsApp supports these)
        content = re.sub(r'\*\*(.*?)\*\*', r'*\1*', content)

        # Replace italic markers with underscores (WhatsApp supports these)
        content = re.sub(r'\*(.*?)\*', r'_\1_', content)

        # Keep simple lists
        content = re.sub(r'-\s+(.*)', r'• \1', content)
        content = re.sub(r'\d+\.\s+(.*)', r'• \1', content)

        # Limit length to WhatsApp's message limit (4096 characters)
        if len(content) > 4000:  # Leave room for potential additions
            content = content[:4000] + "... [truncated]"

        return content.strip()

    @staticmethod
    def format_with_template(content: str, template: str, variables: Optional[Dict[str, str]] = None) -> str:
        """
        Format content using a template with variable substitution

        Args:
            content: Main content to insert
            template: Template string with placeholders
            variables: Dictionary of variable substitutions

        Returns:
            Formatted content with template applied
        """
        if variables is None:
            variables = {}

        # Add the main content as a special variable
        variables['content'] = content

        # Substitute variables in the template
        formatted = template
        for var_name, var_value in variables.items():
            placeholder = f"{{{var_name}}}"
            formatted = formatted.replace(placeholder, var_value or "")

        return formatted

    @staticmethod
    def sanitize_content(content: str, channel: str) -> str:
        """
        Sanitize content to remove potentially problematic elements for the specified channel

        Args:
            content: Raw content to sanitize
            channel: Communication channel

        Returns:
            Sanitized content string
        """
        # Remove any potentially harmful content
        sanitized = content

        # Remove potential script tags (for email/html)
        if channel.lower() in ['email']:
            import re
            sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
            sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)

        # Remove any leading/trailing whitespace
        sanitized = sanitized.strip()

        return sanitized

    @staticmethod
    def format_response_signature(signoff: str = "AI Employee", channel: str = "email") -> str:
        """
        Format a signature for responses

        Args:
            signoff: Signoff text
            channel: Communication channel

        Returns:
            Formatted signature string
        """
        if channel.lower() == "email":
            return f"\n\nBest regards,\n{signoff}"
        elif channel.lower() == "linkedin":
            return f"\n\nBest regards,\n{signoff}"
        elif channel.lower() == "whatsapp":
            return f"\n\n-{signoff}"
        else:
            return f"\n\n-{signoff}"