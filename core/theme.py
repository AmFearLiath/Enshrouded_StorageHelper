from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


class ThemeManager:
    def __init__(self, widget: QWidget, dark_mode: bool = True):
        self.widget = widget
        self.dark_mode = dark_mode

    def apply_theme(self):
        if self.dark_mode:
            self._apply_dark_theme()
        else:
            self._apply_light_theme()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def _apply_dark_theme(self):
        dark_palette = QPalette()

        # Grundfarben
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(40, 40, 40))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)

        # Links und Auswahl
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(204, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(204, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)

        self.widget.setPalette(dark_palette)

    def _apply_light_theme(self):
        self.widget.setPalette(self.widget.style().standardPalette())
