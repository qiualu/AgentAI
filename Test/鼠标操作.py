
from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import win32con
import win32api
import win32clipboard
import time,random

def anli():

    # 将字符串text复制到剪切板
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText('text')
    win32clipboard.CloseClipboard()

    # 将字符串text复制到剪切板
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText('text')
    win32clipboard.CloseClipboard()

    win32api.SetCursorPos([200,370])
    #执行左单键击，若需要双击则延时几毫秒再点击一次即可
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    #右键单击
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)



    #执行左单键击，若需要双击则延时几毫秒再点击一次即可
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    #右键单击
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)

    #键盘点击操作
    # Ctrl+s （Ctrl+a、Ctrl+v操作类似）
    win32api.keybd_event(17, 0, 0, 0) # 按下Ctrl键
    win32api.keybd_event(83, 0, 0, 0) # 按下s键
    win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0) # 释放Ctrl键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    # 按下回车并释放回车键
    win32api.keybd_event(13, 0, 0, 0)
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)


def shubiao():
    def read_txt_file(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            ts = 1681200260010
            for line in f.readlines():
                data = line.strip()
                x = int(data.split("Btn : x,")[1].split(", y ")[0])
                y = int(data.split("Btn : x,")[1].split(", y ")[1].split(", utime=")[0])
                timed = int(data.split("Btn : x,")[1].split(", y ")[1].split(", utime=")[1])

                sc = (timed - ts) / 1000
                ts = timed
                print("时间差 : ", sc, "  ", data, x, y, timed, time.time())
                win32api.SetCursorPos([x, y])
                # 执行左单键击，若需要双击则延时几毫秒再点击一次即可
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                time.sleep(sc)

    read_txt_file("mouse.txt")
    print(" ------ end ------ ")
import ctypes
import socket
BUFSIZE = 1024

def udp_send():
    ip_port = ('192.168.0.102', 8888)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ctypes.windll.user32.SetCursorPos(0, 0)
    time.sleep(0.3)
    msg = "mouse,9," + str(0) + "," + str(0) + "\n"
    client.sendto(msg.encode('utf-8'), ip_port)
    time.sleep(1)
    a = 0
    b = 0.8
    while True:
        x = int(random.randint(200,1000) * b)
        y = int(random.randint(600,720) * b)
        a += 1
        # msg = "mouse,8,100,100\n"
        # win32api.SetCursorPos([x, y])
        msg = "mouse,9," + str(x) + "," + str(y) + "\n"
        # ctypes.windll.user32.SetCursorPos(x, y)
        time.sleep(0.2)
        client.sendto(msg.encode('utf-8'), ip_port)

        time.sleep(0.5)
        msg = "mouse,8,100,100\n"
        client.sendto(msg.encode('utf-8'), ip_port)

        if a > 10:
            break
        time.sleep(2)
        print(msg,a,x, y)
    client.close()

def udp_sendyc():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ctypes.windll.user32.SetCursorPos(0, 0)
    time.sleep(0.2)
    # ctypes.windll.user32.SetCursorPos(400, 600)
    # time.sleep(0.2)
    # ctypes.windll.user32.SetCursorPos(800, 600)
    # time.sleep(0.2)

    ip_port = ('192.168.0.102', 8888)

    # b = 0.8
    # x = int(300 * b)
    # y = int(650 * b)
    # msg = "mouse,9," + str(x) + "," + str(y) + "\n"
    # client.sendto(msg.encode('utf-8'), ip_port)

    b = 0.8
    msg = "mouse,9," + str(0) + "," + str(0) + "\n"
    client.sendto(msg.encode('utf-8'), ip_port)


    client.close()



if __name__ == '__main__':


    # udp_send()

    time.sleep(2)
    print(" start ")
    # udp_sendyc()
    udp_send()


