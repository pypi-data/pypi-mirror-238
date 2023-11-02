from abc import abstractmethod, ABCMeta
from functools import wraps
from warnings import filterwarnings

import MySQLdb
import pandas as pd

from quantit_snapshot.util.config_utils.config_getter import get_db_connect_info

filterwarnings('ignore', category=MySQLdb.Warning)


def handle_db_exception(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        self._connect()
        try:
            return f(self, *args, **kwargs)
        except Exception as e:
            print('Exception catched')
            if 'retry' in kwargs and kwargs['retry'] > 0:
                kwargs['retry'] -= 1
                print('Retry started, remain retry:', kwargs['retry'])
                return f(self, *args, **kwargs)
            elif 'failover' in kwargs and kwargs['failover'] is True:
                kwargs['failover'] = False
                print('Failover started')
                self.__do_failover()
                return f(self, *args, **kwargs)
            else:
                self._conn.rollback()
                raise e
        finally:
            self._cursor.close()
            self._conn.close()

    return wrapper


class DbConnUnit:
    def __init__(self, db_name, mode="w", database=None):
        self.__DB_NAME = db_name
        self.__MODE = mode
        self.__DATABASE = database

    def __do_failover(self):
        pass

    def _connect(self):
        self._conn = MySQLdb.connect(
            charset='utf8',
            **get_db_connect_info(self.__DB_NAME, self.__MODE, self.__DATABASE)
        )
        self._cursor = self._conn.cursor()

    def conn(self):
        return self._conn

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            try:
                self._conn.commit()
            except Exception as e:
                print(e)
                self._conn.rollback()
            finally:
                self._cursor.close()
                self._conn.close()
        else:
            self._conn.rollback()
            self._cursor.close()
            self._conn.close()

    @handle_db_exception
    def query(self, query, params=None, retry=0, failover=False):
        if params is not None:
            self._cursor.execute(query, params)
        else:
            self._cursor.execute(query)
        result = self._cursor.fetchall()
        return result

    @handle_db_exception
    def execute(self, query, params=None, retry=0, failover=False):
        if params is not None:
            self._cursor.execute(query, params)
        else:
            self._cursor.execute(query)

    @handle_db_exception
    def executemany(self, query, params=None, retry=0, failover=False):
        if params is not None:
            self._cursor.executemany(query, params)
        else:
            self._cursor.executemany(query)


class IDbHandle(metaclass=ABCMeta):
    @abstractmethod
    def get_df(self, table_name, condition):
        pass

    @abstractmethod
    def get_df_from_query(self, sql, select):
        pass


class DbHandle(DbConnUnit, IDbHandle):
    def __init__(self, db_name: str, mode="w", database=None):
        super(DbHandle, self).__init__(db_name, mode, database)

    def get_df(self, table_name, condition=None):
        df_columns = self.get_col(table_name)
        df = self.__get_df(table_name, df_columns, condition)
        return df

    def get_df_from_query(self, sql, select):
        table_rows = self.query(sql)
        df = pd.DataFrame(list(table_rows), columns=select)
        return df

    def get_col(self, table_name):
        sql = "SHOW COLUMNS FROM %s" % table_name
        column_info = self.query(sql)
        columns = [i[0] for i in column_info]
        return columns

    def __get_df(self, table_name, columns, condition):
        if not condition:
            sql = "SELECT * FROM %s" % table_name
        else:
            sql = "SELECT * FROM %s WHERE %s" % (table_name, condition)
        table_rows = self.query(sql)
        if table_rows:
            df = pd.DataFrame(list(table_rows), columns=columns)
        else:
            df = pd.DataFrame(columns=columns)
        return df
