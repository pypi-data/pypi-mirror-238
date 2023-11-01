from typing import List

from eventkit import Event

from ico_trade.contract.ICOContract import ICOContract


class AbstractDataApi():
    """
    数据api的抽象类，定义所有方法及属性
    """

    # 类属性，本类支持的所有的事件
    events = []

    def __init__(self):
        # 创建支持的事件
        self._createEvents()

    def _createEvents(self):
        self.newBarEvent = Event("newBarEvent")
        self.newTickerEvent = Event("newTickerEvent")


    def connect(self):
        """
        连接数据源
        :return:
        """
        pass

    def disconnect(self):
        """
        断开数据源
        :return:
        """
        pass

    def run(self):
        """
        开始运行
        :return:
        """
        pass

    def subContracts(self, cons=List[ICOContract]):
        pass

    def __del__(self):
        # 销毁时，释放资源
        self.disconnect()
