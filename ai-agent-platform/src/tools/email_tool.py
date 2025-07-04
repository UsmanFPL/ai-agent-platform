from .base import BaseTool, ToolInput, ToolOutput
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, EmailStr
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailSendInput(ToolInput):
    to: List[EmailStr]
    subject: str
    body: str
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None
    html: bool = False

class EmailReadInput(ToolInput):
    folder: str = "INBOX"
    limit: int = 10
    unread_only: bool = True

class EmailTool(BaseTool):
    """Tool for email operations"""
    
    def __init__(self):
        super().__init__(
            name="email_operations",
            description="Send and read emails"
        )
        
        # SMTP Configuration
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        
        # IMAP Configuration
        self.imap_server = os.getenv("IMAP_SERVER", "imap.gmail.com")
        self.imap_port = int(os.getenv("IMAP_PORT", "993"))
        self.imap_username = os.getenv("IMAP_USERNAME", self.smtp_username)
        self.imap_password = os.getenv("IMAP_PASSWORD", self.smtp_password)
    
    async def execute(self, input_data: Dict[str, Any]) -> ToolOutput:
        """Execute email operation"""
        try:
            operation = input_data.get("operation")
            
            if operation == "send":
                return await self._send_email(EmailSendInput(**input_data))
            elif operation == "read":
                return await self._read_emails(EmailReadInput(**input_data))
            else:
                return ToolOutput(success=False, error="Invalid operation. Use 'send' or 'read'")
                
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
    
    async def _send_email(self, input_data: EmailSendInput) -> ToolOutput:
        """Send an email"""
        if not self.smtp_username or not self.smtp_password:
            return ToolOutput(success=False, error="SMTP credentials not configured")
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_username
            msg['To'] = ', '.join(input_data.to)
            msg['Subject'] = input_data.subject
            
            if input_data.cc:
                msg['Cc'] = ', '.join(input_data.cc)
            
            # Add body
            if input_data.html:
                body_part = MIMEText(input_data.body, 'html')
            else:
                body_part = MIMEText(input_data.body, 'plain')
            
            msg.attach(body_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                
                recipients = input_data.to[:]
                if input_data.cc:
                    recipients.extend(input_data.cc)
                if input_data.bcc:
                    recipients.extend(input_data.bcc)
                
                server.send_message(msg, to_addrs=recipients)
            
            return ToolOutput(
                success=True,
                data={
                    "message": "Email sent successfully",
                    "recipients": len(recipients),
                    "subject": input_data.subject
                }
            )
            
        except Exception as e:
            return ToolOutput(success=False, error=f"Failed to send email: {str(e)}")
    
    async def _read_emails(self, input_data: EmailReadInput) -> ToolOutput:
        """Read emails from inbox"""
        if not self.imap_username or not self.imap_password:
            return ToolOutput(success=False, error="IMAP credentials not configured")
        
        try:
            # Connect to IMAP server
            with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as mail:
                mail.login(self.imap_username, self.imap_password)
                mail.select(input_data.folder)
                
                # Search for emails
                search_criteria = "UNSEEN" if input_data.unread_only else "ALL"
                status, messages = mail.search(None, search_criteria)
                
                if status != 'OK':
                    return ToolOutput(success=False, error="Failed to search emails")
                
                email_ids = messages[0].split()
                emails = []
                
                # Get latest emails (up to limit)
                for email_id in email_ids[-input_data.limit:]:
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    
                    if status == 'OK':
                        email_message = email.message_from_bytes(msg_data[0][1])
                        
                        # Extract email data
                        email_data = {
                            "id": email_id.decode(),
                            "subject": email_message.get("Subject", ""),
                            "from": email_message.get("From", ""),
                            "to": email_message.get("To", ""),
                            "date": email_message.get("Date", ""),
                            "body": self._extract_body(email_message)
                        }
                        
                        emails.append(email_data)
                
                return ToolOutput(
                    success=True,
                    data={
                        "emails": emails,
                        "count": len(emails),
                        "folder": input_data.folder
                    }
                )
                
        except Exception as e:
            return ToolOutput(success=False, error=f"Failed to read emails: {str(e)}")
    
    def _extract_body(self, email_message) -> str:
        """Extract email body text"""
        body = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()
        
        return body
    
    def get_schema(self) -> Dict[str, Any]:
        """Get tool schema"""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["send", "read"],
                    "description": "Email operation to perform"
                },
                "to": {
                    "type": "array",
                    "items": {"type": "string", "format": "email"},
                    "description": "Recipient email addresses (for send)"
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject (for send)"
                },
                "body": {
                    "type": "string",
                    "description": "Email body content (for send)"
                },
                "cc": {
                    "type": "array",
                    "items": {"type": "string", "format": "email"},
                    "description": "CC recipients (for send)"
                },
                "bcc": {
                    "type": "array",
                    "items": {"type": "string", "format": "email"},
                    "description": "BCC recipients (for send)"
                },
                "html": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether body is HTML (for send)"
                },
                "folder": {
                    "type": "string",
                    "default": "INBOX",
                    "description": "Email folder to read from (for read)"
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "description": "Maximum number of emails to read"
                },
                "unread_only": {
                    "type": "boolean",
                    "default": True,
                    "description": "Only read unread emails (for read)"
                }
            },
            "required": ["operation"]
        }