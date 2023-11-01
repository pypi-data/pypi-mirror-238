from ico_trade.indicator.BaseIndicator import BaseIndicator
from ico_trade.objecs.enum import IndicatorType


class StaticIndicator(BaseIndicator):
    def __init__(self):
        self.name = "STATIC"
        self.show_name = "静态指标"
        self.type = IndicatorType.STATIC

    def loadValue(self, dataApi):
        pass
