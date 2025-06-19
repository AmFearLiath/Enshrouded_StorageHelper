"""
core/config_handler.py

Konfigurationsmanagement:
- Laden und Speichern der Einstellungen als JSON-Datei
- Default-Werte und Validierung
- Unterstützung für Import/Export (z.B. auch für QR-Code-Export)
"""

import json
import os
from typing import Optional, Dict, Any

class ConfigHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.config = {}

    def _default_config(self) -> Dict[str, Any]:
        return {
            "ftp": {
                "host": "",
                "port": 21,
                "username": "",
                "password": "",
                "remote_path": "",
            },
            "local": {
                "install_dir": "",
                "temp_dir": "",
            },
            "smtp": {
                "enabled": False,
                "smtp_server": "",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "sender_email": "",
                "recipient_email": "",
                "use_tls": True,
            },
            "logging": {
                "level": "INFO",
            },
            "update": {
                "auto_check": True,
                "repo_owner": "",
                "repo_name": "",
                "current_version": "",
            },
            "ui": {
                "language": "de",
                "dark_mode": True,
            },
            "backup": {
                "enabled": True,
                "backup_dir": "",
            }
        }

    def load(self) -> dict:
        if not os.path.isfile(self.filepath):
            return {}
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.config = json.load(f)
            return self.config
        except (json.JSONDecodeError, IOError):
            return {}

    def save(self, config: dict) -> bool:
        try:
            # Sicherstellen, dass Verzeichnis existiert
            ensure_dir_exists(os.path.dirname(self.filepath))
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except IOError:
            return False

    def get(self, key: str, default=None):
        return self.config.get(key, default)

    def set(self, key: str, value):
        self.config[key] = value
        self.save(self.config)
