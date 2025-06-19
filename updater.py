# updater.py

import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget,
    QLineEdit, QPushButton, QComboBox, QCheckBox, QSpinBox, QFileDialog,
    QListWidget, QMessageBox, QGroupBox, QFormLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer, Qt

from core.config_handler import ConfigHandler
from core.logger import Logger
from core.ftp_worker import FTPWorker
from core.scheduler import Scheduler
from core.updater_logic import UpdaterLogic
from core.backup_logic import BackupLogic
from core.i18n import I18n
from core.tray_icon import TrayIcon
from core.utils import ensure_dir_exists

APP_VERSION = "1.0.0"
APP_NAME = "Savegame FTP JSON Updater"
CONFIG_FILE = "config.json"
ICON_PATH = "assets/icons/app_icon.png"
TMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")

class UpdaterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.resize(800, 600)

        # Ensure temp dir exists
        ensure_dir_exists(TMP_DIR)

        # Init core modules
        self.logger = Logger()
        self.config = ConfigHandler(CONFIG_FILE)
        self.ftp_worker = None
        self.scheduler = None
        self.i18n = I18n()
        self.updater_logic = None
        self.backup_logic = None

        self.tray_icon = TrayIcon(app, ICON_PATH)
        self.tray_icon.toggle_visibility.connect(self.toggle_visibility)
        self.tray_icon.quit_app.connect(self.quit_app)

        self.init_ui()
        self.load_config()
        self.connect_signals()
        self.setup_scheduler()
        self.update_status("stopped")

        # FTPWorker anlegen
        host = self.config.get("ftp_host", "")
        username = self.config.get("ftp_username", "")
        password = self.config.get("ftp_password", "")
        ftp_dir = self.config.get("ftp_dir", "/")

        # Scheduler starten
        interval = self.config.get("update_interval", 60) * 60  # Minuten zu Sekunden
        self.scheduler = Scheduler(interval, self.run_update)

        self.ftp_worker = FTPWorker(host, username, password, ftp_dir, self.logger)

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        # Logo (simple label placeholder for now)
        logo_label = QLabel()
        logo_label.setPixmap(QIcon(ICON_PATH).pixmap(48, 48))
        header_layout.addWidget(logo_label)

        header_layout.addStretch()

        # Language selector top right
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Deutsch", "English"])
        header_layout.addWidget(self.lang_combo)

        main_layout.addLayout(header_layout)

        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Server Tab
        self.tab_server = QWidget()
        self.tabs.addTab(self.tab_server, self.i18n.t("Server"))
        self.build_tab_server()

        # Update Tab
        self.tab_update = QWidget()
        self.tabs.addTab(self.tab_update, self.i18n.t("Update"))
        self.build_tab_update()

        # Backup Tab
        self.tab_backup = QWidget()
        self.tabs.addTab(self.tab_backup, self.i18n.t("Backup"))
        self.build_tab_backup()

        # Options Tab
        self.tab_options = QWidget()
        self.tabs.addTab(self.tab_options, self.i18n.t("Optionen"))
        self.build_tab_options()

        # Footer
        footer_layout = QHBoxLayout()
        footer_label = QLabel(f"© 2025 Savegame FTP JSON Updater | Version: {APP_VERSION}")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(footer_label)
        main_layout.addLayout(footer_layout)

        self.setLayout(main_layout)

    def log(self, message: str):
        print(message)
    
    def update_status(self, status: str):
        if hasattr(self, 'tray_icon') and self.tray_icon is not None:
            self.tray_icon.set_status(status)
        self.log(f"[Status] Status auf '{status}' gesetzt.")
    
    def build_tab_server(self):
        layout = QFormLayout()
        self.ftp_host = QLineEdit()
        self.ftp_port = QLineEdit()
        self.ftp_user = QLineEdit()
        self.ftp_pass = QLineEdit()
        self.ftp_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.ftp_dir = QLineEdit()

        layout.addRow(self.i18n.t("FTP Host:"), self.ftp_host)
        layout.addRow(self.i18n.t("FTP Port:"), self.ftp_port)
        layout.addRow(self.i18n.t("FTP Benutzer:"), self.ftp_user)
        layout.addRow(self.i18n.t("FTP Passwort:"), self.ftp_pass)
        layout.addRow(self.i18n.t("FTP Verzeichnis:"), self.ftp_dir)

        self.btn_test_ftp = QPushButton(self.i18n.t("Verbindung testen"))
        self.ftp_status = QLabel()
        layout.addRow(self.btn_test_ftp, self.ftp_status)

        self.tab_server.setLayout(layout)

    def build_tab_update(self):
        layout = QVBoxLayout()

        self.chk_interval_30 = QCheckBox("Intervall 30 Minuten")
        self.chk_interval_60 = QCheckBox("Intervall 60 Minuten")

        interval_layout = QHBoxLayout()
        interval_layout.addWidget(self.chk_interval_30)
        interval_layout.addWidget(self.chk_interval_60)

        layout.addLayout(interval_layout)

        self.spin_30_1 = QSpinBox()
        self.spin_30_1.setRange(0, 29)
        self.spin_30_2 = QSpinBox()
        self.spin_30_2.setRange(0, 29)
        self.spin_60 = QSpinBox()
        self.spin_60.setRange(0, 59)

        self.spin_30_1.setEnabled(False)
        self.spin_30_2.setEnabled(False)
        self.spin_60.setEnabled(False)

        times_30_layout = QHBoxLayout()
        times_30_layout.addWidget(QLabel("Zeit 1 (Minuten):"))
        times_30_layout.addWidget(self.spin_30_1)
        times_30_layout.addWidget(QLabel("Zeit 2 (Minuten):"))
        times_30_layout.addWidget(self.spin_30_2)

        times_60_layout = QHBoxLayout()
        times_60_layout.addWidget(QLabel("Zeit (Minuten):"))
        times_60_layout.addWidget(self.spin_60)

        layout.addLayout(times_30_layout)
        layout.addLayout(times_60_layout)

        self.btn_run_update = QPushButton("Jetzt ausführen")
        layout.addWidget(self.btn_run_update)

        self.tab_update.setLayout(layout)
        
    def run_update(self):
        self.log("[Update] Update gestartet.")
        # TODO: Update-Logik implementieren
        # Beispiel: FTP Verbindung testen, Dateien herunterladen, Backup machen etc.
        self.log("[Update] Update beendet.")
    
    def run_updater_now(self):
        from core.ftp_worker import FTPWorker
        from core.config_handler import ConfigHandler

        config = ConfigHandler.load_config()
        ftp_config = config.get("ftp", {})

        ftp = FTPWorker(
            ftp_config.get("host", ""),
            ftp_config.get("user", ""),
            ftp_config.get("password", "")
        )

        try:
            ftp.connect()
            self.tray_icon.show_message("Updater", "Updatevorgang gestartet.")
            # Hier ggf. weitere Logik zum Übertragen/Prüfen einbauen
        except Exception as e:
            self.tray_icon.show_message("Fehler", f"Update fehlgeschlagen:\n{e}")
        finally:
            ftp.disconnect()    

    def update_intervals_enabled(self):
        if self.chk_interval_30.isChecked():
            self.chk_interval_60.setChecked(False)
            self.chk_interval_60.setEnabled(False)
        else:
            self.chk_interval_60.setEnabled(True)
    
    def setup_scheduler(self):
        from core.scheduler import Scheduler

        # Task-Funktion, die der Scheduler ausführen soll
        def scheduled_task():
            self.log("[Scheduler] Starte geplante Update-Aufgabe...")
            try:
                # Hier die eigentliche Update-Logik aufrufen
                self.perform_update()
                self.log("[Scheduler] Update-Aufgabe erfolgreich abgeschlossen.")
                self.tray_icon.set_status('running')
            except Exception as e:
                self.log(f"[Scheduler] Fehler bei Update-Aufgabe: {e}")
                self.tray_icon.set_status('error')

        # Intervall aus GUI, z.B. aus Checkboxen oder Eingabefeldern (in Sekunden)
        if self.chk_interval_30.isChecked():
            interval_seconds = 1800  # 30 Minuten
        elif self.chk_interval_60.isChecked():
            interval_seconds = 3600  # 60 Minuten
        else:
            interval_seconds = 0  # Deaktiviert oder manuell

        if interval_seconds > 0:
            self.scheduler = Scheduler(interval_seconds, scheduled_task)
            self.scheduler.start()
            self.log(f"[Scheduler] Scheduler mit Intervall {interval_seconds}s gestartet.")
            self.tray_icon.set_status('running')
        else:
            self.scheduler = None
            self.log("[Scheduler] Scheduler deaktiviert (kein Intervall gewählt).")
            self.tray_icon.set_status('stopped')

    
    def build_tab_backup(self):
        layout = QVBoxLayout()

        self.spin_backup_rotate = QSpinBox()
        self.spin_backup_rotate.setRange(1, 100)
        self.spin_backup_rotate.setValue(10)

        self.backup_folder = QLineEdit()
        self.btn_browse_backup = QPushButton("Ordner wählen")

        backup_folder_layout = QHBoxLayout()
        backup_folder_layout.addWidget(self.backup_folder)
        backup_folder_layout.addWidget(self.btn_browse_backup)

        self.btn_backup_now = QPushButton("Jetzt sichern")

        self.list_backups = QListWidget()

        layout.addWidget(QLabel("Backup-Rotation (Anzahl):"))
        layout.addWidget(self.spin_backup_rotate)
        layout.addWidget(QLabel("Backup-Ordner:"))
        layout.addLayout(backup_folder_layout)
        layout.addWidget(QLabel("Vorhandene Backups:"))
        layout.addWidget(self.list_backups)
        layout.addWidget(self.btn_backup_now)

        self.tab_backup.setLayout(layout)

    def select_backup_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Backup-Ordner wählen")
        if folder:
            self.backup_folder.setText(folder)

    def run_backup_now(self):
        backup_folder = self.backup_folder.text()  # Pfad aus Eingabefeld
        if not backup_folder:
            self.show_message("Backup Fehler", "Kein Backup-Ordner angegeben.")
            return
        
        # TODO: Backup-Logik hier ergänzen (z.B. FTP-Daten laden, Dateien herunterladen, speichern)
        
        self.show_message("Backup", f"Backup wurde im Ordner '{backup_folder}' gestartet.")
    
    def build_tab_options(self):
        layout = QFormLayout()
        # Beispieloptionen:
        self.chk_logging = QCheckBox("Logging aktivieren")
        layout.addRow(self.chk_logging)

        self.tab_options.setLayout(layout)

    def connect_signals(self):
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        self.btn_test_ftp.clicked.connect(self.test_ftp_connection)
        self.btn_run_update.clicked.connect(self.run_updater_now)
        self.btn_browse_backup.clicked.connect(self.select_backup_folder)
        self.btn_backup_now.clicked.connect(self.run_backup_now)
        self.chk_interval_30.stateChanged.connect(self.update_intervals_enabled)
        self.chk_interval_60.stateChanged.connect(self.update_intervals_enabled)

    def load_config(self):
        cfg = self.config.load()
        if not cfg:
            return
        # Server
        self.ftp_host.setText(cfg.get("ftp_host", ""))
        self.ftp_port.setText(str(cfg.get("ftp_port", 21)))
        self.ftp_user.setText(cfg.get("ftp_user", ""))
        self.ftp_pass.setText(cfg.get("ftp_pass", ""))
        self.ftp_dir.setText(cfg.get("ftp_dir", ""))

        # Update
        self.chk_interval_30.setChecked(cfg.get("update_interval_30", False))
        self.chk_interval_60.setChecked(cfg.get("update_interval_60", False))
        self.spin_30_1.setValue(cfg.get("update_30_time_1", 0))
        self.spin_30_2.setValue(cfg.get("update_30_time_2", 0))
        self.spin_60.setValue(cfg.get("update_60_time", 0))

        # Backup
        self.spin_backup_rotate.setValue(cfg.get("backup_rotation", 10))
        self.backup_folder.setText(cfg.get("backup_folder", os.path.join(os.getcwd(), "backups")))

        # Optionen
        self.chk_logging

    def test_ftp_connection(self):
        host = self.ftp_host.text()
        user = self.ftp_user.text()
        password = self.ftp_pass.text()

        from core.ftp_worker import FTPWorker

        ftp = FTPWorker(host, user, password)
        try:
            ftp.connect()
            self.tray_icon.show_message("FTP", "Verbindung erfolgreich!")
        except Exception as e:
            self.tray_icon.show_message("FTP", f"Verbindung fehlgeschlagen:\n{e}")
        finally:
            ftp.disconnect()

    
    def change_language(self):
        selected_lang = self.lang_combo.currentData()
        if selected_lang:
            self.i18n.set_language(selected_lang)
            self.retranslate_ui()
    
    def retranslate_ui(self):
        _ = self.i18n.translate

        # Tabs
        self.tab_widget.setTabText(0, _("Server"))
        self.tab_widget.setTabText(1, _("Update"))
        self.tab_widget.setTabText(2, _("Backup"))
        self.tab_widget.setTabText(3, _("Options"))

        # Server-Tab
        self.label_ftp_host.setText(_("FTP Host:"))
        self.label_ftp_user.setText(_("FTP Benutzer:"))
        self.label_ftp_pass.setText(_("FTP Passwort:"))
        self.ftp_test_button.setText(_("Verbindung testen"))
        self.ftp_test_button.setToolTip(_("Testet die Verbindung zum FTP-Server."))

        # Update-Tab
        self.update_now_button.setText(_("Jetzt ausführen"))
        self.label_interval.setText(_("Intervall:"))
        self.checkbox_interval.setText(_("Alle %s Minuten") % self.spin_interval.value())

        # Backup-Tab
        self.backup_now_button.setText(_("Jetzt sichern"))
        self.label_backup_folder.setText(_("Backup-Ordner:"))
        self.label_rotation.setText(_("Anzahl behalten:"))

        # Optionen-Tab
        self.label_logging.setText(_("Logging-Level:"))
        self.label_autoupdate.setText(_("Auto-Update aktivieren"))
        self.label_deinstall.setText(_("Skript deinstallieren"))

        # Sprache (Dropdown)
        self.lang_label.setText(_("Sprache:"))

        # Footer
        self.footer_label.setText(_("© 2025 Liath | Version %s") % self.config.get("version", "0.0.1"))

        # Tray-Menü (optional, falls zugänglich)
        if hasattr(self, "tray_icon"):
            self.tray_icon.action_toggle.setText(_("Anzeigen/Verstecken"))
            self.tray_icon.action_quit.setText(_("Beenden"))
            self.tray_icon.tray_icon.setToolTip(_("Savegame FTP JSON Updater"))

        # Fenster-Titel
        self.setWindowTitle(_("Savegame FTP JSON Updater"))

    def quit_app(self):
        self.logger.log_info("Anwendung wird beendet.")
        self.config.save()
        self.tray_icon.hide()
        QApplication.quit()

if __name__ == "__main__":
    print("[INFO] Starte Updater-GUI...")
    app = QApplication(sys.argv)
    window = UpdaterGUI()
    window.show()
    sys.exit(app.exec())