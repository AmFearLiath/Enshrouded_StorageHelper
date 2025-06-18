import sys
from PyQt6.QtGui import QIcon, QAction, QCursor
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtCore import Qt, QObject, pyqtSignal

class TrayIcon(QObject):
    toggle_visibility = pyqtSignal()
    quit_app = pyqtSignal()

    def __init__(self, app, icon_path, parent=None):
        super().__init__(parent)
        self.app = app
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), parent)
        self.menu = QMenu()

        # Menüeinträge
        self.action_toggle = QAction("Show/Hide")
        self.action_quit = QAction("Exit")

        self.menu.addAction(self.action_toggle)
        self.menu.addSeparator()
        self.menu.addAction(self.action_quit)

        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.setToolTip("Savegame FTP JSON Updater")

        # Signale verbinden
        self.action_toggle.triggered.connect(self.toggle_visibility.emit)
        self.action_quit.triggered.connect(self.quit_app.emit)
        self.tray_icon.activated.connect(self.on_activated)

        self.tray_icon.show()

    def on_activated(self, reason):
        # Linksklick zeigt/verbirgt das Fenster
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.toggle_visibility.emit()

    def set_status(self, status):
        """
        Ändert das Tray-Icon je nach Status.
        status: 'running', 'stopped', 'error'
        """
        icons = {
            'running': 'assets/icons/tray_running.png',
            'stopped': 'assets/icons/tray_stopped.png',
            'error': 'assets/icons/tray_error.png'
        }
        icon_path = icons.get(status, 'assets/icons/tray_stopped.png')
        self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setToolTip(f"Updater Status: {status.capitalize()}")

    def show_message(self, title, message):
        """
        Zeigt eine kurze Benachrichtigung am Tray-Icon.
        """
        self.tray_icon.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, 3000)
