package iloghub.logback.benchmark;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.yaml.snakeyaml.Yaml;

/**
 * Created by xyc on 2018/7/9.
 * 线程测试类
 */
public class TestThread extends Thread {
    private static final Logger LOGGER = LoggerFactory.getLogger(TestThread.class);

    private Integer printLogNum;//0 无限输入 5 每秒发送5条

    public TestThread(Integer printLogNum) {
        this.printLogNum = printLogNum;
    }

    @Override
    public void run() {
        while (true) {
            if (0 == printLogNum) {
                printLog();
            } else if (5 == printLogNum) {
                printIntervalLog();
            }
        }
    }

    private void printLog() {
        LOGGER.warn(getName() + "print log test, time is " + System.currentTimeMillis());
    }

    private void printIntervalLog() {
        long startTime = System.currentTimeMillis();
        for (int i = 0; i < printLogNum; i++) {
            printLog();
        }
        long endTime = System.currentTimeMillis();
        long sleepTime = 1000 - (endTime - startTime);
        if (sleepTime > 0) {
            try {
                sleep(sleepTime);
            } catch (InterruptedException e) {
                LOGGER.error("sleep is error", e);
            }
        }
    }
}
