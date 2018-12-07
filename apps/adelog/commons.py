import sys
import time
import datetime
import os
from ADE.settings import BASE_DIR

def show_exc(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return ("ERROR ===:> [%s in %s:%d]: %s" % (exc_type, exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno, str(e)))

class Log(object):
    def __init__(self, logfile = 'mylog.log'):
        self.path = os.path.join(BASE_DIR,logfile)
        print("Init class log %s" % self.path)

    def write_log(self, code, message):
        f = open(self.path, 'a')
        f.write("[%lf]|[%s]|%s\n" % (time.time(), code,message))
        f.close()

    def debug(self, message, app=None):
        if app :
            message = "[%s][%s]" % (app, message)
        self.write_log('DBG', message)

    def info(self, message, app=None):
        if app :
            message = "[%s][%s]" % (app, message)
        self.write_log('INFO', message)

    def warning(self, message, app=None):
        if app :
            message = "[%s][%s]" % (app, message)
        self.write_log('WARN', message)

    def error(self, message, app=None):
        if app :
            message = "[%s][%s]" % (app, message)
        self.write_log('ERROR', message)
