import logging
import redis
import time
import iloghub

iloghub.LogHub.confog()

# create logger
logger = logging.getLogger('simple_example')

#formater = logging.Formatter(style=" %(message)s")
fmt = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
datefmt = "%H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

pool = redis.ConnectionPool(host='10.8.3.51', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
r.execute_command("AUTH", "12345678901234567890")
# 发布消息例子


# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     filename='D:/test1/test.log',
#                     filemode='w')

class MyHandle(logging.Handler):
    def emit(self,record):
        lineLog = self.formatter.format(record)
        r.publish('hyp-dev.test', lineLog)
        print(lineLog)

class MyFilter(logging.Filter):
    def filter(self, record):
        print("filter:" +record.msg)

myFilter = MyFilter()

handle = MyHandle()
handle.setFormatter(formatter)

# add ch to logger
logger.addHandler(handle)
#logger.addFilter(myFilter)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
for i in range(100):
    logger.critical('critical message')
    time.sleep(1)