import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional

def send_email(subject: str, body: str, to_email: Optional[str] = None):
    """
    Sends an email using SMTP.
    Requires SMTP_EMAIL, SMTP_PASSWORD, and optionally RECIPIENT_EMAIL in env vars.
    """
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")
    if not to_email:
        to_email = os.getenv("RECIPIENT_EMAIL")

    if not sender_email or not sender_password or not to_email:
        print("Skipping email: Missing SMTP_EMAIL, SMTP_PASSWORD, or RECIPIENT_EMAIL variables.")
        return

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Default to Gmail SMTP
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
