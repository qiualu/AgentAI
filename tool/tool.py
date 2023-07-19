
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
import sys
sys.path.append(parent_directory)



from serpent.utilities import clear_terminal, display_serpent_logo, is_linux, is_windows, wait_for_crossbar

from serpent.window_controller import WindowController

import offshoot
# 代替 offshoot
from serpent.Editlibrary.yl_offshoot.base import discover

# Add the current working directory to sys.path to discover user plugins!
sys.path.insert(0, os.getcwd())

# On Windows, disable the Fortran CTRL-C handler that gets installed with SciPy
if is_windows:
    os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = 'T'

VERSION = "2020.2.1"

valid_commands = [
    "创建游戏插件",
    "创建游戏代理",
    "启动游戏"
]

def 命令入口():
    if len(sys.argv) == 1:
        输出相关命令的说明()
    elif len(sys.argv) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            输出相关命令的说明()
        else:
            command = sys.argv[1]

            if command not in valid_commands:
                # raise Exception("'%s' is not a valid Serpent command." % command)
                print(" 输入错误  '%s' 不是本库的相关指令,查看 -h 帮助然后确定输入." % command)
            函数指令集[command](*sys.argv[2:])

def 输出相关命令的说明():
    print(f"\n当前游戏控制的版本  v{VERSION}")
    print("命令集 列表 :\n")

    for command, description in command_description_mapping.items():
        print(f"{command.rjust(16)}: {description}")

    print("")

def 创建游戏插件():
    print("创建游戏插件")
def 创建游戏代理():
    print("创建游戏代理")
def 启动游戏():
    print("启动游戏")


函数指令集 = {
    "创建游戏插件": 创建游戏插件,
    "创建游戏代理": 创建游戏代理,
    "启动游戏": 启动游戏
}


command_description_mapping = {
    "创建游戏插件": "创建游戏插件",
    "创建游戏代理": "创建游戏代理",
    "启动游戏": "启动游戏"
}


if __name__ == "__main__":
    命令入口()
