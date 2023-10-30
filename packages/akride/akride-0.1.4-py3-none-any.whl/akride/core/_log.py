"""
 Copyright (C) 2023, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""
import logging
import logging.config

import yaml


class PPrintFormatter(logging.Formatter):
    """Logging Formatter resembling pprint format"""

    def __init__(self, fmt: str, *args, **kwargs):
        super().__init__(fmt=fmt, *args, **kwargs)

    def format(self, record):
        message = super().format(record)
        message = message.replace("(asctime)", "")
        message = message.replace("(levelname)", "")
        return message


def get_logger(module: str, config_file_path):
    logger = logging.getLogger(module)

    try:
        with open(config_file_path, "r") as file:
            config = yaml.safe_load(file.read())
            logging.config.dictConfig(config)
    except Exception:
        if config_file_path:
            logging.warning(
                f"Failed to create logger using the "
                f"config file {config_file_path}"
            )
        stream_handler = logging.StreamHandler()
        logger.addHandler(stream_handler)

        logger.info(
            "No config found for logger. Redirecting to Standard output!"
        )

    return logger
