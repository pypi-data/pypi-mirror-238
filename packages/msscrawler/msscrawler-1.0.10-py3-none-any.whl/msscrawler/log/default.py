import logging
import os

from graypy import GELFTLSHandler


def get_default_log(instance_name):
    logger = logging.getLogger(f"crawling_{instance_name}_log")
    logger.setLevel(logging.INFO)

    handler = GELFTLSHandler(os.getenv("GRAYLOG_ADDR"), 12201)
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler())
    return logger
