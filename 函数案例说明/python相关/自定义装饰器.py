def timeit(func):
    import time

    def wrapper(*args, **kwargs):
        start_time = time.time()

        print(" 接收到得函数参数 : ",type(args[0]),type(args[0]),args[0], **kwargs)
        sf = int(args[0])
        if  sf == 10:
            print("确定参数")
            # *args = 100
            new_args = (100,)  # 创建一个包含新参数的元组
        result = func(*new_args, **kwargs)
        # result = func(*args, **kwargs)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"函数 {func.__name__} 的执行时间为：{execution_time} 秒")
        return result

    return wrapper


@timeit
def calculate_factorial(n):
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
    return factorial


result = calculate_factorial(10)
print(result)


