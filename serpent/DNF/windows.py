
import time, win32con,win32gui
import ctypes
class windows():

    def __init__(self):

        self.windows_id = None
        self.windows_name = None

    def openWeGame(self):
        print("Open WeGame")


    def 激活窗口(self,window_title):
        hwnd = win32gui.FindWindow(None, window_title)
        # print(hwnd)
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




