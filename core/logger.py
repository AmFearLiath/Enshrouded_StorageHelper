# core/logger.py

import logging
import sys
from datetime import datetime

class Logger:
    """
    Logger-Klasse zur zentralen Protokollierung.
    Unterstützt verschiedene Level: INFO, WARNING, ERROR.
    """

    def __init__(self, log_file: str = None, level=logging.INFO):
        self.logger = logging.getLogger("UpdaterLogger")
        self.logger.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Konsolenausgabe
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Optional: Datei-Logging
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def log_info(self, message: str):
        self.logger.info(message)

    def log_warning(self, message: str):
        self.logger.warning(message)

    def log_error(self, message: str):
        self.logger.error(message)
