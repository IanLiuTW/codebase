from loguru import logger as lo

LOGGER_CONFIG = {
    "handlers": [
        {
            "sink": sys.stderr,
            "level": os.environ.get("LOG_LEVEL", "INFO"),
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        },
    ],
}


lo.configure(**LOGGER_CONFIG)