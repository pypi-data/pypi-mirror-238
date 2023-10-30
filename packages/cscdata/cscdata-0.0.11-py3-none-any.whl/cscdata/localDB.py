# -*- coding:utf-8 -*-

import os
import re
import h5py
import pandas as pd
from pyspark.sql import SparkSession

from .config import LOCAL_DATA_PATH, READ_REPORT_GB, USERDB_LIST, DATABASE_LIST
from .utils import create_simple_not_exists, remove_file_path, get_directory_and_size, list_keys, read_h5

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
        self.spark = SparkSession.builder.\
        master(f"local[{num_core}]").\
        appName(name).\
        config("spark.driver.memory", drive_momory).\
        config("spark.executor.memory", exe_memory).\
        getOrCreate()

        self.spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
        return self.spark
    
    def stop_spark(self):
        """
        停用spark，释放资源
        """
        self.spark.stop()
    

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

    def to_narrow_parquet(self, df: pd.DataFrame, keys:list[str]= None, partition_by: list[str] = None):
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
            df_feature = df[list(set(keys)- set(partition_by))+[fea]]
            df_feature.to_parquet(os.path.join(self.table_path,fea), partition_cols= partition_by)

        print(f"save to {self.table_path}")

    def to_wide_parquet(self, df:pd.DataFrame):
        if self.table_path is None:
            raise Exception(f"please use function 'use_table' to init your target table first")
        print(self.table_path)
        table_name = re.split(r"[\\/]", self.table_path)[-1] + '.parquet'
        print(table_name)

        df.to_parquet(os.path.join(self.table_path, table_name))
        
        print(f"save to {self.table_path}")


class ParquetDB(DataFile):
    def __init__(self, db_name):
        super().__init__()
        self.db_name = db_name
        self.use_db(db_name)

    def select_limit_tables(self, table_name:str = None, start_date:int = 20100104, end_date:int = 20211231):
        """
        读取文件，通过日期命名的可以读取只在日期范围内的日期
        """
        self.raise_table_name(table_name)
        
        if start_date and end_date and start_date> end_date:
            raise Exception(f"start_date bigger than end_date")
        table_size, target_list = get_directory_and_size(self.table_path, start_date, end_date)

        if table_size > 1073741824 * self.read_report_gb:
            print(f"读取的数据超过{self.read_report_gb}GB,输入 'c' 继续")
            a = str(input()).replace(" ","").replace("'", "")
            if a != 'c':
                raise Exception(f"over {self.read_report_gb} GB. keyboard exception.")
        
        return target_list
            
    def spark_read(self, table_name: str=  None,  start_date:int = 20100104, end_date:int = 20211231):
        """
        通过spark读取parquet
        """
        target = self.select_limit_tables(table_name=table_name, start_date= start_date, end_date=end_date)

        self.active_spark(name= 'Read Parquet')
        df = self.spark.read.parquet(*target).toPandas()
        self.stop_spark()

        return df
    
    def read_df(self, table_name: str=  None, start_date:int = 20100104, end_date:int = 20211231):
        """
        通过pandas读取parquet
        """
        target = self.select_limit_tables(table_name = table_name, start_date= start_date, end_date=end_date)

        df = pd.read_parquet(target[-1])
        for tar in target[1:]:
            df_s = pd.read_parquet(tar)
            df = pd.concat([df, df_s], axis=0)
            df = df.reset_index(drop=True)

        return df
    
    def use_table(self, table_name):
        return super().use_table(table_name)
    
    def show_tables(self):
        return super().show_tables()

    def show_path(self):
        return super().show_path()
    
    def active_spark(self, num_core: str = 10, exe_memory: str = '8g', drive_momory: str = '20g', name='demo'):
        return super().active_spark(num_core, exe_memory, drive_momory, name)
    
    def stop_spark(self):
        super().stop_spark()



class H5DB(DataFile):
    def __init__(self, db_name):
        super().__init__()
        self.db_name = db_name
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
    
    def active_spark(self, num_core: str = 10, exe_memory: str = '8g', drive_momory: str = '20g', name='demo'):
        return super().active_spark(num_core, exe_memory, drive_momory, name)
    
    def stop_spark(self):
        super().stop_spark()

class DataApi:
    def __init__(self,
                 db_name:str,
                #  password:str
                 ):
       self.db_name = db_name
       self.user = ConnectUser(db_name= db_name)

    def read_db(self, db_name, db_mode= "parquet" ):
        """
        基于不同模式的read方法扩展
        """
        if db_mode.upper() == 'PARQUET':
            return ParquetDB(db_name)
        elif db_mode.upper() == 'H5':
            return H5DB(db_name)
        else:
            raise Exception(f"db name error, {db_name} wrong!")
    
    def use_table(self, table_name: str):
        self.user.use_table(table_name)
        
    def show_tables(self,):
        return self.user.show_tables()

    def show_path(self,):
        return self.user.show_path()

    def active_spark(self, num_core: str = 10, exe_memory: str = '8g', drive_momory: str = '20g', name='demo'):
        return self.user.active_spark(num_core, exe_memory, drive_momory, name)
    
    def stop_spark(self,):
        self.user.stop_spark()
    
    def read(self, table_name, start_date =None, end_date = None):
        """
        默认使用parquet，如需要扩展请使用use_db来扩展
        """
        db = self.read_db(self.db_name, db_mode= 'parquet')
        return db.read_df(table_name=table_name,start_date=start_date, end_date=end_date)
        
    def write(self, df:pd.DataFrame, table_name:str, table_struct: str = "narrow", keys: list[str] = None, partition_by: list[str] = None, write_mode:str = 'a'):
        """
        写入功能，将df写入table当中
        备注:
            1. mode： narrow or wide
            2. write_mode: append or overwrite --> 'a','w'
        """
        table_path = os.path.join(self.user.db_path, table_name)
        if write_mode == 'w':
            if os.path.exists(table_path):
                remove_file_path(table_path)
            self.user.use_table(table_name)
        elif write_mode == 'a':
            self.user.use_table(table_name)
        else:
            raise Exception(f"write_mode = '{write_mode}' is error!")
        
        if table_struct == 'narrow':
            self.user.to_narrow_parquet(df, keys= keys, partition_by= partition_by)
        elif table_struct == 'wide':
            self.user.to_wide_parquet(df)
        else:
            raise Exception(f"{table_struct} not exists, consider 'narrow' or 'wide'.")


if __name__ == "__main__":
    pass