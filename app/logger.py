import logging
from logging.handlers import RotatingFileHandler
import os
import sys

def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    
    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # app logger
    app_logger = logging.getLogger("app")
    app_logger.handlers = [file_handler, console_handler]
    app_logger.setLevel(logging.INFO)
    app_logger.propagate = False

    # uvicorn logger
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers = [file_handler, console_handler]
        uvicorn_logger.setLevel(logging.INFO)
        uvicorn_logger.propagate = False