"""
Logging Configuration Function.

This function configures logging for the application by setting up three different loggers:
- Main logger for INFO level messages.
- debug_logger for DEBUG level messages.
- error_logger for ERROR level messages.

Log messages are saved in separate log files in the 'logs' directory.

Functions:
    - configure_logging(): Configures the logging settings.

Returns:
    None
"""


import logging


def configure_logging():
    """
    Log Configuration Function.

    This function configures logging for the application by setting up three different loggers:
    - Main logger for INFO level messages.
    - debug_logger for DEBUG level messages.
    - error_logger for ERROR level messages.

    Log messages are saved in separate log files in the 'logs' directory.

    Functions:
        - configure_logging(): Configures the logging settings.

    Returns:
        None
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [INFO] %(message)s',
        handlers=[
            logging.FileHandler('logs/info.log'),
        ]
    )

    debug_logger = logging.getLogger("debug_logger")
    debug_logger.setLevel(logging.DEBUG)
    debug_handler = logging.FileHandler('logs/debug.log')
    debug_handler.setLevel(logging.DEBUG)
    debug_formatter = logging.Formatter('%(asctime)s [DEBUG] %(message)s')
    debug_handler.setFormatter(debug_formatter)
    debug_logger.addHandler(debug_handler)

    error_logger = logging.getLogger("error_logger")
    error_logger.setLevel(logging.ERROR)
    error_handler = logging.FileHandler('logs/error.log')
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter('%(asctime)s [ERROR] %(message)s')
    error_handler.setFormatter(error_formatter)
    error_logger.addHandler(error_handler)
