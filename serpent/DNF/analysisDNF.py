


import threading
import socket, time

import pyautogui,os

from serpent.DNF.windows import windows

import cv2 , random
from PIL import ImageGrab
import numpy as np,math
import mss


key_mapping = {
    "up": 0xDA,
    "down": 0xD9,
    "left": 0xD8,
    "right": 0xD7,
    "ctrl": 0x80,
    "shift": 0x81,
    "alt": 0x82,
    "tab": 0xB3,
    "backspace": 0xB2,
    "enter": 0xB0,
    "esc": 0xB1,
    "space": 32
}

guan8 = [
    [31, 104, [236, 191, 12]],
    [31, 86, [229, 184, 4]],
    [13, 86, [229, 184, 4]],
    [13, 68, [236, 191, 12]],
    [31, 68, [230, 186, 6]],
    [49, 68, [229, 185, 5]],
    [49, 86, [236, 191, 12]],
    [31, 50, [236, 191, 12]]
]




import math

# 像素相似度
def rgb_similarity2(c1,c2):
    b1, g1, r1 = c1
    b2, g2, r2 = c2
    # print(r1,g1,b1,r2,g2,b2)
    diff_r = r1 - r2
    diff_g = g1 - g2
    diff_b = b1 - b2
    distance = math.sqrt(diff_r ** 2 + diff_g ** 2 + diff_b ** 2)
    similarity = 1 - (distance / math.sqrt(255 ** 2 + 255 ** 2 + 255 ** 2))
    return similarity

def rgb_similarity(image, y1, x1, y2, x2):
    b1, g1, r1 = image[y1, x1]
    b2, g2, r2 = image[y2, x2]

    diff_r = r1 - r2
    diff_g = g1 - g2
    diff_b = b1 - b2

    distance = math.sqrt(diff_r ** 2 + diff_g ** 2 + diff_b ** 2)
    similarity = 1 - (distance / math.sqrt(255 ** 2 + 255 ** 2 + 255 ** 2))

    return similarity

class DNFmanage(windows):
    def __init__(self):
        super().__init__()
        self.running = False

        # 二值化的阀值
        self.threshold_value = 136  # 阈值
        self.max_value = 255  # 设置的最大值

    def openDNF(self):
        print("")
    def start(self):
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self.DNF_loop)
            thread.start()
    # DNF_loop
    def stop(self):
        print("stop DNF 循环")
        self.running = False



    def DNF_loop(self):
        folder_path = r"E:\Projece\python\SerpentAI\AgentAI\serpent\DNF\data\image\dataji"  # 替换成你的文件夹路径
        image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        self.img_index = 0
        self.read_img = True
        self.print_img8 = False
        image_path = os.path.join(folder_path, image_files[self.img_index])
        image = cv2.imread(image_path)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 灰度
        resized_image = cv2.resize(image, (image.shape[1] * 10, image.shape[0] * 10))

        def click_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:  # 当鼠标左键按下时
                # 获取放大后的坐标
                resized_x, resized_y = math.ceil(x / 10), math.ceil(y / 10)

                # 获取点击位置的像素值
                pixel_value = resized_image[y, x]
                pixel_valuey = image[resized_y, resized_x]

                # 输出当前的坐标和 RGB 值
                print(
                    f"Clicked at ({x}, {y}) 放大的 : {pixel_value}  {resized_x}, {resized_y}原来的: {pixel_valuey}  ")

        # 创建窗口并显示图像
        cv2.namedWindow('Image')
        cv2.imshow('Image', resized_image)
        cv2.moveWindow('Image', 1000, 100)
        # 设置鼠标回调函数
        cv2.setMouseCallback('Image', click_event)


        while True:

            if self.read_img:
                self.read_img = False
                if self.img_index <= len(image_files) - 1:
                    image_path = os.path.join(folder_path, image_files[self.img_index])
                    # print("image_path : ",image_path)
                    image = cv2.imread(image_path)
                    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 灰度
                    resized_image = cv2.resize(image, (image.shape[1] * 10, image.shape[0] * 10))
                else:
                    print("文件读取完成")

            # 创建窗口并显示图像
            cv2.namedWindow('Image')
            cv2.imshow('Image', resized_image)
            # cv2.moveWindow('Image', 1000, 100)
            # 设置鼠标回调函数
            # cv2.setMouseCallback('Image', click_event)
            # indexa = 1
            # if self.print_img8:
            #     print(" 八个关卡的当前值 : ",end="")
            #     self.print_img8 = False
            #     for zxy in guan8:
            #         pixel_valuey = image[zxy[1], zxy[0]]
            #         print(indexa," ",pixel_valuey, "  " ,end="")
            #         indexa += 1
            #     print("")
            indexa = 1
            if self.print_img8:
                print("八个关卡的当前值:", end="")
                self.print_img8 = False
                for zxy in guan8:
                    pixel_valuey = image[zxy[1], zxy[0]]
                    print("{} [{:<3d}, {:<3d}, {:<3d}]".format(indexa, pixel_valuey[0], pixel_valuey[1], pixel_valuey[2]),
                          end="   ")
                    indexa += 1
                print("")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # guan8

            if not self.running:
                print("退出udp 按键线程")
                break




    def 跑图线程(self,zl):
        if self.跑图停止:
            self.跑图(zl)  # 启动游戏循环

    def udpKey(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 设置超时时间为 5 秒
        timeout = 2.0
        sock.settimeout(timeout)
        server_address = ('0.0.0.0', 8846)
        sock.bind(server_address)
        gu = True
        jindex = 1
        keylist = []
        while True:
            try:
                data, address = sock.recvfrom(1024)
                command = data.decode()[:-1]
                key = command.split(":")

                keyname = key[1]
                if keyname == "+" or keyname == "-":
                    if gu:
                        print("keylist: ",keylist)
                        gu = False
                        self.key记录[str(jindex)] = keylist
                        jindex += 1
                        keylist = []
                    continue

                gu = True
                if len(keyname) == 1:
                    ds = ord(keyname)
                elif keyname in key_mapping:
                    ds = key_mapping[keyname]
                else:
                    continue
                btn = int(key[2])
                times = int(key[3])

                keylist.append([key[1],btn,times,ds])

                print(key[1][:1],end="")
                data = f"key,{btn},{ds},0\n"  # 释放所有按键
                self.send_udp_data(data)

            except socket.timeout:
                # 发生超时
                # print("Timeout occurred")
                if not self.running:
                    print("退出udp 按键线程")
                    break
        # 关闭套接字
        sock.close()

    def udp_loop(self):



        # 创建UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('0.0.0.0', 8848)
        sock.bind(server_address)

        while True:
            data, address = sock.recvfrom(1024)
            # command = data.decode()

            # print('从客户端', address, '接收到数据:', data.decode()[:-1])
            zl = data.decode()[:-1]

            # 根据接收到的命令控制while循环的状态
            if zl == "1":
                self.start() # 启动游戏循环
            elif zl == "2":
                self.stop()  # 停止游戏循环
            elif zl == "3":  # 退出整个程序
                self.stop()
                break
            elif zl == "4":  # 退出整个程序
                self.img_index += 1
                self.read_img = True

            elif zl == "5":  # 退出整个程序
                self.img_index -= 1
                if  self.img_index < 0:
                    self.img_index = 0
                self.read_img = True

            elif zl == "6":  # 退出整个程序
                    self.print_img8 = True

            elif zl == "7":  # 游戏结束，退出整个程序
                current_x, current_y = pyautogui.position()
                print("当前鼠标位置 : ",current_x, current_y)
            elif zl == "8":  # 游戏结束，退出整个程序
                self.激活句柄窗口(self.DNF_id)
            elif zl == "9":  # 游戏结束，退出整个程序
                self.threshold_value += 1
                print("更改阀值 : ", self.threshold_value)

            elif zl == "10":  # 游戏结束，退出整个程序
                self.threshold_value += 1
                print("更改阀值 : ", self.threshold_value)
            elif zl == "11":  # 游戏结束，退出整个程序
                print("\n****************\n")
                print(self.key记录)
                print("\n****************\n")

        # 关闭套接字
        sock.close()




if __name__ == '__main__':
    # Create an object
    DNF = DNFmanage()
    # DNF.openDNF()
    # DNF.udp_loop()

    sd = [[38, 53, 57], [52, 67, 80]]
    print(rgb_similarity2(sd[0],sd[1]))
'''

1 31, 104原来的: [236 191  12]  
2 31, 86原来的: [229 184   4]  
3 13, 86原来的: [229 184   4]
4 13, 68原来的: [236 191  12]  
5 31, 68原来的: [230 186   6]  
6 49, 68原来的: [229 185   5]  
7 49, 86原来的: [236 191  12]  
8 31, 50原来的: [236 191  12]  

# 左上牛角
26, 28 原来的: [  2  48 229]  

? 
[66,76,99],[ 87,100,130],[51,62,71]


[45 36  1]
[230 186   6]
[170 138   4]
[92 74  2]

[56 68 77]

 1 : 
[ 97 108 118]


[47 35 33]   [47 35 33]   [ 0 11  6]   [17 17 11]   [21 20 13]   [ 0 11  4]  

'''


























