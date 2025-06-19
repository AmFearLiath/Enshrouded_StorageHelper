# core/scheduler.py

import threading
import time
import logging

class Scheduler:
    """
    Ein einfacher Scheduler, der eine wiederkehrende Aufgabe in einem eigenen Thread ausführt.
    Unterstützt Start, Stop, Pause, und Intervalldynamik.
    """

    def __init__(self, interval_seconds: int, task, logger=None):
        """
        :param interval_seconds: Intervall in Sekunden zwischen den Ausführungen der Aufgabe
        :param task: Callable, die periodisch ausgeführt wird (ohne Parameter)
        :param logger: Optionaler Logger, falls None wird logging.getLogger(__name__) verwendet
        """
        self.interval_seconds = interval_seconds
        self.task = task
        self._logger = logger or logging.getLogger(__name__)
        self._thread = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._pause_event.set()  # Nicht pausiert am Anfang

    def _run(self):
        self._logger.info("Scheduler gestartet mit Intervall %d Sekunden.", self.interval_seconds)
        while not self._stop_event.is_set():
            self._pause_event.wait()  # Falls pausiert, hier warten

            start_time = time.time()
            try:
                self.task()
            except Exception as e:
                self._logger.error("Fehler bei der Ausführung des Scheduler-Tasks: %s", e)

            elapsed = time.time() - start_time
            sleep_time = self.interval_seconds - elapsed
            if sleep_time > 0:
                # Warten, aber stop_event überwachen
                stopped = self._stop_event.wait(timeout=sleep_time)
                if stopped:
                    break

        self._logger.info("Scheduler beendet.")

    def start(self):
        """
        Scheduler-Thread starten.
        Wenn bereits gestartet, passiert nichts.
        """
        if self._thread and self._thread.is_alive():
            self._logger.debug("Scheduler bereits gestartet.")
            return

        self._stop_event.clear()
        self._pause_event.set()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self._logger.debug("Scheduler-Thread gestartet.")

    def stop(self):
        """
        Scheduler stoppen (Thread wird beendet).
        """
        self._logger.debug("Scheduler wird gestoppt.")
        self._stop_event.set()
        self._pause_event.set()  # Falls pausiert, wecken zum Beenden
        if self._thread:
            self._thread.join()
            self._thread = None
        self._logger.debug("Scheduler wurde gestoppt.")

    def pause(self):
        """
        Scheduler pausieren (Aufgaben-Ausführung aussetzen).
        """
        self._logger.debug("Scheduler pausiert.")
        self._pause_event.clear()

    def resume(self):
        """
        Scheduler fortsetzen (falls pausiert).
        """
        if not self._pause_event.is_set():
            self._logger.debug("Scheduler wird fortgesetzt.")
            self._pause_event.set()

    def set_interval(self, interval_seconds: int):
        """
        Intervall ändern. Neue Intervalle wirken ab dem nächsten Intervallzyklus.
        """
        self._logger.info("Scheduler-Intervall geändert: %d Sekunden.", interval_seconds)
        self.interval_seconds = interval_seconds

    def is_running(self) -> bool:
        """
        True wenn Scheduler-Thread läuft (auch wenn pausiert).
        """
        return self._thread is not None and self._thread.is_alive()

    def is_paused(self) -> bool:
        """
        True wenn Scheduler pausiert ist.
        """
        return not self._pause_event.is_set()
