



import cv2
from PIL import ImageGrab
import numpy as np
import mss,math

import time, win32con,win32gui,pyautogui
import ctypes
from serpent.window_controller import WindowController # 窗口句柄管理
# 获得所有窗口标题
from win32gui import *
import subprocess,random,socket
import json



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


class windows():

    def __init__(self):

        self.windows_id = None
        self.windows_name = None
        self.windows_manage = WindowController()

        self.WeGame_id = 0
        self.WeGame_name = "WeGame"
        self.WeGame_path = r"E:\ProgramFiles\Game\WeGame\wegame.exe"
        self.DNF_id = 0
        self.DNF_name = None

        self.UDP_IP = "192.168.0.105"
        self.UDP_PORT = 8888

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.WeGame_grid = None

        self.WeGame_btn = {
            "主页" : [410,29],
            "地下城": [104, 208],
            "启动" : [1127,790]
        }


        self.DNF角色 = [[369,288],[582,271],[804,280],[1006,285],[1227,303],[187,654],[395,640],[579,641],[789,643],[1009,653],[1223,657],[1443,666]]

        # 读取 JSON 文件
        with open('data/配置文件.json', 'r', encoding="utf-8") as file:
            json_data = file.read()
        # 将 JSON 数据解析为字典
        self.DNF_btn = json.loads(json_data) # 地下城信息

        self.跑图按键 = None
        self.跑图停止 = True

        self.key记录 = {}

        self.通关情况 = [0] * self.DNF_btn["关卡"]["毁坏的寂静城"]["王之摇篮"]["关卡数量"]


    def send_udp_data(self,data):
        # 创建UDP套接字
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 发送数据
        self.sock.sendto(data.encode(), (self.UDP_IP, self.UDP_PORT))
        # 关闭套接字
        # sock.close()


    def openWeGame(self):
        print("Open WeGame")
    def 打开软件(self):
        # WeGame_path
        subprocess.Popen(self.WeGame_path, shell=True)

    def 截屏(self,截屏类型, path = None, 范围 = None,灰度 = True):

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

    def 激活标题窗口(self,window_title):
        hwnd = win32gui.FindWindow(None, window_title)
        # print(hwnd)
        self.windows_id = hwnd
        self.windows_name = window_title
        if not hwnd:
            print("句柄获取失败 ", window_title, hwnd)
        #     # 将窗口还原
        #     win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        #
        #     # 激活窗口到前台
        #     win32gui.SetForegroundWindow(hwnd)
        user32 = ctypes.windll.user32
        if user32:
            # 将窗口还原
            user32.ShowWindow(hwnd, 9)  # SW_RESTORE = 9
            # 激活窗口到前台
            user32.SetForegroundWindow(hwnd)
    def 激活句柄窗口(self,hwnd):
        user32 = ctypes.windll.user32
        if user32:
            # 将窗口还原
            user32.ShowWindow(hwnd, 9)  # SW_RESTORE = 9
            # 激活窗口到前台
            user32.SetForegroundWindow(hwnd)


    def 鼠标移动到指定位置(self,x,y):

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
                print(" 移动到位 : ", a, " 次 原设: " , x, y ," 实际 ",dx1 , dy1 ,"  误差: ",x - dx1,y - dy1)
                break


            data = f"mouse,4,{cx1},{cy1},\n"  # 根据需求组装数据

            # print(data ,"data : ", x, y, dx1, dy1, "  误差: ", x - dx1, y - dy1)
            time.sleep(0.1)
            self.send_udp_data(data)
            a += 1
            if a > 500:
                print("移动鼠标异常")
                break


    def 初始化跑图按键(self,filepath ='data/通关按键/王之摇篮.json'): # self.跑图按键控制台
        # 读取 JSON 文件
        with open(filepath, 'r', encoding="utf-8") as file:
            json_data = file.read()
        # 将 JSON 数据解析为字典
        self.跑图按键 = json.loads(json_data)  # 地下城信息



    def 跑图(self,index,p = True):
        if not self.跑图按键:
            self.初始化跑图按键()
        self.跑图停止 = False
        keylist = self.跑图按键[str(index)]
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
                break

            data = f"key,{new_key_1},{ds},0\n"
            self.send_udp_data(data)
            if p:
                print("按键 : ", data.replace("\n", ""), key)
            time.sleep(key[2])

        data = f"key,4,0,0\n" # 释放所有按键
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



    def 启动DNF(self):
        self.点击游戏管理器(self.WeGame_btn["主页"])
        time.sleep(2)
        self.点击游戏管理器(self.WeGame_btn["地下城"])
        time.sleep(2)
        self.点击游戏管理器(self.WeGame_btn["启动"])

    def 点击地下城游戏(self, xy, ds = 5):
        if self.DNF_id == 0:
            self.获取地下城标题和句柄()
            if self.DNF_id == 0:
                print("窗口异常 WeGame_id 点击主页")
                return
        self.激活句柄窗口(self.DNF_id)
        time.sleep(0.5)
        grid = self.windows_manage.get_window_geometry(self.DNF_id)
        time.sleep(0.5)
        x = grid["x_offset"] + xy[0]  # 406
        y = grid["y_offset"] + xy[1]  # 35
        self.鼠标移动到指定位置(x,y)
        time.sleep(0.5)
        # print(grid, x,y)
        data = f"mouse,{ds},0,0,\n"  # 根据需求组装数据
        self.send_udp_data(data)


    def 通关图对比(self,image1, image2, threshold=30):
        # 计算差异
        diff = cv2.absdiff(gray1, gray2)

        # 应用阈值来获得二值图像
        _, thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

        # 计算差异区域的像素数量
        diff_pixels = cv2.countNonZero(thresholded)
        print(diff_pixels , threshold)
        # 判断差异是否大于阈值
        if diff_pixels > threshold:
            return False
        else:
            return True

    def 打开角色(self,index):
        self.点击地下城游戏(self.DNF角色[index], 6)  # 6 双击
        self.点击地下城游戏(self.DNF角色[index], 6)  # 6 双击

    def 获取窗口信息(self,rj = 0):

        if rj == 0:
            hwnd = self.WeGame_id
            window_title = self.WeGame_name
        else:
            hwnd = self.DNF_id
            window_title = self.DNF_name

        if not hwnd:
            self.获取地下城标题和句柄()
            self.获取游戏启动器题和句柄()

        if rj == 0:
            hwnd = self.WeGame_id
            window_title = self.WeGame_name
        else:
            hwnd = self.DNF_id
            window_title = self.DNF_name

        if not hwnd:
            print("窗口未启动 异常")
            return

        grid = self.windows_manage.get_window_geometry(hwnd)
        print("窗口信息 ",window_title ," : ", grid)
        return grid

    def 获取地下城标题和句柄(self):
        titles = set()
        def foo(hwnd, mouse):
            # 去掉下面这句就所有都输出了，但是我不需要那么多
            if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
                titles.add(GetWindowText(hwnd))

        EnumWindows(foo, 0)
        lt = [t for t in titles if t]
        lt.sort()
        for t in lt:
            # print("窗口标题: ", t)
            if "地下城与勇士" in t:
                print("地下城标题 : ",t)
                self.DNF_id = win32gui.FindWindow(None, t)
                self.DNF_name = t

    def 获取游戏启动器题和句柄(self):
        titles = set()
        def foo(hwnd, mouse):
            # 去掉下面这句就所有都输出了，但是我不需要那么多
            if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
                titles.add(GetWindowText(hwnd))

        EnumWindows(foo, 0)
        lt = [t for t in titles if t]
        lt.sort()
        for t in lt:
            # print("窗口标题: ", t)
            if "WeGame" in t:
                print("地下城标题 : ",t)
                self.WeGame_id = win32gui.FindWindow(None, t)
                self.WeGame_name = t