"""
gmail_sender.py
Sends cover letter emails via Gmail API using OAuth2.
First run opens a browser for authentication. Credentials are cached locally.
"""

import os
import base64
import pickle
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import date

# Google API imports — install if missing
try:
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install",
        "google-auth-httplib2", "google-auth-oauthlib", "google-api-python-client", "-q"])
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

SCOPES            = ["https://www.googleapis.com/auth/gmail.send"]
CREDENTIALS_FILE  = Path(__file__).parent / "credentials.json"   # downloaded from Google Cloud Console
TOKEN_FILE        = Path(__file__).parent / "token.pickle"
SENDER_EMAIL      = "laurie@lambot.co"


def get_gmail_service():
    """Authenticate and return a Gmail API service object."""
    creds = None

    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    "credentials.json not found.\n"
                    "Download it from: https://console.cloud.google.com/\n"
                    "APIs & Services > Credentials > OAuth 2.0 Client IDs > Download JSON\n"
                    f"Save as: {CREDENTIALS_FILE}"
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build("gmail", "v1", credentials=creds)


def build_email(
    to_email: str,
    to_name: str,
    company: str,
    job_title: str,
    cover_letter_text: str,
    pdf_path: Path = None,
    cv_path: Path = None,
) -> MIMEMultipart:
    """Build a MIME email with the cover letter and optional PDF attachments."""

    subject = f"Application — {job_title} at {company}"
    today   = date.today().strftime("%B %d, %Y")

    # Plain text body — the cover letter itself, formatted for email
    body = cover_letter_text.strip()

    # Add footer
    body += f"""

--
Laurie Lambot, PhD | EMT
laurie@lambot.co | lambot.co
(847) 246-2086
"""

    msg = MIMEMultipart()
    msg["From"]    = f"Laurie Lambot <{SENDER_EMAIL}>"
    msg["To"]      = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # Attach PDF cover letter
    if pdf_path and Path(pdf_path).exists():
        with open(pdf_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="CoverLetter_Lambot_{company}.pdf"')
        msg.attach(part)

    # Attach CV if provided
    if cv_path and Path(cv_path).exists():
        with open(cv_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="CV_Lambot.pdf"')
        msg.attach(part)

    return msg


def send_email(
    to_email: str,
    to_name: str,
    company: str,
    job_title: str,
    cover_letter_text: str,
    pdf_path: Path = None,
    cv_path: Path = None,
    dry_run: bool = False,
) -> dict:
    """
    Send the application email.
    dry_run=True prints the email without sending (safe for testing).
    """
    msg = build_email(to_email, to_name, company, job_title,
                      cover_letter_text, pdf_path, cv_path)

    if dry_run:
        print("=== DRY RUN — Email not sent ===")
        print(f"To: {to_email}")
        print(f"Subject: {msg['Subject']}")
        print("--- Body ---")
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                print(part.get_payload(decode=True).decode())
        print("=== END DRY RUN ===")
        return {"status": "dry_run", "to": to_email, "subject": msg["Subject"]}

    service = get_gmail_service()
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    sent = service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print(f"  Email sent to {to_email} (Message ID: {sent['id']})")
    return {"status": "sent", "message_id": sent["id"], "to": to_email}


def send_spontaneous(
    company: str,
    hiring_contact: str,
    contact_email: str,
    cover_letter_text: str,
    pdf_path: Path = None,
    cv_path: Path = None,
    dry_run: bool = False,
) -> dict:
    """Send a spontaneous application to a company with no open posting."""
    return send_email(
        to_email=contact_email,
        to_name=hiring_contact,
        company=company,
        job_title="Spontaneous Application — Research Scientist",
        cover_letter_text=cover_letter_text,
        pdf_path=pdf_path,
        cv_path=cv_path,
        dry_run=dry_run,
    )


if __name__ == "__main__":
    # Dry run test
    sample = """
Dear Dr. Tremblay,

With a PhD in Neuroscience and 15 years of research experience, I am writing with genuine enthusiasm for the Senior Research Scientist role at Aifred Health.

Warm regards,

Laurie Lambot, PhD
"""
    result = send_email(
        to_email="test@example.com",
        to_name="Dr. Tremblay",
        company="Aifred Health",
        job_title="Senior Research Scientist",
        cover_letter_text=sample,
        dry_run=True
    )
    print(result)
