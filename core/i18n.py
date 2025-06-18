import json
from pathlib import Path

class I18n:
    def __init__(self, default_lang="de"):
        self.locales_path = Path(__file__).parent.parent / "locales"
        self._translations = {}
        self._lang = default_lang
        self._load_language(default_lang)

    def _load_language(self, lang):
        lang_file = self.locales_path / f"{lang}.json"
        if lang_file.exists():
            with open(lang_file, "r", encoding="utf-8") as f:
                self._translations = json.load(f)
                self._lang = lang
        else:
            self._translations = {}
            self._lang = "en"

    def translate(self, key):
        return self._translations.get(key, key)

    def set_language(self, lang_code):
        self._load_language(lang_code)

    def current_language(self):
        return self._lang

    def available_languages(self):
        langs = []
        for file in self.locales_path.glob("*.json"):
            langs.append(file.stem)
        return sorted(langs)
