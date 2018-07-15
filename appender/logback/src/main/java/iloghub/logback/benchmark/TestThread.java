package iloghub.logback.benchmark;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Created by xyc on 2018/7/9.
 * 线程测试类
 */
public class TestThread extends Thread {
    private static final Logger LOGGER = LoggerFactory.getLogger(TestThread.class);

    @Override
    public void run() {
        while (true) {
            LogTest.printLog(getName());
            LOGGER.warn(getName() + "print log success" );
        }
    }
}
