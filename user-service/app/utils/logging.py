import logging
from pathlib import Path
from logging_loki import LokiHandler  # Loki integration

# Create a logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure root logger for app logs
logger = logging.getLogger("user_service")
logger.setLevel(logging.INFO)

# File handler for local log storage
file_handler = logging.FileHandler(LOG_DIR / "audit.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Loki handler for centralized logging
# loki_url = "http://localhost:3100/loki/api/v1/push"  # Change this to Loki's URL in your setup
# loki_handler = LokiHandler(
#     url=loki_url,
#     tags={"app": "user_service", "env": "development"},  # Add custom labels
#     version="1",
# )
# loki_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
# logger.addHandler(loki_handler)

# Optional: Configure the root logger to include FastAPI/uvicorn logs
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.setLevel(logging.INFO)
uvicorn_logger.addHandler(file_handler)
# uvicorn_logger.addHandler(loki_handler)

logger.info("Logging initialized with Loki and file storage!")
