package flythinker.iloghub.log.test.tool;

/**
 * Created by wlhua on 2018/10/19.
 * Redis服务器的配置信息
 */
public class RedisConfig {
    private String host;

    private Integer port;

    private String password;

    private Integer database = 0;

    public String getHost() {
        return host;
    }

    public void setHost(String host) {
        this.host = host;
    }

    public Integer getPort() {
        return port;
    }

    public void setPort(Integer port) {
        this.port = port;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public Integer getDatabase() {
        return database;
    }

    public void setDatabase(Integer database) {
        this.database = database;
    }
}
