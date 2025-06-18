import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QPushButton,
    QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtCore import Qt

from core.i18n import I18n
from core.theme import ThemeManager

class UpdaterGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Basisinitialisierungen
        self.setWindowTitle("Savegame FTP JSON Updater")
        self.setMinimumSize(700, 450)

        # Ressourcenpfad
        self.assets_dir = Path(__file__).parent.parent / "assets"
        self.logo_path = self.assets_dir / "logo.png"

        # Sprach- und Theme-Manager
        self.i18n = I18n()
        self.theme_manager = ThemeManager(self)

        self._init_ui()

    def _init_ui(self):
        # Hauptlayout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # --- Obere Leiste: Logo links, Sprachwahl rechts ---
        top_bar = QHBoxLayout()

        # Logo anzeigen (oben links)
        logo_label = QLabel()
        if self.logo_path.exists():
            pixmap = QPixmap(str(self.logo_path)).scaled(100, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("LOGO")
        top_bar.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Spacer zwischen Logo und rechtsseitigem Menü
        top_bar.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Sprachumschaltung (ComboBox)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(self.i18n.available_languages())
        self.lang_combo.setCurrentText(self.i18n.current_language())
        self.lang_combo.currentTextChanged.connect(self.on_language_change)
        top_bar.addWidget(self.lang_combo, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addLayout(top_bar)

        # --- Platzhalter für zentrale GUI-Inhalte ---
        self.content_label = QLabel(self.i18n.translate("GUI will be implemented here..."))
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.content_label, stretch=1)

        # --- Unten rechts: Copyright ---
        copyright_label = QLabel("© Liath")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(copyright_label)

        # Theme anwenden
        self.theme_manager.apply_theme()

    def on_language_change(self, lang_code):
        self.i18n.set_language(lang_code)
        self.content_label.setText(self.i18n.translate("GUI will be implemented here..."))


def main():
    app = QApplication(sys.argv)
    window = UpdaterGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
