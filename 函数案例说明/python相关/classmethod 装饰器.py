class MyClass:
    count = 0
    count2 = 0

    def __init__(self):
        MyClass.count += 1
        self.count2 += 1

    @classmethod
    def get_count(cls):
        return cls.count

    def get_count2(self):
        return self.count2

# 使用类方法
print(MyClass.get_count())  # 输出: 0

obj1 = MyClass()
print(obj1.get_count())  # 输出: 1

obj2 = MyClass()
print(obj2.get_count())  # 输出: 2


# obj1 = MyClass()
print(obj1.get_count2())  # 输出: 2

# obj2 = MyClass()
print(obj2.get_count2())  # 输出: 2

