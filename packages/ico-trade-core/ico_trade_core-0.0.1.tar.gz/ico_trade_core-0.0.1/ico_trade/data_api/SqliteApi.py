from ico_trade.data_api.AbstractDataApi import AbstractDataApi


class SqliteApi(AbstractDataApi):
    """
    连接本地数据库的高级类
    """
    def __init__(self):
        super().__init__()
        # ib 对象
        self.conn = None

    def connect(self):
        pass

    def disconnect(self):
        pass

    def run(self):
        pass