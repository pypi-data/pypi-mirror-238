import os
import subprocess

import git
from git.exc import InvalidGitRepositoryError, NoSuchPathError, GitCommandError

from quantit_snapshot.util.db.orm.snapshot import Snapshot as sh
from quantit_snapshot.util.cloud.aws.s3_quanda_ex import S3QuandaEx
from quantit_snapshot.util.config.log.log import get_logger
from quantit_snapshot.util.db.alchemy import AlchemyUtils, DBSess
from quantit_snapshot.base.setting.settings import (
    SNAPSHOT_AWS_S3_KEY, SNAPSHOT_AWS_S3_SECRET_KEY,
    SNAPSHOT_S3_BUCKET, SNAPSHOT_S3_CODE_BUCKET
)

LOGGER = get_logger()


def register(sess, snapshot_info, snapshot_meta=None):
    assert all(
        [
            c in sh.__table__.c for c in snapshot_info.keys()
        ]
    )
    try:
        assert not sh.exists(sess, str(sh(**snapshot_info))), "Model already registered."
    except TypeError:
        raise TypeError("Info based on name structure is needed. ('service', 'source', 'category', 'name')")
    sess.add(sh(**snapshot_info))


def delete(snapshot_name):
    engine = AlchemyUtils.load_engine("snapshot")
    with AlchemyUtils.make_session(engine) as sess:
        info = dict(zip(sh.NAME_STRUCT, snapshot_name.split(".")))
        assert sh.exists(sess, str(sh(**info))), "Model not existed."
        sess.query(sh).filter_by(**info).delete()
        sess.commit()

    S3QuandaEx.delete_file(
        snapshot_name,
        SNAPSHOT_S3_BUCKET,
        SNAPSHOT_AWS_S3_KEY,
        SNAPSHOT_AWS_S3_SECRET_KEY
    )


class GitNotInstalledError(Exception):
    def __init__(self, message="Git is not installed on your system."):
        self.message = message
        super().__init__(self.message)


class GitHelper:
    def __init__(self, snapshot_info, folder=None):
        self.snapshot_path = os.getenv("SNAPSHOT_PATH")
        try:
            self.repo = git.Repo(self.snapshot_path)
        except (InvalidGitRepositoryError, NoSuchPathError):
            self.repo = git.Repo.init(self.snapshot_path)
        finally:
            self.origin = self.connect_remote()

        self.snapshot_info = snapshot_info
        self.folder = folder

    def connect_remote(self):
        try:
            return self.repo.create_remote('origin', url="http://gitlab.quantit.io/quanda/snapshot.git")
        except GitCommandError:
            return self.repo.remote('origin')

    def pull_subdir(self, service):
        try:
            subprocess.run(
                ['git', 'config', 'core.sparseCheckout', 'true'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
        except subprocess.CalledProcessError:
            raise GitNotInstalledError()
        self.origin.fetch()
        self.repo.git().checkout("origin/master", "--", service)

    @staticmethod
    def is_git_installed():
        try:
            subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except subprocess.CalledProcessError:
            raise GitNotInstalledError()

    def code_status(self):
        log = self.repo.git.log('--stat', max_count=3)
        status = self.repo.git.status()
        return log + status

    def merge_commit(self):
        def _add_commit_push():
            self.repo.git.add(self.folder)
            self.repo.index.commit(self.folder)
            self.repo.git.merge("origin/master", strategy="recursive", no_ff=True)
            self.repo.git.push()

        assert self.folder is not None, "To submit code, `folder` is needed"
        _add_commit_push()
        return True

    def check_diff_and_merge(self):
        msg = f"""The code you submitted currently has the following differences. 
        
        {self.code_status()}
        
        Do you want to submit? [y/N] 
        """

        if input(msg) == 'y':
            return self.merge_commit()
        return -1


def submit_snapshot(
        snapshot_info: dict,
        folder: str
):
    def _is_resubmit():
        return input("Snapshot already registered. Do you want to resubmit? [y/N]") == 'y'

    engine = AlchemyUtils.load_engine("snapshot")
    with AlchemyUtils.make_session(engine) as sess:
        try:
            register(sess, snapshot_info)
            sess.commit()
        except AssertionError as assert_err:
            if _is_resubmit():
                pass
            else:
                raise assert_err
        except Exception as e:
            sess.rollback()
            raise e

    LOGGER.info(f'Snapshot Registered: {snapshot_info}')

    user_git = GitHelper(snapshot_info, folder)
    snapshot_path = user_git.snapshot_path
    if GitHelper.is_git_installed():
        LOGGER.info("[START] Push commit to git")
        res = user_git.check_diff_and_merge()
        if res:
            LOGGER.info("[END] Push commit to git")
        else:
            LOGGER.info("[END] Push commit Failed")
    else:
        LOGGER.info("Git is not installed on your system. the code version is not saved.")
        raise GitNotInstalledError()
