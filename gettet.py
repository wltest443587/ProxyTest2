from db import RedisClient
from crawler import Crawler

max_proxy =10000

class Gettet():
    def __init__(self):
        self.redis = RedisClient()
        self.crawl = Crawler()

    def is_over_proxy(self):
        '''
        判断是否达到代理池的极限
        :return:
        '''
        if self.redis.count() >= max_proxy:
            return True
        else:
            return False

    def run(self):
        print('获取器开始执行》》》》》》》》》》')
        if not self.is_over_proxy():
            print(1)
            for callbak_lable in range(self.crawl.__CrawlFuncCount__):
                print(2)
                callbak = self.crawl.__CrawlFunc__[callbak_lable]
                print(3)
                proxies = self.crawl.get_proxies(callbak)
                for proxy in proxies:
                    self.redis.add(proxy)

if __name__ == '__main__':
    scheduler = Gettet()
    scheduler.run() # 调度器运行