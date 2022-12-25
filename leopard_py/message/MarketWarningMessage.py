class TodayWarningMessage:

    def __init__(self, market, currentPrice, todayChangePercent, lastDayChangePercent):
        # 当前交易对
        self.market = market
        # 当前价格
        self.currentPrice = currentPrice
        # 今日涨幅
        self.todayChangePercent = todayChangePercent
        # 24小时涨幅
        self.lastDayChangePercent = lastDayChangePercent


class ChangePercentMessage:
    def __init__(self, minutes, changePercent, changeAmount):
        # 周期
        self.minutes = minutes
        # 上涨百分百
        self.changePercent = changePercent
        # 上涨金额
        self.changeAmount = changeAmount