import sys

from loguru import logger

from config import config
from utils.config_class import Logger


def setup_logger(logger_config: Logger = config.logger):
    """Function to configure logger

    Parameters
    ----------
    logger_config : LogConfig, optional
        config class for logger setup, by default config.logger
    """

    is_debug = logger_config.level == "DEBUG"

    # Remove existing loggers to prevent log duplication
    logger.remove()

    # File handler
    logger.add(
        logger_config.file_path,
        format=logger_config.format,
        rotation=logger_config.rotation,
        enqueue=logger_config.enqueue,
        serialize=logger_config.serialize,
        level=logger_config.level,
        backtrace=is_debug,
        diagnose=is_debug,
    )

    # Stdout handler
    logger.add(
        sys.stderr,
        format=logger_config.format,
        enqueue=logger_config.enqueue,
        level=logger_config.level,
        backtrace=is_debug,
        diagnose=is_debug,
        colorize=True,
    )
    return logger


log = setup_logger()