import random
import time
import socket
import pyautogui

x = 0
y = 0


def move_linear(value, scale):
    # 根据线性比例计算实际移动距离
    return int(value / scale * 127)


class KK:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ("192.168.0.102", 8888)

    def send_command(self, command):
        self.sock.sendto(command.encode(), self.server_address)

    def get_mouse_position(self):
        position = pyautogui.position()
        return position.x, position.y

    def move_mouse_to_target(self, target_x, target_y):
        error_threshold = 5  # 误差阈值，达到该误差范围内停止逼近
        scale = 127  # 数值范围

        # 第一次移动的距离
        move_x = move_linear(target_x, scale)
        move_y = move_linear(target_y, scale)

        while True:
            current_x, current_y = self.get_mouse_position()

            error_x = target_x - current_x
            error_y = target_y - current_y

            if abs(error_x) <= error_threshold and abs(error_y) <= error_threshold:
                break

            move_x = move_linear(error_x, scale)
            move_y = move_linear(error_y, scale)

            self.move_mouse(move_x, move_y)

            time.sleep(random.uniform(0.1, 0.5))

    def move_mouse(self, move_x, move_y):
        global x, y

        if move_x > 127:
            move_x = 127
        elif move_x < -127:
            move_x = -127

        if move_y > 127:
            move_y = 127
        elif move_y < -127:
            move_y = -127

        x += move_x
        y += move_y

        command = "mouse,4," + str(x) + "," + str(y) + ",\n"
        self.server_address = ("192.168.0.102", 8888)
        self.sock.sendto(command.encode(), self.server_address)

# 有一个udp的接口发送的数据是这样的
# command = "mouse,4," + str(x) + "," + str(y) + ",\n"
# self.server_address = ("192.168.0.102", 8888)
# self.sock.sendto(command.encode(), self.server_address)
# 这里的x y 的范围是 [-127,127]
#
# 但是实际上 如果传入的是0 则鼠标移动 0 个像素
# 如果传入的是 10 则移动 16 个像素 有时候根据传输速度块了也移动32个像素
# 如果传入的是 20 则移动 49 个像素 有时候根据传输速度块了也移动32个像素
# 如果传入的是 30 则移动 89 个像素 有时候根据传输速度块了也移动32个像素
# 对应的 入 40 动 130
# 入 50 动 170
# 入 60 动 210
# 入 70 动 250
# 入 80 动 330
# 入 90 动 390
#
# 入 100 动 371
# 入 127 动 480
#
#
# import pyautogui
#
#
#
#
#
# 有一个udp的接口发送的数据是这样的
# command = "mouse,4," + str(x) + "," + str(y) + ",\n"
# self.server_address = ("192.168.0.102", 8888)
# self.sock.sendto(command.encode(), self.server_address)
# 这里的x y 的范围是 [-127,127]
#
# 上面发送的xy 可以移动鼠标像素
# 通过移动前和移动后 用下面获取当前和移动后的坐标,得出 127 具体移动的像素 用一个列表对应输出 每次移动的时候注意是不是边上导致移动无效的可能
# import pyautogui
# pyautogui.position()