from datetime import datetime, timedelta

def tms2datetime(tms):
    tm = datetime.fromtimestamp(tms)
    return tm.strftime('%Y%m%d%H%M')