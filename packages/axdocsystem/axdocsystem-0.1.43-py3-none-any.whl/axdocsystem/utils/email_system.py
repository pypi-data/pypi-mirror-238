import aiosmtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .settings import EmailSystemSettings
from .notification_system import NotificationSystem


class EmailSystem(NotificationSystem):
    def __init__(self, settings: EmailSystemSettings) -> None:
        self.settings = settings
    
    async def send(self, receiver: str, content: str, title: str = '', parse_mode: str = 'html'):
        message = MIMEMultipart()
        message['From'] = self.settings.EMAIL_SENDER
        message['To'] = receiver
        message['Subject'] = title
            
        body = MIMEText(content, parse_mode)
        message.attach(body)

        smtp = aiosmtplib.SMTP(
            hostname=self.settings.EMAIL_HOST, 
            port=self.settings.EMAIL_PORT, 
            use_tls=True,
        )
        
        async with smtp:
            await smtp.login(self.settings.EMAIL_SENDER, self.settings.EMAIL_SENDER_PASSWD)
            return await smtp.send_message(message)

