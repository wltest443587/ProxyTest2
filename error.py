class PoolEmptyerror(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        '''
        repr() 函数将对象转化为供解释器读取的形式,返回一个对象的 string 格式。
        :return:
        '''
        return repr('代理池已经枯竭')