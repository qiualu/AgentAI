import warnings

x = 10
if x > 5:
    warnings.warn("x is greater than 5.") # 非致命错误提示


warnings.filterwarnings("ignore")
warnings.warn("x is 大多数都是 than 5.") # 非致命错误提示

# 在 warnings.filterwarnings() 函数中，可以指定多个参数来控制警告消息的处理方式。以下是部分常用的参数及其意义：
#
# action：设置警告的显示方式。常见的取值有：
#
# "error"：将警告消息转换为异常抛出。
# "ignore"：忽略警告消息，不进行任何处理。
# "always"：始终显示警告消息。
# "default"：使用默认行为显示警告消息。
# category：指定要过滤的警告类型。常见的取值有：
#
# Warning：所有警告的基类。
# DeprecationWarning：关于已弃用功能的警告。
# SyntaxWarning：关于语法问题的警告。
# RuntimeWarning：关于运行时可能出现问题的警告。
# 等等。

