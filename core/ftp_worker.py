# core/ftp_worker.py

import ftplib
import io
import os
import zipfile
import json
from typing import Optional, List
from core.logger import Logger

class FTPWorker:
    def __init__(self, host: str, username: str, password: str, ftp_dir: str = "/", logger: Logger = None):
        self.host = host
        self.username = username
        self.password = password
        self.ftp_dir = ftp_dir
        self.logger = logger
        self.ftp = None

    def connect(self) -> bool:
        try:
            self.ftp = ftplib.FTP(self.host, timeout=10)
            self.ftp.login(self.username, self.password)
            self.ftp.cwd(self.ftp_dir)
            if self.logger:
                self.logger.log_info(f"FTPWorker: Verbunden mit {self.host} und Verzeichnis {self.ftp_dir}")
            return True
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"FTPWorker Verbindungsfehler: {e}")
            return False

    def disconnect(self):
        if self.ftp:
            try:
                self.ftp.quit()
                if self.logger:
                    self.logger.log_info("FTPWorker: Verbindung geschlossen")
            except Exception as e:
                if self.logger:
                    self.logger.log_error(f"FTPWorker Fehler beim Trennen: {e}")

    def download_file(self, filename: str) -> Optional[bytes]:
        try:
            with io.BytesIO() as bio:
                self.ftp.retrbinary(f"RETR {filename}", bio.write)
                data = bio.getvalue()
                if self.logger:
                    self.logger.log_info(f"FTPWorker: Datei {filename} heruntergeladen ({len(data)} Bytes)")
                return data
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"FTPWorker Fehler beim Download {filename}: {e}")
            return None

    def upload_file(self, filename: str, data: bytes) -> bool:
        try:
            with io.BytesIO(data) as bio:
                bio.seek(0)
                self.ftp.storbinary(f"STOR {filename}", bio)
                if self.logger:
                    self.logger.log_info(f"FTPWorker: Datei {filename} hochgeladen ({len(data)} Bytes)")
            return True
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"FTPWorker Fehler beim Upload {filename}: {e}")
            return False

    def list_files(self) -> Optional[List[str]]:
        try:
            files = self.ftp.nlst()
            if self.logger:
                self.logger.log_info(f"FTPWorker: Verzeichnisinhalt abgerufen ({len(files)} Dateien)")
            return files
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"FTPWorker Fehler beim Auflisten der Dateien: {e}")
            return None

    def download_and_zip(self, filenames: List[str], zip_name: str) -> Optional[bytes]:
        """
        Lädt mehrere Dateien herunter und gibt ein ZIP-Archiv als Bytes zurück.
        """
        try:
            with io.BytesIO() as zip_buffer:
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for filename in filenames:
                        data = self.download_file(filename)
                        if data is not None:
                            zipf.writestr(filename, data)
                        else:
                            if self.logger:
                                self.logger.log_error(f"FTPWorker: Datei {filename} konnte nicht geladen werden, wird nicht ins ZIP gepackt.")
                zip_data = zip_buffer.getvalue()
                if self.logger:
                    self.logger.log_info(f"FTPWorker: ZIP-Archiv {zip_name} erstellt ({len(zip_data)} Bytes)")
                return zip_data
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"FTPWorker Fehler beim Erstellen des ZIP-Archivs: {e}")
            return None
