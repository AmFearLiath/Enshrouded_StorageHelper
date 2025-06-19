# core/utils.py

import os
import datetime

def ensure_dir_exists(path: str) -> None:
    """
    Erstellt das Verzeichnis, falls es nicht existiert.
    
    Args:
        path (str): Pfad zum Verzeichnis.
    """
    if not os.path.exists(path):
        os.makedirs(path)

def format_timestamp(ts: float = None, fmt: str = "%Y-%m-%d_%H-%M-%S") -> str:
    """
    Formatiert einen Zeitstempel in lesbare Form.
    
    Args:
        ts (float, optional): Zeitstempel als Unix-Timestamp. Standard: jetzt.
        fmt (str, optional): Format-String für strftime.
        
    Returns:
        str: Formatierter Zeitstring.
    """
    if ts is None:
        ts = datetime.datetime.now().timestamp()
    return datetime.datetime.fromtimestamp(ts).strftime(fmt)

def validate_time_format(time_str: str) -> bool:
    """
    Validiert, ob ein String das Format HH:MM hat.
    
    Args:
        time_str (str): Zeitstring.
        
    Returns:
        bool: True wenn korrektes Format, sonst False.
    """
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False
