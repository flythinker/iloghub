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
            } else {
                
            }
        }
    }

    private void printLog() {
        LOGGER.warn(getName() + "print log test, time is " + System.currentTimeMillis());
    }
}
