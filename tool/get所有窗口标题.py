#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 获得所有窗口标题
from win32gui import *
titles = set()
def foo(hwnd,mouse):
    #去掉下面这句就所有都输出了，但是我不需要那么多
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        titles.add(GetWindowText(hwnd))
EnumWindows(foo, 0)
lt = [t for t in titles if t]
lt.sort()
for t in lt:
    print(t)
    if t == "Fatal Error":
        print("--------------------------------------------------")


# TD
# 正常   /perform
# TouchDesigner
# Fatal Error
# import os
# os.system('taskkill /f /im TouchPlayer099.exe')


# 获得句柄
import win32gui,win32con
handle = win32gui.FindWindow(None, "泼墨")
print(handle)

def show():
    # windows handlers
    hwnd = handle
    win32gui.SetForegroundWindow(hwnd)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 1000, 1000, 0, 0,win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW)

def hide():

    # windows handlers
    hwnd = handle
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_HIDEWINDOW | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER)

# win32gui.SetForegroundWindow(handle)
# show()
# hide()