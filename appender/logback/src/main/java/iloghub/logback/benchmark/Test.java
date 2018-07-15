package iloghub.logback.benchmark;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by xyc on 2018/7/9.
 */
public class Test {
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
