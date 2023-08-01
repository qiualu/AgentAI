import sys
print(sys.path)







import numpy as np
import cv2

# 读取图片
# image = cv2.imread(r'E:\Projece\python\AgentAI\Test\data\as.png')
image = cv2.imread(r'E:\Projece\python\AgentAI\yolov7\mask\train\images\00031.jpg')

# 检查是否成功读取图片
if image is not None:
    # 图片读取成功
    # 进行后续操作，比如显示、处理等
    print("image ",type(image),image.shape)

    # 转换为形状 (3, 897, 1600)
    arr_transposed = np.transpose(image, (2, 0, 1))
    print("color ", type(arr_transposed), arr_transposed.shape)
    # 转换回形状 (897, 1600, 3)
    arr_reshaped = np.transpose(arr_transposed, (1, 2, 0))

    print("color ", type(arr_reshaped), arr_reshaped.shape)
    # cv2.imshow('Image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
else:
    # 图片读取失败
    print('无法读取图片')


 # <class 'numpy.ndarray'>

# <class 'numpy.ndarray'> (897, 1600, 3)
#
# 怎么互相转换
#
# class 'numpy.ndarray'> (3 , 897, 1600)