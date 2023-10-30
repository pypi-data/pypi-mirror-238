# -*- coding:utf-8 -*-

import json
import time
import h5py
import os
import re
from functools import wraps
from .map import *

def get_directory_and_size(directory, start_date, end_date):
    """计算目录下所有文件的总大小（包括子目录中的文件）。"""
    total_size = 0
    target_list = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            if start_date is None or end_date is None:
                fp = os.path.join(dirpath, f)
                # 跳过如果是链接
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
                    target_list.append(fp)
            else:
                if to_YYYYMMDD(f) >= start_date and to_YYYYMMDD(f)<=end_date:
                    fp = os.path.join(dirpath, f)
                    # 跳过如果是链接
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
                        target_list.append(fp)

    return total_size, target_list

def to_YYYYMMDD(filename):
    """通过正则匹配filenam中的数字"""
    return int("".join(re.split(r"\D+", str(filename)))[:8])

def remove_file_path(path):
    """remove exists file"""
    if os.path.exists(path):
        os.remove(path)

def create_simple_not_exists(path):
    """create not exists file"""
    if not os.path.exists(path):
        os.mkdir(path)

def create_multi_not_exists(path):
    """create mutil not exists file"""
    if not os.path.exists(path):
        os.makedirs(path)
    
def read_json(json_file):
    """Read a JSON file and return its content as a Python object."""
    with open(json_file, 'r') as file:
        return json.load(file)

def clickhouse_create_file_table_sql(table_name:str ,file_path:str, schema:str or dict, engine:str = 'parquet', ck_schema:bool = False):
    """
    ClickHouse 的 File 表引擎支持多种文件格式
    备注：
        1. 这里支持parquet和csv格式
        2. 为了使用某些格式，例如 Parquet、ORC 或 Protobuf，
            可能需要在 ClickHouse 中安装额外的库或模块。
            您应该查看 ClickHouse 的文档或您的 ClickHouse 安装，
            以确定支持哪些格式。
    """

    if engine.upper() == 'PARQUET':
        engine = "Parquet"
    elif engine.upper() == 'CSV':
        engine = "CSV"
    else:
        raise Exception(f"path is '{file_path}', engine is '{engine}'. format not support or wrong path")

    if isinstance(schema, str):
        schema = read_json(schema)
    if not ck_schema:
        schema = dict(zip(schema.keys(), [df2ck[i] for i in schema.values()]))

    columns = ',\n '.join([f"{column_name} {data_type}" for column_name, data_type in schema.items()])
    create_table_sql = f"CREATE TABLE {table_name}\n(\n {columns}\n) ENGINE= File({engine}, '{file_path}')"
    return create_table_sql

def clickhouse_create_url_table_sql(table_name:str ,file_path_url:str, schema:str or dict, engine:str = 'parquet', ck_schema:bool = False):
    """
    ClickHouse 的 URL 表引擎支持多种文件格式
    """

    if engine.upper() == 'PARQUET':
        engine = "Parquet"
    elif engine.upper() == 'CSV':
        engine = "CSV"
    else:
        raise Exception(f"path url is '{file_path_url}', engine is '{engine}'. format not support or wrong path")

    if isinstance(schema, str):
        schema = read_json(schema)
    if not ck_schema:
        schema = dict(zip(schema.keys(), [df2ck[i] for i in schema.values()]))

    columns = ',\n '.join([f"{column_name} {data_type}" for column_name, data_type in schema.items()])
    create_table_sql = f"CREATE TABLE {table_name}\n(\n {columns}\n) ENGINE= URL('{file_path_url}', '{engine}')"
    return create_table_sql

def clickhouse_create_table_sql(table_name, schema, order_by,partition_by, ck_schema:bool = False, engine='MergeTree', settings = None):
    """ 生成clickhouse创建表的sql语句
    schema: dict
    order_by: list
    settings: list 例如：
        ['PARTITION BY toYYYYMMDD(toDate(date))', 'ORDER BY (date, symbol, time)';
    """
    if isinstance(schema, str):
        schema = read_json(schema)
    if not ck_schema:
        schema = dict(zip(schema.keys(), [df2ck[i] for i in schema.values()]))

    columns = ',\n '.join([f"{column_name} {data_type}" for column_name, data_type in schema.items()])
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name}\n(\n {columns}\n) ENGINE = {engine}()\n"
    order_by = "(" + ", ".join(order_by) + ")\n"
    partition_by = "(" + ", ".join(partition_by) + ")\n"
    create_table_sql += f"ORDER BY {order_by}\n"
    create_table_sql += f"PARTITION BY {partition_by}\n"

    if settings:
        for setting in settings:
            create_table_sql += f"{setting}\n"
    return create_table_sql

def clickhosue_create_materialized_table(table_name:str, source_table:str, function:list, order_by:list, partition_by:list, engine:str = 'MergeTee', settings_cur_table:list = None, setting_source_table:list = None):
    """基于base数据生成物化视图"""
    function = ','.join(function)
    create_table_sql = f"CREATE MATERIALIZED TABLE IF NOT EXISTS {table_name}\nENGINE = {engine}()\n"
    order_by = "(" + ", ".join(order_by) + ")\n"
    partition_by = "(" + ", ".join(partition_by) + ")\n"
    create_table_sql += f"ORDER BY {order_by}\n"
    create_table_sql += f"PARTITION BY {partition_by}\n"
    if settings_cur_table:
        for setting in settings_cur_table:
            create_table_sql += f"{setting}\n"
    create_table_sql += f"\nPOPULATE AS SELECT\n{function} FROM {source_table}\n"
    if setting_source_table:
        for setting in setting_source_table:
            create_table_sql += f"{setting}\n"
    return create_table_sql

def insert_table(table_name:str, source_table:str, function:list, order_by:list, group_by:list, settings = None):
    function = ','.join(function)
    create_table_scripts = f"INSERT INTO {table_name} SELECT\n{function}\nFROM {source_table}\n"

    order_by = "(" + ", ".join(order_by) + ")\n"
    group_by = "(" + ", ".join(group_by) + ")\n"

    create_table_scripts += f"ORDER BY {order_by}\n"
    create_table_scripts += f"GROUP BY {group_by}\n"

    if settings:
        for setting in settings:
            create_table_scripts += f"{setting}\n"

    return create_table_scripts


def check_schema(df, schema):
    """检查df的schema是否和schema一致"""
    clickhouseFormat2dfFormat = ck2df
    columns_name =df.columns.tolist()
    df_dtypes = [str(i) for i in list(df.dtypes)]

    df_schema = dict(zip(columns_name, df_dtypes))

    for key in schema.keys():
        if key not in df_schema:
            print(df_schema)
            return False
        if key in df_schema and clickhouseFormat2dfFormat[schema[key]] != df_schema[key]:
            print(df_schema)
            return False
    return True

def read_h5(pth, key):
    with h5py.File(pth, 'r') as h5r:
        data = h5r[key][()]
    return data

def list_keys(pth):
    with h5py.File(pth, 'r') as h5r:
        return list(h5r.keys())
    
def read_h5_flow(pth, key, chunk_size):
    with h5py.File(pth, 'r') as f:
        dset = f[key]
        n = dset.shape[0]

        for i in range(0, n, chunk_size):
            yield dset[i: i+chunk_size]

def timer(func):
    """一个用于计时的装饰器"""
    @wraps(func)  # 用于保持原始函数的名称和文档字符串
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 开始时间
        result = func(*args, **kwargs)  # 函数执行
        end_time = time.time()  # 结束时间
        run_time = end_time - start_time  # 运行时间
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return result
    return wrapper

if __name__ == '__main__':
    clickhouse_create_table_sql('test', read_json(r"K:\qtData\futdata\fut_lev1_schma.json"), order_by = ['symbol','date','time'],settings =['PARTITION BY toYYYYMMDD(toDate(date))'])