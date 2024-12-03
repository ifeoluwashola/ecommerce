import logging
from pathlib import Path

# Create a logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure logger
logger = logging.getLogger("user_service")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_DIR / "audit.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
