from dataclasses import dataclass
from pathlib import Path
from typing import Any
import emails
from jinja2 import Template
from mjml import mjml_to_html
from app.core.config import settings


@dataclass
class EmailData:
    content: str
    subject: str


def _render_email_template(template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent.parent / "email-templates" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    dm = mjml_to_html(html_content)
    if dm.errors:
        raise Exception(f"mjml_to_html errors: {dm.errors}")
    return dm.html


def send_email(email_to: str, subject: str, html_content: str) -> None:
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.PROJECT_NAME, settings.EMAILS_FROM_EMAIL),
    )

    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD

    response = message.send(to=email_to, smtp=smtp_options)
    if response.status_code != 250:
        raise Exception(f"fail to send email: {response}")


def generate_new_account_email(email_to: str, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {email_to}"
    link = f"{settings.server_host}/verify-email?token={token}"

    html_content = _render_email_template(
        template_name="new_account.mjml",
        context={
            "project_name": project_name,
            "email": email_to,
            "link": link,
        },
    )
    return EmailData(content=html_content, subject=subject)


def generate_reset_password_email(email_to: str, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email_to}"
    link = f"{settings.server_host}/reset-password?token={token}"

    html_content = _render_email_template(
        template_name="reset_password.mjml",
        context={
            "project_name": project_name,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return EmailData(content=html_content, subject=subject)
