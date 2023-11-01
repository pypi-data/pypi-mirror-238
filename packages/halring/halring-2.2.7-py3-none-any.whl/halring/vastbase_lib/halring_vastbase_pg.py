# -*- coding:utf-8 -*-
import psycopg2
import psycopg2.extras


class VastBaseUtil(object):

    def __int__(self, database, user, password, host, port=5432):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect_vastbase(self):
        return psycopg2.connect(database=self.database, user=self.user,
                                     password=self.password, host=self.host, port=self.port)

    def query(self, sql):
        """ 查询 """
        conn = self.connect_vastbase()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql)
        records = cursor.fetchall()
        conn.close()
        dict_records = [dict(x) for x in records]
        return dict_records

    def execute_sql(self, sql):
        """ 增删改 """
        conn = self.connect_vastbase()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

