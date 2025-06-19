"""
core/qr_tools.py

Erzeugt und liest QR-Codes zur Konfigurations-Import/Export-Funktion.

Abhängigkeiten:
- qrcode
- Pillow (für Bildbearbeitung)
- pyzbar (für QR-Code-Scannen)

Funktionen:
- QR-Code aus Text generieren und als Bild speichern
- QR-Code aus Bilddatei oder Kamera lesen
"""

import qrcode
from PIL import Image
from typing import Optional
from pyzbar.pyzbar import decode


class QRTools:
    @staticmethod
    def generate_qr_code(data: str, output_path: str, box_size: int = 10, border: int = 4) -> None:
        """
        Generiert einen QR-Code aus dem übergebenen Text und speichert ihn als PNG.

        Args:
            data (str): Zu codierender Text.
            output_path (str): Pfad zur Ausgabedatei (PNG).
            box_size (int): Größe der QR-Code-Boxen.
            border (int): Breite des Rands.
        """
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)

    @staticmethod
    def read_qr_code(image_path: str) -> Optional[str]:
        """
        Liest einen QR-Code aus einer Bilddatei und gibt den Text zurück.

        Args:
            image_path (str): Pfad zur Bilddatei.

        Returns:
            Optional[str]: Inhalt des QR-Codes oder None wenn keiner gefunden wurde.
        """
        try:
            img = Image.open(image_path)
            decoded_objects = decode(img)
            if decoded_objects:
                return decoded_objects[0].data.decode('utf-8')
            return None
        except Exception:
            return None
