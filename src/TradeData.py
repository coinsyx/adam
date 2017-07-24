# encoding=utf8
#################################################################################
# TradeData类维护trade data buffer，并且负责落盘，提供基本的取数据接口.
# 但是不负责和exchanger服务器通信
#################################################################################
from Config import Config
import sys
import os
from Util import *
import time
from datetime import datetime, timedelta
import json
import traceback

class TradeData:
    def __init__(self, locker, symbol):
        self.locker = locker
        self.tradeData = []
        self.max_q_size = Config.TRADE_DATA_MAX_QUEUE_SIZE
        self.symbol = symbol # btc_cny, ltc_cny
        self.current_tid = 0
        
        # save to file
        self.add_times = 0
        self.save_freq = 20
        self.filename = 'trade'
        self.saved_tid = 0
        self.current_tm = (0,0,0,0) # y,m,d,h   tuple support compare
        self.fout = None
    
    def get_file_handler(self):
        now = datetime.now()
        tm = (now.year, now.month, now.day, now.hour)
        if self.current_tm < tm:
            if self.fout != None:
                self.fout.close()
            fout_file = '%s/%s_%s_%d%02d%02d%02d.dat' % (Config.LOG_DIR, self.filename, self.symbol, tm[0], tm[1], tm[2], tm[3])
            self.fout = open(fout_file, 'a')
            self.current_tm = tm
            return self.fout
        return self.fout
    
    def check_data(self, data):
        if 'tid' not in data:
            return False
        if data['tid'] <= self.current_tid:
            return False
        return True
    
    def save_to_disk(self):
        fout = self.get_file_handler()
        for data in self.tradeData:
            if data['tid'] <= self.saved_tid:
                continue
            fout.writelines(json.dumps(data)+'\n')
            self.saved_tid = data['tid']
        fout.flush()
        
    def add(self, dataList):
        acquired = False
        try:
            l = []
            for data in dataList:
                if self.check_data(data) == False:
                    continue
                if 'date_ms' in data:
                    data.pop('date_ms')
                data['price'] = float(data['price'])
                l.append(data)
                self.current_tid = data['tid']
            self.locker.acquire()
            acquired = True
            
            self.tradeData.extend(l)
            sz = len(self.tradeData)
            for ii in range(sz - self.max_q_size):
                self.tradeData.pop(0)
            
            self.add_times += 1
            if self.add_times % self.save_freq == 0:
                self.save_to_disk()
        except:
            print(traceback.print_exc())
            if acquired:
                self.locker.release()
            return False
        if acquired:
            self.locker.release()
        return True