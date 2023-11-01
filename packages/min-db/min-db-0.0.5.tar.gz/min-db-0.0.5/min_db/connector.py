from typing import Optional

import oracledb
from mysql.connector import pooling

from min_db.mapper import Mapper
from min_db.types import DB_INFO, DB_TYPE


class Connector:
    def __init__(self, db_type: str, ip: str, port: int, user: str, query_path: str,
                 password: str, db: str | None = None, sid: str | None = None, dsn: str | None = None,
                 session_pool_min: int = 2, session_pool_max: int = 5):
        if db_type == DB_TYPE.ORACLE:
            if sid is None:
                raise AttributeError("sid must be defined on oracle")
        if db_type == DB_TYPE.MYSQL:
            if db is None:
                raise AttributeError("db must be defined on oracle")
        self._db_info = DB_INFO(type=db_type, sid=sid, db=db, user=user,
                                password=password, ip=ip, port=port,
                                session_pool_min=session_pool_min, session_pool_max=session_pool_max)
        self._mapper = Mapper(path=query_path)
        self._session_pool: oracledb.SessionPool | pooling.MySQLConnectionPool | None = None
        self._chunk_cursor = None
        self._chunk_conn = None

        if db_type == DB_TYPE.ORACLE:
            if dsn in None:
                self._dsn = oracledb.makedsn(host=ip, port=port, sid=sid)
            else:
                self._dsn = dsn
            self._session_pool = oracledb.SessionPool(user=user, password=password, dsn=self._dsn,
                                                      min=session_pool_min, max=session_pool_max,
                                                      increment=1, encoding="UTF-8")
        elif db_type == DB_TYPE.MYSQL:
            self._session_pool = pooling.MySQLConnectionPool(pool_name="pool_mysql",
                                                             pool_size=session_pool_max,
                                                             pool_reset_session=True,
                                                             host=ip,
                                                             port=port,
                                                             database=db,
                                                             user=user,
                                                             password=password)

    def connection_test(self) -> None:
        try:
            if self._db_info.type == DB_TYPE.MYSQL:
                test_connection = self._session_pool.get_connection()
                print(test_connection.get_server_info())
                test_connection.close()
            elif self._db_info.type == DB_TYPE.ORACLE:
                test_connection = self._session_pool.acquire()
                self._session_pool.release(test_connection)
        except Exception as exc:
            raise exc
        else:
            print("success")

    def select_one(self, namespace: str, query_id: str, param: Optional[dict] = None):
        query = self._mapper.get_query(namespace, query_id, param)
        print(query)
        if self._db_info.type == DB_TYPE.MYSQL:
            connection_obj = self._session_pool.get_connection()
            cursor = connection_obj.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            connection_obj.close()
            return result
            # with self._session_pool.get_connection() as connection_obj:
            #     cursor = connection_obj.cursor()
            #     cursor.execute(query)
            #     result = cursor.fetchone()
            #     cursor.close()
            #     return result
        elif self._db_info.type == DB_TYPE.ORACLE:
            with self._session_pool.acquire() as connection_obj:
                cursor = connection_obj.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                cursor.close()
                return result

    def select(self, namespace: str, query_id: str, param: Optional[dict] = None):
        query = self._mapper.get_query(namespace, query_id, param)
        print(query)
        if self._db_info.type == DB_TYPE.MYSQL:
            connection_obj = self._session_pool.get_connection()
            cursor = connection_obj.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection_obj.close()
            return result
            # with self._session_pool.get_connection() as connection_obj:
            #     cursor = connection_obj.cursor()
            #     cursor.execute(query)
            #     result = cursor.fetchall()
            #     cursor.close()
            #     return result
        elif self._db_info.type == DB_TYPE.ORACLE:
            with self._session_pool.acquire() as connection_obj:
                cursor = connection_obj.cursor()
                result = cursor.execute(query)
                result = result.fetchall()
                cursor.close()
                return result

    def set_chunk_prefetch(self, namespace: str, query_id: str, param: Optional[dict] = None,
                           prefetch_row: Optional[int] = None, array_size: Optional[int] = None) -> None:
        if self._db_info.type != DB_TYPE.ORACLE:
            raise AttributeError("prefetch api only available in oracle")
        else:
            self._chunk_conn = self._session_pool.acquire()
            self._chunk_cursor = self._chunk_conn.cursor()
            if prefetch_row is not None:
                self._chunk_cursor.prefetchrows = prefetch_row
            if array_size is not None:
                self._chunk_cursor.arraysize = array_size
            query = self._mapper.get_query(namespace, query_id, param)
            print(query)
            self._chunk_cursor.execute(query)

    def select_chunk(self) -> list:
        if self._chunk_cursor is not None:
            cursor = self._chunk_cursor
            while True:
                results = cursor.fetchmany(numRows=self._chunk_cursor.arraysize)
                if not results:
                    cursor.close()
                    self._session_pool.release(self._chunk_conn)
                    self._chunk_cursor = None
                    self._chunk_conn = None
                    yield []
                    break
                yield results

    def execute(self, namespace: str, query_id: str, param: dict = None):
        query = self._mapper.get_query(namespace, query_id, param)
        print(query)
        if self._db_info.type == DB_TYPE.ORACLE:
            with self._session_pool.acquire() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                print("commit: ", cursor.rowcount)
                cursor.close()
                return
        elif self._db_info.type == DB_TYPE.MYSQL:
            connection_obj = self._session_pool.get_connection()
            cursor = connection_obj.cursor()
            cursor.execute(query)
            connection_obj.commit()
            print("commit: ", cursor.rowcount)
            cursor.close()
            connection_obj.close()
            return
            # with self._session_pool.get_connection() as conn:
            #     cursor = conn.cursor()
            #     cursor.execute(query)
            #     conn.commit()
            #     print("commit: ", cursor.rowcount)
            #     cursor.close()
            #     return
