# encoding=utf-8
########################################################
# this project should be run under python 3 
########################################################
import sys
import os
from Util import *
import time
from datetime import datetime, timedelta
import threading
from Config import Config
from TradeData import TradeData
from OkCoinCollector import OkCoinCollector

for i in range(1, len(sys.argv)):
    x,y = sys.argv[i].split('=')
    setattr(Config, x, type(getattr(Config, x))(y))

            
class Server:
    def __init__(self):
        self._check_dirs()
        
        self.btcTradeDataLocker = threading.Lock()
        self.btcTradeData = TradeData(self.btcTradeDataLocker, 'btc_cny')
        self.ok_collector = OkCoinCollector(self.btcTradeData)
    def _check_dirs(self):
        if not os.path.exists(Config.LOG_DIR):
            os.mkdir(Config.LOG_DIR)

    def main(self):
        self.ok_collector.start()
        

if __name__ == '__main__':
    server = Server()
    server.main()
