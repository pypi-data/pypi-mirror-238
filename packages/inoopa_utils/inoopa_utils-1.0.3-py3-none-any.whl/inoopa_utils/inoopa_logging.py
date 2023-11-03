"""Base Inoopa configuration for python Logging."""
import logging
from typing import Literal
from datetime import datetime

from utils.env_variables_helper import get_env_name


LoggingLevel = Literal["CRITICAL","FATAL","ERROR","WARN","WARNING","INFO","DEBUG"]

def create_logger(logger_name: str, logging_level: LoggingLevel | None = None) -> logging.Logger:
    """
    Configure how logging should be done.
    
    :param logger_name: The logger name to return.
    :param logging_level: The level of logging to filter. If none, will deduce from "ENV" env variable:
        'dev' will set logging_level to "DEBUG"
        'staging' will set logging_level to "INFO"
        'prod' will set logging_level to "INFO"
    """
    logging.basicConfig(
        # Define the log level for externals (libs) loggers
        level=logging.ERROR,
        handlers=[
            # Write logs to file
            logging.FileHandler(f"logs/{datetime.now().strftime('%d-%m-%Y_%H:%M')}.log"),
            # Allow the logger to also log in console
            logging.StreamHandler(),
        ],
        format="%(asctime)s %(levelname)-8s %(name)-20s -> %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )
    
    if logging_level is None:
        logging_level = "DEBUG" if get_env_name() == "dev" else "INFO"

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    return logger