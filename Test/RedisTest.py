import redis,time

def 测试是否安装成功(): # 测试是否安装成功：

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set('foo', 'bar')

    print(r.get('foo'))  # 输出结果>>>'bar'

# redis 提供两个类 Redis 和 StrictRedis, StrictRedis 用于实现大部分官方的命令，Redis 是 StrictRedis 的子类，用于向后兼用旧版本。
# redis 取出的结果默认是字节，我们可以设定 decode_responses=True 改成字符串。
def 使用案例():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.set('name', 'runoob')  # 设置 name 对应的值
    r.set('nameds', 'runoonamedsb')  # 设置 name 对应的值
    print(r)
    print(r.get('name'),r.get('nameds'))  # 取出键 name 对应的值
    print(type(r.get('name')))  # 查看类型

# 测试是否安装成功()
# 使用案例()

# 连接池
# redis-py 使用 connection pool 来管理对一个 redis server 的所有连接，避免每次建立、释放连接的开销。
# 默认，每个Redis实例都会维护一个自己的连接池。可以直接建立一个连接池，然后作为参数 Redis，这样就可以实现多个 Redis 实例共享一个连接池。

def 连接池():

    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.set('namelj', 'runonameljob')  # 设置 name 对应的值
    print(r.get('namelj'))  # 取出键 name 对应的值

# 连接池()

def redis模块常用操作():
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.set('gender', 'runonameljob')  # 设置 name 对应的值
    print(r.get('gender'))  # 取出键 name 对应的值

    # 1. 删除

    # delete(*names)
    # 根据删除redis中的任意数据类型（string、hash、list、set、有序set）
    r.delete("gender")  # 删除key为gender的键值对

    # 2. 检查名字是否存在

    # exists(name)
    # 检测redis的name是否存在，存在就是True，False 不存在
    print(r.exists("zset1"))

    # 3.模糊匹配

    # 复制代码
    # keys(pattern='')

    #根据模型获取redis的name

    #更多：

    #KEYS * 匹配数据库中所有 key 。
    #KEYS h?llo 匹配 hello ， hallo 和 hxllo 等。
    #KEYS hllo 匹配 hllo 和 heeeeello 等。
    #KEYS h[ae]llo 匹配 hello 和 hallo ，但不匹配 hillo

    print(r.keys("foo*"))

    # 4.设置超时时间

    # 复制代码
    # expire(name ,time)

    #为某个redis的某个name设置超时时间

    r.lpush("list5", 11, 22)
    r.expire("list5", time=3)
    print(r.lrange("list5", 0, -1))
    time.sleep(3)
    print(r.lrange("list5", 0, -1))

redis模块常用操作()
