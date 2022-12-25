import logging

from wxpusher import WxPusher

import MarketWarningMessage as message
import Constants as constants

logger = logging.getLogger(__name__)

"""
微信消息发送助手
"""


def sendWxPusherMessage(content):
    # token
    wx_pusher_token = constants.WX_PUSHER_TOKEN
    # uid
    wx_pusher_uid = constants.EDIT_WX_PUSHER_UID

    result = WxPusher.send_message(content, uids=wx_pusher_uid, token=wx_pusher_token, content_type=3)
    logger.warning(result)


"""
发送市场预警消息
"""


def sendMarketWarningMessage(todayMessage: message.TodayWarningMessage,
                             percentMessageList: set[message.ChangePercentMessage]):
    # 消息标题
    content = '<font size=5 color=lightseagreen >[{0}]行情通知</font> \n <br/> '.format(todayMessage.market)
    # 消息内容
    content = content + "当前价格：${0}\n今日涨幅：{1}%\n24h涨幅：{2}%\n\n".format(todayMessage.currentPrice,
                                                                      todayMessage.todayChangePercent,
                                                                      todayMessage.lastDayChangePercent)
    for percentMessage in percentMessageList:
        # 颜色
        color = ""
        # 方向
        direction = ""
        if percentMessage.changePercent < 0:
            color = "green"
            direction = "下跌"
        else:
            color = "red"
            direction = "上涨"
        content = content + "<font size=4 color={0}>{1}分钟{2}</font>\n百分比：{3}%\n金额：${4}\n\n".format(
            color, percentMessage.minutes, direction, percentMessage.changePercent, percentMessage.changeAmount)
    # 发送wx消息
    sendWxPusherMessage(content)
