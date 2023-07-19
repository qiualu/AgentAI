from serpent.utilities import is_linux, is_windows


class WindowControllerError(BaseException):
    pass


class WindowController:

    def __init__(self):
        self.adapter = self._load_adapter()()
        # 等同于  self.adapter = Win32WindowController() | windows 系统   LinuxWindowController

    # 获取句柄id
    def locate_window(self, name):
        # print("locate_window 窗口标题 : ", name)
        return self.adapter.locate_window(name)
    # 移动窗口到指定位置
    def move_window(self, window_id, x, y):
        self.adapter.move_window(window_id, x, y)
    # 改变窗口大小
    def resize_window(self, window_id, width, height):
        self.adapter.resize_window(window_id, width, height)
    # 通过窗口标识符激活指定的窗口
    def focus_window(self, window_id):
        self.adapter.focus_window(window_id)
    # 激活指定的窗口 和 上面一样
    def bring_window_to_top(self, window_id):
        self.adapter.bring_window_to_top(window_id)

    # 检查指定的窗口是否处于焦点状态
    def is_window_focused(self, window_id):
        return self.adapter.is_window_focused(window_id)

    # 焦点状态位于那个窗口
    def get_focused_window_name(self):
        return self.adapter.get_focused_window_name()

    # 获取指定窗口的几何信息，包括窗口的宽度、高度以及在屏幕上的位置偏移。
    def get_window_geometry(self, window_id):
        return self.adapter.get_window_geometry(window_id)

    def _load_adapter(self):
        # print("_load_adapter")
        if is_linux():
            from serpent.window_controllers.linux_window_controller import LinuxWindowController
            return LinuxWindowController
        elif is_windows():
            from serpent.window_controllers.win32_window_controller import Win32WindowController
            return Win32WindowController
