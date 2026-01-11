from email.mime.image import MIMEImage
from typing import Optional
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject: str, body: str, to_email: Optional[str] = None, image_path: Optional[str] = None):
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
    
    # Attach Image if provided
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as f:
                img_data = f.read()
                image = MIMEImage(img_data, name=os.path.basename(image_path))
                image.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
                msg.attach(image)
        except Exception as e:
            print(f"Warning: Could not attach image {image_path}: {e}")

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
