import Wxpusher as wxpusher
from MarketWarningMessage import TodayWarningMessage, ChangePercentMessage

todayWarningMessage = TodayWarningMessage("BTC-USDT", 1000, 12.2, 24.2)

percentMessageList = set()
changePercentMessage1 = ChangePercentMessage(10, 12, 24.8)
changePercentMessage2 = ChangePercentMessage(5, -7, 27.2)
percentMessageList.add(changePercentMessage1)
percentMessageList.add(changePercentMessage2)
wxpusher.sendMarketWarningMessage(todayWarningMessage, percentMessageList)
