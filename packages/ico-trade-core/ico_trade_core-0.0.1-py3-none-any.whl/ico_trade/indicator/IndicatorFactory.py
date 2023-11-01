class IndicatorFactory:
    """
    Indicator工厂类，根据指标名称，返回指标对象，并进行初始化
    """
    # 当前支持的指标的名称列表
    indicator_names = ["LastPrice", "LatestNewHighTime", "OpenPrice", "LowPrice", "HighPrice", "LastDayClose", "TodayMovePercent", "DayMovePercent",
                       "PreMovePercent", "TimeToOpen", "PreStd", "PreVolumeAvg", "FiveMinMaxUpPercent", "FiveMinMaxDownPercent",
                       "AskPrice", "BidPrice", "CurrentTime", "AvgDayMove30", "EMA10", "EMA15", "PreMoveLevel", "TodayPreVolume"]
    # 静态指标
    daily_indicators = ["LastDayClose", "AvgDayMove30", "PreStd", "PreVolumeAvg", "PreMoveLevel"]

    @classmethod
    def generate_indicator(cls, indicator_name: str):
        """
        给出指标名称，创建指标实例
        :param indicator_name:
        :return:
        """
        if indicator_name in cls.indicator_names:
            class_str = "Ai"+ indicator_name + "Indicator"
            # 通过类名字符串获取类对象
            class_obj = globals()[class_str]
            return class_obj()
        else:
            raise Exception("未定义此指标：%s " % indicator_name)

