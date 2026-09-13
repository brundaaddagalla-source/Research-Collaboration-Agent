"""
Direct SMTP email service for Agent 24 v2.

No n8n, no external workflow automation - the FastAPI backend sends
email itself, using Python's built-in smtplib. Configured entirely
through environment variables (see .env.example):

    SMTP_HOST
    SMTP_PORT
    SMTP_USERNAME
    SMTP_PASSWORD       (use a Gmail "app password" if using Gmail SMTP)
    SMTP_FROM_EMAIL
    AUTHORITY_EMAIL

If SMTP is not configured (e.g. local dev without credentials), emails
are logged to the console instead of raising - so the rest of the
collaboration-request flow can still be exercised and tested without
a real mailbox. This is surfaced back to the caller via the returned
dict's `sent` flag so routes can decide whether to warn the user.
"""

import os
import smtplib
import ssl
from email.message import EmailMessage
from typing import Optional

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USERNAME)

AUTHORITY_EMAIL = os.getenv("AUTHORITY_EMAIL")


def _is_configured() -> bool:
    return bool(SMTP_HOST and SMTP_USERNAME and SMTP_PASSWORD and SMTP_FROM_EMAIL)


def send_email(to_email: str, subject: str, html_body: str, text_body: Optional[str] = None) -> dict:
    """
    Send an email directly via SMTP. Returns {"sent": bool, "error": str|None}.

    Never raises on a missing SMTP configuration or a delivery failure -
    the collaboration-request workflow (request/accept/reject/approve)
    must still complete and be reflected in the database even if email
    delivery is unavailable in a given environment; the caller decides
    whether/how to surface that to the user.
    """
    if not to_email:
        return {"sent": False, "error": "No recipient email address."}

    if not _is_configured():
        print(
            "[email_service] SMTP is not configured (SMTP_HOST/SMTP_USERNAME/"
            "SMTP_PASSWORD/SMTP_FROM_EMAIL) - logging email instead of sending.\n"
            f"To: {to_email}\nSubject: {subject}\n{'-' * 40}\n{text_body or html_body}\n{'-' * 40}"
        )
        return {"sent": False, "error": "SMTP is not configured."}

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = SMTP_FROM_EMAIL
    message["To"] = to_email
    message.set_content(text_body or "Please view this email in an HTML-capable client.")
    message.add_alternative(html_body, subtype="html")

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.starttls(context=context)
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)
        return {"sent": True, "error": None}
    except Exception as exc:  # noqa: BLE001 - surface any SMTP failure, never crash the request flow
        print(f"[email_service] Failed to send email to {to_email}: {exc}")
        return {"sent": False, "error": str(exc)}


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