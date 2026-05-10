import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def send_email(to_email, email_text):
    """
    Send the generated email via Gmail SMTP.
    The email_text must start with:
    Subject: ...
    """

    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_APP_PASSWORD")

    if not sender_email or not sender_password:
        raise ValueError(
            "SENDER_EMAIL or SENDER_APP_PASSWORD missing in .env"
        )

    # Split subject and body
    lines = email_text.strip().split("\n")
    subject_line = lines[0].strip()

    if subject_line.lower().startswith("subject:"):
        subject = subject_line[len("Subject:"):].strip()
    else:
        subject = "Payment Follow-Up"

    body = "\n".join(lines[1:]).strip()

    # Create email
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # Send via Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)