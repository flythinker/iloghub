package iloghub.logback.core;

import iloghub.logback.core.util.JedisPoolUtil;
import ch.qos.logback.core.OutputStreamAppender;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.ByteBuffer;

/**
 * Created by xyc on 2018/7/9.
 * logback send log to redis util
 */
public class LogbackRedisAppender<E> extends OutputStreamAppender<E> {
    JedisPool pool;

    String redisConfig;//格式为 redis://pass@host:port 例如: redis://123456@127.0.0.1:6379
    String logName;//日志名称(服务器上的名称)log.[应用名称].[服务器名称] 例如: log.api1._8070

    public String getRedisConfig() {
        return redisConfig;
    }

    public void setRedisConfig(String redisConfig) {
        this.redisConfig = redisConfig;
    }

    public String getLogName() {
        return logName;
    }

    public void setLogName(String logName) {
        this.logName = logName;
    }

    private void publishLogToRedis(byte[] log, int startPos, int size) {
        Jedis client = pool.getResource();
        try {
            client.publish(logName, new String(log, startPos, size, "UTF-8"));
        } catch (Exception e) {
            e.printStackTrace();
            client.close();
            client = null;
        } finally {
            if (client != null) {
                client.close();
            }
            addInfo("LogbackRedisAppender send log to redis is end");
        }
    }

    @Override
    public void start() {
        addInfo("LogbackRedisAppender send log to redis is start");
        if (logName == null || redisConfig == null) {
            addError("LogbackRedisAppender start is error, logName or redisConfig is null");
            return;
        }

        pool = JedisPoolUtil.getJedisPoolByRedisConfig(redisConfig);

        if (pool == null) {
            addError("LogbackRedisAppender start is error, logName or redisConfig is null");
            return;
        }

        OutputStream targetStream = new OutputStream() {
            private ByteBuffer buf = ByteBuffer.allocate(1024 * 10);

            @Override
            public void write(int b) throws IOException {
                buf.put((byte) b);
                if (b == '\n') {
                    publishLogToRedis(buf.array(), 0, buf.position());
                    buf.clear();
                }
            }
        };
        this.setOutputStream(targetStream);
        super.start();
    }
}
