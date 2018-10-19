package flythinker.iloghub.log.test.tool;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

import java.util.Map;

/**
 * Created by wlhua on 2018/10/19.
 */
public class RedisLogGenerator
{
    private static final Logger logger = LoggerFactory.getLogger(RedisLogGenerator.class);

    RedisConfig config;
    public RedisLogGenerator(RedisConfig config)
    {
        this.config = config;
    }
    public JedisPool getJedisPool()
    {
        int timeOut = 2000;//超时时间
        JedisPoolConfig poolConfig = new JedisPoolConfig();
        poolConfig.setMaxTotal(500);
        poolConfig.setTestOnBorrow(false);
        poolConfig.setTestOnReturn(false);
        return new JedisPool(poolConfig, config.getHost(), config.getPort(), timeOut, config.getPassword(), config.getDatabase());
    }

    class RunConfig{
        int threadCount  = 1;
        int logStringSize = 10;
        long sleepTime = 10;
        long rndSleepTime = 10;
        String channelName = "log.LogTestTool.devServer" ;
    }
    RunConfig runConfig = new RunConfig();

    static String longString = "asdfwoeruodfiuqwrewquiepfadfuipwefdfsdfwefasfaweasdfwaefadfasdfsdfasdfasdfsadfdd" +
            "sadfasdfasdfiudpfoiuwepfuiasdfaskldwewefwfewefwefefwfasdfafawefafeiwue" +
            "asdfasdfasdfasdfasdfasdfasdfasdfasdfw2eq234rdf3w4rdfdgdfgdfgdfgdfg" +
            "asdfasdfasdfasdfasdfasdfasdfasdfasdfw2eq234rdf3w4rdfdgdfgdfgdfgdfg" +
            "asdfasdfasdfasdfasdfasdfasdfasdfasdfw2eq234rdf3w4rdfdgdfgdfgdfgdfg" +
            "asdfasdfasdfasdfasdfasdfasdfasdfasdfw2eq234rdf3w4rdfdgdfgdfgdfgdfg" +
            "asdfasdfasdfasdfasdfasdfasdfasdfasdfw2eq234rdf3w4rdfdgdfgdfgdfgdfg" +
            "asdfasdfasdfasdfasdfasdfasdfasdfasdfw2eq234rdf3w4rdfdgdfgdfgdfgdfg" +

            "dfgsadfgs45tfg435tfdg43tfg34tdefger34tgfdeg3rt34dfgdfgdfgdfgdfgff" +
            "dfg4gdfg45dfgergret45tgfre5tgfdfgfdgdfgdgdfffffffoapsdfiuaw";

    static class TotalTask
    {
        String logStr = "";
        int totalCount = 0;
        int currentCount = 0;
        int totalThread = 0;
        int finishThreadCount = 0;
        long startTime;

        public TotalTask(int totalCount)
        {
            this.totalCount = totalCount;
            startTime = System.currentTimeMillis();
        }

        public synchronized int getNext100Task(){
            if(currentCount % 5000 == 0){
                logger.info("TotalTask.currentCount:" + currentCount);
            }
            if(currentCount >= totalCount ){
                finish();
                return 0;
            }else{
                if(totalCount - currentCount >= 100 ){
                    currentCount += 100;
                    return 100;
                }else{
                    currentCount = totalCount;
                    return totalCount - currentCount;
                }
            }
        }
        private void finish(){
            finishThreadCount++;
            if(finishThreadCount >= totalThread){
                //当所有线程完成时，整个任务完成，计算运行时间。
                long endTime = System.currentTimeMillis();
                StringBuilder buf = new StringBuilder();
                buf.append("total time:").append( endTime - startTime ).append("ms");
                logger.info(buf.toString());
            }
        }
    }

    static int TaskThreadID = 0;
    class TaskThread extends Thread
    {
        private TotalTask totalTask;
        TaskThread(TotalTask totalTask){
            super("TaskThread_" + TaskThreadID);
            TaskThreadID++;
            this.totalTask = totalTask;
        }
        public void run()
        {
            JedisPool jedisPool= getJedisPool();
            while(true){
                int taskCount = totalTask.getNext100Task();
                if(taskCount <=0){ //没有任务是结束任务
                    break;
                }
                Jedis jedis=jedisPool.getResource();
                for(int i=0;i<taskCount;i++){
                    jedis.publish( runConfig.channelName, totalTask.logStr );
                }
                jedis.close();
            }
            jedisPool.close();
        }
    }

    /**
     * 运行发送日志任务
     * @param totalCount
     */
    public void runSendLogTask(int totalCount)
    {
        TotalTask totalTask = new TotalTask(totalCount);
        totalTask.logStr = longString.substring(0,runConfig.logStringSize);
        totalTask.totalThread = runConfig.threadCount;

        for(int i=0;i<runConfig.threadCount;i++){
            TaskThread taskThread = new TaskThread(totalTask);
            taskThread.start();
        }
    }
}
