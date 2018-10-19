package flythinker.iloghub.log.test.tool;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.yaml.snakeyaml.Yaml;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.io.FileInputStream;
import java.util.Map;
import java.util.Properties;

/**
 * Created by wlhua on 2018/10/19.
 */
public class RedisLogGeneratorDevRun {

    private static final Logger logger = LoggerFactory.getLogger(RedisLogGeneratorDevRun.class);

    static void test1() throws Exception
    {
        //运行特定线程，特定长度的任务。
        RedisConfig redisConfig = ConfigFileUtil.getRedisConfig();
        RedisLogGenerator redisLogGenerator = new RedisLogGenerator(redisConfig);
        redisLogGenerator.runConfig.threadCount = 30;
        redisLogGenerator.runConfig.logStringSize = 10;
        redisLogGenerator.runSendLogTask(1000000); 
    }
    static void test2() throws Exception
    {
        RedisConfig redisConfig = ConfigFileUtil.getRedisConfig();
        RedisLogGenerator redisLogGenerator = new RedisLogGenerator(redisConfig);
        JedisPool jedisPool = redisLogGenerator.getJedisPool();
        Jedis jedis = jedisPool.getResource();
        long start1 = System.currentTimeMillis();
        String str1 = "1234567890";
        String str2 = "12345678901234567890";
        for(int i=0;i<2000000;i++){
            jedis.publish("log.LogTestTool.devServer",str2);
            if(i % 10000 == 0){
                System.out.println(i);
            }
        }
        long end = System.currentTimeMillis();
        System.out.println( (end - start1) );
        jedis.close();
        jedisPool.destroy();
    }
    public static void main(String[] args){

        try {
            test1();
            // test2();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
