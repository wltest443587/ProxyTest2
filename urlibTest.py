import requests

user_agent = r'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
# Keep-Alive功能使客户端到服务器端的连接持续有效
headers = {'User-Agent': user_agent}
proxy = '127.0.0.1:9734'
proxy_handler = {
    'http': 'http://' + proxy,
    'https': 'http://' + proxy
}

try:
    req = requests.get('http://httpbin.org/get',proxies = proxy_handler,headers=headers)
    print(req.text)
except Exception as e:
    print(e)

