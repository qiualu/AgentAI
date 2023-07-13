import offshoot

from serpent.Editlibrary.yl_offshoot.base import executable_hook
from serpent.Editlibrary.yl_offshoot.plugin import Plugin



class SerpentMLAGamePlugin(Plugin):
    name = "SerpentMLAGamePlugin"
    version = "0.1.0"

    libraries = []

    files = [
        {"path": "serpent_MLA_game.py", "pluggable": "Game"}
    ]

    config = {
        "fps": 2
    }

    @classmethod
    def on_install(cls):
        print("\n\n%s was installed successfully!" % cls.__name__)

    @classmethod
    def on_uninstall(cls):
        print("\n\n%s was uninstalled successfully!" % cls.__name__)

def plugin_main(command):
    print("plugin_main 插件文件开始运行")
    executable_hook(SerpentMLAGamePlugin, command)

from serpent.window_controller import WindowController


import pyautogui,time

def plugin_init():
    print("plugin_init 初始化")

    window_name = "VirtuaNESex"
    window_controller = WindowController()

    current_attempt = 1
    loop = 10
    window_id = 0
    while current_attempt <= loop:
        window_id = window_controller.locate_window(window_name)
        # print("尝试获取游戏窗口", current_attempt, "次")

        if window_id not in [0, "0"]:
            break
        current_attempt += 1
        time.sleep(1)
    if window_id in [0, "0"]:
        print("尝试打开游戏失败")
        return
    # 激活窗口
    window_controller.focus_window(window_id)
    # 按下Alt键，然后依次按下对应的按键组合，模拟打开文件操作
    pyautogui.keyDown('alt')
    pyautogui.press('f')
    pyautogui.press('f')
    pyautogui.press('enter')
    pyautogui.keyUp('alt')

    # window_controller = WindowController()
    # window_id = window_controller.locate_window(winname)
    # print("window_id",window_id)
    # window_controller.move_window(window_id, 0, 0)
    # # window_controller.resize_window(window_id, 300, 500)
    # # window_controller.bring_window_to_top(window_id)
    # window_controller.focus_window(window_id)
    #
    # import time
    # # time.sleep(2)
    # focused = window_controller.is_window_focused(window_id)
    # print("focused : ",focused)
    # time.sleep(1)
    # focused = window_controller.get_focused_window_name()
    # print("windows : ", focused)
    # window_id = window_controller.locate_window(focused)
    # print("window_id : ", window_id)
    # dwh = window_controller.get_window_geometry(window_id)
    # print("高宽 : ", dwh)

if __name__ == "__main__":
    offshoot.executable_hook(SerpentMLAGamePlugin)
