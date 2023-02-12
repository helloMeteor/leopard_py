from decimal import Decimal

from cryptofeed import FeedHandler
from cryptofeed.defines import TRADES, TICKER, CANDLES
from cryptofeed.exchanges import Gateio

import Constants as Constants
import Wxpusher as wxpusher
from MarketWarningMessage import TodayWarningMessage, ChangePercentMessage
from RedisHelper import getConnect as redisConnect

# #定义交易对
marketList = []
# 监控交易对和市场行情周期
market_warning_config = Constants.market_warning_config


async def ticker(t, receipt_timestamp):
    for market_warning in market_warning_config:

        # 当前交易对
        market = t.raw["result"]["currency_pair"]
        # 当前价格
        current_price = Decimal(t.raw["result"]["last"])
        # 今日涨幅
        todayChangePercent = Decimal(t.raw["result"]["change_percentage"])
        # 组装微信消息
        todayWarningMessage = TodayWarningMessage(market, current_price, todayChangePercent, 0)
        percentMessageList = set()

        # 循环监控交易对和市场行情周期
        for item in market_warning:
            if item != 'market':
                # 交易对+周期
                market_key = market + "_" + item
                market_key_msg = market + "_" + item + "_msg"

                # 获取存储的值
                last_market_value = redisConnect.get_str_pickle(market_key)
                # 换算成秒
                cycle_time = int(item) * 60
                # redis 中没有值
                if last_market_value is None:
                    redisConnect.set_str_pickle(market_key, t, cycle_time)
                else:
                    # 上一次价格
                    last_price = Decimal(last_market_value.raw["result"]["last"])
                    # 上一次时间
                    last_timestamp = last_market_value.timestamp
                    # 周期金额变动
                    change_amount = current_price - last_price
                    # 周期的涨幅
                    change_percent = round(change_amount / last_price, 4) * 100
                    """
                    上次预警时间 + 周期 >= 当前时间 并且 振幅的绝对值 >=预期
                    """
                    if abs(change_percent) >= market_warning[item]:
                        # 组装消息
                        changePercentMessage = ChangePercentMessage(item, change_percent, change_amount)
                        percentMessageList.add(changePercentMessage)
                        # 重新赋值
                        redisConnect.set_str(market_key_msg, market_key)
                        redisConnect.set_str_pickle(market_key, t, cycle_time)
        # 如果符合预期,就发消息
        if len(percentMessageList) > 0:
            wxpusher.sendMarketWarningMessage(todayWarningMessage, percentMessageList)


async def trade(t, receipt_timestamp):
    print(f"Trade received at {receipt_timestamp}: {t}")


async def candles(t, receipt_timestamp):
    print("candles:", t)


ticker_cb = {TICKER: ticker}


def main():
    fh = FeedHandler()

    fh.add_feed(Gateio(symbols=marketList, channels=[CANDLES],
                       callbacks={TICKER: ticker, TRADES: trade, CANDLES: candles}))
    fh.run()


if __name__ == '__main__':
    for item in market_warning_config:
        marketList.append(item.get("market"))
    main()
