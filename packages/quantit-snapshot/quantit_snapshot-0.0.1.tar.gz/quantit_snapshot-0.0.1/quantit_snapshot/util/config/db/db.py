import json
import enum
from collections import defaultdict
from quantit_snapshot.base.setting.settings import (
    SNAPSHOT_S3_BUCKET_CONFIG,
    SNAPSHOT_AWS_S3_KEY,
    SNAPSHOT_AWS_S3_SECRET_KEY
)

from quantit_snapshot.util.cloud.aws.s3_quanda_ex import S3QuandaEx


class DBConfigType(enum.Enum):
    URL = "url"
    JSON = "json"


def make_db_config_as(conf, db_info):
    if conf == DBConfigType.JSON:
        return db_info
    elif conf == DBConfigType.URL:
        return f"mysql://{db_info['user']}:{db_info['password']}@{db_info['host']}:{db_info['port']}/{db_info['db']}"
    else:
        raise TypeError(
            "Invalid DBConfigType: DBConfigType.JSON and DBConfigType.URL are only allowed"
        )


def get_db_config_as(conf):
    if conf == DBConfigType.JSON:
        return "db/connect.json"
    elif conf == DBConfigType.URL:
        return "db/alchemy.json"
    else:
        raise TypeError("Invalid DBConfigType: DBConfigType.JSON and DBConfigType.URL are only allowed")


def _get_db_connect_info(config_type: DBConfigType):
    f_name = get_db_config_as(config_type)
    credit = json.loads(
        S3QuandaEx.get_data(
            f_name,
            SNAPSHOT_S3_BUCKET_CONFIG,
            SNAPSHOT_AWS_S3_KEY,
            SNAPSHOT_AWS_S3_SECRET_KEY
        )
    )
    return credit


def get_db_connect_info(db_name, config_type: DBConfigType):
    return _get_db_connect_info(config_type)[db_name]


def register_db_connect_info(db_name, db_info):
    credit_data = defaultdict(dict)

    try:
        for t in DBConfigType:
            credit_data[t.value] = _get_db_connect_info(t)
            assert db_name not in credit_data[t.value]
            conf_new = make_db_config_as(t, db_info)
            credit_data[t.value][db_name] = conf_new
    except AssertionError:
        raise AssertionError(f"{db_name} is already registered")
    for t in DBConfigType:
        S3QuandaEx.put_data(
            json.dumps(credit_data[t.value]),
            get_db_config_as(t),
            SNAPSHOT_S3_BUCKET_CONFIG,
            SNAPSHOT_AWS_S3_KEY,
            SNAPSHOT_AWS_S3_SECRET_KEY
        )
