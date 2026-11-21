import logging
import sys

from .config import settings


def setup_logging() -> None:
    """Настроить логирование приложения."""

    log_level = settings.log_level.upper()
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

    if log_level not in valid_levels:
        raise ValueError(f"Некорректный уровень логирования: {settings.log_level}")

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
