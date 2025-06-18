# updater/core/logger.py

import logging
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'updater.log')

os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(level: str = "INFO") -> logging.Logger:
    """Initialisiert das Logger-Objekt mit gewünschtem Level und Ausgabe in Datei + Konsole."""
    logger = logging.getLogger("UpdaterLogger")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Bestehende Handler entfernen (bei Neuladen in GUI)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Datei-Handler
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

    # Stream-Handler (Konsole)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger