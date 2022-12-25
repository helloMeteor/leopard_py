# EDIT_ 为前缀的参数是需要修改的

# wx pusher的 token
WX_PUSHER_TOKEN = 'AT_Aq2YoDboIRTygzhurdMIfg9b8Lq521m3'
# wx pusher的uid  需要替换
EDIT_WX_PUSHER_UID = ['UID_h2h8PcU8FL76mSCJBU31rQPHgCOl']

# redis 的配置
EDIT_REDIS_HOST = '127.0.0.1'
EDIT_REDIS_PORT = 6379
EDIT_REDIS_DB = 1

# 监控交易对和市场行情周期
market_warning_config = (
    {"market": "BTC-USDT", "1": 1, "5": 1.5, "10": 2, "15": 3, "30": 4, "60": 5},
    {"market": "ETH-USDT", "1": 1, "5": 1.5, "10": 2, "15": 3, "30": 4, "60": 5}
)
