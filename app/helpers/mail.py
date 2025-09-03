import logging
import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Sequence

from pydantic import BaseModel, field_validator

from ..config import settings

logger = logging.getLogger()
context = ssl.create_default_context()


class EmailSchema(BaseModel):
    to: str | Sequence[str]
    cc: str | Sequence[str] | None = None
    bcc: str | Sequence[str] | None = None
    subject: str
    body: str

    @field_validator("to", "cc", "bcc", mode="before")
    @classmethod
    def normalize_recipients(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            return [email.strip() for email in v.split("/")]
        return list(v)


def create_mail_message(
    email: EmailSchema, attachment_paths: Sequence[Path] | None, content_type: str
) -> MIMEMultipart:
    message = MIMEMultipart()
    message["From"] = settings.mail_user
    message["To"] = ", ".join(email.to)
    message["Cc"] = ", ".join(email.cc or "")
    message["Bcc"] = ", ".join(email.bcc or "")
    message["Subject"] = email.subject
    message.attach(MIMEText(email.body, content_type, "utf-8"))

    for path in attachment_paths or []:
        try:
            with open(path, "rb") as f:
                part = MIMEApplication(f.read(), Name=path.name)
                part["Content-Disposition"] = f'attachment; filename="{path.name}"'
                message.attach(part)
        except Exception as e:
            logger.error(f"Could not attach {path}: {e}")
    return message


async def send_email(
    email: EmailSchema,
    attachment_paths: Sequence[Path] | None = None,
    content_type: str = "plain",
):
    message = create_mail_message(email, attachment_paths, content_type)
    logger.debug(f"Prepared email: {message.as_string()}")
    try:
        with smtplib.SMTP_SSL(
            host="ms-mx-vct01.tuf.p.mcld.fr", port=465, context=context
        ) as server:
            try:
                server.login(user=settings.mail_user, password=settings.mail_pass)
            except smtplib.SMTPAuthenticationError as e:
                logger.error(f"SMTP login failed: {e}")
                return
            except smtplib.SMTPException as e:
                logger.error(f"SMTP error during login: {e}")
                return

            recipients = list(email.to)
            recipients.extend(email.cc or [])
            recipients.extend(email.bcc or [])
            try:
                server.sendmail(
                    from_addr=settings.mail_user,
                    to_addrs=recipients,
                    msg=message.as_string(),
                )
            except smtplib.SMTPException as e:
                logger.error(f"Failed to send email: {e}")
                return

    except smtplib.SMTPConnectError as e:
        logger.error(f"Could not connect to SMTP server: {e}")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {e}")
