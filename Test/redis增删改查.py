import redis

class RedisClient:
    def __init__(self, host, port, db):
        self.client = redis.StrictRedis(host=host, port=port, db=db)

    #  String 类似键值对
    # 增加 self.client.set(name,value,ex,px,nx,xx,keepttl,get,exat,pxat)
    # 删除 client.delete('name')
    # 查 code = client.get('code').decode()

    def String_Case(self):
        self.client.set("String案例键","String案例值")      # 增
        data = self.client.get('String案例键').decode()    # 查
        print("String_案例 查询 ",data)
        self.client.set("String案例键", "String案例值2")    # 改
        data = self.client.get('String案例键').decode()    # 查
        print("String_案例 改 查询 ", data)
        self.client.delete('String案例键')                 # 删除

    # List
    # 增加 client.lpush(name, 'value1', 'value2', 'value3')  # 从左端插入元素
    # 增加 client.rpush(name, 'value1', 'value3')  # 从右端插入元素
    # 获取：length = client.llen('colors')   # 获取列表长度
    # 获取 colors1 = [client.lindex('colors', i).decode() for i in range(length)] # 通过索引获取元素，需要进行解码
    # 获取 colors2 = [client.lpop('colors').decode()  for _ in range(length)] # 从左端弹出元素，需要进行解码
    # 删除：client.delete('colors')

    def List_Case(self):
        self.client.lpush("list案例键", "String案例值")  # 增 # 从左端插入元素
        self.client.lpush("list案例键", 'readd1', 'readd2', 'readd3')  # 增 # 从左端插入元素
        self.client.rpush("list案例键", 'value1', 'value2', 'value3')  # 增 # 从右端插入元素
        length = self.client.llen('list案例键')  # 获取列表长度 # 查
        print("list案例键 的长度 : ", length)
        colors1 = [self.client.lindex('list案例键', i).decode() for i in range(length)]  # 通过索引获取元素，需要进行解码
        print("list案例键  : ", colors1)
        for i in range(length):
            value = self.client.lindex('list案例键', i).decode()
            print(" For i : ", i, ' value ', value)

        # colors2 = [self.client.lpop('list案例键').decode() for _ in range(length)]  # 从左端弹出元素，需要进行解码
        # print("list案例键  : ", colors2)
        colors2 = [self.client.rpop('list案例键').decode() for _ in range(length)]  # 从右端弹出元素，需要进行解码 # 拿出来相当于删除原来的
        print("list案例键  : ", colors2)

        self.client.delete('list案例键')

    def Hash_Case(self):
        print("  -------------Hash_Case--------------  ")
        self.client.hset('Hash案例键', 'title', 'Redis Tutorial')  # 存储单个字段

        # self.client.hset('Hash案例键', {'author': 'Alice',
        #                          'date': '2022-10-01'})  # 存储多个字段

        title = self.client.hget('Hash案例键', 'title').decode()  # 获取单个字段的值，需要解码
        details = self.client.hgetall('Hash案例键')  # 获取所有字段和值，返回字典类型
        #
        print(" Q:   ",title)  # 输出 Redis Tutorial
        print(" Q:   ",details)  # 输出 {b'title': b'Redis Tutorial',
        #
        self.client.hdel('Hash案例键',"title") # 删除指定字段

    # Set  存储：
    def Set_Case(self):
        print("  -------------Set_Case--------------  ")
        self.client.sadd('Set案例键', 'apple', 'banana', 'orange')  # 添加元素到集合

        length = self.client.scard('Set案例键')  # 获取集合中元素的数量
        print("length", length)  #
        fruits1 = [fruit.decode() for fruit in self.client.smembers('Set案例键')]  # 获取集合中所有元素，需要解码
        data = self.client.smembers('Set案例键')
        print("fruits1 ", fruits1)  # 输出 ['banana', 'orange', 'apple']
        print("data ", data)  # 输出 ['banana', 'orange', 'apple']
        fruits2 = []
        while True:
            fruit = self.client.spop('Set案例键')
            if not fruit:
                break
            fruits2.append(fruit.decode())  # 弹出并删除集合中的元素，需要解码

        print("fruits1", fruits1)  # 输出 ['banana', 'orange', 'apple']
        print("fruits1", fruits2)  # 输出 ['apple', 'banana', 'orange']，相当于把集合清空

    def Zset_Case(self):
        self.client.zadd('scores', {'Alice': 95, 'Bob': 85, 'Charlie': 75})  # 添加元素和分数到有序集合
        length = self.client.zcard('scores')  # 获取有序集合中元素的数量
        scores1 = [(name.decode(), score) for name, score in
                   self.client.zrange('scores', 0, -1, withscores=True)]  # 获取有序集合中所有元素和分数，需要解码

        print(self.client.zrange('scores', 1, 3))  # 需要解码
        self.client.delete('scores')
    def getAll(self):
        # 获取所有键值对
        print("----------获取所有键值对-----------")
        keys = self.client.scan_iter('*')
        data = {}
        for key in keys:
            key_type = self.client.type(key).decode()
            print("key_type ",key_type," key : ",key)
            if key_type == "string":
                data[key.decode()] = self.client.get(key).decode()
            elif key_type == "list":
                data[key.decode()] = [v.decode() for v in self.client.lrange(key, 0, -1)]
            elif key_type == "hash":
                data[key.decode()] = {k.decode(): v.decode() for k, v in self.client.hgetall(key).items()}
            elif key_type == "set":
                data[key.decode()] = [v.decode() for v in self.client.smembers(key)]
            elif key_type == "zset":
                data[key.decode()] = [(v.decode(), s) for v, s in self.client.zrange(key, 0, -1, withscores=True)]
        return data

if __name__ == '__main__':
    r = RedisClient(host='localhost', port=6379, db=0)
    # r.String_Case()
    # r.List_Case()
    # r.Hash_Case()
    # r.Set_Case()
    # r.Zset_Case()
    data = r.getAll()
    print("data" ,data)
    print(" --------------------------------------------- ")
    for key, value in data.items():
        print(key, ":", value)