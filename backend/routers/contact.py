"""Contact form router."""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from models.contact import Contact
from schemas.schemas import ContactCreate, ContactResponse
from utils.auth import get_current_admin
from fastapi import Depends
import smtplib
import os
from email.mime.text import MIMEText

router = APIRouter()


async def send_notification_email(contact: Contact):
    """Send email notification when contact form is submitted."""
    smtp_host = os.getenv("SMTP_HOST")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    notify_email = os.getenv("NOTIFY_EMAIL")

    if not all([smtp_host, smtp_user, smtp_pass, notify_email]):
        return  # Skip if not configured

    try:
        body = f"""
New message from: {contact.name} ({contact.email})
Subject: {contact.subject}

{contact.message}
        """
        msg = MIMEText(body)
        msg["Subject"] = f"[Portfolio] New message from {contact.name}"
        msg["From"] = smtp_user
        msg["To"] = notify_email

        with smtplib.SMTP_SSL(smtp_host, 465) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
    except Exception as e:
        print(f"Email notification failed: {e}")


@router.post("/", response_model=ContactResponse)
async def submit_contact(payload: ContactCreate, background_tasks: BackgroundTasks):
    """Submit contact form."""
    contact = Contact(
        name=payload.name,
        email=payload.email,
        subject=payload.subject,
        message=payload.message
    )
    await contact.insert()

    # Send email in background
    background_tasks.add_task(send_notification_email, contact)

    return ContactResponse(
        success=True,
        message="Message received! I'll get back to you soon 💌"
    )


@router.get("/", dependencies=[Depends(get_current_admin)])
async def get_messages(limit: int = 20, unread_only: bool = False):
    """Get all contact messages (admin only)."""
    query = {}
    if unread_only:
        query["read"] = False
    messages = await Contact.find(query).sort("-created_at").limit(limit).to_list()
    return [{"id": str(m.id), **m.model_dump(exclude={"id"})} for m in messages]


@router.patch("/{message_id}/read", dependencies=[Depends(get_current_admin)])
async def mark_read(message_id: str):
    """Mark message as read."""
    from beanie import PydanticObjectId
    contact = await Contact.get(PydanticObjectId(message_id))
    if not contact:
        raise HTTPException(404, "Message not found")
    contact.read = True
    await contact.save()
    return {"success": True}
