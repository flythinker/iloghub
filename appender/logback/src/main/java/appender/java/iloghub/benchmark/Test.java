package appender.java.iloghub.benchmark;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by xyc on 2018/7/9.
 */
public class Test {
    private static final Logger LOGGER = LoggerFactory.getLogger(Test.class);

    public static void main(String[] args) {
        test();
    }

    private static void test() {
        List<TestThread> ttList = new ArrayList<>();
        for (int i = 0; i < 50; i++) {
            TestThread tt = new TestThread();
            tt.setName("thread-" + i);
            ttList.add(tt);
        }
        ttList.forEach(TestThread::start);
    }
}
