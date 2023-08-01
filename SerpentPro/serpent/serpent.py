#!/usr/bin/env python
import os
import sys
import shutil
import subprocess
import shlex
import time

import offshoot
import sys
sys.path.append(r"E:\Projece\python\AgentAI\SerpentPro\serpent")

from serpent.utilities import clear_terminal, display_serpent_logo, is_linux, is_windows, wait_for_crossbar

# Add the current working directory to sys.path to discover user plugins!
sys.path.insert(0, os.getcwd())

# On Windows, disable the Fortran CTRL-C handler that gets installed with SciPyc
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = 'T' # 表示禁用 Fortran 的 Ctrl+C 处理程序。


VERSION = "2020.2.1"

valid_commands = [
    "setup",
    "update",
    "modules",
    "grab_frames",
    "launch",
    "play",
    "record",
    "generate",
    "activate",
    "deactivate",
    "plugins",
    "train",
    "capture",
    "visual_debugger",
    "window_name",
    "record_inputs",
    "dashboard",
    "object_recognition",
    "test"
]

# 入口函数
def execute():
    if len(sys.argv) == 1:
        executable_help()
    elif len(sys.argv) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            executable_help()
        else:
            command = sys.argv[1]

            if command not in valid_commands:
                # raise Exception("'%s' 不是本库的相关指令,查看帮助然后确定输出." % command)
                print(" 输入错误  '%s' 不是本库的相关指令,查看 -h 帮助然后确定输入." % command)
                return
            command_function_mapping[command](*sys.argv[2:])

# 显示帮助
def executable_help():
    print(f"\nSerpent 的版本:  v{VERSION}")
    print("Available Commands:")

    for command, description in command_description_mapping.items():
        print(f"{command.rjust(16)}: {description}")

    print("-------")


# setup: 进行框架的首次安装设置
def setup(module=None,*args):
    print("setup",module)
    clear_terminal() # 清空屏幕
    display_serpent_logo() # 打印logo
    print("")



#  update: 将框架更新至最新版本
def update():
    print("update")

#   modules: 列出框架所有可选模块的安装状态
def modules():
    print("modules")

# grab_frames: 启动帧抓取器
def grab_frames():
    print("grab_frames")

#  activate: 激活一个插件
def activate():
    print("activate")

def deactivate():
    print("deactivate")

def plugins():
    print("plugins")


def launch():
    print("launch")

def play():
    print("play")

def record():
    print("record")

# 创建一个游戏插件
def generate(plugin_type):
    print("generate")
    if plugin_type == "game":
        generate_game_plugin()
    elif plugin_type == "game_agent":
        generate_game_agent_plugin()
    else:
        # raise Exception(f"'{plugin_type}' is not a valid plugin type...")
        raise Exception(f" 创建游戏插件  '{plugin_type}'  不是插件类型... 请输入game 或者 game_agent")

def train():
    print("train")

def capture():
    print("capture")

def visual_debugger():
    print("visual_debugger")
def window_name():
    print("window_name")
def record_inputs():
    print("record_inputs")
def dashboard():
    print("dashboard")
def object_recognition():
    print("object_recognition")


def generate_game_plugin():
    clear_terminal()
    display_serpent_logo()
    print("")

    # game_name = input("输入游戏名字 \n")
    # game_platform = input("游戏是如何发行的?(其中之一:'steam'， 'executable'， 'web_browser'): \n")

    game_name = "DNF"
    game_platform = "2"

    if game_name in [None, ""]:
        raise Exception("Invalid game name.")

    if game_platform  in ["1", "2", "3"]:
        if game_platform == "1":
            game_platform = 'steam'
        elif game_platform == "2":
            game_platform = 'executable'
        elif game_platform == "3":
            game_platform = 'web_browser'

    if game_platform not in ["steam", "executable", "web_browser"]:
        raise Exception("Invalid game platform.")




    print("game_name: ", game_name , "  game_platform: ", game_platform)
    prepare_game_plugin(game_name, game_platform)

    print("CMD : ",shlex.split(f"serpent activate Serpent{game_name}GamePlugin"))
    # subprocess.call(shlex.split(f"serpent activate Serpent{game_name}GamePlugin"))



def generate_game_agent_plugin():
    clear_terminal()
    display_serpent_logo()
    print("")

    game_agent_name = input("What is the name of the game agent? (Titleized, No Spaces i.e. AwesomeGameAgent): \n")

    if game_agent_name in [None, ""]:
        raise Exception("Invalid game agent name.")

    # prepare_game_agent_plugin(game_agent_name)

    subprocess.call(shlex.split(f"serpent activate Serpent{game_agent_name}GameAgentPlugin"))
    # print(shlex.split(f"serpent activate Serpent{game_agent_name}GameAgentPlugin"))

def prepare_game_plugin(game_name, game_platform):
    plugin_destination_path = f"{offshoot.config['file_paths']['plugins']}/Serpent{game_name}GamePlugin".replace("/", os.sep)
    print("plugin_destination_path :  ",plugin_destination_path,game_name,game_platform)

    if os.path.exists(plugin_destination_path):
        # 文件夹已经存在
        print("插件已存在")
        pass
    else:
        # 文件夹不存在
        shutil.copytree(
            os.path.join(os.path.dirname(__file__), "templates/SerpentGamePlugin".replace("/", os.sep)),
            plugin_destination_path
        )
    return

    # 读取插件目的地地址下的 plugin.py 文件：
    # Plugin Definition
    with open(f"{plugin_destination_path}/plugin.py".replace("/", os.sep), "r") as f:
        contents = f.read()
    # 然后将读取到的文件内容中的 SerpentGamePlugin 替换为 Serpent{game_name}GamePlugin，serpent_game.py 替换为 serpent_{game_name}_game.py：
    contents = contents.replace("SerpentGamePlugin", f"Serpent{game_name}GamePlugin")
    contents = contents.replace("serpent_game.py", f"serpent_{game_name}_game.py")
    # 接着，将替换后的内容写入到 plugin.py 文件中：
    with open(f"{plugin_destination_path}/plugin.py".replace("/", os.sep), "w") as f:
        f.write(contents)
    # 然后移动 files/serpent_game.py 到 files/serpent_{game_name}_game.py：
    shutil.move(f"{plugin_destination_path}/files/serpent_game.py".replace("/", os.sep), f"{plugin_destination_path}/files/serpent_{game_name}_game.py".replace("/", os.sep))

    # Game
    with open(f"{plugin_destination_path}/files/serpent_{game_name}_game.py".replace("/", os.sep), "r") as f:
        contents = f.read()

    contents = contents.replace("SerpentGame", f"Serpent{game_name}Game")
    contents = contents.replace("MyGameAPI", f"{game_name}API")

    if game_platform == "steam":
        contents = contents.replace("PLATFORM", "steam")

        contents = contents.replace("from serpent.game_launchers.web_browser_game_launcher import WebBrowser", "")
        contents = contents.replace('kwargs["executable_path"] = "EXECUTABLE_PATH"', "")
        contents = contents.replace('kwargs["url"] = "URL"', "")
        contents = contents.replace('kwargs["browser"] = WebBrowser.DEFAULT', "")
    elif game_platform == "executable":
        contents = contents.replace("PLATFORM", "executable")

        contents = contents.replace("from serpent.game_launchers.web_browser_game_launcher import WebBrowser", "")
        contents = contents.replace('kwargs["app_id"] = "APP_ID"', "")
        contents = contents.replace('kwargs["app_args"] = None', "")
        contents = contents.replace('kwargs["url"] = "URL"', "")
        contents = contents.replace('kwargs["browser"] = WebBrowser.DEFAULT', "")
    elif game_platform == "web_browser":
        contents = contents.replace("PLATFORM", "web_browser")

        contents = contents.replace('kwargs["app_id"] = "APP_ID"', "")
        contents = contents.replace('kwargs["app_args"] = None', "")
        contents = contents.replace('kwargs["executable_path"] = "EXECUTABLE_PATH"', "")

    with open(f"{plugin_destination_path}/files/serpent_{game_name}_game.py".replace("/", os.sep), "w") as f:
        f.write(contents)

    # Game API
    with open(f"{plugin_destination_path}/files/api/api.py".replace("/", os.sep), "r") as f:
        contents = f.read()

    contents = contents.replace("MyGameAPI", f"{game_name}API")

    with open(f"{plugin_destination_path}/files/api/api.py".replace("/", os.sep), "w") as f:
        f.write(contents)

def test():
    print("test")
    game_name = "DNF"
    game_platform = "executable"
    plugin_destination_path = f"{offshoot.config['file_paths']['plugins']}/Serpent{game_name}GamePlugin".replace("/",
                                                                                                                 os.sep)
    print("plugin_destination_path :  ", plugin_destination_path, game_name)

    # with open(f"{plugin_destination_path}/plugin.py".replace("/", os.sep), "r") as f:
    #     contents = f.read()
    #
    # # 然后将读取到的文件内容中的 SerpentGamePlugin 替换为 Serpent{game_name}GamePlugin，serpent_game.py 替换为 serpent_{game_name}_game.py：
    # contents = contents.replace("SerpentGamePlugin", f"Serpent{game_name}GamePlugin")
    # contents = contents.replace("serpent_game.py", f"serpent_{game_name}_game.py")
    #
    # # 接着，将替换后的内容写入到 plugin.py 文件中：
    # with open(f"{plugin_destination_path}/plugin.py".replace("/", os.sep), "w") as f:
    #     f.write(contents)

    # # 然后移动 files/serpent_game.py 到 files/serpent_{game_name}_game.py：
    # shutil.move(f"{plugin_destination_path}/files/serpent_game.py".replace("/", os.sep),
    #             f"{plugin_destination_path}/files/serpent_{game_name}_game.py".replace("/", os.sep))

    print("end test")

command_function_mapping = {
    "setup": setup,
    "update": update,
    "modules": modules,
    "grab_frames": grab_frames,
    "activate": activate,
    "deactivate": deactivate,
    "plugins": plugins,
    "launch": launch,
    "play": play,
    "record": record,
    "generate": generate,
    "train": train,
    "capture": capture,
    "visual_debugger": visual_debugger,
    "window_name": window_name,
    "record_inputs": record_inputs,
    "dashboard": dashboard,
    "object_recognition": object_recognition,
    "test":test
}



command_description_mapping = {
    "setup": "进行框架的首次安装设置",
    "update": "将框架更新至最新版本",
    "modules": "列出框架所有可选模块的安装状态",
    "grab_frames": "启动帧抓取器",
    "activate": "激活一个插件",
    "deactivate": "停用一个插件",
    "plugins": "列出所有本地可用插件",
    "launch": "通过插件启动一个游戏",
    "play": "通过插件让游戏代理玩游戏",
    "record": "记录游戏玩家的输入操作",
    "generate": "生成游戏和游戏代理插件的代码",
    "train": "使用收集的上下文帧训练上下文分类器",
    "capture": "从游戏中捕获帧、屏幕区域和上下文",
    "visual_debugger": "启动可视化调试器",
    "window_name": "启动工具以查找游戏的窗口名称",
    "record_inputs": "开始输入记录器",
    "dashboard": "启动仪表盘",
    "object_recognition": "对收集的帧进行物体识别"
}



if __name__ == "__main__":
    execute()
