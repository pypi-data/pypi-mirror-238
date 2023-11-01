import os
import re
import pandas as pd
from pyspark.sql import SparkSession

from .config import LOCAL_DATA_PATH, READ_REPORT_GB, USERDB_LIST, DATABASE_LIST
from .utils import create_simple_not_exists, remove_file_path, get_directory_and_size

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
        self.db_path = os.path.join(self.local_data_path, db_name)
        self.exists(self.db_path)

    def use_table(self, table_name):
        self.table_path = os.path.join(self.db_path, table_name)
        # self.exists(self.table_path)
        create_simple_not_exists(self.table_path)

    def active_spark(self, num_core:str = 10, exe_memory:str = '8g', drive_momory:str = '20g', name= 'demo'):
        self.spark = SparkSession.builder.\
        master(f"local[{num_core}]").\
        appName(name).\
        config("spark.driver.memory", drive_momory).\
        config("spark.executor.memory", exe_memory).\
        getOrCreate()

        self.spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    
    def stop_spark(self):
        self.spark.stop()
    
    def _read_parquet(self, start_date:int = None, end_date:int = None):
        """读取文件，通过日期命名的可以读取只在日期范围内的日期"""
        if start_date and end_date and start_date> end_date:
            raise Exception(f"start_date bigger than end_date")
        table_size, target_list = get_directory_and_size(self.table_path, start_date, end_date)

        if table_size > 1073741824 * self.read_report_gb:
            print(f"读取的数据超过{self.read_report_gb}GB,输入 'c' 继续")
            a = str(input()).replace(" ","").replace("'", "")
            if a != 'c':
                raise Exception(f"over {self.read_report_gb} GB. keyboard exception.")
            
        self.active_spark(name= 'Read Parquet')
        df = self.spark.read.parquet(*target_list).toPandas()
        self.stop_spark()
        return df

    def read_h5(self,):
        pass
    

class ConnectBase(DataFile):
    def __init__(self,
                 db_name: str = None,
                 ):
        super().__init__()
        self.db_name = db_name
        self.raise_db()
        self.use_db(db_name)
    
    def raise_db(self):
        """初始化db，保证db in database db list"""
        if self.db_name is None or self.db_name not in DATABASE_LIST:
            raise Exception(f"确保存在 database db_name'{self.db_name}")
        
    def use_db(self, db_name):
        """使用基础数据的db"""
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
        """初始化db，保证db in user db list"""
        if self.db_name is None or self.db_name not in USERDB_LIST :
            raise Exception(f"确保存在 user db_name'{self.db_name}'")
    
    def use_db(self, db_name):
        """使用用户的db"""
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


class Connection:
    def __init__(self,
                 database_db:str,
                 user_db:str,
                 ):
       self.database = ConnectBase(db_name= database_db)
       self.user = ConnectUser(db_name= user_db)

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
        
    def use_database_db(self, db_name:str):
        """切换基础数据database"""
        self.database.use_db(db_name)
    
    def use_user_db(self, db_name:str):
        """切换用户的database"""
        self.user.use_db(db_name)
    
    def read(self, db_name: str, table_name:str, start_date:int = None, end_date:int = None):
        """
        提供用户读取table

        """
        if db_name == self.database.db_name:
            table_path = os.path.join(self.database.db_path, table_name)
            if not os.path.exists(table_path):
                raise Exception(f"file {table_path} not exists!")

            self.database.use_table(table_name)
            return self.database._read_parquet(start_date, end_date)
        elif db_name == self.user.db_name:
            table_path = os.path.join(self.user.db_path, table_name)
            if not os.path.exists(table_path):
                raise Exception(f"file {table_path} not exists!")

            self.user.use_table(table_name)
            return self.user._read_parquet(start_date , end_date)
        else:
            raise Exception(f"db_name {db_name} not correctly.")


if __name__ == "__main__":
    con = Connection("intraday_data","rp")

    df = con.read('intraday_data', 'fut_tick', start_date=20210601, end_date=20210601)

    con.write(df, 'test', table_struct='narrow', keys = ['date', 'time', 'symbol'],)


    print(df.head())


    # df = connection.df_read(**arg, **kwargs)
    # sdf = connection.spark_read(columns, fitler)

    # connection.write(df, partition_on = [], order_by = [], mode = 'wide_table')


    # import sys
    # import tqdm
    # import pandas as pd
    # from joblib import Parallel, delayed
    # sys.path.append("/mnt/k")
    # from cscfut.data.sample_data.gen_factor import  gen_factor_tick
    
    # data_path = data.datapath
    # def tick_dev():
    #     """ 生成tick数据的因子"""
    #     files = os.listdir(data.datapath)
    #     for file in tqdm(files):
    #         df = pd.read_parquet(f'{data_path}/{file}')
    #         tasks = [delayed(gen_factor_tick)(symbol, sample) for symbol, sample in df.groupby(by='symbol')]
    #         dfs_f_dts = Parallel(n_jobs=12)(tasks)
    #         result = pd.concat(dfs_f_dts, ignore_index=True)
    #         # result.to_parquet(save_path + f"/{file}")
    #         user.to_narrow_parquet(result)

    # tick_dev()
