import time

import win32gui
import win32con

import re

window_id = 0


class Win32WindowController():

    def __init__(self):
        self.init_dnf_windows()


    def init_dnf_windows(self):
        self.dnf_name, self.dnf_id = self.locate_left_name_window("地下城")


    # 获取ID
    def locate_window(self, name):
        global window_id
        # print("Win32WindowController locate_window : ",name)
        window_id = win32gui.FindWindow(None, name)
        if window_id != 0:
            return window_id
        def callback(wid, pattern):
            global window_id
            if re.match(pattern, str(win32gui.GetWindowText(wid))) is not None:
                window_id = wid
        win32gui.EnumWindows(callback, name)
        return window_id
    # 移动
    def move_window(self, window_id, x, y):
        x0, y0, x1, y1 = win32gui.GetWindowRect(window_id)
        win32gui.MoveWindow(window_id, x, y, x1 - x0, y1 - y0, True)
    # 显示变化大小
    def resize_window(self, window_id, width, height):
        x0, y0, x1, y1 = win32gui.GetWindowRect(window_id)
        win32gui.MoveWindow(window_id, x0, y0, width, height, True)
    # 通过窗口标识符激活指定的窗口
    def focus_window(self, window_id):
        win32gui.SetForegroundWindow(window_id)

    # 激活指定的窗口 和 上面一样
    def bring_window_to_top(self, window_id):
        win32gui.ShowWindow(window_id, win32con.SW_RESTORE)
        win32gui.SetWindowPos(window_id, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)  
        win32gui.SetWindowPos(window_id, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)  
        win32gui.SetWindowPos(window_id, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)

    # 检查指定的窗口是否处于焦点状态
    def is_window_focused(self, window_id):
        focused_window_id = win32gui.GetForegroundWindow()
        return focused_window_id == window_id

    # 焦点状态位于那个窗口
    def get_focused_window_name(self):
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())

    # 获取指定窗口的几何信息，包括窗口的宽度、高度以及在屏幕上的位置偏移。
    def get_window_geometry(self, window_id):
        geometry = dict()
        x, y, width, height = win32gui.GetClientRect(window_id)
        geometry["width"] = width
        geometry["height"] = height
        x0, y0, x1, y1 = win32gui.GetWindowRect(window_id)
        border_width = ((x1 - x0 - width) // 2)
        geometry["x_offset"] = x0 + border_width
        geometry["y_offset"] = y0 + (y1 - y0 - height - border_width)
        return geometry

    # 地下城是否激活状态
    def dnf_focused(self):
        if self.dnf_id:
            name = self.get_focused_window_name()
            if name == self.dnf_name:
                return True
            else:
                return False
        else:
            self.init_dnf_windows()
            return False

    # 返回第一个拥有 name 的窗口和窗口id
    def locate_name_window(self,name):
        titles = set()
        titles_id = 0
        titles_name = name
        def foo(hwnd, mouse):
            # 去掉下面这句就所有都输出了，但是我不需要那么多
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                titles.add(win32gui.GetWindowText(hwnd))

        win32gui.EnumWindows(foo, 0)
        lt = [t for t in titles if t]
        lt.sort()
        for t in lt:
            # print("窗口标题: ", t)
            if name in t:
                print("地下城标题 : ",t)
                titles_id = win32gui.FindWindow(None, t)
                titles_name = t
                return titles_name, titles_id
        return titles_name, titles_id

    # 获取窗口的完整名称 和 id  ,name 补齐右边
    def locate_left_name_window(self,name):
        titles = set()
        titles_id = 0
        titles_name = name
        def foo(hwnd, mouse):
            # 去掉下面这句就所有都输出了，但是我不需要那么多
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                titles.add(win32gui.GetWindowText(hwnd))

        win32gui.EnumWindows(foo, 0)
        lt = [t for t in titles if t]
        lt.sort()
        for t in lt:
            # print("窗口标题: ", t)
            if name in t[:len(name)]:
                print("地下城标题 : ",t)
                titles_id = win32gui.FindWindow(None, t)
                titles_name = t
                return titles_name, titles_id
        return titles_name, titles_id

    # 打印所有窗口标题
    def get_all_name_window(self):
        titles = set()
        titles_id = 0
        # titles_name = name
        def foo(hwnd, mouse):
            # 去掉下面这句就所有都输出了，但是我不需要那么多
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                titles.add(win32gui.GetWindowText(hwnd))

        win32gui.EnumWindows(foo, 0)
        lt = [t for t in titles if t]
        lt.sort()
        for t in lt:

            titles_id = win32gui.FindWindow(None, t)
            print("窗口标题: ", t , " id : " ,titles_id)
            # if name in t:
            #     print("地下城标题 : ",t)
            #     titles_id = win32gui.FindWindow(None, t)
            #     titles_name = t
                # return titles_name, titles_id
        # return titles_name, titles_id

if __name__ == '__main__':
    win = Win32WindowController()
    #name, id = win.locate_left_name_window("地下城")

    a = 1
    while True:
        a += 1
        if a > 1000:
            break
        time.sleep(1)
        dq = win.get_focused_window_name()
        if dq == win.dnf_name:
            print("当前是dnf")
        else:
            print("当前 : ",dq)



    # print(" 地下城的信息 ",name, id)