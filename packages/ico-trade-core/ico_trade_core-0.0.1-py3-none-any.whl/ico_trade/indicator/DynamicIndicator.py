from ico_trade.indicator.BaseIndicator import BaseIndicator
from ico_trade.objecs.ICOBar import ICOBar
from ico_trade.objecs.ICOTicker import ICOTicker
from ico_trade.objecs.enum import IndicatorType


class StaticIndicator(BaseIndicator):
    def __init__(self):
        self.name = "DYNAMIC"
        self.show_name = "动态指标"
        self.type = IndicatorType.DYNAMIC

    def loadValue(self, dataApi):
        pass

    def calculateByBar(self, bar: ICOBar, indicators) -> None:
        pass

    def calculateByTicker(self, ticker:ICOTicker, indicators) -> None:
        pass