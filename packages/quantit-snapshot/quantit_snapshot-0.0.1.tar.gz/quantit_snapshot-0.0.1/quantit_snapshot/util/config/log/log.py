import logging
import logging.handlers
import inspect
from os import path, makedirs, getpid
from datetime import datetime

from quantit_snapshot.base.setting.settings import log_level

__loggers = {}


def get_logger(level=None, is_save_file=True, base_path=None):
    level = level or log_level
    global __loggers
    caller_f_name = path.abspath(inspect.stack()[-1].filename)
    if __loggers.get(caller_f_name):
        return __loggers.get(caller_f_name)
    else:
        now_str = datetime.now().strftime("%Y%m%d.%H%M%S")

        log_format = '[%(levelname)s|%(pathname)s:%(lineno)s] %(asctime)s > %(message)s'

        logger = logging.getLogger(caller_f_name)
        logger.setLevel(getattr(logging, level))
        logger.propagate = 0

        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter(log_format))
        logger.addHandler(ch)

        if is_save_file and base_path:
            log_path = base_path + path.join(
                caller_f_name.replace(base_path, '').replace('.py', ''),
                '%s.%s.log' % (now_str, getpid())
            )
            if not path.exists(path.dirname(log_path)):
                makedirs(path.dirname(log_path))

            logger.debug("log func.py saved: %s" % log_path)

            fileMaxByte = 1024 * 1024 * 100  # 100MB
            fh = logging.handlers.RotatingFileHandler(log_path, maxBytes=fileMaxByte, backupCount=10)
            fh.setFormatter(logging.Formatter(log_format))
            logger.addHandler(fh)

        __loggers[caller_f_name] = logger
        return logger
