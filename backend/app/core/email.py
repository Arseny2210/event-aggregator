"""Email delivery abstraction.

EmailBackend ABC — swap SMTP for SendGrid, SES, or Mailgun without
changing notification channel code.
"""

from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib


class EmailBackend(ABC):
    """Abstract interface for email delivery."""

    @abstractmethod
    async def send_email(self, to: str, subject: str, html_body: str) -> None: ...


class SMTPEmailBackend(EmailBackend):
    """Sends email via SMTP using aiosmtplib."""

    def __init__(
        self,
        host: str,
        port: int,
        username: str | None = None,
        password: str | None = None,
        use_tls: bool = True,
        from_address: str = "noreply@example.com",
    ) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._use_tls = use_tls
        self._from_address = from_address

    async def send_email(self, to: str, subject: str, html_body: str) -> None:
        message = MIMEMultipart("alternative")
        message["From"] = self._from_address
        message["To"] = to
        message["Subject"] = subject
        message.attach(MIMEText(html_body, "html", "utf-8"))

        await aiosmtplib.send(
            message,
            hostname=self._host,
            port=self._port,
            username=self._username,
            password=self._password,
            start_tls=self._use_tls,
        )
