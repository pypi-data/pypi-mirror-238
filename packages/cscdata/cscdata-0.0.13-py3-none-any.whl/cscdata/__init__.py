from .config import LOCAL_DATA_PATH, USERDB_LIST, DATABASE_LIST
import os

def init(path):
    """提供给外部测试数据源的init方法"""

    global LOCAL_DATA_PATH, USERDB_LIST, DATABASE_LIST

    LOCAL_DATA_PATH = path

    USERDB_LIST = [i for i in os.listdir(path)]

    DATABASE_LIST = [i for i in os.listdir(path)]
