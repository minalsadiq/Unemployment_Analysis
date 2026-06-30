"""
utils.py
Shared helper utilities: logging setup and generic helpers.
"""

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """
    Create (or retrieve) a configured logger instance.

    Parameters
    ----------
    name : str
        Name of the logger, usually __name__ of the calling module.

    Returns
    -------
    logging.Logger
        Configured logger writing to stdout.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def print_section(title: str) -> None:
    """Print a formatted section header to stdout for readable CLI output."""
    line = "=" * 70
    print(f"\n{line}\n{title}\n{line}")
