import json
import logging
import logging.config
import os
from pathlib import Path

from dotenv import load_dotenv


def setup_logging():
    load_dotenv()
    logging_config = Path("logging_config.json")

    with open(logging_config) as f:
        config = json.load(f)
    try:
        log_dir = os.getenv("LOG_DIR")
        if log_dir:
            log_path = Path(log_dir).expanduser()
            log_path.mkdir(parents=True, exist_ok=True)
            config["handlers"]["file"]["filename"] = str(log_path / "backend.log")
            print(f"Created log directory at: {log_path}")
    except Exception as e:
        log_dir = Path(config["handlers"]["file"]["filename"]).parent
        print(f"Error creating log directory. Falling back to local folder: {e}")
    finally:
        logging.config.dictConfig(config)
        logging.info("Logger started")


if __name__ == "__main__":
    setup_logging()
