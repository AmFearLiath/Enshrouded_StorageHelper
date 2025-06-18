# updater/core/ftp_worker.py

import ftplib
import os
import shutil
from datetime import datetime


class FTPWorker:
    def __init__(self, host: str, user: str, password: str, remote_file: str, local_file: str,
                 temp_dir: str, enable_backup: bool = True, logger=None):
        self.host = host
        self.user = user
        self.password = password
        self.remote_file = remote_file
        self.local_file = local_file
        self.temp_dir = temp_dir
        self.enable_backup = enable_backup
        self.logger = logger

        os.makedirs(self.temp_dir, exist_ok=True)

    def _log(self, message, level="info"):
        if self.logger:
            getattr(self.logger, level)(message)
        else:
            print(f"[FTP] {message}")

    def _connect(self) -> ftplib.FTP:
        self._log(f"Verbinde mit FTP-Server {self.host}...")
        ftp = ftplib.FTP(self.host)
        ftp.login(self.user, self.password)
        self._log("Verbindung hergestellt.")
        return ftp

    def download(self):
        """Lädt die Remote-Datei herunter und speichert sie temporär."""
        try:
            ftp = self._connect()
            temp_file = os.path.join(self.temp_dir, os.path.basename(self.remote_file))
            with open(temp_file, 'wb') as f:
                ftp.retrbinary(f"RETR {self.remote_file}", f.write)
            ftp.quit()
            self._log(f"Datei erfolgreich heruntergeladen: {temp_file}")

            if self.enable_backup and os.path.exists(self.local_file):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = f"{self.local_file}.bak_{timestamp}"
                shutil.copy2(self.local_file, backup_file)
                self._log(f"Backup erstellt: {backup_file}")

            shutil.copy2(temp_file, self.local_file)
            self._log("Datei lokal aktualisiert.")
        except Exception as e:
            self._log(f"Fehler beim Download: {e}", level="error")

    def upload(self):
        """Lädt die lokale Datei auf den FTP-Server hoch."""
        try:
            ftp = self._connect()
            with open(self.local_file, 'rb') as f:
                ftp.storbinary(f"STOR {self.remote_file}", f)
            ftp.quit()
            self._log("Datei erfolgreich hochgeladen.")
        except Exception as e:
            self._log(f"Fehler beim Upload: {e}", level="error")

    def test_connection(self) -> bool:
        """Testet die FTP-Verbindung."""
        try:
            ftp = self._connect()
            ftp.quit()
            self._log("FTP-Testverbindung erfolgreich.")
            return True
        except Exception as e:
            self._log(f"FTP-Testverbindung fehlgeschlagen: {e}", level="error")
            return False