import logging
import redis
import time
import math
import getopt
import sys,os
import yaml

from pathlib import Path

logger = logging.getLogger('itail')
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)-8s: %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

ilogback_client_sample_yml='''
redis:
  host: 127.0.0.1
  port: 6379
  pass: pass
  database: 0
'''

class LogHubTail:
    def __init__(self):
        self.f_arg = None
        self.c_arg = None
        self.isOnlyStat = False

    def redis_test(self):
        pool = redis.ConnectionPool(host='10.8.3.51', port=6379, db=0)
        r = redis.Redis(connection_pool=pool)
        r.execute_command("AUTH", "12345678901234567890")

        #接收消息
        ps = r.pubsub()
        #ps.subscribe('log.hyp.mydev1')
        ps.subscribe('hyp-dev.test')

        def listen_task():
            for i in ps.listen():
                if i['type'] == 'message':
                    #print(i)
                    print("Task get", i['data'].decode("utf8"))
        listen_task()

    def init_action(self):
        print("init_action")
        cwd = os.getcwd()
        filepath = cwd + "/iloghub_client.yml"
        if not os.path.exists(filepath):
            print("created ",filepath )
            file_object = open(filepath, 'w')
            file_object.write(ilogback_client_sample_yml)
            file_object.close()
        home = str(Path.home())
        glb_iloghub_cfg_dir = home + '.iloghub'
        if not os.path.exists(glb_iloghub_cfg_dir):
            os.mkdir(glb_iloghub_cfg_dir)
            print( "created" , glb_iloghub_cfg_dir )

    def read_config(self):
        # 读取配置文件
        config_filepath = self.c_arg
        if (config_filepath == None):
            # 先读取当前文件
            cwd = os.getcwd()
            filepath = cwd + "/iloghub_client.yml"
            logger.info("filepath:%s" % filepath)
            filepath2 = home = str(Path.home()) + "/.iloghub/iloghub_client.yml"
            logger.info("filepath2:%s" % filepath2)
            if os.path.exists(filepath): #如果存在
                config_filepath = filepath
            elif os.path.exists(filepath2):
                config_filepath = filepath2
            else:
                pass

        if config_filepath == None :
            logger.info("ilogback_client.yml is not exist.Please create by 'itail init' command")
            sys.exit(0)

        f = open(config_filepath)
        self.config = yaml.load(f)
        f.close()
        print('config',self.config )

    def start_tail_task(self):
        logger.info('itail starting')
        #config
        #{'redis': {'host': '127.0.0.1', 'port': 6379, 'pass': 'pass', 'database': 0}}
        redisConfig = self.config['redis']
        redis_host = redisConfig['host']
        redis_port = redisConfig['port']
        redis_pass = redisConfig['pass']
        redis_database = redisConfig ['database']
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_database)
        r = redis.Redis(connection_pool=pool)
        r.execute_command("AUTH", redis_pass)
        logger.info('redis connect success')
        # 接收消息
        ps = r.pubsub()
        # ps.subscribe('log.hyp.mydev1')
        ps.subscribe( self.f_arg )




        def listen_task():
            logger.info("listen_task ... ")
            last_time_5sec_int = math.floor(time.time() / 5)  #每5秒种这个值变化一次
            total_line = 0
            total_size = 0
            for i in ps.listen():
                if i['type'] == 'message':
                    if not self.isOnlyStat:
                        print("Task get", i['data'].decode("utf8"))
                    else:
                        cur_time_5sec_int = math.floor(time.time() / 5)
                        if cur_time_5sec_int == last_time_5sec_int:
                            total_line += 1
                            total_size += len(i['data'])
                        else:
                            logger.info("5 second stat -- line:%s size:%s" % (total_line,total_size))
                            total_line = 1
                            total_size = len(i['data'])
                            last_time_5sec_int = cur_time_5sec_int

        logger.info('start listen log:' + self.f_arg)
        listen_task()

    # 再读取全局配置
    def start_tail(self):
        self.opts, self.args = getopt.getopt(sys.argv[1:], 'sf:c:', [])  # -s 只做统计 -f loghub_日志通道名称  -c 手动制定配置文件
        logger.info ( ["opts" , self.opts] )
        logger.info( ["args", self.args] )
        if "init" in self.args:
            self.init_action()
            sys.exit(0)
        for opt in self.opts:
            print( opt[0], opt[1] )
            if opt[0] == '-f':
                self.f_arg = opt[1]
            if opt[0] == '-c':
                self.c_arg = opt[1]
            if opt[0] == '-s':
                self.isOnlyStat = True
        self.read_config()
        logger.info("....")
        if self.f_arg is not None:
            self.start_tail_task()
        else:
            print("-f parameter is not exists.")

if __name__ == "__main__":
    #test1()
    #redis_test()
    tail = LogHubTail()
    tail.start_tail()