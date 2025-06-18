"""
core/qr_tools.py

QR-Code Import/Export Modul für Konfigurationsdaten.
Ermöglicht das Generieren von QR-Codes aus JSON-Daten und das Einlesen von QR-Codes.

Abhängigkeiten:
- qrcode
- pillow
- pyzbar
"""

import io
import json
from typing import Optional

import qrcode
from PIL import Image
from pyzbar.pyzbar import decode


def generate_qr_code(data: dict, box_size: int = 10, border: int = 4) -> Image.Image:
    """
    Generiert ein QR-Code Bild aus einem Dictionary (JSON-kompatibel).

    Args:
        data (dict): Die zu kodierenden Daten.
        box_size (int): Größe der QR-Boxen.
        border (int): Breite des Randes.

    Returns:
        PIL.Image.Image: Generiertes QR-Code Bild.
    """
    json_str = json.dumps(data, ensure_ascii=False)
    qr = qrcode.QRCode(box_size=box_size, border=border)
    qr.add_data(json_str)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


def decode_qr_code(image: Image.Image) -> Optional[dict]:
    """
    Liest QR-Code Daten aus einem PIL Bild und gibt ein Dictionary zurück.

    Args:
        image (PIL.Image.Image): Das Bild mit QR-Code.

    Returns:
        Optional[dict]: Die dekodierten Daten als Dictionary oder None bei Fehler.
    """
    decoded_objects = decode(image)
    if not decoded_objects:
        return None

    # Nur ersten QR-Code im Bild auslesen
    qr_data = decoded_objects[0].data.decode('utf-8')
    try:
        data = json.loads(qr_data)
        return data
    except json.JSONDecodeError:
        return None


def load_qr_code_from_file(file_path: str) -> Optional[dict]:
    """
    Lädt ein Bild von Datei und liest darin enthaltenen QR-Code aus.

    Args:
        file_path (str): Pfad zur Bilddatei.

    Returns:
        Optional[dict]: Dekodierte Daten oder None.
    """
    try:
        img = Image.open(file_path)
        return decode_qr_code(img)
    except Exception:
        return None


def save_qr_code_to_file(data: dict, file_path: str) -> None:
    """
    Speichert den QR-Code für die gegebenen Daten als Bilddatei.

    Args:
        data (dict): Zu kodierende Daten.
        file_path (str): Speicherpfad (z.B. .png).
    """
    img = generate_qr_code(data)
    img.save(file_path)
