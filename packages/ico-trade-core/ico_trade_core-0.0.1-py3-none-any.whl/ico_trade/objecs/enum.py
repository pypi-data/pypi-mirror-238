txt_dict = {
    "STATIC": "静态指标",
    "DYNAMIC": "动态指标"
}


def traslateEnum(name: str) -> str:
    if name in txt_dict.keys():
        return txt_dict[name]
    else:
        return name


class IndicatorType:
    # 静态指标
    STATIC = "STATIC"
    # 动态指标
    DYNAMIC = "DYNAMIC"
