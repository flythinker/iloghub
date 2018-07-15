package iloghub.logback.benchmark;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Created by xyc on 2018/7/9.
 */
public class LogTest {
    private static final Logger LOGGER = LoggerFactory.getLogger(LogTest.class);

    public static void printLog(String name) {
        LOGGER.warn("thread-" + name + "print log test, time is " + System.currentTimeMillis());
    }
}
