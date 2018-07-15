package iloghub.logback.benchmark;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.yaml.snakeyaml.Yaml;

import java.io.FileInputStream;
import java.net.MalformedURLException;
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
        yamlTest(sc.nextLine());
        sc.close();
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

    private static void yamlTest(String configFileUrl) {
        try {
            URL url = getConfigFileUrl(configFileUrl);
            if (url == null) {
                System.out.println("config file is not find");
                return;
            }

            Yaml yaml = new Yaml();
            String config = yaml.load(new FileInputStream(url.getFile())).toString();
            System.out.println(config);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static URL getConfigFileUrl(String configFileUrl) {
        URL url;
        try {
            if (null == configFileUrl || configFileUrl.length() == 0) {
                url = Test.class.getClassLoader().getResource("config.yaml");
            } else {
                url = new URL(configFileUrl);
            }
        } catch (Exception e) {
            return null;
        }
        return url;
    }
}
