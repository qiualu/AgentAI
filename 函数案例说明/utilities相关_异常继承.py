

class SerpentError(BaseException):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code

    def __str__(self):
        return f"错误代码: {self.error_code}, 错误消息: {self.message}"

    def log_error(self):
        # 在这里执行将错误信息记录到日志文件或发送给开发者的操作
        print("log : ",self.message,self.error_code)
        pass

# 抛出错误
def divide(a, b):
    if b == 0:
        raise SerpentError("发生了一个错误", 500)
    return a / b

def 调试错误():
    try:
        result = divide(10, 0)
    except SerpentError as e:
        print(e)  # 打印错误消息和错误代码
        e.log_error()  # 记录错误到日志文件

    z做 = "fsf"


if __name__ == '__main__':
    调试错误()