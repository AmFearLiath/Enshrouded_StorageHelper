# Anleitung zur Installation und Nutzung des Savegame FTP JSON Updaters mit GUI

---

## 1. Installation von Python unter Windows

* Gehe auf die offizielle Python-Webseite: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
* Lade die aktuell empfohlene Version (mindestens Python 3.10) herunter.
* Starte den Installer und **achte unbedingt darauf, dass du die Option „Add Python to PATH“ anklickst**, bevor du auf „Install Now“ klickst.
* Warte bis die Installation abgeschlossen ist.

---

## 2. Nutzung der Eingabeaufforderung (Konsole)

* Drücke `Win + R`, gib `cmd` ein und drücke Enter, um die Eingabeaufforderung zu öffnen.
* Alternativ kannst du im Startmenü nach „Eingabeaufforderung“ suchen.
* In der Eingabeaufforderung kannst du Python mit folgendem Befehl testen:

```bash
python --version
```

* Die Ausgabe sollte die installierte Python-Version zeigen, z.B. `Python 3.11.2`.
* Wechsle in das Verzeichnis, in dem dein Script liegt, mit:

```bash
cd Pfad\zum\Script\Verzeichnis
```

(z.B. `cd C:\Users\DeinBenutzer\Documents\SavegameUpdater`)

---

## 3. Installieren der Abhängigkeiten

Das Script benötigt einige externe Python-Bibliotheken, die nicht standardmäßig mit Python installiert werden.

Führe in der Eingabeaufforderung folgende Befehle aus:

```bash
pip install requests
pip install pillow
```

Erklärung:

* `requests`: Für HTTP-Anfragen, z.B. Update-Prüfung bei GitHub
* `pillow`: Für QR-Code-Erstellung und Bildverarbeitung

Wenn `pip` nicht erkannt wird, versuche:

```bash
python -m pip install requests
python -m pip install pillow
```

---

## 4. Starten und Verwenden des Scripts

* Im Hauptverzeichnis befindet sich die Datei `updater.py`.
* Starte das GUI mit:

```bash
python updater.py
```

* Das Fenster öffnet sich und du kannst die FTP-Zugangsdaten sowie weitere Einstellungen konfigurieren.
* Im Menü kannst du Sprache (Deutsch/Englisch) sowie Dark Mode wechseln.
* Über Import/Export kannst du Einstellungen als Datei oder QR-Code sichern und laden.
* Nach Konfiguration kannst du den Updater starten, der dann in festgelegten Intervallen automatisch deine Savegame-Daten synchronisiert.
* Das Taskbar-Icon zeigt den Status (aktiv/inaktiv) an.
* Bei Fehlern kannst du eine E-Mail-Benachrichtigung aktivieren (SMTP-Konfiguration notwendig).
* Das Script prüft automatisch Updates und informiert dich, wenn eine neue Version verfügbar ist.

---

## 5. Einstellungen

* FTP-Zugangsdaten: Server, Benutzer, Passwort, Port, Pfad zur Savegame-Datei.
* Intervall oder feste Zeitpunkte zur Synchronisation.
* SMTP: Server, Port, Benutzername, Passwort, Absender und Empfänger für Fehlerbenachrichtigungen.
* Theme: Hell/Dunkel, Sprache.
* Backup-Optionen vor Upload.
* Auto-Update aktivieren/deaktivieren.
* Logs und Debug-Informationen im GUI einsehbar.
* QR-Code Import/Export für einfache Konfiguration per Kamera.

---

**Viel Erfolg! Bei Fragen einfach melden.**
