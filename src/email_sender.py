import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv


class EmailSenderConfigError(Exception):
    pass


class EmailSender:
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    receiver_email: str
    sender_email: str
    smtp: smtplib.SMTP

    def __init__(self):
        load_dotenv()
        try:
            self.smtp_server = os.getenv('SMTP_SERVER')
            if self.smtp_server is None:
                raise EmailSenderConfigError("Failed to load smtp_server from .env file")
            smtp_port = os.getenv('SMTP_PORT')
            if smtp_port is None:
                raise EmailSenderConfigError("Failed to load smtp_port from .env file")
            self.smtp_port = int(smtp_port)
            self.smtp_username = os.getenv('SMTP_USERNAME')
            if self.smtp_username is None:
                raise EmailSenderConfigError("Failed to load smtp_username from .env file")
            self.smtp_password = os.getenv('SMTP_PASSWORD')
            if self.smtp_password is None:
                raise EmailSenderConfigError("Failed to load smtp_password from .env file")
            self.receiver_email = os.getenv('RECEIVER_EMAIL')
            if self.receiver_email is None:
                raise EmailSenderConfigError("Failed to load receiver_email from .env file")
            self.sender_email = os.getenv('SENDER_EMAIL')
            if self.sender_email is None:
                raise EmailSenderConfigError("Failed to load sender_email from .env file")

            self.smtp = smtplib.SMTP(host=self.smtp_server, port=self.smtp_port)
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.login(user=self.smtp_username, password=self.smtp_password)
        except Exception as e:
            raise EmailSenderConfigError(f"Failed to read config {e}")
        
    
    def send_email(self, subject: str, content: str):
        msg = MIMEText(content, 'html')
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email

        self.smtp.sendmail(from_addr=self.sender_email, to_addrs=[self.receiver_email], msg=msg.as_string())
        self.smtp.quit()