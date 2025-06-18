# updater/core/scheduler.py

import threading
import time
from datetime import datetime
from typing import Callable, List, Optional


class TaskScheduler:
    """Plant Aufgaben entweder im festen Intervall oder zu bestimmten Uhrzeiten."""

    def __init__(self, interval: int = 30, start_times: Optional[List[str]] = None, callback: Optional[Callable] = None, logger=None):
        self.interval = interval
        self.start_times = start_times or []
        self.callback = callback
        self.logger = logger
        self._stop_event = threading.Event()
        self._thread = None

    def _log(self, message):
        if self.logger:
            self.logger.info(message)
        else:
            print("[Scheduler]", message)

    def _run_interval_mode(self):
        self._log(f"Starte Intervallmodus (alle {self.interval} Minuten)")
        while not self._stop_event.is_set():
            self._log("Führe geplante Aufgabe aus (Intervallmodus)")
            if self.callback:
                self.callback()
            self._stop_event.wait(self.interval * 60)

    def _run_fixed_times_mode(self):
        self._log(f"Starte Zeitplanmodus (Startzeiten: {self.start_times})")
        while not self._stop_event.is_set():
            now = datetime.now().strftime("%H:%M")
            if now in self.start_times:
                self._log(f"Führe geplante Aufgabe aus ({now})")
                if self.callback:
                    self.callback()
                time.sleep(60)  # vermeidet Doppelausführung
            else:
                time.sleep(10)

    def start(self):
        """Startet den Scheduler im Hintergrund."""
        if self._thread and self._thread.is_alive():
            self._log("Scheduler läuft bereits.")
            return
        self._stop_event.clear()
        if self.start_times:
            self._thread = threading.Thread(target=self._run_fixed_times_mode, daemon=True)
        else:
            self._thread = threading.Thread(target=self._run_interval_mode, daemon=True)
        self._thread.start()
        self._log("Scheduler gestartet.")

    def stop(self):
        """Stoppt den Scheduler."""
        self._log("Stoppe Scheduler...")
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        self._log("Scheduler gestoppt.")

    def is_running(self):
        return self._thread is not None and self._thread.is_alive()
