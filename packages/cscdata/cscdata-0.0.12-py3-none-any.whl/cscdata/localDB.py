# -*- coding:utf-8 -*-

import os
import re
import h5py
import shutil
import uuid
import pandas as pd
from pyspark.sql import SparkSession

from .config import LOCAL_DATA_PATH, READ_REPORT_GB, USERDB_LIST, DATABASE_LIST
from .utils import create_simple_not_exists, remove_file_path, get_directory_and_size, remove_file_in_directory

class DataFile:
    def __init__(self,
                 local_data_path = LOCAL_DATA_PATH,
                 read_report_gb = READ_REPORT_GB
                 ):
        self.local_data_path = local_data_path
        self.exists(local_data_path)
        self.db_path = None
        self.table_path = None
        self.read_report_gb = read_report_gb
    
    def exists(self,file):
        if not os.path.exists(file):
            raise Exception(f"{file} not exists!")
    
    def use_db(self, db_name):
        """
        切换database
        """
        self.db_path = os.path.join(self.local_data_path, db_name)
        self.exists(self.db_path)

    def use_table(self, table_name):
        """
        使用table
        """
        self.table_path = os.path.join(self.db_path, table_name)
        # self.exists(self.table_path)
        create_simple_not_exists(self.table_path)

    def active_spark(self, num_core:int = 10, exe_memory:str = '8g', drive_momory:str = '20g', name:str = 'demo'):
        """
        激活spark，调用spark功能，默认设置spark内容
        """
        spark = SparkSession.builder.\
        master(f"local[{num_core}]").\
        appName(name).\
        enableHiveSupport().\
        config("spark.driver.memory", drive_momory).\
        config("spark.executor.memory", exe_memory).\
        getOrCreate()

        spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
        return spark
    
    def stop_spark(self, spark):
        """
        停用spark，释放资源
        """
        spark.stop()

    def show_tables(self,):
        """
        显示当前db的所有table name
        """
        talbe_list = os.listdir(self.db_path)
        print(f"current tables as blow:")
        print(f"{talbe_list}")
        return talbe_list

    def show_path(self,):
        """
        显示当前的路径：db path 和 table path
        """
        print(f"current datapath is {self.db_path}, current table_path is {self.table_path}")
        return self.db_path, self.table_path
    
    def raise_table_name(self, table_name):
        if table_name is None and self.table_path is None:
            raise ValueError(f"please define the table name")
        if self.table_path is None:
            self.use_table(table_name)
    
    def get_table_update_date(self, table_name:str = None):
        """返回最后更新的日期"""
        table_path  = os.path.join(self.db_path, table_name)
        return "".join(re.split(r"[-/\\.a-zA-Z ]", os.listdir(table_path).sort()[-1]))[:8]
    

class ConnectBase(DataFile):
    def __init__(self,
                 db_name: str = None,
                 ):
        super().__init__()
        self.db_name = db_name
        self.raise_db()
        self.use_db(db_name)
    
    def raise_db(self):
        """
        初始化db，保证db in database db list
        """
        if self.db_name is None or self.db_name not in DATABASE_LIST:
            raise Exception(f"确保存在 database db_name'{self.db_name}'")
        
    def use_db(self, db_name):
        """
        使用基础数据的db
        """
        if db_name in DATABASE_LIST:
            return super().use_db(db_name)
        else:
            print(f"{db_name} not in database db list")


class ConnectUser(DataFile):
    def __init__(self,
                 db_name: str = None,
                 ):
        super().__init__()
        self.db_name = db_name
        self.raise_db()
        self.use_db(db_name)

    def raise_db(self):
        """
        初始化db，保证db in user db list
        """
        if self.db_name is None or self.db_name not in USERDB_LIST :
            raise Exception(f"确保存在 user db_name'{self.db_name}'")
    
    def use_db(self, db_name):
        """
        使用用户的db
        """
        if db_name in USERDB_LIST:
            return super().use_db(db_name)
        else:
            print(f"{db_name} not in users db list")
    
    def use_table(self, table_name):
        super().use_table(table_name)

    def to_narrow_parquet(self, df: pd.DataFrame, table_anme,keys:list[str]= None, partition_by: list[str] = None, write_mode = 'w', **kwargs):
        self.raise_table_name(table_anme)
        self.table = Table(self.table_path)
        self.table.to_narrow_parquet(df, keys, partition_by, write_mode = write_mode, **kwargs)

    def to_wide_parquet(self, df: pd.DataFrame, table_name, partition_by: list[str] = None, write_mode = 'w', **kwargs):
        self.raise_table_name(table_name)
        self.table = Table(self.table_path)
        self.table.to_wide_parquet(df,partition_by, write_mode=write_mode, **kwargs)


class Table:
    def __init__(self, table_path):
        self.table_path = table_path

    
    def get_partitions_list(self, df, base_path, partition_cols):
        """检查已存在的partition路径"""
        partition_list = []
        if partition_cols is None or len(partition_cols) == 0:
            return partition_list
        for _, partition_df in df.groupby(partition_cols):
        # 生成每个分区的路径
            partition_path = base_path
            for col in partition_cols:
                partition_path = os.path.join(partition_path, f"{col}={partition_df.iloc[0][col]}")

            partition_list.append(partition_path)
            # 如果分区路径存在，则删除
            # if os.path.exists(partition_path):
            #     shutil.rmtree(partition_path)
        return partition_list

        
    def write_with_mode(self, df, base_path, partition_by: list = [], write_mode = 'w',**kwargs ):
        """
        选择模式来写入数据
        备注:
            这里包括两个层面的写入模式，一种是本身table的直接写入，一种是带有partition的写入
        """
        partition_list = self.get_partitions_list(df, base_path, partition_by)
        if write_mode == 'w':
            for path in partition_list:
                if os.path.exists(path):
                    shutil.rmtree(path)
            if len(partition_by) == 0 or len(partition_list) == 0:
                # 如果不是按照分区保存的数据则删除table文件夹下的文件内容（目前不限制，删除全部非文件夹）
                remove_file_in_directory(base_path)
            df.to_parquet(base_path, partition_cols= partition_by,**kwargs)

        elif write_mode == 'a':
            df.to_parquet(base_path, partition_cols= partition_by,**kwargs)

        elif write_mode == 'e':
            if len(partition_by) ==0 and os.path.exists(base_path):
                raise Exception(f"exists duplicate table")
            if len(partition_by) !=0 and len(partition_list) != 0:
                raise Exception(f"exists duplicate partitions.")
            df.to_parquet(base_path, partition_cols= partition_by,**kwargs)

        elif write_mode == 'i':
            if len(partition_by) == 0 and len([os.path.join(base_path, i) for i in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, i)) ]) !=0 :
                # 文件层面，文件夹内的废文件夹内容不是0个 则忽略
                return 
            
            if len(partition_by) ==0 :
                df.to_parquet(base_path,**kwargs)
            else:
                for _, partition_df in df.groupby(partition_by):
                    partition_path = base_path
                    # 生成每个分区的路径
                    for col in partition_by:
                        partition_path = os.path.join(partition_path, f"{col}={partition_df.iloc[0][col]}")

                    # 检查分区路径是否存在，如果不存在则写入数据
                    if not os.path.exists(partition_path):
                        os.makedirs(partition_path, exist_ok=True)
                        partition_df.to_parquet(partition_path, index=False ,partition_cols = [], **kwargs)
                            
        else:
            raise Exception(f"write_mode = '{write_mode}' is error!")

    def to_narrow_parquet(self, df: pd.DataFrame, keys:list[str]= None, partition_by: list[str] = None, write_mode = 'w', **kwargs):
        """
        提供生成窄表的方法
        备注:
            1. 保证传入的df为dataframe的格式
            2. keys为必须传入的参数, 通过keys来确定每个窄表中包含的字段 [*kyes, fea]
            3. partition_by可选
        """
        if self.table_path is None:
            raise Exception(f"please use function 'use_table' to init your target table first")

        if keys is None:
            raise Exception(f"please define 'keys'")

        if partition_by is None:
            partition_by = []

        columns = df.columns.to_list()
        feature_list = [i for i in columns if i not in keys]

        for fea in feature_list:
            if set(partition_by)&set(keys) != set(partition_by):
                raise Exception(f"make sure your folder '{partition_by}' in keys '{keys}'.")
            # df_feature = df[list(set(keys)- set(partition_by))+[fea]]
            df_feature = df[keys+[fea]]
            base_path = os.path.join(self.table_path, fea)
            # df_feature.to_parquet(base_path, partition_cols= partition_by,**kwargs)
            self.write_with_mode(df_feature, base_path, partition_by, write_mode= write_mode, **kwargs)
 
        print(f"save to {self.table_path}")

    def to_wide_parquet(self, df:pd.DataFrame, partition_by: list[str] = None, write_mode = 'w', **kwargs):
        """保存为宽表"""
        if self.table_path is None:
            raise Exception(f"please use function 'use_table' to init your target table first")
        
        if partition_by is None:
            partition_by = []
        
        # table_name = re.split(r"[\\/]", self.table_path)[-1] + '.parquet'
        # df.to_parquet(os.path.join(self.table_path, table_name), partition_cols=  partition_cols, **kwargs)
        self.write_with_mode(df, self.table_path, partition_by, write_mode= write_mode, **kwargs)
        
        print(f"save to {self.table_path}")



class ParquetDB(DataFile):
    def __init__(self, db_name, outer_path: str = None):
        super().__init__()
        self.db_name = db_name
        if outer_path is not None:
            self.local_data_path = outer_path
        self.use_db(db_name)


    def get_table_files(self, table_name:str = None, start_date:int = None, end_date:int = None):
        """
            通过table_name获取table的满足条件
        """
        self.raise_table_name(table_name)
        
        if start_date and end_date and start_date> end_date:
            raise Exception(f"start_date bigger than end_date")
        table_size, file_list = get_directory_and_size(self.table_path, start_date, end_date)

        if table_size > 1073741824 * self.read_report_gb:
            print(f"读取的数据超过{self.read_report_gb}GB,输入 'c' 继续")
            a = str(input()).replace(" ","").replace("'", "")
            if a != 'c':
                raise Exception(f"over {self.read_report_gb} GB. keyboard exception.")
        return file_list
            
    def spark_read(self, spark, table_name: str=  None,  start_date:int = None, end_date:int = None):
        """
        通过spark读取parquet
        """
        file_list = self.get_table_files(table_name=table_name, start_date= start_date, end_date=end_date)

        # self.active_spark(name= 'Read Parquet')
        df = spark.read.parquet(*file_list).toPandas()
        # self.stop_spark()

        return df
    
    def read_df(self, table_name, start_date:int = None, end_date:int = None, **kwargs):
        """
        通过pandas读取parquet
        """
        file_list = self.get_table_files(table_name = table_name, start_date= start_date, end_date=end_date)

        df = pd.read_parquet(file_list,**kwargs)

        return df
    
    def use_table(self, table_name):
        return super().use_table(table_name)
    
    def show_tables(self):
        return super().show_tables()

    def show_path(self):
        return super().show_path()
    
    def active_spark(self, name:str = "demo", **kwargs):
        return super().active_spark(name = name, **kwargs)
    
    def stop_spark(self):
        super().stop_spark()
    
    def get_table_update_date(self, table_name: str = None):
        return super().get_table_update_date(table_name)



class H5DB(DataFile):
    def __init__(self, db_name, outer_path = None):
        super().__init__()
        self.db_name = db_name
        if outer_path is not None:
            self.local_data_path = outer_path
        self.use_db(db_name)

    def list_keys(self ,table_name: str=  None):
        """
        读取h5的keys
        """
        self.raise_table_name(table_name)

        with h5py.File(self.table_path, 'r') as h5r:
            keys= list(h5r.keys())
        return keys

    def read_df(self, key,table_name: str=  None):
        """
        读取h5文件数据为
        """
        self.raise_table_name(table_name)

        with h5py.File(self.table_path, 'r') as h5r:
            data = h5r[key][()]
        return data

    def read_flow(self, key, chunk_size, table_name: str=  None):
        """
        read h5 file as data flow
        """
        self.raise_table_name(table_name)

        with h5py.File(self.table_path, 'r') as f:
            dset = f[key]
            n = dset.shape[0]

            for i in range(0, n, chunk_size):
                yield dset[i: i+chunk_size]

    def use_table(self, table_name):
        return super().use_table(table_name)
    
    def show_path(self):
        return super().show_path()
    
    def show_tables(self):
        return super().show_tables()
    
    def active_spark(self, name='demo', **kwargs):
        return super().active_spark(name= name, **kwargs)
    
    def stop_spark(self, name):
        super().stop_spark(name)
    
    def get_table_update_date(self, table_name: str = None):
        return super().get_table_update_date(table_name)
    


class DataApi:
    def __init__(self,
                 db_name:str,
                #  password:str
                 ):
       self.db_name = db_name
       self.user = ConnectUser(db_name= db_name)

    def pdb(self, db_name: str, path:str = None, db_mode: str = "parquet" ):
        """
        基于不同模式的read方法扩展
        db_name: 需要实例化的数据文件源
        path: 切换 LOCAL_DATA_BASE， 默认user和database的路径均为 LOCAL_DATA_BASE
        """
        if db_mode.upper() == 'PARQUET':
            parquet_db = ParquetDB(db_name, outer_path= path)
            return parquet_db
        elif db_mode.upper() == 'H5':
            h5_db = H5DB(db_name, outer_path= path)
            return h5_db
        else:
            raise ValueError(f"db_mode '{db_mode}' not support.")

    def use_table(self, table_name: str):
        self.user.use_table(table_name)
        
    def show_tables(self,):
        return self.user.show_tables()

    def show_path(self,):
        return self.user.show_path()

    def active_spark(self, name='demo', **kwargs):
        return self.user.active_spark(name = name, **kwargs)
    
    def stop_spark(self,):
        self.user.stop_spark()
    
    def read(self, table_name, start_date =None, end_date = None):
        """
        默认使用parquet，如需要扩展请使用use_db来扩展
        """
        db = self.pdb(self.db_name, db_mode= 'parquet')
        return db.read_df(table_name=table_name,start_date=start_date, end_date=end_date)
        
    def write(self, df:pd.DataFrame, table_name:str, table_struct: str = "narrow", keys: list[str] = None, partition_by: list[str] = None, write_mode:str = 'w',**kwargs):
        """
        写入功能，将df写入table当中
        备注:
            1. mode： narrow or wide
            2. write_mode: 
                - append -> 'a'
                - overwrite -> 'w'
                - error -> 'e'
                - ignore -> 'i'
        """
        self.user.raise_table_name(table_name)
        if table_struct == 'narrow':
            if keys is None:
                #保存为窄表需指定keys，如果不指定则默认保存为宽表
                self.user.to_wide_parquet(df, table_name, keys = keys, partition_by=partition_by, write_mode= write_mode, **kwargs)
            else:
                self.user.to_narrow_parquet(df, table_name, keys= keys, partition_by= partition_by, write_mode= write_mode, **kwargs)
        elif table_struct == 'wide':
            self.user.to_wide_parquet(df, table_name, partition_by= partition_by, write_mode= write_mode, **kwargs)
        else:
            raise Exception(f"{table_struct} not exists, consider 'narrow' or 'wide'.")


if __name__ == "__main__":
    pass