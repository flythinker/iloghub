
import logging
import redis
import time

def redis_test():
    pool = redis.ConnectionPool(host='10.8.3.51', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    r.execute_command("AUTH", "12345678901234567890")

    # 接收消息
    ps = r.pubsub()
    # ps.subscribe('log.hyp.mydev1')
    #ps.subscribe('log.app1.srv2')
    ps.psubscribe('log.*')

    def handle_message(message):
        if message['type'] == 'message' or message['type'] == 'pmessage' :
            print(message['data'].decode("utf8"))

    while True:
        message = ps.get_message()
        if message:
            print(message)
            print( message['channel'].decode("utf8") )
            handle_message(message)
            time.sleep(0.001)  # be nice to the system :)
        else:
            time.sleep(0.1)

    # def listen_task():
    #     for i in ps.listen():
    #         if i['type'] == 'message':
    #             # print(i)
    #             print("Task get", i['data'].decode("utf8"))
    # listen_task()

if __name__ == "__main__":
    redis_test()