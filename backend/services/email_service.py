"""
Direct Gmail API email service for Agent 24 v2.

The FastAPI backend sends email directly through the Gmail API
using OAuth 2.0 credentials.

Sender:
    agent24.notification@gmail.com

Required environment variables:

    GMAIL_SENDER_EMAIL

    GMAIL_CREDENTIALS_JSON
        Optional when credentials.json exists locally.
        For deployment, store the OAuth client JSON as an environment variable.

    GMAIL_TOKEN_JSON
        OAuth token JSON created after the first authorization.

For local development:
    - credentials.json can be placed in the backend directory.
    - On first run, the browser OAuth flow will create token.json.
    - token.json can then be converted to GMAIL_TOKEN_JSON for deployment.

If Gmail is not configured, emails are logged to the console instead
of raising, so the collaboration-request flow can still be exercised.
"""

import os
import json
import base64
from email.message import EmailMessage
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Only request permission to send email.
# This is narrower than full Gmail access.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

GMAIL_SENDER_EMAIL = os.getenv(
    "GMAIL_SENDER_EMAIL",
    "agent24.notification@gmail.com",
)

GMAIL_CREDENTIALS_JSON = os.getenv("GMAIL_CREDENTIALS_JSON")
GMAIL_TOKEN_JSON = os.getenv("GMAIL_TOKEN_JSON")

AUTHORITY_EMAIL = os.getenv("AUTHORITY_EMAIL")

# Local development files.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")


def _load_credentials() -> Optional[Credentials]:
    """
    Load Gmail OAuth credentials.

    Priority:
    1. GMAIL_TOKEN_JSON environment variable
    2. Local token.json
    3. Interactive OAuth flow using credentials.json
       (local development only)
    """

    creds = None

    # ---------------------------------------------------------
    # 1. Deployment: token supplied through environment variable
    # ---------------------------------------------------------
    if GMAIL_TOKEN_JSON:
        try:
            token_data = json.loads(GMAIL_TOKEN_JSON)

            creds = Credentials.from_authorized_user_info(
                token_data,
                SCOPES,
            )
        except Exception as exc:
            print(
                f"[email_service] Failed to load GMAIL_TOKEN_JSON: {exc}"
            )
            return None

    # ---------------------------------------------------------
    # 2. Local development: token.json
    # ---------------------------------------------------------
    elif os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(
                TOKEN_FILE,
                SCOPES,
            )
        except Exception as exc:
            print(
                f"[email_service] Failed to load token.json: {exc}"
            )
            return None

    # ---------------------------------------------------------
    # Refresh an expired access token
    # ---------------------------------------------------------
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())

            # Save refreshed credentials locally.
            if not GMAIL_TOKEN_JSON:
                with open(TOKEN_FILE, "w", encoding="utf-8") as token:
                    token.write(creds.to_json())

        except Exception as exc:
            print(
                f"[email_service] Failed to refresh Gmail credentials: {exc}"
            )
            return None

    # ---------------------------------------------------------
    # 3. First-time local OAuth authorization
    # ---------------------------------------------------------
    if not creds or not creds.valid:

        if GMAIL_CREDENTIALS_JSON:
            try:
                credentials_data = json.loads(GMAIL_CREDENTIALS_JSON)

                flow = InstalledAppFlow.from_client_config(
                    credentials_data,
                    SCOPES,
                )

            except Exception as exc:
                print(
                    "[email_service] Failed to load "
                    f"GMAIL_CREDENTIALS_JSON: {exc}"
                )
                return None

        elif os.path.exists(CREDENTIALS_FILE):
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE,
                    SCOPES,
                )

            except Exception as exc:
                print(
                    f"[email_service] Failed to load credentials.json: {exc}"
                )
                return None

        else:
            print(
                "[email_service] Gmail OAuth credentials are not configured. "
                "Expected credentials.json or GMAIL_CREDENTIALS_JSON."
            )
            return None

        try:
            print(
                "[email_service] Opening browser for Gmail authorization..."
            )

            creds = flow.run_local_server(
                port=0,
                access_type="offline",
                prompt="consent",
            )

            # Save locally for future runs.
            with open(TOKEN_FILE, "w", encoding="utf-8") as token:
                token.write(creds.to_json())

            print(
                "[email_service] Gmail authorization completed. "
                "token.json created."
            )

        except Exception as exc:
            print(
                f"[email_service] Gmail OAuth authorization failed: {exc}"
            )
            return None

    return creds


def _get_gmail_service():
    """
    Build an authenticated Gmail API service.
    """

    creds = _load_credentials()

    if not creds:
        return None

    try:
        return build(
            "gmail",
            "v1",
            credentials=creds,
        )

    except Exception as exc:
        print(
            f"[email_service] Failed to build Gmail service: {exc}"
        )
        return None


def send_email(
    to_email: str,
    subject: str,
    html_body: str,
    text_body: Optional[str] = None,
) -> dict:
    """
    Send an email through the Gmail API.

    Returns:
        {
            "sent": bool,
            "error": str | None
        }

    Never raises on email configuration or delivery failures.
    The collaboration-request workflow should still complete even
    if email delivery is temporarily unavailable.
    """

    if not to_email:
        return {
            "sent": False,
            "error": "No recipient email address.",
        }

    try:
        service = _get_gmail_service()

        if not service:
            return {
                "sent": False,
                "error": "Could not authenticate with Gmail API.",
            }

        message = EmailMessage()

        message["To"] = to_email
        message["From"] = GMAIL_SENDER_EMAIL
        message["Subject"] = subject

        message.set_content(
            text_body
            or "Please view this email in an HTML-capable client."
        )

        message.add_alternative(
            html_body,
            subtype="html",
        )

        encoded_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        create_message = {
            "raw": encoded_message
        }

        service.users().messages().send(
            userId="me",
            body=create_message,
        ).execute()

        print(
            f"[email_service] Gmail email sent successfully "
            f"to {to_email}"
        )

        return {
            "sent": True,
            "error": None,
        }

    except Exception as exc:
        print(
            f"[email_service] Failed to send Gmail email "
            f"to {to_email}: {exc}"
        )

        return {
            "sent": False,
            "error": str(exc),
        }


def build_collaboration_request_email(
    *,
    requester_name: str,
    target_name: str,
    topic: str,
    proposal: str,
    reason: str,
    matching_score,
    matching_expertise,
    relevant_publications,
    relevant_projects,
    relevant_research_work,
    funding_label,
    mou_label,
    university_benefit,
    accept_url: str,
    reject_url: str,
) -> tuple[str, str]:
    """Returns (subject, html_body) for the faculty accept/reject email."""

    subject = f"Research Collaboration Request — {topic}"

    def _list_html(items):
        if not items:
            return "<p style='color:#667085;margin:4px 0;'>None on file.</p>"

        return "<ul style='margin:4px 0;padding-left:18px;'>" + "".join(
            f"<li>{item}</li>" for item in items
        ) + "</ul>"

    html_body = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1a2b4c;">
      <h2 style="color:#1a2b4c;">Agent 24 — Research Collaboration</h2>
      <p><strong>{requester_name}</strong> would like to collaborate with <strong>{target_name}</strong>.</p>
      <h3>Topic</h3>
      <p>{topic}</p>
      <h3>Proposal</h3>
      <p>{proposal or "Not provided."}</p>
      <h3>Reason for collaboration</h3>
      <p>{reason or "Not provided."}</p>
      <h3>Matching score</h3>
      <p>{matching_score if matching_score is not None else "N/A"}%</p>
      <h3>Matching expertise</h3>
      {_list_html(matching_expertise)}
      <h3>Relevant publications</h3>
      {_list_html(relevant_publications)}
      <h3>Relevant projects</h3>
      {_list_html(relevant_projects)}
      <h3>Relevant uploaded research</h3>
      {_list_html(relevant_research_work)}
      <h3>Funding opportunity</h3>
      <p>{funding_label or "No relevant funding opportunity found."}</p>
      <h3>MoU</h3>
      <p>{mou_label or "No active/relevant MoU found."}</p>
      <h3>Expected university benefit</h3>
      <p>{university_benefit or "Not provided."}</p>
      <div style="margin-top:28px;">
        <a href="{accept_url}" style="background:#2f6feb;color:#fff;padding:12px 24px;
           border-radius:8px;text-decoration:none;font-weight:bold;margin-right:12px;">
           Accept Collaboration
        </a>
        <a href="{reject_url}" style="background:#e5484d;color:#fff;padding:12px 24px;
           border-radius:8px;text-decoration:none;font-weight:bold;">
           Reject Collaboration
        </a>
      </div>
      <p style="margin-top:24px;color:#667085;font-size:12px;">
        This link is unique to you and will expire. If you did not expect this
        email, you can safely ignore it.
      </p>
    </div>
    """

    return subject, html_body


def build_authority_review_email(
    *,
    requester_name: str,
    target_name: str,
    requester_department: str,
    target_department: str,
    topic: str,
    proposal: str,
    reason: str,
    matching_score,
    matching_expertise,
    relevant_publications,
    relevant_projects,
    relevant_research_work,
    funding_label,
    mou_label,
    university_benefit,
    approve_url: str,
    reject_url: str,
) -> tuple[str, str]:
    """Returns (subject, html_body) for the authority approve/reject email."""

    subject = f"Authority Review — Research Collaboration — {topic}"

    def _list_html(items):
        if not items:
            return "<p style='color:#667085;margin:4px 0;'>None on file.</p>"

        return "<ul style='margin:4px 0;padding-left:18px;'>" + "".join(
            f"<li>{item}</li>" for item in items
        ) + "</ul>"

    html_body = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1a2b4c;">
      <h2 style="color:#1a2b4c;">Agent 24 — Authority Review</h2>
      <p>
        <strong>{requester_name}</strong> ({requester_department}) and
        <strong>{target_name}</strong> ({target_department}) have agreed to
        collaborate and the request now needs authority approval.
      </p>
      <h3>Topic</h3>
      <p>{topic}</p>
      <h3>Proposal</h3>
      <p>{proposal or "Not provided."}</p>
      <h3>Reason for collaboration</h3>
      <p>{reason or "Not provided."}</p>
      <h3>Matching score</h3>
      <p>{matching_score if matching_score is not None else "N/A"}%</p>
      <h3>Matching expertise</h3>
      {_list_html(matching_expertise)}
      <h3>Relevant publications</h3>
      {_list_html(relevant_publications)}
      <h3>Relevant projects</h3>
      {_list_html(relevant_projects)}
      <h3>Relevant uploaded research</h3>
      {_list_html(relevant_research_work)}
      <h3>Funding opportunity</h3>
      <p>{funding_label or "No relevant funding opportunity found."}</p>
      <h3>MoU</h3>
      <p>{mou_label or "No active/relevant MoU found."}</p>
      <h3>Expected university benefit</h3>
      <p>{university_benefit or "Not provided."}</p>
      <div style="margin-top:28px;">
        <a href="{approve_url}" style="background:#2f6feb;color:#fff;padding:12px 24px;
           border-radius:8px;text-decoration:none;font-weight:bold;margin-right:12px;">
           Approve Collaboration
        </a>
        <a href="{reject_url}" style="background:#e5484d;color:#fff;padding:12px 24px;
           border-radius:8px;text-decoration:none;font-weight:bold;">
           Reject Collaboration
        </a>
      </div>
      <p style="margin-top:24px;color:#667085;font-size:12px;">
        This link is unique to this review and will expire.
      </p>
    </div>
    """

    return subject, html_body