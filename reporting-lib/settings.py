import logging

LOG_FUNCTIONS_TO_PATCH = [
    logging.debug,
    logging.info,
    logging.error,
    logging.critical,
    logging.exception,
]
