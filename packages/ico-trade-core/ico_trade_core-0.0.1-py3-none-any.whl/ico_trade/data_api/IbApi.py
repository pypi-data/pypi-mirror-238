from ib_insync import IB

from ico_trade.data_api.AbstractDataApi import AbstractDataApi


class IbApi(AbstractDataApi):
    """
    连接IB的高级类
    """
    def __init__(self):
        super().__init__()
        # ib 对象
        self.ib = IB()

    def connect(self, ip="127.0.0.1", port=7497, clientId=1):
        self.ib.connect(host=ip, port=port, clientId=clientId)

    def disconnect(self):
        if self.ib.isConnected():
            self.ib.isConnected()

    def run(self):
        # 开始订阅的数据
        self.ib.run()