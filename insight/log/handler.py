import logging
from datetime import datetime
from pathlib import Path

LOG_FILE_NAME = f"{datetime.now().strftime("%d_%B_%Y")}.log"


class MonthlyRotatingFileHandler(logging.Handler):
    def __init__(self, log_dir: Path):
        super().__init__()
        self.log_dir = log_dir

        self.log_file_name = LOG_FILE_NAME

        self.stream = open(
            self.log_dir / self.log_file_name, mode="a", encoding="utf-8"
        )

    def emit(self, record):
        try:
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
