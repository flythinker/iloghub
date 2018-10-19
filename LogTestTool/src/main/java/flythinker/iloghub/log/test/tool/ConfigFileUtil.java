package flythinker.iloghub.log.test.tool;

import org.yaml.snakeyaml.Yaml;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Map;
import java.util.Properties;

/**
 * Created by wlhua on 2018/10/19.
 * 配置文件载入工具类
 */
public class ConfigFileUtil {
    private static final String ConfigFileName = "log_test_tool.yml";

    public static RedisConfig getRedisConfig() throws IOException {
        //优先载入当前目录下的配置文件
        File f = new File(ConfigFileName );
        if(!f.exists()){
            //如果不存在，则载入home目录下 config 下的相应配置文件
            String userHome = System.getProperty("user.home");
            f = new File(userHome + "/config/" + ConfigFileName );
        }
        if(!f.exists()){
            throw new RuntimeException(ConfigFileName + " config file is not exist.");
        }

        Yaml yaml = new Yaml();
        FileInputStream fis = new FileInputStream(f);
        Map configMap = (Map)(yaml.load(fis));
        fis.close();

        //{host=10.8.3.51, port=6379, pass=2222222, db=0}
        configMap = (Map)(configMap.get("log.redis"));
        String host = (String)(configMap.get("host"));
        Integer port = (Integer)(configMap.get("port"));
        String pass = configMap.get("pass").toString();
        Integer db = (Integer)(configMap.get("db"));

        RedisConfig redisConfig = new RedisConfig();
        redisConfig.setDatabase(db);
        redisConfig.setHost(host);
        redisConfig.setPassword(pass);
        redisConfig.setPort(port);
        return redisConfig;
    }
}
