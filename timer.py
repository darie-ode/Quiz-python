import threading
import time


class CountdownTimer:
    def __init__(self, seconds, update_callback, finish_callback):
        self.seconds = seconds
        self.update_callback = update_callback
        self.finish_callback = finish_callback
        self._running = False
        self._thread = None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()

    def _run(self):
        remaining = self.seconds
        while remaining > 0 and self._running:
            time.sleep(1)
            remaining -= 1
            if self._running:
                self.update_callback(remaining)
        if self._running:
            self.finish_callback()

    def cancel(self):
        self._running = False
