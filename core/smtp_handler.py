"""
core/smtp_handler.py

SMTP-Integration für Fehlerbenachrichtigungen via E-Mail.

Konfiguration:
- SMTP-Server
- Port
- Benutzername
- Passwort
- Absenderadresse
- Empfängeradresse

Features:
- Versand einfacher Text-E-Mails
- SSL/TLS Unterstützung
- Fehlerhandling mit Logging
"""

import smtplib
import ssl
from email.message import EmailMessage
from typing import Optional

from core.logger import Logger

class SMTPHandler:
    """
    SMTP-Client für das Versenden von Fehlerbenachrichtigungen per E-Mail.
    """

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        sender_email: str,
        recipient_email: str,
        use_tls: bool = True,
        logger: Optional[Logger] = None,
    ):
        """
        Initialisiert den SMTP-Handler.

        Args:
            smtp_server (str): SMTP-Serveradresse.
            smtp_port (int): SMTP-Port (z.B. 465 für SSL, 587 für TLS).
            username (str): SMTP-Benutzername.
            password (str): SMTP-Passwort.
            sender_email (str): Absenderadresse.
            recipient_email (str): Empfängeradresse.
            use_tls (bool): Ob TLS verwendet wird. SSL bei Port 465 wird automatisch verwendet.
            logger (Logger, optional): Logger-Instanz zur Protokollierung.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.sender_email = sender_email
        self.recipient_email = recipient_email
        self.use_tls = use_tls
        self.logger = logger

    def send_email(self, subject: str, body: str) -> bool:
        """
        Sendet eine E-Mail mit dem angegebenen Betreff und Text.

        Args:
            subject (str): Betreff der E-Mail.
            body (str): Nachrichtentext.

        Returns:
            bool: True bei Erfolg, False bei Fehler.
        """
        msg = EmailMessage()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = subject
        msg.set_content(body)

        try:
            if self.smtp_port == 465:
                # SSL Verbindung
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                    server.login(self.username, self.password)
                    server.send_message(msg)
            else:
                # TLS Verbindung
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.ehlo()
                    if self.use_tls:
                        server.starttls(context=ssl.create_default_context())
                        server.ehlo()
                    server.login(self.username, self.password)
                    server.send_message(msg)

            if self.logger:
                self.logger.log_info(f"SMTP: E-Mail erfolgreich gesendet an {self.recipient_email}")
            return True
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"SMTP-Fehler beim Senden der E-Mail: {e}")
            return False
