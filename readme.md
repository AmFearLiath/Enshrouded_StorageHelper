**Phasen:**

1. Strukturaufbau der GUI und Grundfunktionen
2. Einbindung von:

   * Sprache & Theme
   * Konfigurationslogik
   * FTP & Schedulernutzung
   * Logs, Tray-Integration, SMTP
3. Feinschliff, Taskbar-Icon, QR-Code, Updateprüfung

⚠️ Es wird modular in mehrere Dateien aufgeteilt, u. a.:

updater/                           # Hauptordner des Updaters
├── updater.py                    # Haupt-GUI-Script (Entry Point)
├── config.json                  # Konfigurationsdatei (wird von GUI gelesen/geschrieben)
├── assets/                      # Grafische Ressourcen (Icons, Logos, Themes)
│   ├── logo.png
│   ├── icon_password_show.png
│   ├── icon_password_hide.png
│   ├── icon_test.png
│   ├── ... (weitere Icons)
├── core/                        # Kernmodule mit Logik und Backend
│   ├── config_handler.py        # Laden, Speichern, Validierung der Konfiguration
│   ├── ftp_worker.py            # FTP-Download/Upload-Logik
│   ├── scheduler.py             # Taskplanung und Schedule-Management
│   ├── logger.py                # Log-Management, Log-Level, Ausgabe (GUI + Datei)
│   ├── tray_icon.py             # Taskbar/Tray-Icon und Interaktion
│   ├── theme.py                 # Dark/Light-Mode und GUI-Theme-Management
│   ├── qr_tools.py              # Import/Export via QR-Code
│   ├── smtp_handler.py          # SMTP-Integration für Fehlerbenachrichtigungen
│   ├── update_checker.py        # Update-Check-Logik vom GitHub-Repo
│   ├── i18n.py                  # Sprachumschaltung, Übersetzungen laden
│   ├── utils.py                 # Diverse Hilfsfunktionen (z.B. Pfad, Validierungen)
└── locales/                     # Sprachdateien (z.B. JSON oder YAML)
    ├── de.json
    ├── en.json
    └── ... (weitere Sprachen)
