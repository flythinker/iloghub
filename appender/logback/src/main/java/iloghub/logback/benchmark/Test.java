package iloghub.logback.benchmark;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.yaml.snakeyaml.Yaml;

import java.io.FileInputStream;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

/**
 * Created by xyc on 2018/7/9.
 */
public class Test {
    private static final Logger LOGGER = LoggerFactory.getLogger(Test.class);

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Please enter the configuration file address. If you use the default configuration file, please press Enter.");
        test(getConfigMapByYmlFile(sc.nextLine()));
        sc.close();
    }

    private static void test(Map configMap) {
        if (null == configMap) {
            LOGGER.error("configMap file is null");
            return;
        }

        List<TestThread> ttList = new ArrayList<>();
        for (int i = 0; i < Integer.valueOf(configMap.get("threadNum").toString()); i++) {
            TestThread tt = new TestThread(Integer.valueOf(configMap.get("printLogNum").toString()));
            tt.setName("thread-" + i);
            ttList.add(tt);
        }
        ttList.forEach(TestThread::start);
    }

    private static Map getConfigMapByYmlFile(String configFileUrl) {
        try {
            URL url = getConfigFileUrl(configFileUrl);
            if (url == null) {
                LOGGER.error("config file is not find");
                return null;
            }

            Yaml yaml = new Yaml();
            return (Map) yaml.load(new FileInputStream(url.getFile()));
        } catch (Exception e) {
            LOGGER.error("Test-getConfigMapByYmlFile is error", e);
            return null;
        }
    }

    private static URL getConfigFileUrl(String configFileUrl) {
        URL url;
        try {
            if (null == configFileUrl || configFileUrl.length() == 0) {
                url = Test.class.getClassLoader().getResource("iloghub.yml");
            } else {
                url = new URL(configFileUrl);
            }
        } catch (Exception e) {
            return null;
        }
        return url;
    }
}
