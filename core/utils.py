import os
import json
from pathlib import Path


def get_base_path():
    """
    Gibt den Basisordner zurück, in dem das Script liegt.
    """
    return Path(__file__).resolve().parent.parent


def get_default_config_path():
    """
    Gibt den Pfad zur Standard-Konfigurationsdatei zurück.
    """
    return get_base_path() / "config.json"


def ensure_dir_exists(directory):
    """
    Erstellt ein Verzeichnis, wenn es nicht existiert.
    """
    os.makedirs(directory, exist_ok=True)


def is_valid_json(file_path):
    """
    Prüft, ob die angegebene Datei eine gültige JSON-Datei ist.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, FileNotFoundError, PermissionError):
        return False


def load_json(file_path):
    """
    Lädt und gibt eine JSON-Datei als dict zurück.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(file_path, data):
    """
    Speichert ein Dictionary als JSON-Datei.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_temp_directory():
    """
    Gibt das Standard-Temp-Verzeichnis zurück.
    """
    tmp_path = get_base_path() / "tmp"
    ensure_dir_exists(tmp_path)
    return tmp_path


def is_windows():
    return os.name == 'nt'


def is_linux():
    return os.name == 'posix'
