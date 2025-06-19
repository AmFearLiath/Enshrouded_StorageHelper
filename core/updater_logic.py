# core/updater_logic.py

import json
from typing import Optional
from core.ftp_worker import FTPWorker
from core.logger import Logger

class UpdaterLogic:
    """
    Logik zum Herunterladen, Bearbeiten und Hochladen der "3ad85aea-index"-Datei
    im konfigurierten FTP-Verzeichnis.
    """

    def __init__(self, ftp_worker: FTPWorker, logger: Logger):
        """
        Args:
            ftp_worker (FTPWorker): FTP-Worker für Dateioperationen.
            logger (Logger): Logger für Protokollierung.
        """
        self.ftp_worker = ftp_worker
        self.logger = logger
        self.index_filename = "3ad85aea-index"

    def process_index_file(self) -> bool:
        """
        Holt die Index-Datei vom FTP-Server, liest 'latest' aus, reduziert ihn um 1,
        schreibt die Datei zurück und loggt den Vorgang.

        Returns:
            bool: True bei Erfolg, False bei Fehlern.
        """
        try:
            self.logger.log_info("UpdaterLogic: Lade Index-Datei herunter...")
            content = self.ftp_worker.download_file(self.index_filename)
            if content is None:
                self.logger.log_error("UpdaterLogic: Index-Datei nicht gefunden oder leer.")
                return False

            data = json.loads(content.decode('utf-8'))
            if 'latest' not in data:
                self.logger.log_error("UpdaterLogic: 'latest' Schlüssel nicht gefunden.")
                return False

            original_latest = data['latest']
            if not isinstance(original_latest, int):
                self.logger.log_error("UpdaterLogic: 'latest' ist kein Integer.")
                return False

            new_latest = max(0, original_latest - 1)
            data['latest'] = new_latest

            updated_content = json.dumps(data, indent=2).encode('utf-8')

            self.logger.log_info(f"UpdaterLogic: Aktualisiere 'latest' von {original_latest} auf {new_latest}.")

            upload_result = self.ftp_worker.upload_file(self.index_filename, updated_content)
            if not upload_result:
                self.logger.log_error("UpdaterLogic: Fehler beim Hochladen der aktualisierten Datei.")
                return False

            self.logger.log_info("UpdaterLogic: Index-Datei erfolgreich aktualisiert und hochgeladen.")
            return True

        except Exception as e:
            self.logger.log_error(f"UpdaterLogic: Ausnahmefehler: {e}")
            return False
