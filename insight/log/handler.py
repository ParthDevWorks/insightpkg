import logging
from datetime import datetime
from pathlib import Path

LOG_FILE = f"{datetime.now().strftime("%B_%Y")}.log"


class MonthlyRotatingFileHandler(logging.Handler):
    def __init__(self, log_dir: Path):
        super().__init__()
        self.log_dir = log_dir

        self.current_month = LOG_FILE
        self.stream = None
        self._open_new_log_file()

    def _get_log_filename(self):
        return self.log_dir / LOG_FILE

    def _open_new_log_file(self):
        if self.stream:
            self.stream.close()
        self.current_month = LOG_FILE
        self.stream = open(self._get_log_filename(), mode="a", encoding="utf-8")

    def emit(self, record):
        try:
            # Check if month has changed
            current_month = LOG_FILE
            if current_month != self.current_month:
                self._open_new_log_file()

            msg = self.format(record)
            self.stream.write(msg + "\n")
            self.stream.flush()
        except Exception:
            self.handleError(record)

    def close(self):
        if self.stream:
            try:
                self.stream.close()
            except Exception:
                pass
        super().close()
