
import threading
import socket, time

import pyautogui,os

from serpent.DNF.windows import windows

import cv2 , random
from PIL import ImageGrab
import numpy as np
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
            # 创建并启动处理while循环的线程
            thread = threading.Thread(target=self.udpKey)
            thread.start()
            thread = threading.Thread(target=self.DNF_loop)
            thread.start()
    # DNF_loop
    def stop(self):
        print("stop DNF 循环")
        self.running = False

    def DNF_loop(self):
        print(" DNF 开始 工作")
        grid = self.获取窗口信息(1)
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

            if not self.running:
                print("退出 DNF_loop 按键线程")
                break
        # 关闭窗口和摄像头
        cv2.destroyAllWindows()
        # screencap.release()



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

                if keyname == "*":
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

            print('从客户端', address, '接收到数据:', data.decode()[:-1])
            zl = data.decode()[:-1]

            # if int(zl) <= 12:
            #     thread = threading.Thread(target=self.跑图线程,args=(zl,))
            #     thread.start()
            #     continue
            # elif int(zl) == 13:
            #     self.跑图停止 = True


            # 根据接收到的命令控制while循环的状态
            if zl == "1":
                self.start() # 启动游戏循环
            elif zl == "2":
                self.stop()  # 停止游戏循环
            elif zl == "3":  # 退出整个程序
                self.stop()
                break
            elif zl == "4":  # 退出整个程序
                self.threshold_value += 1
                print("更改阀值 : ", self.threshold_value)
            elif zl == "5":  # 退出整个程序
                self.threshold_value -= 1
                print("更改阀值 : ", self.threshold_value)

            elif zl == "6":  # 退出整个程序
                self.打开角色(4)

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

# # 创建MyClass实例
# my_object = DNFmanage()
#
# # 创建并启动接收UDP控制的线程
# control_thread = threading.Thread(target=my_object.control_loop)
# control_thread.start()
#
# # 主线程继续执行其他任务...




if __name__ == '__main__':
    # Create an object
    DNF = DNFmanage()
    # DNF.openDNF()
    DNF.udp_loop()

    # DNF.鼠标移动到指定位置(100,200)
