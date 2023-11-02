import os

from quantit_snapshot.util.db.orm.snapshot import Snapshot as sh
from quantit_snapshot.util.cloud.aws.s3_quanda_ex import S3QuandaEx
from quantit_snapshot.util.config.log.log import get_logger
from quantit_snapshot.base.setting.settings import (
    SNAPSHOT_AWS_S3_KEY, SNAPSHOT_AWS_S3_SECRET_KEY,
    SNAPSHOT_S3_BUCKET
)
from quantit_snapshot.util.db.alchemy import AlchemyUtils, DBSess

LOGGER = get_logger()


class SmHelper:
    @staticmethod
    def load(object_name):
        return S3QuandaEx.get_data(
            object_name,
            SNAPSHOT_S3_BUCKET,
            SNAPSHOT_AWS_S3_KEY,
            SNAPSHOT_AWS_S3_SECRET_KEY
        )

    @staticmethod
    def put(object_name, data):
        return S3QuandaEx.put_data(
            data,
            object_name,
            SNAPSHOT_S3_BUCKET,
            SNAPSHOT_AWS_S3_KEY,
            SNAPSHOT_AWS_S3_SECRET_KEY
        )

    @staticmethod
    def delete(object_name):
        S3QuandaEx.delete_file(
            object_name,
            SNAPSHOT_S3_BUCKET,
            SNAPSHOT_AWS_S3_KEY,
            SNAPSHOT_AWS_S3_SECRET_KEY
        )

    @staticmethod
    def getsize(object_name):
        return S3QuandaEx.get_size(
            object_name,
            SNAPSHOT_S3_BUCKET,
            SNAPSHOT_AWS_S3_KEY,
            SNAPSHOT_AWS_S3_SECRET_KEY
        )

    @staticmethod
    def get_obj_list(prefix):
        obj_list = S3QuandaEx.get_obj_list(
            prefix,
            SNAPSHOT_S3_BUCKET,
            SNAPSHOT_AWS_S3_KEY,
            SNAPSHOT_AWS_S3_SECRET_KEY
        )
        if obj_list is None:
            obj_list = []
        return obj_list

    @staticmethod
    def upload_file(obj_name, local_path):
        S3QuandaEx.upload_file(
            local_path,
            obj_name,
            SNAPSHOT_S3_BUCKET,
            SNAPSHOT_AWS_S3_KEY,
            SNAPSHOT_AWS_S3_SECRET_KEY
        )

    @staticmethod
    def download_file(obj_name, local_path):
        dirpath = os.path.dirname(local_path)
        os.makedirs(dirpath, exist_ok=True)
        S3QuandaEx.download_file(
            local_path,
            obj_name,
            SNAPSHOT_S3_BUCKET,
            SNAPSHOT_AWS_S3_KEY,
            SNAPSHOT_AWS_S3_SECRET_KEY
        )

    @staticmethod
    def delete_file(obj_name):
        S3QuandaEx.delete_file(
            obj_name,
            SNAPSHOT_S3_BUCKET,
            SNAPSHOT_AWS_S3_KEY,
            SNAPSHOT_AWS_S3_SECRET_KEY
        )


class SmData(SmHelper):
    @staticmethod
    def load(object_name):
        return SmHelper.load(object_name)

    @staticmethod
    def update(object_name, data):
        engine = AlchemyUtils.load_engine("snapshot")
        with AlchemyUtils.make_session(engine) as sess:
            assert sh.exists(object_name)

        return SmHelper.put(
            object_name=object_name, data=data
        )

    @staticmethod
    def delete(object_name):
        SmHelper.delete_file(object_name)

    @staticmethod
    def getsize(object_name):
        return SmHelper.getsize(object_name)

    @staticmethod
    def get_obj_list(prefix):
        obj_list = SmHelper.get_obj_list(prefix)
        if obj_list is None:
            obj_list = []
        return obj_list

    @staticmethod
    def upload_file(obj_name, local_path):
        SmHelper.upload_file(
            obj_name=obj_name,
            local_path=local_path
        )

    @staticmethod
    def download_file(obj_name, local_path):
        SmHelper.download_file(
            obj_name=obj_name, local_path=local_path
        )

    @staticmethod
    def delete_file(obj_name):
        SmHelper.delete_file(obj_name)
