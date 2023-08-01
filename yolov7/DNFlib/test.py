

import time

class asdm():

    def add(self,a,b):
        return a+b

    def sub(self,a,b):
        return a-b

    def mul(self,a,b):
        return a*b

    def div(self,a,b):
        return a/b

    def biant(self,hans):

        fa = 100
        fb = 5
        da = hans(fa,fb)
        print(da)

def add_func(a, b):
    return a + b


asd = asdm()
asd.biant(asd.sub)  # 调用 biant 方法，并传入 add_func 函数作为参数




