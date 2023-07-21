
import threading
import socket, time

import pyautogui,os

from serpent.DNF.windows import windows

import cv2 , random
from PIL import ImageGrab
import numpy as np
import mss

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
        # 通关提示区[0] = 王之摇篮通关提示区[0] + grid["x_offset"]
        # 通关提示区[1] = 王之摇篮通关提示区[1] + grid["y_offset"]
        # 通关提示区[2] = 王之摇篮通关提示区[2] - 王之摇篮通关提示区[0]
        # 通关提示区[3] = 王之摇篮通关提示区[3] - 王之摇篮通关提示区[1]
        print(" 通关提示区 : ", 通关提示区)
        path = "data/quanKin"
        index = 1000
        while self.running:

            gray_image = self.截屏("区域", 范围=通关提示区, 灰度=False)
            filepath = path + "/" + str(index) + ".png"
            index += 1
            cv2.imwrite(filepath, gray_image)  # 保存

            _, binary_image = cv2.threshold(gray_image, self.threshold_value, self.max_value, cv2.THRESH_BINARY)

            # 显示截图
            cv2.imshow('Continuous Screenshot', binary_image)
            cv2.moveWindow('Continuous Screenshot', 2046, 24)
            # 按下 'q' 键退出循环
            if cv2.waitKey(300) & 0xFF == ord('q'):
                break
        # 关闭窗口和摄像头
        cv2.destroyAllWindows()
        # screencap.release()

    def udp_loop(self):
        # 创建UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('0.0.0.0', 8848)
        sock.bind(server_address)

        while True:
            data, address = sock.recvfrom(1024)
            command = data.decode()

            print('从客户端', address, '接收到数据:', data.decode()[:-1])
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
