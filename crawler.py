import json
from utils import get_page
from lxml import etree
from bs4 import BeautifulSoup

class ProxyMetaclass(type):
    '''
    定义元类
    '''
    def __new__(cls, name,bases,attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls,name,bases,attrs)


class Crawler(object,metaclass=ProxyMetaclass):
    '''
    第一：元类的attrs参数，来自定义类的所有属性。
    第二：自定义的类proxy mataclass的attrs属性，额外添加了两个属性：
          一个是’__crawlfunc__'属性，其对应的值为列表，用来存储包含crawl_字段的所有属性名称。
          另一个额外的属性是"__crawlcount__",对应的值，存储了crawlfunc属性的个数。

    '''
    def get_proxies(self,callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            print('成功获取到代理:',proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self,page_count = 22):
        '''
        获取代理66
        :param page_count: 页码
        :return: 代理
        '''
        urls = ['http://www.66ip.cn/{}.html'.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('获取代理：',url)
            html = get_page(url)
            if html:
                doc = etree.HTML(html)
                ip = doc.xpath('//div[@align="center"]//table//tr[position()>1]//td[1]/text()')
                port = doc.xpath('//div[@align="center"]//table//tr[position()>1]//td[2]/text()')
                ip_port = list(zip(ip, port))
                for ip, port in ip_port:
                    yield ':'.join([ip, port])



    def crawl_xici(self):
        url = 'https://www.xicidaili.com/nn/'
        html = get_page(url)
        soup = BeautifulSoup(html, 'lxml')
        trs = soup.find_all('tr')
        ip_list = []
        for i in range(1, len(trs)):
            tds = trs[i].find_all('td')
            yield tds[1].text + ':' + tds[2].text
