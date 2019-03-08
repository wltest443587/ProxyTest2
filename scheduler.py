from multiprocessing import Process
from api import app
from tester import Tester
from gettet import Gettet
import time

tester_cycle = 20 # 测试模块运行的间隔
getter_cycle = 20  # 获取模块运行间隔
tester_enabled = True # 测试模块开关
getter_enable = True  # 获取模块开关
api_enabled = True # 接口模块开关


class Scheduler():
    def scheduler_tester(self,cycle = tester_cycle):
        '''
        定时测试代理
        :param cycle:
        :return:
        '''
        tester = Tester()
        while True:
            print('测试器开始调度，运行。。。')
            tester.run()
            time.sleep(cycle)

    def scheduler_getter(self,cycle = getter_cycle):
        '''
        定时获取代理
        :param cycle:
        :return:
        '''
        getter = Gettet()
        while True:
            print('开始抓取代理..........')
            getter.run()
            time.sleep(cycle)

    def scheduler_api(self):
        '''
        开启API
        :return:
        '''
        print('开启API')
        app.run('127.0.0.1',3333)

    def run(self):
        print('调度器开始运行')
        if getter_enable:
            getter = Process(target=self.scheduler_getter)
            getter.start()
        if tester_enabled:
            tester = Process(target = self.scheduler_tester)
            tester.start()
        if api_enabled:
            api = Process(target=self.scheduler_api)
            api.start()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run() # 调度器运行