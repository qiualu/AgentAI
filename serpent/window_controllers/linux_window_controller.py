from serpent.window_controller import WindowController

import subprocess
import shlex

import re


class LinuxWindowController(WindowController):

    def __init__(self):
        pass

    def locate_window(self, name):
        print("locate_window")
        return subprocess.check_output(shlex.split(f"xdotool search --onlyvisible --name \"^{name}$\"")).decode("utf-8").strip()

    def move_window(self, window_id, x, y):
        subprocess.call(shlex.split(f"xdotool windowmove {window_id} {x} {y}"))
    # 改变窗口大小
    def resize_window(self, window_id, width, height):
        subprocess.call(shlex.split(f"xdotool windowsize {window_id} {width} {height}"))

    def focus_window(self, window_id):
        """
            通过窗口标识符激活指定的窗口。

            参数：
            - window_id：窗口标识符，用于唯一标识一个窗口。

            注意：
            - 该函数使用了外部命令 "xdotool" 来实现窗口激活操作，请确保系统中已安装并配置了该命令行工具。
            - 该函数只适用于 Linux 系统。

            示例用法：
            focus_window("0x12345678")
        """
        subprocess.call(shlex.split(f"xdotool windowactivate {window_id}"))

    def bring_window_to_top(self, window_id):
        subprocess.call(shlex.split(f"xdotool windowactivate {window_id}"))

    def is_window_focused(self, window_id):
        """
            检查指定的窗口是否处于焦点状态。

            参数：
            - window_id：窗口标识符，用于唯一标识一个窗口。

            返回值：
            - 如果指定窗口处于焦点状态，则返回 True；否则返回 False。

            注意：
            - 该函数使用了外部命令 "xdotool" 来获取当前焦点窗口的标识符，请确保系统中已安装并配置了该命令行工具。
            - 该函数只适用于 Linux 系统。

            示例用法：
            is_focused = is_window_focused("0x12345678")
            """
        focused_window_id = subprocess.check_output(shlex.split("xdotool getwindowfocus")).decode("utf-8").strip()
        return focused_window_id == window_id

    def get_focused_window_name(self):
        focused_window_id = subprocess.check_output(shlex.split("xdotool getwindowfocus")).decode("utf-8").strip()
        return subprocess.check_output(shlex.split(f"xdotool getwindowname {focused_window_id}")).decode("utf-8").strip()
    # 获取指定窗口的几何信息，包括窗口的宽度、高度以及在屏幕上的位置偏移
    def get_window_geometry(self, window_id):
        """
            获取指定窗口的几何信息，包括窗口的宽度、高度以及在屏幕上的位置偏移。

            参数：
            - window_id：窗口标识符，用于唯一标识一个窗口。

            返回值：
            - 一个包含窗口几何信息的字典，包括以下键值对：
                - "width"：窗口的宽度（以像素为单位）
                - "height"：窗口的高度（以像素为单位）
                - "x_offset"：窗口相对于屏幕左上角的水平位置偏移（以像素为单位）
                - "y_offset"：窗口相对于屏幕左上角的垂直位置偏移（以像素为单位）

            注意：
            - 该函数使用了外部命令 "xdotool" 和 "xwininfo" 来获取窗口的几何信息，请确保系统中已安装并配置了这两个命令行工具。
            - 该函数只适用于 Linux 系统。

            示例用法：
            geometry = get_window_geometry("0x12345678")
            print(geometry)
            # 输出示例: {'width': 800, 'height': 600, 'x_offset': 100, 'y_offset': 50}
        """

        geometry = dict()

        window_geometry = subprocess.check_output(shlex.split(f"xdotool getwindowgeometry {window_id}")).decode("utf-8").strip()
        size = re.match(r"\s+Geometry: ([0-9]+x[0-9]+)", window_geometry.split("\n")[2]).group(1).split("x")

        geometry["width"] = int(size[0])
        geometry["height"] = int(size[1])

        window_information = subprocess.check_output(shlex.split(f"xwininfo -id {window_id}")).decode("utf-8").strip()
        geometry["x_offset"] = int(re.match(r"\s+Absolute upper-left X:\s+([0-9]+)", window_information.split("\n")[2]).group(1))
        geometry["y_offset"] = int(re.match(r"\s+Absolute upper-left Y:\s+([0-9]+)", window_information.split("\n")[3]).group(1))

        return geometry
