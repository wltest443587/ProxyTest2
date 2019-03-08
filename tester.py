import asyncio
import aiohttp
from db import RedisClient
import time
import sys

valid_status_codes = [200]
test_url = 'http://www.baidu.com'
batch_test_size = 100

class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self,proxy):
        '''
        测试单个代理
        :param proxy: 单个代理
        :return: None
        '''
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                # 判断一个对象是否是一直类型
                if isinstance(proxy,bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://'+proxy
                print('正在测试...')
                async with session.get(test_url,proxy=real_proxy,timeout=15) as response:
                    if response.status in valid_status_codes:
                        self.redis.max(proxy) # 代理可用，代理设置为最大值
                        print('代理可用')
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应码不合法，代理检测失败')
            except Exception as e:
                self.redis.decrease(proxy)
                print('代理请求失败',proxy)

    def run(self):
        '''
        测试主函数
        :return: None
        '''
        print('测试器开始运行>>>>>>')
        try:
            proxie = self.redis.all()  # 获取全部代理
            loop = asyncio.get_event_loop()
            # asyncio实现并发，就需要多个协程组成列表来完成任务【创建多个协程的列表，然后将这些协程注册到事件循环中】，
            # 每当有任务阻塞的时候就await，然后其他协程继续工作，所以下面是协程列表；
            # 所谓的并发：多个任务需要同时进行；

            # 批量测试
            for i in range(0,len(proxie),batch_test_size):
                test_proxies = proxie[i:i + batch_test_size]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
            print('检测完成')

        except Exception as e:
            print('测试发生错误！！',e)
