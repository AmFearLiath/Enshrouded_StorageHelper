# updater/core/config_handler.py

import json
import os

DEFAULT_CONFIG = {
    "ftp_host": "",
    "ftp_port": 21,
    "ftp_user": "",
    "ftp_pass": "",
    "remote_path": "",
    "interval": 30,
    "start_times": [],
    "temp_dir": "tmp",
    "target_dir": ".",
    "log_level": "INFO",
    "create_backup": True,
    "auto_update": False,
    "github_url": "https://example.com/default-repo",
    "email_notify": "",
    "smtp_server": "",
    "smtp_user": "",
    "smtp_pass": "",
    "smtp_port": 587
}

CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'config.json')


def load_config():
    """Lädt die Konfiguration von der Festplatte, falls vorhanden. Ansonsten wird DEFAULT verwendet."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return {**DEFAULT_CONFIG, **data}
        except Exception as e:
            print(f"[Config] Fehler beim Laden: {e}")
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config: dict):
    """Speichert die übergebene Konfiguration."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[Config] Fehler beim Speichern: {e}")
        return False


def get_default_config():
    """Liefert eine neue Kopie der Standardkonfiguration zurück."""
    return DEFAULT_CONFIG.copy()
