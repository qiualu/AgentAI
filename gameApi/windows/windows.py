

# 获得所有窗口标题
import win32gui

import os, time


import socket




class windows:

    def __init__(self):
        self.titles = set()
        # self.getDNFtitle()
        self.DNFtitles = ""
        self.DNFhandle = 0

        self.keyip = "192.168.0.102"

    def foo(self,hwnd, mouse):
        # 去掉下面这句就所有都输出了，但是我不需要那么多
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            self.titles.add(win32gui.GetWindowText(hwnd))

    def getDNFtitle(self):
        win32gui.EnumWindows(self.foo, 0)
        lt = [t for t in self.titles if t]
        lt.sort()
        for t in lt:
            # print(t)
            if "地下城与勇士" in t[:8]:
                print("地下城与勇士 : ", t)
                self.DNFhandle = win32gui.FindWindow(None, t)
                print("地下城与勇士 handle : ", self.DNFhandle)


