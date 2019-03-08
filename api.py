from flask import Flask,g
from db import RedisClient

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g,'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    return '<h2>welcome to Proxy Pool system</h2>'

@app.route('/random')
def get_proxy():
    '''
    获取随机可用代理
    :return:
    '''
    conn = get_conn()
    return conn.randomex()

@app.route('/count')
def get_counts():
    conn = get_conn()
    return conn.count()

if __name__ == '__main__':
    app.run()

