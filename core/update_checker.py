"""
core/update_checker.py

Automatischer Update-Checker für das Script.

Prüft ein konfigurierbares GitHub-Repository auf neue Releases (oder Tags)
und benachrichtigt die Hauptanwendung, falls ein Update verfügbar ist.

Abhängigkeiten:
- requests

Funktionen:
- Versionsvergleich
- Fetch GitHub API
- Update-Verfügbarkeit melden
"""

import requests
from typing import Optional

from core.logger import Logger

class UpdateChecker:
    """
    Prüft GitHub auf neue Releases und meldet Update-Verfügbarkeit.
    """

    def __init__(self, repo_owner: str, repo_name: str, current_version: str, logger: Optional[Logger] = None):
        """
        Args:
            repo_owner (str): GitHub-Benutzer oder Organisation.
            repo_name (str): Repository-Name.
            current_version (str): Aktuelle Version des Scripts (z.B. "1.0.0").
            logger (Logger, optional): Logger-Instanz für Logs.
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.logger = logger
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"

    def get_latest_version(self) -> Optional[str]:
        """
        Holt die neueste Release-Version von GitHub.

        Returns:
            Optional[str]: Versionsstring der neuesten Version oder None bei Fehler.
        """
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            latest_version = data.get("tag_name")
            if self.logger:
                self.logger.log_info(f"UpdateChecker: Neueste Version laut GitHub: {latest_version}")
            return latest_version
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"UpdateChecker Fehler: {e}")
            return None

    def is_update_available(self) -> Optional[bool]:
        """
        Vergleicht aktuelle Version mit der neuesten Version.

        Returns:
            Optional[bool]: True wenn Update verfügbar, False wenn nicht, None bei Fehler.
        """
        latest_version = self.get_latest_version()
        if latest_version is None:
            return None

        def version_tuple(v):
            return tuple(int(x) for x in v.lstrip('v').split('.') if x.isdigit())

        try:
            current = version_tuple(self.current_version)
            latest = version_tuple(latest_version)
            update_available = latest > current
            if self.logger:
                if update_available:
                    self.logger.log_info(f"UpdateChecker: Update verfügbar ({latest_version} > {self.current_version})")
                else:
                    self.logger.log_info("UpdateChecker: Kein Update verfügbar.")
            return update_available
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"UpdateChecker Vergleichsfehler: {e}")
            return None
