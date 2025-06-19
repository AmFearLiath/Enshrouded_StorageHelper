"""
core/i18n.py

Internationalisierung und Sprachumschaltung.
Unterstützt einfache Schlüssel/Wert-Übersetzung über Sprachdateien (JSON).

- Automatisches Laden der Sprachdateien aus `core/de.json` und `core/en.json`
- Fallback auf Englisch bei fehlenden Schlüsseln
- Umschaltbare Sprache zur Laufzeit
"""

import json
import os

class I18n:
    def __init__(self, default_lang="de"):
        self.supported_languages = ["de", "en"]
        self.translations = {}
        self.lang = default_lang
        self.load_translations()

    def load_translations(self):
        """
        Lädt alle verfügbaren Übersetzungsdateien.
        """
        for lang in self.supported_languages:
            file_path = os.path.join("locales", f"{lang}.json")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.translations[lang] = json.load(f)
            except FileNotFoundError:
                print(f"[WARN] Sprachdatei fehlt: {file_path}")
                self.translations[lang] = {}

    def set_language(self, lang):
        """
        Setzt die aktuelle Sprache, falls unterstützt.
        """
        if lang in self.supported_languages:
            self.lang = lang
        else:
            print(f"[WARN] Sprache nicht unterstützt: {lang}")

    def t(self, key):
        """
        Holt die Übersetzung für den gegebenen Schlüssel.

        Fallback auf Englisch, falls Schlüssel fehlt.
        """
        return (
            self.translations.get(self.lang, {}).get(key) or
            self.translations.get("en", {}).get(key) or
            f"[{key}]"
        )

    def get_current_language(self):
        """
        Gibt die aktuell gesetzte Sprache zurück.
        """
        return self.lang
