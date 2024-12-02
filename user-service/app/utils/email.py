from aiosmtplib import send
from email.mime.text import MIMEText
from app.config import settings

async def send_email(to: str, subject: str, body: str):
    """
    Send an email using an SMTP server.
    Args:
        to (str): Recipient's email address.
        subject (str): Email subject.
        body (str): Email body content.
    """
    message = MIMEText(body)
    message["From"] = "noreply@ecommerce.com"
    message["To"] = to
    message["Subject"] = subject

    await send(
        message,
        hostname="smtp.mailtrap.io",
        port=587,
        username=settings.SMTP_USERNAME,
        password=settings.SMTP_PASSWORD,
    )
