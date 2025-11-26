from aiosmtplib import send
from email.message import EmailMessage
from app.core.config import settings
from celery import Celery
import asyncio

celery = Celery(
        "worker",
        backend=settings.REDIS_URL,
        broker=settings.REDIS_URL
    )


@celery.task()
def email_send(to_email: str, subject: str, text: str):
    """this function sends an email"""
    msg = EmailMessage()
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.add_alternative(text, subtype="html")
    try:
        asyncio.run( send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True
        ))
        return {"status": "Email was sent successfully"}
    except Exception as e:
        return {"status": "Failed to send email", "error": str(e)}



