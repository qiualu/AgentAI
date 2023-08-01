import argparse
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages,letterbox
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel

from PIL import ImageFont, ImageDraw, Image

import numpy as np
import torch


def showimages():


    # 读取图片
    image = cv2.imread(r'E:\Projece\python\AgentAI\Test\data\as.png')

    x, y, w, h = 100, 100, 200, 150  # 示例：框的左上角坐标 (x, y)，宽度 w 和高度 h
    color = (0, 255, 0)  # 指定框的颜色，示例为绿色（BGR）
    thickness = 2  # 指定线宽，示例为 2 像素
    # 在图像上绘制矩形框
    cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)

    text = "Example 中文种"  # 要显示的文字内容
    font = cv2.FONT_HERSHEY_SIMPLEX  # 字体类型
    font_scale = 1  # 字体缩放比例
    text_color = (255, 255, 255)  # 文字颜色，示例为白色（BGR）
    text_thickness = 1  # 文字线宽，示例为 1 像素

    # 在图像上显示文字
    cv2.putText(image, text, (x, y - 10), font, font_scale, text_color, text_thickness)


    cv2.imshow('Image', image)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

def showimages2():
    # 加载图片
    # image = cv2.imread('image.png')
    image = cv2.imread(r'E:\Projece\python\AgentAI\Test\data\as.png')

    # 定义矩形框的位置和大小
    x, y, w, h = 100, 100, 300, 300

    # 绘制矩形框
    color = (255, 255, 255)  # 绿色
    thickness = 2
    cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)

    # 转换图像为 PIL 格式
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # 创建 ImageDraw 对象
    draw = ImageDraw.Draw(pil_image)
    # E:\Projece\python\AgentAI\yolov7_dnf\DNFlib\simkai.ttf
    # 设置字体文件路径和大小
    font_path = 'DNFlib/simkai.ttf'  # 替换为实际的字体文件路径
    font_size = 20

    # 创建字体对象
    font = ImageFont.truetype(font_path, font_size)

    # 设置文字内容和颜色
    text = "示例文本"
    text_color = (255, 255, 255)  # 白色



    # 在图像上绘制中文文字
    draw.text((x + 10, y + 10), text, fill=text_color, font=font)

    # 将 PIL 图像转换回 OpenCV 格式
    result_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # 显示结果图像
    cv2.imshow('Image', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def imagetest():

    # source :   mask/test/images 640 32
    source = "mask/test/images"
    imgsz = 640
    stride = 32

    dataset = LoadImages(source)

    # 读取图片
    img0 = cv2.imread(r'E:\Projece\python\AgentAI\Test\data\as.png')
    print(" img0 : ",img0.shape)
    img = letterbox(img0, imgsz, stride=stride)[0]
    print(" img  : ",img.shape,img.shape[2])
    img = cv2.imread(r'E:\Projece\python\AgentAI\Test\data\as.png')
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    print(" img  : ",img.shape)
    # img0: (897, 1600, 3)
    # img: (384, 640, 3)


    # dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # for path, img, im0s, vid_cap in dataset:
    #     imgds = np.transpose(img, (1, 2, 0))
    #     print(" YL06 names : ", path, img.shape, type(img), im0s.shape, type(im0s), imgds.shape, type(vid_cap))
    # # 00001.jpg (3, 384, 640) <class 'numpy.ndarray'> (900, 1600, 3) <class 'numpy.ndarray'> (384, 640, 3) <class 'NoneType'>

def tensord():
    data = [[3.14750e+02, 2.76250e+02, 3.59250e+02, 3.07250e+02, 8.63281e-01, 0.00000e+00],
            [1.87875e+02, 2.36750e+02, 2.58000e+02, 2.77750e+02, 7.20215e-01, 0.00000e+00],
            [5.09250e+02, 2.12750e+02, 5.61000e+02, 2.87750e+02, 7.12891e-01, 1.00000e+00],
            [2.03000e+02, 1.20250e+02, 2.54250e+02, 2.11000e+02, 5.70801e-01, 1.00000e+00],
            [1.93750e+02, 2.53250e+02, 2.21250e+02, 2.77750e+02, 5.49805e-01, 0.00000e+00]]

    device = torch.device("cuda:0")  # 如果有 CUDA 设备可用，则将张量放在 CUDA 上

    tensor = torch.tensor(data, device=device)

    # print(type(tensor),tensor

    print(tensor[0])
    for i in range(len(tensor)):
        print(" i: ",i, " :: ",tensor[i],type(tensor[i]))
    print(" \n ")
    tensor_list = tensor.tolist()
    for i in range(len(tensor_list)):
        print(" i: ",i, " :: ",tensor_list[i],type(tensor_list[i]),len(tensor_list[i]))


# 识别图片文字
def ocr():
    from paddleocr import PaddleOCR, draw_ocr

    # img0 = cv2.imread(r'E:\Projece\python\AgentAI\yolov7_dnf\mask\train\images\00031.jpg')
    image_path = r'E:\Projece\python\AgentAI\yolov7_dnf\mask\train\images\00031.jpg'
    # 初始化 PaddleOCR
    ocr = PaddleOCR(use_gpu=False, lang='ch')

    to = time.time()

    # 读取图像
    # image_path = 'example.jpg'
    image = ocr.ocr(image_path)

    # 提取识别结果和位置
    result = image[0]
    print(result)
    # text_boxes = result['text_boxes']
    # texts = [box[-1] for box in text_boxes]

    # 绘制识别结果
    # output_image = draw_ocr(image_path, text_boxes, texts)

    # 显示结果
    # output_image.show()
    # [[[[43.0, 179.0], [82.0, 179.0], [82.0, 192.0], [43.0, 192.0]], ('艾草羽', 0.8366004824638367)]]

    t1 = time.time() - to
    print("t时间1 : ", t1)

def ocr2():
    from paddleocr import PaddleOCR, draw_ocr


    # 初始化 PaddleOCR
    ocr = PaddleOCR(use_gpu=True, lang='ch')

    # 读取图像
    # image_path = 'example.jpg'
    image_path = r'E:\Projece\python\AgentAI\yolov7_dnf\mask\train\images\00031.jpg'
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    to = time.time()
    # 进行文本识别
    result = ocr.ocr(image_bytes)
    print(result)
    # # 获取识别结果中的文本框信息
    # boxes = [line[-1] for line in result]
    #
    # # 调整文本框框架形状
    # adjusted_boxes = ocr.adjust_text_boxes(boxes, image_bytes.shape[:2])
    #
    # # 使用调整后的文本框进行识别
    # result = ocr.ocr(image_bytes, text_box=adjusted_boxes)
    #
    # # 绘制识别结果
    # output_image = draw_ocr(image_bytes, result)
    #
    # # 显示结果
    # output_image.show()

    t1 = time.time() - to
    print("t时间2 : ", t1)

ocr2()

ocr()

# tensord()
# imagetest()

# showimages()
# showimages2()

'''
<class 'torch.Tensor'> <class 'int'> 0 5 tensor([[3.14750e+02, 2.76250e+02, 3.59250e+02, 3.07250e+02, 8.63281e-01, 0.00000e+00],
        [1.87875e+02, 2.36750e+02, 2.58000e+02, 2.77750e+02, 7.20215e-01, 0.00000e+00],
        [5.09250e+02, 2.12750e+02, 5.61000e+02, 2.87750e+02, 7.12891e-01, 1.00000e+00],
        [2.03000e+02, 1.20250e+02, 2.54250e+02, 2.11000e+02, 5.70801e-01, 1.00000e+00],
        [1.93750e+02, 2.53250e+02, 2.21250e+02, 2.77750e+02, 5.49805e-01, 0.00000e+00]], device='cuda:0')

<class 'torch.Tensor'> tensor([[3.14750e+02, 2.76250e+02, 3.59250e+02, 3.07250e+02, 8.63281e-01, 0.00000e+00],
        [1.87875e+02, 2.36750e+02, 2.58000e+02, 2.77750e+02, 7.20215e-01, 0.00000e+00],
        [5.09250e+02, 2.12750e+02, 5.61000e+02, 2.87750e+02, 7.12891e-01, 1.00000e+00],
        [2.03000e+02, 1.20250e+02, 2.54250e+02, 2.11000e+02, 5.70801e-01, 1.00000e+00],
        [1.93750e+02, 2.53250e+02, 2.21250e+02, 2.77750e+02, 5.49805e-01, 0.00000e+00]], device='cuda:0')
        
'''

