import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

# ====== CONFIGURE THESE ======
AWS_REGION = "ap-south-1"  # Mumbai region
SENDER = "dataengineer@vepolink.com"  # Verified SES sender
TO = [
    "guptavinod118@gmail.com",
    "guptavinodqwerty@gmail.com",
    "jaydevkrsah@gmail.com"
]  # ✅ Three recipients
CC = []  # No CC
SUBJECT = "Confirmation – Daily Report Delivery Restored for MONGIA POWER PVT. LTD"
ATTACH_PATH = r"C:\Users\Vepol\OneDrive\Desktop\vinod\test\report.pdf"  # Update file path
LOG_FILE = r"C:\Logs\email_audit.log"

BODY_TEXT = """\
Dear Team,

This is to inform you that the earlier issue with the delivery of the daily report for MONGIA POWER PVT. LTD has been resolved.
The system is now functioning correctly, and the daily reports are being sent automatically through the Vepolink Portal.

This is the same automated daily report that is now being successfully delivered to you.

Kindly confirm that you are receiving the report and the attachment as expected.

Regards,
Vinod Gupta
"""

# ====== Ensure log directory ======
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_entry(status, message_id="", error=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    attach_size = os.path.getsize(ATTACH_PATH) if os.path.isfile(ATTACH_PATH) else 0
    line = (
        f"{timestamp} | STATUS={status} | MSG_ID={message_id} | "
        f"SENDER={SENDER} | TO={','.join(TO)} | CC={','.join(CC)} | "
        f"SUBJECT={SUBJECT} | ATTACH={ATTACH_PATH} ({attach_size} bytes) | ERROR={error}\n"
    )
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

def send_via_ses():
    client = boto3.client("ses", region_name=AWS_REGION)

    # Read attachment
    if not os.path.isfile(ATTACH_PATH):
        log_entry("FAILED", error=f"Attachment not found: {ATTACH_PATH}")
        raise FileNotFoundError(f"Attachment not found: {ATTACH_PATH}")
    with open(ATTACH_PATH, "rb") as f:
        data = f.read()

    # Build raw MIME message
    import mimetypes
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    msg = MIMEMultipart()
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = ", ".join(TO)

    msg.attach(MIMEText(BODY_TEXT, "plain"))

    filename = os.path.basename(ATTACH_PATH)
    mime_type, _ = mimetypes.guess_type(ATTACH_PATH)
    if mime_type:
        maintype, subtype = mime_type.split("/")
    else:
        maintype, subtype = ("application", "octet-stream")

    part = MIMEBase(maintype, subtype)
    part.set_payload(data)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
    msg.attach(part)

    try:
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=TO,
            RawMessage={"Data": msg.as_string()}
        )
        message_id = response.get("MessageId", "")
        log_entry("SENT", message_id=message_id)
        print(f"Email sent, SES Message ID: {message_id}")
    except ClientError as e:
        log_entry("FAILED", error=str(e))
        print(f"Send failed: {e}")

if __name__ == "__main__":
    send_via_ses()
name = "vinod gupta"