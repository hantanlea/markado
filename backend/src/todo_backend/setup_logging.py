import logging
import logging.config
import os
from pathlib import Path

from dotenv import load_dotenv


def setup_logging():
    load_dotenv()

    # log_profile = os.getenv("LOG_PROFILE", "PROD").upper()
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_dir = Path(
        f"{os.getenv('BASE_DIR', '../../')}/{os.getenv('LOG_DIR', 'data/logs')}"
    ).expanduser()
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = os.path.join(log_dir, "backend.log")

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(levelname)s:     %(name)s - %(asctime)s - %(message)s"
            },
            "detailed": {
                "format": (
                    "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s"
                ),
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
        },
        "handlers": {
            "stderr": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": "ext://sys.stderr",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "detailed",
                "filename": log_file,
                "maxBytes": 1000000,
                "backupCount": 3,
            },
        },
        "loggers": {"root": {"level": log_level, "handlers": ["file", "stderr"]}},
    }

    logging.config.dictConfig(logging_config)
    logger = logging.getLogger("backend")
    logger.info(f"Logging initialized. Log directory: {log_dir}")


if __name__ == "__main__":
    setup_logging()
