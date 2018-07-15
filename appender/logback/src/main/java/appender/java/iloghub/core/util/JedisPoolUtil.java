package appender.java.iloghub.core.util;

import appender.java.iloghub.core.RedisConfig;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by xyc on 2018/7/15.
 * jedisPoll工具类
 */
public class JedisPoolUtil {
    private static final String host = "host";//redis服务器地址
    private static final String port = "port";//redis服务器端口号
    private static final String passWord = "passWord";//redis服务器密码

    /**
     * 根据redisConfig获取jedisPool
     * redisConfig格式为 redis://pass@host:port 例如: redis://123456@127.0.0.1:6379
     */
    public static JedisPool getJedisPoolByRedisConfig(String redisConfig) {
        int timeOut = 2000;//超时时间
        RedisConfig config = getRedisConfig(redisConfig);
        return new JedisPool(getJedisPoolConfig(), config.getHost(), config.getPort(), timeOut, config.getPassword(), config.getDatabase());
    }

    private static RedisConfig getRedisConfig(String redisConfig) {
        Map<String, String> redisConfigMap = resolveRedisConfig(redisConfig);
        RedisConfig config = new RedisConfig();
        config.setHost(redisConfigMap.get(host));
        config.setPort(Integer.valueOf(redisConfigMap.get(port)));
        config.setPassword(redisConfigMap.get(passWord));
        return config;
    }

    private static Map<String, String> resolveRedisConfig(String redisConfig) {
        redisConfig = redisConfig.substring(8, redisConfig.length());
        Map<String, String> redisConfigMap = new HashMap<>();
        int passWordEndIndex = redisConfig.indexOf("@");
        int hostEndIndex = redisConfig.indexOf(":");
        redisConfigMap.put(passWord, redisConfig.substring(0, passWordEndIndex));
        redisConfigMap.put(host, redisConfig.substring(passWordEndIndex + 1, hostEndIndex));
        redisConfigMap.put(port, redisConfig.substring(hostEndIndex + 1, redisConfig.length()));
        return redisConfigMap;
    }

    private static JedisPoolConfig getJedisPoolConfig() {
        JedisPoolConfig config = new JedisPoolConfig();
        config.setMaxTotal(500);
        config.setTestOnBorrow(false);
        config.setTestOnReturn(false);
        return config;
    }
}
