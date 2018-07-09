
# 123456789abcd

import redis
import time

def redis_test():
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


if __name__ == "__main__":
    #test1()
    redis_test()