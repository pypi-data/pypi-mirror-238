import logging
from os import environ
from dotenv import load_dotenv


def set_config(path):
    load_dotenv(path)
    for v in [
        "ENV",
        "SNAPSHOT_AWS_S3_KEY",
        "SNAPSHOT_AWS_S3_SECRET_KEY"
    ]:
        env = environ.get(v, None)
        if env is None:
            logging.warning(f"{v} doesn't set.")