#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@CreateTime: 2023-06-21 10:29
@Author: Stephen Wan
@Email: stephen.wan@colourdata.com.cn
@LastEditors: Stephen Wan
@LastEditTime: 2023-06-21 10:29
@FileName: ExecPgSql.py
@ProjectName: nlp_project
@Description:
"""
import os
import math
import toml
import psycopg2
import pandas as pd
from io import StringIO


class TomlConfig:

    def __init__(self, toml_filename):
        self.t_dict = dict()  # 创建空字典
        self.toml_file_path = os.path.join(os.path.dirname(__file__), toml_filename)

    def update(self, t_data):
        # 给toml文件添加配置
        self.t_dict.update(t_data)
        return self.t_dict

    def write(self, t_data):
        # 写入到toml文件
        with open(self.toml_file_path, "w", encoding="utf-8") as fs:
            toml.dump(t_data, fs)

    def read(self):
        # 读取toml文件
        with open(self.toml_file_path, "r", encoding="utf-8") as fs:
            t_data = toml.load(fs)
        return t_data

    def read_str(self, s_data):
        # 从字符串中解析TOML，返回一个字典对象或类的实例对象
        t_data = toml.loads(s_data, _dict=dict)
        return t_data

    def read_dict(self, dict):
        # 将字典对象格式化成toml字符串
        t_data = toml.dumps(dict)
        return t_data


class ExecPgSql(object):
    """
    Pg SQL数据库操作封装
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        初始化mysql配置
        :param platform_name:
        """
        self.pymssql_config = TomlConfig('db_config.toml').read()
        self.sql_conf = self._get_sql_conf()
        self.host = self.sql_conf['HOST']
        self.port = self.sql_conf['PORT']
        self.user = self.sql_conf['USERNAME']
        self.pwd = self.sql_conf['PASSWORD']
        self.test_db = self.sql_conf['DB']
        self.options = self.sql_conf['OPTIONS']

    def load_config(self):
        # 读取环境变量数据库信息如果有|直接使用，如果没有再读取本地配置文件
        if os.getenv("PG_HOST", None):
            config = {"HOST": os.getenv("PG_HOST"), "PORT": int(os.getenv(
                "PG_PORT")), "USERNAME":
                os.getenv("PG_USERNAME"), "PASSWORD": os.getenv("PG_PASSWORD"),
                "DB": os.getenv("PG_DB"), "OPTIONS": os.getenv("PG_OPTIONS")}

        else:
            config = self.pymssql_config['pg_database']
        return config

    def _get_sql_conf(self):
        """
        获取mysql配置
        :param platform_name:
        :return:
        """
        try:
            confirm_config = self.load_config()
            return confirm_config
        except Exception as e:
            print("找不到对应项目：sql server配置")

    def connect_db(self):
        """
        连接mysql
        :return:
        """
        try:
            self.conn = psycopg2.connect(host=self.host, port=None, user=self.user,
                                         password=self.pwd, database=self.test_db,
                                         options="-c search_path=dbo,public")
        except Exception as e:
            print("连接mysql失败：{0}".format(e))

    def get_cursor(self):
        """
        获取游标
        :return:
        """
        self.cursor = self.conn.cursor()
        return self.cursor

    def exec_sql(self, sql_type, sql):
        """
        执行sql语句
        :param sql_type:
        :param sql:
        :return:
        """
        # self.sql_conf = self._get_sql_conf()
        try:
            result = None
            if sql_type == 'select_one':
                self.connect_db()
                cursor = self.get_cursor()
                cursor.execute(sql)
                result = cursor.fetchone()
            elif sql_type == 'select':
                self.connect_db()
                cursor = self.get_cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
            elif sql_type == 'update' or sql_type == 'del' or sql_type == 'insert':
                self.connect_db()
                result = self.get_cursor().execute(sql)
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            return result
        except Exception as e:
            print("sql类型或sql错误：{0}".format(e))

    def _create_table(self, table_name=None, fields_lst=None, table_id=None):
        if table_id:
            confirm_fields = " varchar,".join(map(str, fields_lst)).strip(',') + " " \
                                                                                 "varchar"
            confirm_fields = "t_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY," \
                             "create_time TIMESTAMP DEFAULT current_timestamp," \
                             "update_time " \
                             "TIMESTAMP DEFAULT current_timestamp," + confirm_fields
        else:
            confirm_fields = " varchar,".join(map(str, fields_lst)).strip(',') + " " \
                                    "varchar"
            confirm_fields = "create_time TIMESTAMP DEFAULT current_timestamp,update_time " \
                             "TIMESTAMP DEFAULT current_timestamp," + confirm_fields
        table_template = """create table IF NOT EXISTS {0} ({1});""".format(table_name,
                                                                            confirm_fields)

        self.exec_sql("insert", table_template)

    def _df_trans_sql(self, table_name=None, df_data=None, table_id=None):
        df_data = df_data.fillna('')
        columns = df_data.columns.tolist()  # 表字段
        columns = [f'"{i}"' for i in columns]
        values = df_data.values.tolist()  # 表字段对应的值
        table_name = f'"{self.test_db}".{self.options}."{table_name}"'
        self._create_table(table_name, columns, table_id)

        tmp = []
        for v in values:
            value = [str(s).replace("'", "''") for s in v]
            tmp.append("('" + "','".join(value) + "')")
        SQL = '''INSERT INTO {0}({1}) VALUES {2};'''.format(table_name, ','.join(columns),
                                                            ','.join(tmp))
        SQL = SQL.replace('%', '%%')  # 特殊字符转换
        return SQL

    def _copy_from(self, table_name=None, df_data=None, table_id=None):
        df_data = df_data.fillna('')
        columns = df_data.columns.tolist()  # 表字段
        columns = [f'"{i}"' for i in columns]
        values = df_data.values.tolist()  # 表字段对应的值
        table_name = f'"{self.test_db}".{self.options}."{table_name}"'
        self._create_table(table_name, columns, table_id)
        values_column = ['\t'.join(map(str, column)) for column in values]
        values_row = '\n'.join(values_column)

        self.connect_db()
        cursor = self.get_cursor()
        try:
            cursor.copy_from(StringIO(values_row), table_name.split('.')[-1].strip('"'),
                         null='',
                         columns=[i.strip('"') for i in columns])
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            cursor.close()
            self.conn.close()

    def df_insert(self, table_name=None, df_data=None, batch_size=10000,
                  copy_from=False, id_flag=False):
        total_len = len(df_data)
        epochs = math.ceil(total_len / batch_size)
        for idx in range(epochs):
            batch_df = df_data[idx * batch_size: min((idx + 1) * batch_size, total_len)]
            if copy_from:
                self._copy_from(table_name, batch_df, id_flag)
            else:
                batch_sql = self._df_trans_sql(table_name, batch_df, id_flag)
                self.exec_sql("insert", batch_sql)


if __name__ == "__main__":
    pass
    pg_instance = ExecPgSql()
    sql_temp = """select * from category_test0531 limit 10;"""
    a = pg_instance.exec_sql("select", sql_temp)

    df1 = pd.read_excel("../../UnitTest/5月份规则接口输出品类检查.xlsx")[:3]
    pg_instance.df_insert(table_name="pg_test_wq", df_data=df1, copy_from=False,
                          id_flag=True)
