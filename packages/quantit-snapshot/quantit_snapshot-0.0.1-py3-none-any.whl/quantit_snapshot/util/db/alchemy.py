import pandas as pd
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from quantit_snapshot.util.config.db.db import get_db_connect_info, DBConfigType
from quantit_snapshot.base.setting.settings import DB_NAME


class DBSess(object):
    def __init__(self, engine):
        self.__engine = engine

    def __enter__(self):
        self.__session = sessionmaker(self.__engine)()
        self.__session.autoflush = False
        return self.__session

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.__session.commit()
        except Exception as e:
            print(e)
            self.__session.rollback()
        finally:
            self.__session.close()
            self.__engine.dispose()

    @staticmethod
    def of(db_name):
        return DBSess(AlchemyUtils.load_engine(db_name))


class AlchemyUtils(object):
    engines = {}

    @staticmethod
    def _load_engine(db_name):
        db_url = get_db_connect_info(db_name, DBConfigType.URL)
        AlchemyUtils.engines[db_name] = create_engine(
            db_url,
            pool_recycle=3600,
            pool_pre_ping=True,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=20,
            encoding='utf-8'
        )

    @classmethod
    def __load_default_engine(cls):
        cls._load_engine(DB_NAME)

    @staticmethod
    def load_engine(db_name, **kwargs):
        AlchemyUtils.__load_default_engine()
        if db_name not in AlchemyUtils.engines:
            if "db_url" in kwargs:
                AlchemyUtils._load_engine(db_name, kwargs["db_url"])
            else:
                raise KeyError("'db_url' is required")
        return AlchemyUtils.engines[db_name]

    @staticmethod
    @contextmanager
    def make_session(engine) -> Session:
        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


class AlchemyToDF(object):
    @staticmethod
    def get_df(sess, table, columns=[], filter=None, groupby=[], suffix_fn=lambda x: x):
        def filter_expr(expr_, filter_):
            return expr_.filter(filter_)

        def groupby_expr(expr_, groupby_):
            if isinstance(groupby_[0], str):
                return expr_.group_by(*[getattr(table, col) for col in groupby])
            else:
                return expr_.group_by(*groupby_)

        expr = sess.query(table)

        if columns:
            if isinstance(columns[0], str):
                expr = sess.query(*[getattr(table, col) for col in columns])
            else:
                expr = sess.query(*columns)

        if filter is not None:
            expr = filter_expr(expr, filter)

        if groupby:
            expr = groupby_expr(expr, groupby)

        expr = suffix_fn(expr)

        return pd.read_sql(expr.statement, expr.session.bind)

