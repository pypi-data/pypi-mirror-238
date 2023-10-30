# -*- coding:utf-8 -*-

"""
读写数据库clickhouse
"""
from typing import List

from clickhouse_driver import Client
import pandas as pd
from .utils import *

class ClickhouseClient:
    """ 读写clickhouse数据库 """
    def __init__(self, host='', port=0, user='', password='', database=''):
        """ 初始化 """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

        self.connection= None

    def connect(self):
        """ 连接到server上的某个数据库 """
        # 使用提供的参数或默认值
        # db_name = db_name
        # 创建 ClickHouse 客户端并建立连接
        self.connection = Client(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        if not self.is_connected():
            raise Exception('can not connect to server, please check your login info.')

    @property
    def current_database(self):
        return self.connection.execute("SELECT currentDatabase()")[0][0]

    def is_connected(self):
        """ 是否连接到数据库 """
        if self.connection is None:
            return False
        else:
            return True

    def use_db(self, db_name):
        """ 使用某个数据库 """
        self.connection.execute(f"USE {db_name}")

    def is_db_existed(self, db_name):
        """ 数据库是否存在 """
        databases = self.connection.execute("SHOW DATABASES")
        return db_name in [db[0] for db in databases]

    def is_table_existed(self, table_name):
        """ 表是否存在 """
        tables = self.connection.execute(f"SHOW TABLES FROM {self.current_database}")
        return table_name in [table[0] for table in tables]

    def excu(self, sql_script):
        """ 执行sql语句 """
        return self.connection.execute(sql_script)

    def create_db(self, db_name):
        """ 创建数据库 """
        sql_script = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        self.connection.execute(sql_script)

    def create_table(self, sql_script, db_name = None):
        """ 创建表 """
        # 这里我们假设一个简单的表结构，真实使用中需要具体的字段和数据类型
        if db_name is not None:
            self.use_db(db_name)
        self.connection.execute(sql_script)

    def read_schema(self, table_name):
        """
        读取表的字段类型
        struct as --> name : type 
        """
        data = self.connection.execute(f"DESCRIBE TABLE {table_name}")
        schema = {}
        for record in data:
            schema[record[0]] =record[1]
        return schema

    def async_insert_df(self, df, table_name):
        """ 异步插入 DataFrame 数据 """
        insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) SETTINGS async_insert=1, wait_for_async_insert=1 VALUES"
        self.connection.execute(insert_query, df.to_dict("records"))

    def insert_df(self, df, table_name):
        """ 同步插入 DataFrame 数据"""
        insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES"
        self.connection.execute(insert_query, df.to_dict("records"))

    def read_df(self, sql_query):
        """ 读取数据 """
        # query样例：query = "SELECT * FROM your_table WHERE your_condition"
        results = self.connection.execute(sql_query, with_column_types=True)
        data, column_types = results
        columns = [column[0] for column in column_types]
        df = pd.DataFrame(data, columns=columns)
        return df

    def update_data(self, table_name, data, condition):
        """ 更新数据 """
        updates = ', '.join([f"{key} = '{value}'" for key, value in data.items()])
        self.connection.execute(f"ALTER TABLE {table_name} UPDATE {updates} WHERE {condition}")

    def add_column(self, table_name, column_name, column_type):
        """ 添加列 """
        self.connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")

    def delete_column(self, table_name, column_name):
        """ 删除列 """
        self.connection.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name}")

    def exists(self, table_name):
        """ 表是否存在 """
        pass

    def list_dbs(self):
        """ 列出所有数据库 """
        return [db[0] for db in self.connection.execute("SHOW DATABASES")]

    def list_tables(self, db_name = None):
        """ 列出所有表 """
        db_name = db_name or self.current_database
        return [table[0] for table in self.connection.execute(f"SHOW TABLES FROM {db_name}")]

    def table_size(self, db_name, table_name):
        """ 获取表大小 """
        query = f"SELECT COUNT(*) FROM {db_name}.{table_name}"
        return self.connection.execute(query)[0][0]

    def optimize_table(self):
        pass


class Connect(ClickhouseClient):
    """
    用户友好下载数据和上传数据接口
    """
    def __init__(self,
                host='',
                port=0,
                user='',
                password='',
                db_name = '',
                ):
        super(Connect, self).__init__(host= host,port = port,user = user, password=password)
        self.db_name = db_name
        self.login_db()

    def login_db(self,):
        self.connect()
        self.use_default_db()

    def use_default_db(self):
        """默认使用db"""
        self.excu(f"USE {self.db_name};")

    def use_db(self, db_name):
        """重定向database到 db_name"""
        self.excu(f"USE {db_name};")

    def create_db(self, db_name):
        """不支持用户自建db"""
        raise Exception("not support user create clickhouse db, ask administrator of clickhouse")

    def read_df(self, table_name:str, columns:str or list , key:str = 'symbol', symbol:list=None, start_date:int= None, end_date:int= None ):
        if columns == "*":
            sql_scripts = f"SELECT * FROM {table_name}\n"
        else:
            sql_scripts = f"SELECT\n{', '.join(columns)}\nFROM {table_name}\n"

        if symbol or start_date or end_date:
            sql_scripts += "WHERE\n"
        if symbol is not None and isinstance(symbol, list):
            sql_scripts += "and".join([f"{key}='{i}'\n" for i in symbol])
        if start_date is not None:
            sql_scripts += f"and date>={start_date}\n"
        if end_date is not None:
            sql_scripts += f"and date<={end_date}\n"

        df = super().read_df(sql_scripts)

        return df

    # def dump_parquet(self, sql: str, path: str):
    #     """下载数据输出为parquet"""
    #     df = super().read_df(sql)
    #     return df.to_parquet(path)
    #
    # def dump_csv(self, sql: str, path: str):
    #     """下载数据输出为csv"""
    #     df = super().read_df(sql)
    #     return df.to_csv(path)
    
    def exists(self, table_name: str):
        """判断table是否存在,检查当前的database"""
        table_list = self.list_tables(self.current_database)
        if table_name in table_list:
            return True
        return False

    def create_table(self, table_name:str , schema:dict or str, order_by:list ,partition_by:list, ck_schema:bool= False, engine = "MergeTree",settings:list = None ):
        """
        上传用户特征table
        table_name: str, 指定表单的名字
        schema: dict or path, 通过json文件来传递每一个schema的内容
        order_by: string list
        settings: string list, other setting
        """
        create_sql = clickhouse_create_table_sql(table_name, schema, order_by, partition_by, ck_schema= ck_schema, engine = engine, settings=settings)
        self.excu(create_sql)
    
    def init_table(self, table_name:str, df:pd.DataFrame, _async: bool = False):
        """
        基于df导入数据。初始导入数据，对于存在数据的table不再导入数据，适合固定的表导入，避免重复导入
        备注：
            1. 导入的数据需要跟创建的table的schema匹配不然报错
            2. 默认同步方式上传数据
        """
        if self.table_size(self.current_database, table_name) != 0:
            raise Exception("function not support, consider using update_table to insert data")
        if self.exists(table_name):
            schema = self.read_schema(table_name)
        else:
            raise Exception(f"table not exists, please create it with function 'create_table'")
        if check_schema(df, schema):
            if _async:
                self.async_insert_df(df, table_name)
            else:
                self.insert_df(df, table_name)
        else:
            raise Exception("schema not compare, check df schema and clickhouse schema")

    def update_table(self, table_name:str, df:pd.DataFrame, _async: bool = False):
        """基于df更新用户特征的内容"""
        if self.exists(table_name):
            schema = self.read_schema(table_name)
        else:
            raise Exception("table not exists, please create it with function 'create_table'")
        if check_schema(df, schema):
            if _async:
                self.async_insert_df(df, table_name)
            else:
                self.insert_df(df, table_name)
        else:
            raise Exception("schema not compare, check df schema and clickhouse schema")

    def insert_table(self, table_name:str, source_table:str, function:list, order_by:list, group_by:list, settings = None):
        """基于ck导入数据,对于数据ck基础函数的user更加友好"""
        create_table_scripts = insert_table(table_name, source_table, function, order_by, group_by, settings= settings)
        self.excu(create_table_scripts)

    def create_materialized_table(self, table_name: str, source_table:str, function: list, order_by:list, partition_by:list, settings_cur_table:list=None, setting_source_table:list = None):
        """
        创建物化视图
        基于 function list 构造物化视图， example ’count(*) as count‘：
        """
        create_sql = clickhosue_create_materialized_table(table_name, source_table, function, order_by, partition_by, settings_cur_table = settings_cur_table, setting_source_table= setting_source_table)
        self.excu(create_sql)

    def gen_stk_bar(self, table_name:str, source_table:str, schema:str or dict= None, bar_level:str = "1m",materialized:bool = False):
        """合成股票的bar线"""

        if bar_level == '1m':
            function = [
                "toInt64(concat(toString(`date`), LPAD(toString(floor(time / 10000000)), 2, '0'),\
                               LPAD(toString(floor((time % 10000000) / 100000) + 1), 2, '0'), '00')) AS datetime",
                "first_value(price) as open",
                "max(price) AS high",
                "min(price) AS low",
                "last_value(price) AS close",
                'instrument'
            ]

        if materialized:

            partition_by = [
                "instrument",
                "toYYYYMMDD(toDate(subString(toString(datetime) , 1 , length(toString(datetime))-6)))"
            ]
            order_by = [
                "instrument",
                "datetime"
            ]
            setting_cur_table = [
            ]

            setting_source_table = [
                "GROUP BY (instrument, datetime)"
            ]

            self.create_materialized_table(table_name, source_table, function, order_by, partition_by, settings_cur_table= setting_cur_table, setting_source_table= setting_source_table)
        else:
            order_by = ["instrument", "datetime"]
            partition_by = ["instrument", "toInt32(subString(toString(datetime) , 1 , length(toString(datetime))-6)))"]
            self.create_table(table_name, schema, order_by, partition_by)

            group_by = ["instrument", "datetime"]
            self.insert_table(table_name, source_table, function, order_by, group_by)


    def gen_future_bar(self, table_name:str, source_table:str, schema:str or dict= None, bar_level:str = "1m",materialized:bool = False):
        """合成期货的bar"""
        if bar_level == '1m':
            function = [
                "toInt64(concat(toString(`date`), LPAD(toString(floor(time / 10000000)), 2, '0'),\
                               LPAD(toString(floor((time % 10000000) / 100000) + 1), 2, '0'), '00')) AS datetime",
                "first_value(last) as open",
                "max(last) AS high",
                "min(last) AS low",
                "last_value(last) AS close",
                'symbol'
            ]

        # if 'function' not in locals():
        #     raise Exception("function not define")

        if materialized:

            partition_by = [
                "symbol",
                "toYYYYMMDD(toDate(subString(toString(datetime) , 1 , length(toString(datetime))-6)))"
            ]
            order_by = [
                "symbol",
                "datetime"
            ]
            setting_cur_table = [
            ]

            setting_source_table = [
                "GROUP BY (symbol, datetime)"
            ]

            self.create_materialized_table(table_name, source_table, function, order_by, partition_by, settings_cur_table= setting_cur_table, setting_source_table= setting_source_table)
        else:
            order_by = ["symbol", "datetime"]
            partition_by = ["symbol", "toInt32(subString(toString(datetime) , 1 , length(toString(datetime))-6)))"]
            self.create_table(table_name, schema, order_by, partition_by)

            group_by = ["symbol", "datetime"]
            self.insert_table(table_name, source_table, function, order_by, group_by)


class ConnectFile(Connect):
    """建立基于clickhouse的文件引擎
        备注：
            1.文件路径应该是ClickHouse服务器上的绝对路径。
            2. 确保ClickHouse进程具有对指定文件的读取权限。
            3. 此外，由于这只是一个“只读”表，并不实际存储数据在ClickHouse中，
                所以任何对该表的修改（如INSERT操作）都将失败。
                这种类型的表主要用于一次性导入或查询外部文件。
            4.使用File存储引擎创建的表主要用于测试和原型设计，
                不建议在生产环境中使用，因为这种表的性能可能不如其他专用的ClickHouse存储引擎。
    """
    def __init__(self,
                 host='',
                 port=0,
                 user='',
                 password='',
                 db_name=''
                 ):
        super(ConnectFile, self).__init__(host= host,port = port,user = user, password=password,db_name = db_name)

    def create_file_table(self, table_name:str, file_path:str, schema:str or dict, engine:str = 'Parquet', ck_schema = False):
        """
        创建基于file engine的table
        备注:
            1. 支持parquet、csv
            2. 需强制声明清楚数据类型，数据类型支持dataframe转换为clickhouse的数据类型
        """
        create_table_scripts = clickhouse_create_file_table_sql(table_name, file_path, schema, engine = engine, ck_schema = ck_schema)
        self.excu(create_table_scripts)

    def create_url_table(self, table_name: str, file_path_url: str, schema: str or dict, engine:str = 'Parquet', ck_schema: bool= False):
        """提供基于url创建table的方式"""
        create_table_scripts = clickhouse_create_url_table_sql(table_name, file_path_url, schema, engine=engine,
                                                                ck_schema=ck_schema)
        self.excu(create_table_scripts)



def clickhouseclient_demo(host= '',
                          port= 9000,
                          user='test',
                          password='test'):
    """测试 ClickhouseClient 的 demo方法"""
    ck = ClickhouseClient(host=host, port=port, user=user, password=password)
    ck.connect()
    ck.list_tables()

def connect_demo(host = '',
                                  port = 9000,
                                  user='test',
                                  password='test',
                                  db_name= 'test',
                                  table_name ='test',
                                  schema= {'test':'String'},#or “path.json”
                                  order_by= ['test'],
                                  settings= ['test']):
    """测试 ClickhouseClientFriendly 的 demo方法"""
    ck = Connect(host=host, port=port, user=user, password=password,db_name=db_name)
    ck.create_table(table_name,schema, order_by, settings)
    df = pd.DataFrame({"test":"test"})
    ck.init_table("test",df)
    df = ck.read_df(table_name, "*", )
    #处理df
    ...
    #上传df
    ck.update_table(table_name, df)

if __name__ == '__main__':
    # clickhouseclient_demo(host='')
    connect_demo(host='')