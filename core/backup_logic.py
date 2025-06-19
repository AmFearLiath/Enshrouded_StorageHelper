# core/backup_logic.py

import os
import io
import zipfile
from typing import List
from core.ftp_worker import FTPWorker
from core.logger import Logger
from core.utils import ensure_dir_exists, format_timestamp

class BackupLogic:
    """
    Backup-Logik zum Herunterladen aller Dateien aus dem FTP-Verzeichnis,
    Erstellen eines ZIP-Archivs und Speichern im Backup-Ordner.
    """

    def __init__(self, ftp_worker: FTPWorker, backup_dir: str, logger: Logger):
        """
        Args:
            ftp_worker (FTPWorker): FTP-Worker für Dateioperationen.
            backup_dir (str): Lokaler Pfad zum Backup-Ordner.
            logger (Logger): Logger für Protokollierung.
        """
        self.ftp_worker = ftp_worker
        self.backup_dir = backup_dir
        self.logger = logger

        ensure_dir_exists(self.backup_dir)

    def create_backup(self) -> bool:
        """
        Lädt alle Dateien vom FTP-Server herunter, erstellt ein ZIP-Archiv
        und speichert dieses im Backup-Ordner.

        Returns:
            bool: True bei Erfolg, False bei Fehlern.
        """
        try:
            self.logger.log_info("BackupLogic: Lade Dateiliste vom FTP-Server...")
            files = self.ftp_worker.list_files()
            if not files:
                self.logger.log_error("BackupLogic: Keine Dateien im FTP-Verzeichnis gefunden.")
                return False

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
                for filename in files:
                    self.logger.log_info(f"BackupLogic: Lade Datei {filename} herunter...")
                    content = self.ftp_worker.download_file(filename)
                    if content is None:
                        self.logger.log_error(f"BackupLogic: Fehler beim Herunterladen von {filename}")
                        continue
                    zipf.writestr(filename, content)

            timestamp = format_timestamp()
            backup_filename = os.path.join(self.backup_dir, f"backup_{timestamp}.zip")

            with open(backup_filename, "wb") as f:
                f.write(zip_buffer.getvalue())

            self.logger.log_info(f"BackupLogic: Backup erfolgreich erstellt: {backup_filename}")
            return True

        except Exception as e:
            self.logger.log_error(f"BackupLogic: Ausnahmefehler: {e}")
            return False
