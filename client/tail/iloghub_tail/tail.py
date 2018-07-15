
# 123456789abcd

import redis
import time
import getopt
import sys
import yaml
import os
from pathlib import Path

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
        filepath = cwd + "/ilogback_client.yml"
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
            filepath = cwd + "/ilogback_client.yml"
            filepath2 = home = str(Path.home()) + "/ilogback_client.yml"
            if os.path.exists(filepath): #如果存在
                config_filepath = filepath
            elif os.path.exists(filepath2):
                config_filepath = filepath2
            else:
                pass

        if config_filepath == None :
            print("ilogback_client.yml is not exist.","please create by 'itail init' command")
            sys.exit(0)

        f = open(config_filepath)
        self.config = yaml.load(f)
        f.close()
        print('config',self.config )



    def start_tail_task(self):
        #config
        #{'redis': {'host': '127.0.0.1', 'port': 6379, 'pass': 'pass', 'database': 0}}
        redis = self.config['redis']
        redis_host = redis['host']
        redis_port = redis['port']
        redis_pass = redis['pass']
        redis_database = redis['database']
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_database)
        r = redis.Redis(connection_pool=pool)
        r.execute_command("AUTH", redis_pass)

        # 接收消息
        ps = r.pubsub()
        # ps.subscribe('log.hyp.mydev1')
        ps.subscribe( self.f_arg )
        def listen_task():
            for i in ps.listen():
                if i['type'] == 'message':
                    # print(i)
                    print("Task get", i['data'].decode("utf8"))
        listen_task()

    # 再读取全局配置
    def start_tail(self):
        self.opts, self.args = getopt.getopt(sys.argv[1:], 'f:c:', [])  # -f loghub_日志通道名称  -c 手动制定配置文件
        print("opts", self.opts)
        print("args", self.args)
        if "init" in self.args:
            self.init_action()
            sys.exit(0)
        for opt in self.opts:
            print( opt[0], opt[1] )
            if opt[0] == '-f':
                self.f_arg = opt[1]
            if opt[0] == '-c':
                self.c_arg = opt[1]
        self.read_config()
        if self.f_arg is not None:
            self.start_tail_task()
        else:
            print("-f parameter is not exists.")



if __name__ == "__main__":
    #test1()
    #redis_test()
    tail = LogHubTail()
    tail.start_tail()