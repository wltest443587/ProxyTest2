import redis,random
from error import PoolEmptyerror

max_score = 100 # 最大分数
min_score = 0 # 最小分数
initial_socre = 10 # 初始分数
redis_host = '127.0.0.1'
redis_port = 6379
redis_pwd = None
redis_key = 'proxies' # 有序集合键的名称

class RedisClient():
    def __init__(self, host = redis_host, port = redis_port,password = redis_pwd):
        # 初始化redis链接
        self.db = redis.StrictRedis(host = host,port = port,decode_responses=True)

    def add(self,proxy,score = initial_socre):
        """
        :param proxy: 代理
        :param score: 分数
        :return: 添加代理结果的数量
        """
        if not self.db.zscore(redis_key,proxy):
            return self.db.zadd(redis_key,score,proxy)

    def randomex(self):
        '''
        随机获取有效的代理，先尝试获取100分代理，不存在，则按照排名获取前100名，否则异常。
        :return: 随机获取一个代理
        '''
        # zrangebyscore（key，min_score,max_score) 有序集合名，最低分，最高分:回有序集中指定分数区间内的所有的成员
        # 获取分数为100的代理
        result = self.db.zrangebyscore(redis_key,max_score,max_score)
        if len(result):# 当非空时执行
            return random.choice(result)
        else:
            # Redis Zrevrange 命令返回有序集中，指定区间内的成员。其中成员的位置按分数值递减(从大到小)来排列
            result = self.db.zrevrange(0,100) # 返回100个数量
            try:
                if len(result):
                    return random.choice(result)
            except PoolEmptyerror as e:
                print(e)

    def decrease(self,proxy):
        '''
        代理值减1分，分数小于最小值，则代理删除。
        :param proxy:代理
        :return:修改后的分数
        '''
        score = self.db.zscore(redis_key,proxy)
        if score and score > min_score:
            print('代理',proxy,'当前分数',score,'减1')
            return self.db.zincrby(redis_key,proxy,-1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(redis_key,proxy)  # #删除指定的值

    def exists(self,proxy):
        '''
        判断代理是否存在
        :param proxy:代理
        :return:是否存在
        '''
        return not self.db.zscore(redis_key,proxy) == None

    def max(self,proxy):
        '''
        将代理设置为最大值100
        :param proxy: 代理
        :return: 设置结果
        '''
        print('代理', proxy, '可用，设置为:',max_score)
        return self.db.zadd(redis_key,max_score,proxy)

    def count(self):
        '''
        :return: 获取代理的数量
        '''
        return self.db.zcard(redis_key)

    def all(self):
        '''
        :return: 获取全部的代理
        '''
        return self.db.zrangebyscore(redis_key,min_score,max_score)

    def batch(self, start, stop):
        """
        批量获取代理
        :param start:
        :param stop:
        :return:
        """
        return self.db.zrevrange(redis_key, start, stop)



