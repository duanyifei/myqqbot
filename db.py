# coding:utf8
import copy
import json
import datetime
from collections import OrderedDict

import sqlite3
import pymysql


class SqliteDb(object):
    def __init__(self, database):
        """

        :param db: db文件地址
        :param kwargs:
        """
        self.db = sqlite3.connect(database)
        self.cursor = self.db.cursor()
        pass

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def close(self):
        self.cursor.close()
        self.db.close()

    def handle_values(self, data):
        """
        处理字典中的值 转换为mysql接受的格式
        :param data:
        :return: OrderedDict
        """
        keys = []
        values = []
        for k, v in data.items():
            keys.append("`{}`".format(k))
            if isinstance(v, str):
                v = v.strip()
                values.append("'{}'".format(pymysql.escape_string(v)))
            elif isinstance(v, (int, float)):
                values.append("{}".format(v))
            elif isinstance(v, (datetime.date, datetime.time)):
                values.append("'{}'".format(v))
            elif v is None:
                values.append("null")
            else:
                v = json.dumps(v, ensure_ascii=False)
                values.append("'{}'".format(pymysql.escape_string(v)))
        data = OrderedDict(zip(keys, values))
        return data

    def add(self, data, table_name="", ignore_duplicate=1, **kwargs):
        """
        保存数据
        :param data: 数据
        :param table_name: 表名
        :param ignore_duplicate: 忽略重复错误
        :param kwargs:
        :return:
        """
        data = copy.deepcopy(data)
        if not table_name:
            raise ValueError("table name {}".format(table_name))
        if not data:
            raise ValueError("data is {}".format(data))
        sql = "insert into {table_name} ({keys}) values({values});"
        # 拼接sql
        order_data = self.handle_values(data)
        sql = sql.format(
            **{
                "keys": ",".join(order_data.keys()),
                "values": ",".join(order_data.values()),
                "table_name": table_name,
            }
        )
        try:
            self.cursor.execute(sql)
            self.db.commit()
            resp = 0
        except Exception as e:
            if ignore_duplicate and "Duplicate entry" in str(e):
                print(e)
                resp = 1
            else:
                raise e
        return resp


default_db = SqliteDb("data.db")

if __name__ == '__main__':
    # database = "data.db"
    # sb = SqliteDb(database)

    # default_db.add()
    pass



