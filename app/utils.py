import logging
import random
import shutil
import string
from dataclasses import dataclass
from os import path, makedirs
from pathlib import Path
from typing import Any

import emails
from fastapi import UploadFile
from jinja2 import Template

from app.api_models import UploadFileResponse
from app.core.config import settings


def upload_picture(image: UploadFile) -> UploadFileResponse:
    letter = string.ascii_letters
    rand_str = "".join(random.choice(letter) for _ in range(6))
    append_str = f"_{rand_str}."
    image_name = append_str.join(image.filename.rsplit('.', 1))
    home_dir = Path.home()
    upload_dir = path.join(home_dir, "Meetup", "Pictures")
    if not path.isdir(upload_dir):
        makedirs(upload_dir)
    upload_path = path.join(upload_dir, image_name)
    with open(upload_path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return UploadFileResponse(filename=image_name, type=image.content_type, url=upload_path)


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
            Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


def send_email(
        *,
        email_to: str,
        subject: str = "",
        html_content: str = "",
) -> None:
    assert settings.emails_enabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
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
    logging.info(f"send email result: {response}")


def generate_test_email(email_to: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"project_name": settings.PROJECT_NAME, "email": email_to},
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_reset_password_email(email_to: str, name: str, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {name}"
    link = f"{settings.server_host}/auth/reset-password?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": name,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def send_password_reset_email(email_to: str, name: str, token: str):
    email_data = generate_reset_password_email(email_to=email_to, name=name, token=token)
    send_email(email_to=email_to, subject=email_data.subject,
               html_content=email_data.html_content)
