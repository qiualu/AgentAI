import torch
from torchvision import transforms
from yolov7-main.models import yolov as YOLOv7
from yolov7.utils import non_max_suppression, draw_bounding_boxes
import cv2
import numpy as np


import cv2
from PIL import ImageGrab
import numpy as np
import mss,math

# 获得所有窗口标题
from win32gui import *
import subprocess,random,socket
import json

范围DNF= [0,0,1600,900]

# "imageHeight": 900,
# "imageWidth": 1600
def 截屏(范围=None, 灰度=True):

    with mss.mss() as sct:
        # 设置需要捕获的区域（左上角坐标为(x1, y1)，宽度为width，高度为height）
        monitor = {"top": 范围[1], "left": 范围[0], "width": 范围[2], "height": 范围[3]}
        # 捕获屏幕特定位置
        screenshot = sct.grab(monitor)
        # 将PIL图像转换为NumPy数组
        image = np.array(screenshot)
        # 将图像转换为灰度图像
        if 灰度:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        # cv2.imwrite(path, image) # 保存
        return image

def shibie():
    # 加载模型
    model = YOLOv7()
    model.load_state_dict(torch.load("weights/dnf/last.pt"))
    model.cuda()
    model.eval()

    # 类别列表
    # classes = ["class1", "class2", "class3", ...]  # 根据实际类别进行替换
    classes = ["drop", "door", "foe", "role"]

    # 读取屏幕截图
    screenshot = cv2.imread("screenshot.png")

    # 对屏幕截图进行预处理
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((416, 416)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    input_tensor = transform(screenshot)
    input_tensor = input_tensor.unsqueeze(0).cuda()

    # 运行模型进行推理
    with torch.no_grad():
        predictions = model(input_tensor)

        # 使用非极大抑制进行后处理
    detections = non_max_suppression(predictions, conf_threshold=0.5, iou_threshold=0.5)

    # 在屏幕截图上绘制边界框和类别信息
    output_image = draw_bounding_boxes(screenshot, detections, classes)

    # 显示结果图像
    cv2.imshow("Object Detection", output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    print("123456")


if __name__ == '__main__':
    main()


