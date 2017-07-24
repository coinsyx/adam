# encoding=utf8
#################################################################################
# 负责从okcoin抓取数据
#################################################################################
import threading
import time
from threading import Thread
from OkCoin.OkcoinSpotAPI import OKCoinSpot
from OkCoin.OkcoinFutureAPI import OKCoinFuture
from Config import Config


class OkCoinCollector(Thread):
    def __init__(self, btcTradeData):
        super(OkCoinCollector, self).__init__()

        self.btcTradeData = btcTradeData
        self.okcoinSpot = OKCoinSpot(Config.OK_CN_RESTURL, Config.OK_APIKEY, Config.OK_SECRETKEY)
        
    def run(self):
        while True:
            btcTrade = self.okcoinSpot.trades('btc_cny')
            self.btcTradeData.add(btcTrade)
            time.sleep(0.2)