import pandas as pd

class ClickhouseServer:
    """ 管理clickhouse数据库 """

    def __init__(self):
        pass

    def start(self):
        pass

    def restart(self):
        pass


class ClickhouseServerStatus:
    """返回服务端的信息"""

    def __init__(self,
                 connection=None,
                 ):
        self.connection = connection

    def system_setting(self, ):
        return pd.DataFrame(self.connection.execute("SELECT * FROM system.settings'", with_column_types=True))

    def system_metrics(self, ):
        return pd.DataFrame(self.connection.execute("SELECT * FROM system.metrics'", with_column_types=True))