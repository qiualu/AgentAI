
import threading
import socket, time, win32con,win32gui

import pyautogui,os

from serpent.DNF.windows import windows
from serpent.window_controller import WindowController # 窗口句柄管理
import shlex
import subprocess
import ctypes

import cv2 , random
from PIL import ImageGrab
import numpy as np
import mss

class DNFmanage():
    def __init__(self):
        print("name ")
        self.running = False
        self.WeGame_id = 0
        self.WeGame = "WeGame"
        self.windows_manage = WindowController()
    def openDNF(self):

        pyautogui.moveTo(100, 200)

        self.WeGame_id = self.windows_manage.locate_window(self.WeGame)
        print("self.WeGame_id ",self.WeGame_id )


        grid = self.windows_manage.get_window_geometry(self.WeGame_id)
        print("grid ", grid)
        x = grid["x_offset"] + 100
        y = grid["y_offset"] + 200
        print("x ", x," y ", y)
        # 鼠标移动到指定位置

        pyautogui.moveTo(x, y)
        self.windows_manage.focus_window(self.WeGame_id)
        pyautogui.click()

    def start(self):
        if not self.running:
            self.running = True
            # 创建并启动处理while循环的线程
            thread = threading.Thread(target=self.DNF_loop)
            thread.start()

    def stop(self):
        print("stop DNF 循环")
        self.running = False


    def DNF_loop(self):
        print(" DNF 开始 工作")
        x,y = 0,0
        while self.running:
            # 这里是您的while循环处理逻辑
            # print("Processing...")
            # time.sleep(0.2)
            #
            # # 当前鼠标位置
            # current_x, current_y = pyautogui.position()
            # if x != current_x or y!= current_y:
            #     print("moved X : " , x - current_x," Y:",y - current_y, )
            #     czx = x - current_x
            #     czy = y - current_y
            #     x = current_x
            #     y = current_y
            #     print("当前位置 x : {:<4d} y: {:<4d} 移动 : {:<4d} y: {:<4d}".format(x, y, czx, czy))

            y1 = 366
            x1 = 1461
            width = 1523 - x1
            height = 485 - y1
            # 创建一个屏幕捕获器对象
            with mss.mss() as sct:
                # 设置需要捕获的区域（左上角坐标为(x1, y1)，宽度为width，高度为height）
                monitor = {"top": y1, "left": x1, "width": width, "height": height}

                # 捕获屏幕特定位置
                screenshot = sct.grab(monitor)

                # 将PIL图像转换为NumPy数组
                image = np.array(screenshot)

                # 将图像转换为灰度图像
                gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

                # 显示截图
                cv2.imshow('Continuous Screenshot', gray_image)

                # 按下 'q' 键退出循环
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        # 关闭窗口和摄像头
        cv2.destroyAllWindows()
        screencap.release()

    def udp_loop(self):
        # 创建UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('0.0.0.0', 8848)
        sock.bind(server_address)

        folder_path = str(random.randint(10, 100))
        folder_path = "data/" + folder_path
        # 使用os.makedirs()创建文件夹（若路径不存在）
        os.makedirs(folder_path, exist_ok=True)
        mdd = 1

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
                # print("121")
                folderd = folder_path + "/" + str(mdd) + ".png"
                mdd += 1
                y1 = 366
                x1 = 1461
                width = 1523 - x1
                height = 485 - y1
                # 创建一个屏幕捕获器对象
                with mss.mss() as sct:
                    # 设置需要捕获的区域（左上角坐标为(x1, y1)，宽度为width，高度为height）
                    monitor = {"top": y1, "left": x1, "width": width, "height": height}

                    # 捕获屏幕特定位置
                    screenshot = sct.grab(monitor)

                    # 将PIL图像转换为NumPy数组
                    image = np.array(screenshot)

                    # 将图像转换为灰度图像
                    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                    cv2.imwrite(folderd, gray_image)
                # 在这里处理灰度图像


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


