import logging
import os
import pathlib

CURRENT_DIR = pathlib.Path(os.getcwd())

# stout logging
SERVER_LOG_FILE_PATH = os.path.join(CURRENT_DIR, "server.log")
# create file if it doesn't exist
if not os.path.exists(SERVER_LOG_FILE_PATH):
    with open(SERVER_LOG_FILE_PATH, "a", encoding="UTF-8"):
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(SERVER_LOG_FILE_PATH), logging.StreamHandler()],
)
