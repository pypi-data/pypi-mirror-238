import logging
import os
import socket
import sys

logger = logging.getLogger()

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

BASE_DIR = os.path.expanduser(f"~/.quantit_snapshot/")


TEST = "test"
DEVELOPMENT = "development"
RESEARCH = "research"
REPORT = "report"
STAGING = "staging"
PRODUCTION = "production"

TESTING = any("pytest" in i or "setup.py" in i for i in sys.argv)
SNAPSHOT_PATH = os.environ.get("SNAPSHOT_PATH", None)
ENV = os.environ.get("ENV", "production").lower() if not TESTING else TEST
logger.error(f"""
************** RUNNING ENV: {ENV} argv: {sys.argv} *******************
- SNAPSHOT_PATH: {SNAPSHOT_PATH} 
"""
)


def _hostname_in_list(hostname, group: list):
    if not hostname:
        hostname = socket.gethostname()
    hostname = hostname.lower()
    return any(hostname.startswith(x) for x in group)


def is_test():
    return ENV.lower() == TEST


def is_dev():
    return ENV.lower() == DEVELOPMENT


def is_stage():
    return ENV.lower() == STAGING or socket.gethostname().lower() == "ksaslq001"


def is_research():
    return ENV.lower() == RESEARCH


def is_report():
    return ENV.lower() == REPORT


def is_prod():
    return ENV.lower() == PRODUCTION


def is_db_readonly():
    return is_research() or is_report() or DB_READ_ONLY


def is_use_staging_cache():
    return (
            is_dev()
            or is_test()
            or is_stage()
            or is_research()
            or is_report()
    )


DB_READ_ONLY = False if os.environ.get("DB_MODE", "") != "READ" else True
DB_NAME = "snapshot"
DB_HOST = os.environ.get("DB_HOST", "")  # production

DEBUG = True if is_dev() or is_test() else False

_LOG_LEVEL = {
    "test": "DEBUG",
    "development": "DEBUG",
    "production": "DEBUG",
}

log_level = _LOG_LEVEL[ENV.lower()]

# Scheduler
PROD_HOSTNAMES = []
CACHE_HOSTNAMES = []


def is_prod_server():
    return socket.gethostname().lower() in PROD_HOSTNAMES


SNAPSHOT_AWS_S3_KEY = os.environ.get("SNAPSHOT_AWS_S3_KEY", "")
SNAPSHOT_AWS_S3_SECRET_KEY = os.environ.get("SNAPSHOT_AWS_S3_SECRET_KEY", "")
if not SNAPSHOT_AWS_S3_KEY or not SNAPSHOT_AWS_S3_SECRET_KEY:
    logger.error(f"[ERROR] AWS KEY NOT LOADED!")
    logger.error("""[ERROR] Enter code snippet at the top of your script:
'''
from quantit_snapshot.base.setting import set_config
set_config("/your/env/path")
'''
    """)



FINTER_API_KEY = os.environ.get("FINTER_API_KEY", "")


bucket_postfix = "test" if is_use_staging_cache() else "production"

SNAPSHOT_S3_BUCKET = f"quanda-sm-{bucket_postfix}"
SNAPSHOT_S3_BUCKET_PRODUCTION = f"quanda-sm-production"
SNAPSHOT_S3_BUCKET_TEST = f"quanda-sm-test"
SNAPSHOT_S3_BUCKET_BACKUP = f"quanda-sm-backup"
SNAPSHOT_S3_BUCKET_CONFIG = "quanda-sm-config"
SNAPSHOT_S3_CODE_BUCKET = "quanda-sm-code"