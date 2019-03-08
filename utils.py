from bs4 import BeautifulSoup
import urllib,time
import requests
import random
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}
def get_page(url):
    r = requests.get(url, headers = headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding  #获取网页正确的编码格式
    return r.text

def crawl_daili66(page_count = 4):
    '''
    获取代理66
    :param page_count: 页码
    :return: 代理
    '''

    url = 'https://www.xicidaili.com/nn/'
    html = get_page(url)
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(trs)):
        tds = trs[i].find_all('td')
        yield tds[1].text + ':' + tds[2].text

        #time.sleep(2)

crawl_daili66()