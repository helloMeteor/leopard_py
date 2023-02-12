import requests
import schedule

import Wxpusher


# geteio 自动 签到
def gateSingIn():
    # 请求地址
    url = "https://www.gate.ac/query_rewards"
    # 请求参数
    params = {"action": "checkin"}
    # 请求cookie
    cookieStr = "lang=cn; last_lang=cn; countryId=37; market_title=usdt; curr_fiat=CNY; " \
                "_dx_uzZo5y=60b75ccbe140c3f7a370c4d18a4e485600dd599b3baf9f91e19ee031279bcb64ac53f6f4; " \
                "finger_print=63ddfa39WJEtB0gplM8hIjrFPISdQ2Suq5JI1AG1; _ym_uid=1675491899415565061; " \
                "_ym_d=1675491899; _ym_isad=1; _ym_visorc=b; b_notify=1; is_portfolio_margin_account_1487287=0; " \
                "is_portfolio_margin_switch_status_1487287=0; lasturl=%2Frewards%2Factivity; " \
                "is_portfolio_margin_account_1491003=0; is_portfolio_margin_switch_status_1491003=0; " \
                "t_token=80d68de02ba318ade00896843f45d0a0; uid=1487287; nickname=0meteor; is_on=1; " \
                "pver=c7c1b8e88b2de569e5ef3044fbd4fa34; csrftoken=038c6d97f81b09c18a7df0a422e12320fdd473bede127df8; " \
                "login_notice_check=%2F "
    # cookie 格式转换 为dict
    cookies = {}
    for line in cookieStr.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    # 请求header
    header = {"csrftoken": "038c6d97f81b09c18a7df0a422e12320fdd473bede127df8",
              "content-type": "application/x-www-form-urlencoded"}
    # POST请求
    res = requests.post(url=url, data=params, cookies=cookies, headers=header)
    Wxpusher.sendWxPusherMessage(res.text.encode("utf-8").decode("unicode_escape"))


# 签到任务
def singInTask():
    # 清空任务
    schedule.clear()
    # 每天6点半执行
    schedule.every().days.at("06:30").do(gateSingIn)
    while True:
        # 运行所有可运行的任务
        schedule.run_pending()


if __name__ == '__main__':
    singInTask()
