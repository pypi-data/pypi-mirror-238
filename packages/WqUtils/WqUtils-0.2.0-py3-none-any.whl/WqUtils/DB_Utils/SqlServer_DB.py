#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@CreateTime: 2023-06-19 14:58
@Author: Stephen Wan
@Email: stephen.wan@colourdata.com.cn
@LastEditors: Stephen Wan
@LastEditTime: 2023-06-19 14:58
@FileName: SqlServer_DB.py
@ProjectName: nlp_project
@Description: 操作sqlserver数据库脚本
    1.优先读取环境变量中的数据库配置，如果没有读取本地默认的配置
    2.新建表，DataFrame数据直接输入到库中
"""
import os
import math
import toml
import pymssql


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


class ExecSql(object):
    """
    sql server 数据库操作封装
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
        self.user = self.sql_conf['USERNAME']
        self.pwd = self.sql_conf['PASSWORD']
        self.test_db = self.sql_conf['DB']


    def load_config(self):
        # 读取环境变量数据库信息如果有|直接使用，如果没有再读取本地配置文件
        if os.getenv("MSSQL_HOST", None):
            config = {"HOST": os.getenv("MSSQL_HOST"), "PORT": int(os.getenv(
                "MSSQL_PORT")), "USERNAME":
                os.getenv("MSSQL_USERNAME"), "PASSWORD": os.getenv("MSSQL_PASSWORD"),
                "DB": os.getenv("MSSQL_DB")}

        else:
            config = self.pymssql_config['sqlserver_database']
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
            self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd,
                                        charset="utf8")
        except Exception as e:
            print("连接mysql失败：{0}".format(e))

    def get_cursor(self):
        """
        获取游标
        :return:
        """
        self.cursor = self.conn.cursor()
        return self.cursor

    def exec_sql(self, sql_type, sql, *args):
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
            elif sql_type == 'update' or sql_type == 'del' or sql_type == 'insert' or sql_type == 'insert_many':
                self.connect_db()
                if sql_type == 'insert_many':
                    print(sql)
                    print(args)
                    result = self.get_cursor().executemany(sql, args[0])
                else:
                    result = self.get_cursor().execute(sql)
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            return result
        except Exception as e:
            print("sql类型或sql错误：{0}".format(e))

    def _create_table(self, table_name=None, fields_lst=None):
        confirm_fields = " nvarchar(max),".join(map(str, fields_lst)).strip(',') + " " \
                                                                                  "nvarchar(max)"
        confirm_fields = "t_id BIGINT PRIMARY KEY IDENTITY(1,1)," \
                          "create_time datetime DEFAULT CURRENT_TIMESTAMP,update_time " \
                         "datetime DEFAULT CURRENT_TIMESTAMP," + confirm_fields
        table_template = """IF OBJECT_ID(N'{0}', 'U') IS NULL
                    BEGIN
                        create table {0}
                        ({1})
                    END;""".format(table_name, confirm_fields)

        self.exec_sql("insert", table_template)

    def _df_trans_sql(self, table_name=None, df_data=None):
        columns = df_data.columns.tolist()  # 表字段
        # columns = [f"N'{i}'" for i in columns]
        values = df_data.values.tolist()  # 表字段对应的值
        table_name = f"[{self.test_db}].[dbo].[{table_name}]"
        self._create_table(table_name, columns)

        tmp = []
        for v in values:
            value = [str(s).replace("'", "''") for s in v]
            tmp.append("('" + "','".join(value) + "')")
        SQL = '''INSERT INTO {0}({1}) VALUES {2};'''.format(table_name, ','.join(columns),
                                                     ','.join(tmp))
        SQL = SQL.replace('%', '%%')  # 特殊字符转换
        return SQL

    def _df_trans_sql_many(self, table_name=None, df_data=None):
        """"使用execute many 大量插入数据"""
        columns = df_data.columns.tolist()  # 表字段
        columns_type = ','.join(['%s' for i in range(len(columns))])
        # columns = [f"N'{i}'" for i in columns]
        values = df_data.values.tolist()  # 表字段对应的值
        table_name = f"[{self.test_db}].[dbo].[{table_name}]"
        self._create_table(table_name, columns)

        tmp = []
        for v in values:
            value = [str(s).replace("'", "''") for s in v]
            tmp.append(tuple(value))
        SQL = '''INSERT INTO {0}({1}) VALUES ({2});'''.format(table_name, ','.join(columns),
                                                            columns_type)

        # SQL = SQL.replace('%', '%%')  # 特殊字符转换
        return SQL, tmp

    def df_insert(self, table_name=None, df_data=None, batch_size=1000):

        total_len = len(df_data)
        epochs = math.ceil(total_len / batch_size)
        for idx in range(epochs):
            batch_df = df_data[idx * batch_size: min((idx + 1) * batch_size, total_len)]
            # sql, temp_data = self._df_trans_sql_many(table_name, batch_df)
            sql = self._df_trans_sql(table_name, batch_df)
            self.exec_sql("insert", sql)


if __name__ == "__main__":
    pass
    import os
    import pandas as pd

    # sql server 数据库连接
    os.environ['MSSQL_HOST'] = '123.57.241.126'
    os.environ['MSSQL_PORT'] = "1433"
    os.environ['MSSQL_USERNAME'] = 'wanqiang'
    os.environ['MSSQL_PASSWORD'] = 'wq2022'
    os.environ['MSSQL_DB'] = 'e_commerce_goods_test'
    exec_instance = ExecSql()
    data = exec_instance.exec_sql('select', """select top 1000 sku_name,spu_id,sku_id
from [e_commerce_goods_test].[dbo].[yili_guonei_comment_feature_extraction_0825]""")
    # exec_instance.df_insert(table_name="sql_server_test", df_data=df1)
    data_df = pd.DataFrame(data, columns=['sku_name', 'spu_id', 'sku_id'])
    exec_instance.df_insert(table_name="yili_guonei_comment_backup", df_data=data_df)
