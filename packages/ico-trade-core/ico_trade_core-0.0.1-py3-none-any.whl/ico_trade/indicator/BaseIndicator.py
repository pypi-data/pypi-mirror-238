from ico_trade.objecs.ICOBar import ICOBar
from ico_trade.objecs.ICOTicker import ICOTicker


class BaseIndicator():
    def __init__(self):
        # 名称，用于创造实例
        self.name = "BASE"
        self.show_name = "基类指标"
        self.value = ""
        # 指标类型
        self.type = ""
        # 单位
        self.unit = ""

    def loadValue(self, dataApi):
        pass

    def calculateByBar(self, bar: ICOBar, indicators) -> None:
        pass

    def calculateByTicker(self, ticker:ICOTicker, indicators) -> None:
        pass