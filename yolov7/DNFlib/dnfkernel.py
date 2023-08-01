import numpy as np
import mss
from numpy import random
import cv2, math
from PIL import ImageFont, ImageDraw, Image
import subprocess, random, socket
import json, win32gui, time,threading

# from win32gui import *
from win32gui import IsWindow, IsWindowEnabled, IsWindowVisible, GetWindowText, EnumWindows

from yolov7.DNFlib.window_controllers.win32_window_controller import Win32WindowController

import os

names = [ '掉落物', '通关门', '怪', '角色']

# E:\Projece\python\AgentAI\yolov7_dnf\DNFlib\simkai.ttf

font_path = 'E:/Projece/python/AgentAI/yolov7/DNFlib/simkai.ttf'  # 替换为实际的字体文件路径
font_size = 20  # 字体大小
text_color = (255, 255, 255)  # 字体 白色

# 绘制矩形框
color = (255, 255, 255)  # 绿色
thickness = 2 # 线宽

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


class kernelapi():

    def __init__(self):
        self.windows_manage = Win32WindowController()

        # 存储游戏状态
        self.zt = {}

        self.init_window_id()

        self.fangan = True # 切换按键 库


        # self.UDP_IP = "192.168.0.105"
        self.UDP_IP = "192.168.0.100"
        self.UDP_PORT = 8888

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


        self.zt = self.DNF_btn["角色状态"]
        print("角色状态 : ", self.zt)
    def init_window_id(self):

        self.跑图按键 = None
        self.跑图停止 = True
        self.跑图暂停 = False
        self.xunhuan = 0
        self.light = 0
        self.index = 0


        self.初始化跑图按键()
        # 读取 JSON 文件
        print("os : ",os.getcwd())
        with open('DNFlib/data/配置文件.json', 'r', encoding="utf-8") as file:
            json_data = file.read()
        # 将 JSON 数据解析为字典
        self.DNF_btn = json.loads(json_data)  # 地下城信息

        with open('DNFlib/data/通关按键/王之摇篮.json', 'r', encoding="utf-8") as file:
            json_data = file.read() # DNFlib/data/通关按键/王之摇篮.json
        self.keyjson = json.loads(json_data)  # 地下城信息
        with open('DNFlib/data/通关按键/王之摇篮.json', 'r', encoding="utf-8") as file:
            json_data = file.read()
        self.keyjson2 = json.loads(json_data)  # 地下城信息



        self.runloop_DNF_loop = False
        self.runloop_udpKey_loop = False
        self.runloop_udp跑图loop = False
        # ----------
        self.udpKey_loop_keyindex = 1
        self.udpKey_loop_gu = True
        self.udpKey_loop_keylist = []
        self.key记录 = {}

        self.udp跑图loopKeyindex = 1
        self.udp跑图loopKeylist = []
        self.udp跑图loopKeyrun = False
        self.allkey = True
        self.printKey = True

    def send_udp_data(self,data):
        # 创建UDP套接字
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 发送数据
        self.sock.sendto(data.encode(), (self.UDP_IP, self.UDP_PORT))
        # 关闭套接字
        # sock.close()

    def 截屏(self, 截屏类型= "区域", path=None, 范围= [0,0,1600,900], 灰度=False):

        if not path:
            path = "data/udp/" + 截屏类型 + str(random.randint(1000, 10000)) + ".png"

        if 截屏类型 == "全屏":
            screenshot = ImageGrab.grab()
            # 转换为OpenCV图像格式（BGR）
            image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            cv2.imwrite(path, image)  # 保存

        elif 截屏类型 == "区域" or 截屏类型 == "区域截屏":
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

    def 显示图片(self,image,ssize,lt):

        # image = cv2.resize(image, (int(image.shape[1] / ssize), int(image.shape[0] / ssize)))
        # scale_x = 900 / 384 ≈ 2.34375
        # scale_y = 1600 / 640 = 2.5

        # names: [ '掉落物', '通关门', '怪', '角色']
        # names: ['drop', 'door', 'foe', 'role']
        for i in range(len(lt)):
            print( "  lt : ", int(lt[i][0]), int(lt[i][1]), int(lt[i][2]), int(lt[i][3]))
            # cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
            cv2.rectangle(image, (int(lt[i][0]), int(lt[i][1])), (int(lt[i][2]), int(lt[i][3])), color, thickness)

        # 转换图像为 PIL 格式
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        for i in range(len(lt)):
            sbname = names[int(lt[i][5])] + str(round(lt[i][4], 3))
            # 创建 ImageDraw 对象
            # 设置字体文件路径和大小
            # 创建字体对象
            font = ImageFont.truetype(font_path, font_size)
            # 设置文字内容和颜色
            # text = "示例文本"
            # 在图像上绘制中文文字
            draw.text((int(lt[i][0]) + 10, int(lt[i][1]) + 10), sbname, fill=text_color, font=font)

        # 将 PIL 图像转换回 OpenCV 格式
        result_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return result_image

    def start_udpKey_loop(self):
        if not self.runloop_udpKey_loop:
            print("开启 udpKey_loop 线程")
            self.runloop_udpKey_loop = True
            # 创建并启动处理while循环的线程
            thread = threading.Thread(target=self.udpKey_loop)
            thread.start()

    def stop_udpKey_loop(self):
        self.runloop_udpKey_loop = False

    def udpKey_loop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 设置超时时间为 5 秒
        timeout = 2.0
        sock.settimeout(timeout)
        server_address = ('0.0.0.0', 8846)
        sock.bind(server_address)

        TimeTD = time.time()

        while True:
            try:
                data, address = sock.recvfrom(1024)
                command = data.decode()[:-1]
                key = command.split(":")

                keyname = key[1]
                if keyname == "+" or keyname == "-":
                    #//id += 1
                    if self.udpKey_loop_gu:
                        print("keylist: ",self.udpKey_loop_keylist)
                        self.udpKey_loop_gu = False
                        self.key记录[str(self.udpKey_loop_keyindex)] = self.udpKey_loop_keylist
                        self.udpKey_loop_keyindex += 1
                        self.udpKey_loop_keylist = []
                    continue

                if keyname == "*":
                    print(" 记录标号 : ", str(self.udpKey_loop_keyindex))
                    self.udpKey_loop_keylist = []
                    continue

                self.udpKey_loop_gu = True
                if len(keyname) == 1:
                    ds = ord(keyname)
                elif keyname in key_mapping:
                    ds = key_mapping[keyname]
                else:
                    continue
                btn = int(key[2])


                # times = int(key[3])
                if len(self.udpKey_loop_keylist) == 0:
                    TimeTD = time.time()
                    qish = 0
                else:
                    etimes = time.time()
                    qish = etimes - TimeTD
                    TimeTD = etimes
                qish = round(qish, 3)

                self.udpKey_loop_keylist.append([key[1],btn,qish,ds])

                print(key[1][:1],end="")

                data = f"key,{btn},{ds},0\n"  # 释放所有按键
                #print("data : ",data, " [] ", [key[1], btn, times, ds])
                self.send_udp_data(data)

            except socket.timeout:
                # 发生超时
                # print("Timeout occurred")
                if not self.runloop_udpKey_loop:
                    print("退出udp 按键线程")
                    break
        # 关闭套接字
        sock.close()


    def start_DNF_loop(self):
        if not self.runloop_DNF_loop:
            self.runloop_DNF_loop = True
            # 创建并启动处理while循环的线程
            thread = threading.Thread(target=self.DNF_loop)
            thread.start()

    def stop_DNF_loop(self):
        self.runloop_DNF_loop = False

    def DNF_loop(self):
        print(" DNF 开始 工作")
        grid = self.windows_manage.get_window_geometry(self.dnf_id)
        王之摇篮通关提示区 = self.DNF_btn["关卡"]["毁坏的寂静城"]["王之摇篮"]["通关提示区"]
        print("grid", grid, "通关提示区", 王之摇篮通关提示区)
        通关提示区 = [1,1,grid["width"],grid["height"]]
        通关提示区[0] = 王之摇篮通关提示区[0] + grid["x_offset"]
        通关提示区[1] = 王之摇篮通关提示区[1] + grid["y_offset"]
        通关提示区[2] = 王之摇篮通关提示区[2] - 王之摇篮通关提示区[0]
        通关提示区[3] = 王之摇篮通关提示区[3] - 王之摇篮通关提示区[1]
        print(" 通关提示区 : ", 通关提示区)
        path = "data/image/Yg"

        # 检查文件夹是否已存在
        if not os.path.exists(path):
            os.mkdir(path)

        # 当前 rgb
        当前 = self.DNF_btn["关卡"]["毁坏的寂静城"]["王之摇篮"]["当前"][0]
        通关坐标 = self.DNF_btn["关卡"]["毁坏的寂静城"]["王之摇篮"]["通关坐标"]
        index = 1000
        while self.running:

            gray_image = self.截屏("区域", 范围=通关提示区, 灰度=False)
            filepath = path + "/" + str(index) + ".png"
            index += 1
            cv2.imwrite(filepath, gray_image)  # 保存

            # _, binary_image = cv2.threshold(gray_image, self.threshold_value, self.max_value, cv2.THRESH_BINARY)
            kong = True
            for i in range(len(通关坐标)):
                xy = 通关坐标[i]
                pixel_value = gray_image[xy[1], xy[0]]
                #print("xy : ", xy,当前,pixel_value)
                cy = self.像素差异度(当前,pixel_value)
                if cy > 0.9:
                    kong = False
                    print("当前关卡 : " , i + 1)
                    break
            if kong:
                print("当前关卡 : 空 无状态")
            # 显示截图

            cv2.imshow('Continuous Screenshot', gray_image)
            cv2.resizeWindow('Continuous Screenshot', 300, 300)
            cv2.moveWindow('Continuous Screenshot', 2046, 24)
            # 按下 'q' 键退出循环
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

            if not self.runloop_DNF_loop:
                print("退出 DNF_loop 按键线程")
                break
        # 关闭窗口和摄像头
        cv2.destroyAllWindows()
        # screencap.release()

    def 像素差异度(self,c1, c2):
        if len(c1) == 3:
            b1, g1, r1 = c1
        else:
            b1, g1, r1, a = c1
        if len(c2) == 3:
            b2, g2, r2 = c2
        else:
            b2, g2, r2, a = c2


        # print(r1,g1,b1,r2,g2,b2)
        diff_r = r1 - r2
        diff_g = g1 - g2
        diff_b = b1 - b2
        distance = math.sqrt(diff_r ** 2 + diff_g ** 2 + diff_b ** 2)
        similarity = 1 - (distance / math.sqrt(255 ** 2 + 255 ** 2 + 255 ** 2))
        return similarity



    # E:\Projece\python\AgentAI\yolov7\DNFlib\data\通关按键\王之摇篮.json
    def 初始化跑图按键(self,filepath ='DNFlib/data/通关按键/王之摇篮.json'): # self.跑图按键控制台
        # 读取 JSON 文件
        with open(filepath, 'r', encoding="utf-8") as file:
            json_data = file.read()
        # 将 JSON 数据解析为字典
        self.跑图按键 = json.loads(json_data)  # 地下城信息

        filepath = 'DNFlib/data/通关按键/王之摇篮2.json'
        with open(filepath, 'r', encoding="utf-8") as file:
            json_data = file.read()
        # 将 JSON 数据解析为字典
        self.跑图按键2 = json.loads(json_data)  # 地下城信息

    def start_udp跑图loop(self):
        if not self.runloop_udp跑图loop:
            print(" start_udp跑图loop 开始线程 ")
            self.runloop_udp跑图loop = True
            # 创建并启动处理while循环的线程
            thread = threading.Thread(target=self.udp跑图loop)
            thread.start()

    def stop_udp跑图loop(self):
        self.runloop_udp跑图loop = False

    def allkeyup(self):
        if self.allkey:
            self.allkey = False
            print(" : allkey ")
            data = f"key,4,0,0\n"  # 释放所有按键
            self.send_udp_data(data)
    def udp跑图loop(self):

        # self.udp跑图loopKeyindex = 0
        # self.udp跑图loopKeylist = []
        # self.udp跑图loopKeyrun = True
        self.allkey = True
        while True:
            if not self.runloop_udp跑图loop:
                print("退出 udp跑图loop 按键线程")
                self.allkeyup()
                break
            length = len(self.udp跑图loopKeylist)
            if self.udp跑图loopKeyindex > length - 1:
                self.udp跑图loopKeyrun = False
                self.udp跑图loopKeyindex = 0
                time.sleep(0.1)
                self.allkeyup()
                continue
            if not self.udp跑图loopKeyrun:
                time.sleep(0.1)
                self.allkeyup()
                continue
            self.allkey = True

            key = self.udp跑图loopKeylist[self.udp跑图loopKeyindex]


            new_key_1 = int(key[1]) ^ 1
            keyname = key[0]

            if len(keyname) == 1:
                ds = ord(keyname)
            elif keyname in key_mapping:
                ds = key_mapping[keyname]
            else:
                self.udp跑图loopKeyindex += 1
                continue
            self.udp跑图loopKeyindex += 1


            data = f"key,{new_key_1},{ds},0\n"
            self.send_udp_data(data)
            if self.printKey:
                print(key[0][:1], end=".")
            time.sleep(key[2])
            # print("Test :  ",data,key[2])
        self.allkeyup()


    # def 跑图(self,index, p = True):
    def 跑图(self):
        index = self.index
        p = True

        if not self.跑图按键:
            self.初始化跑图按键()
        self.跑图停止 = False

        if self.fangan:
            keylist = self.跑图按键[str(index)]
            print("王之摇篮 ",index,len(self.跑图按键))
        else:
            keylist = self.跑图按键2[str(index)]
            print("王之摇篮2 ",index,len(self.跑图按键2))


        self.xunhuan = 0

        self.light = len(keylist)

        pindex = 0

        print(" index: ", index, "  Key : ")
        while True:

            if self.xunhuan  >= self.light-1:
                break
            if not self.running:
                print("退出 跑图 按键线程")
                break
            if self.跑图暂停:
                print("跑图暂停 : ", self.xunhuan)
                while self.跑图暂停:
                    time.sleep(0.5)
                    if not self.跑图暂停:
                        data = f"key,4,0,0\n"  # 释放所有按键
                        self.send_udp_data(data)
                        break
                    if not self.running:
                        print("退出 跑图 按键线程")
                        data = f"key,4,0,0\n"  # 释放所有按键
                        self.send_udp_data(data)
                        break
            pindex += 1
            if pindex > 25:
                pindex = 0
                print(" index: ",index,"  Key : ")

            key = keylist[self.xunhuan]

            new_key_1 = int(key[1]) ^ 1
            keyname = key[0]

            if len(keyname) == 1:
                ds = ord(keyname)
            elif keyname in key_mapping:
                ds = key_mapping[keyname]
            else:
                self.xunhuan += 1
                continue
            self.xunhuan += 1
            if self.跑图停止:
                data = f"key,4,0,0\n"  # 释放所有按键
                self.send_udp_data(data)
                break

            data = f"key,{new_key_1},{ds},0\n"
            self.send_udp_data(data)
            if p:
                print(self.xunhuan, key[0], end=" ")
            time.sleep(key[2])

        data = f"key,4,0,0\n"  # 释放所有按键
        self.send_udp_data(data)
        print("跑图 按键 完成")
        self.running = False
        self.light = 0



    def 跑图2(self, index, p=True):
        if not self.跑图按键:
            self.初始化跑图按键()
        self.跑图停止 = False

        if self.fangan:
            keylist = self.跑图按键[str(index)]
            print("王之摇篮", index, len(self.跑图按键))
        else:
            keylist = self.跑图按键2[str(index)]
            print("王之摇篮2", index, len(self.跑图按键2))



        for key in keylist:

            new_key_1 = int(key[1]) ^ 1
            keyname = key[0]

            if len(keyname) == 1:
                ds = ord(keyname)
            elif keyname in key_mapping:
                ds = key_mapping[keyname]
            else:
                continue

            if self.跑图停止:
                data = f"key,4,0,0\n"  # 释放所有按键
                self.send_udp_data(data)
                break

            data = f"key,{new_key_1},{ds},0\n"
            self.send_udp_data(data)
            if p:
                print(key[0], end=" ")
            time.sleep(key[2])

        data = f"key,4,0,0\n"  # 释放所有按键
        self.send_udp_data(data)
        print("跑图 按键 完成")
        self.跑图停止 = True

    # 在 WeGame 中启动 DNF 点击过程
    def 点击游戏管理器(self,xy):
        if self.WeGame_id == 0:
            self.获取游戏启动器题和句柄()
            if self.WeGame_id == 0:
                print("窗口异常 WeGame_id 点击主页")
                return
        self.激活句柄窗口(self.WeGame_id)
        time.sleep(0.5)
        grid = self.windows_manage.get_window_geometry(self.WeGame_id)
        time.sleep(0.5)
        x = grid["x_offset"] + xy[0]  # 406
        y = grid["y_offset"] + xy[1]  # 35
        self.鼠标移动到指定位置(x,y)
        time.sleep(0.5)
        # print(grid, x,y)
        data = f"mouse,5,0,0,\n"  # 根据需求组装数据
        self.send_udp_data(data)

    def 鼠标移动到指定位置(self, x, y):

        fj = 5
        dx1, dy1 = pyautogui.position()
        cx1 = x - dx1
        cy1 = y - dy1
        if cx1 > 127:
            cx1 = 127
        elif cx1 < -127:
            cx1 = -127
        if cy1 > 127:
            cy1 = 127
        elif cy1 < -127:
            cy1 = -127

        a = 1
        while True:
            dx1, dy1 = pyautogui.position()

            zx1 = x - dx1
            zy1 = y - dy1
            if not ((cx1 > 0 and zx1 > 0) or (cx1 < 0 and zx1 < 0)):
                cx1 = cx1 / 2 * -1
            if not ((cy1 > 0 and zy1 > 0) or (cy1 < 0 and zy1 < 0)):
                cy1 = cy1 / 2 * -1

            if abs(zx1) < fj and abs(zy1) < fj:
                print(" 移动到位 : ", a, " 次 原设: ", x, y, " 实际 ", dx1, dy1, "  误差: ", x - dx1, y - dy1)
                break

            data = f"mouse,4,{cx1},{cy1},\n"  # 根据需求组装数据

            # print(data ,"data : ", x, y, dx1, dy1, "  误差: ", x - dx1, y - dy1)
            time.sleep(0.1)
            self.send_udp_data(data)
            a += 1
            if a > 500:
                print("移动鼠标异常")
                break


    # ----------------loop udp----------------------
    def stopallloop(self):
        self.runloop_DNF_loop = False
        self.runloop_udpKey_loop = False
        self.runloop_udp跑图loop = False





