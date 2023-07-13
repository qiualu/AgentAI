
import inspect

import sys
import serpent.game
# m = "serpent.game"
# exec("import %s" % m)

# classes = inspect.getmembers(sys.modules[m], inspect.isclass)
# print("classes", classes)

import ast
import importlib
from serpent.Editlibrary.yl_offshoot.plugin import Plugin

def activateplugin(plugin_name):
    print("activateplugin",plugin_name)

    # from serpent.plugins.SerpentMLAGamePlugin.plugin import plugin_main
    # plugin_main()

    plugin_code = "from serpent.plugins.%s.plugin import plugin_main" % plugin_name
    # exec(plugin_code)
    # classes = inspect.getmembers(sys.modules[plugin_code], inspect.isclass)

    plugin_module = importlib.import_module('serpent.plugins.%s.plugin' % plugin_name)
    classes = inspect.getmembers(plugin_module, inspect.isclass)
    # print(classes)
    # 获取 plugin_main 函数
    plugin_main = getattr(plugin_module, 'plugin_main')

    # 调用 plugin_main 函数
    plugin_main(plugin_name)


from serpent.plugins.SerpentMLAGamePlugin.plugin import SerpentMLAGamePlugin

def PluginTest():
    p = SerpentMLAGamePlugin()
    print(p.files)
    p.install()
    print("Debug : cls.plugins ",p.plugins)

def python_xg():
    install_messages = list()

    file_dict = {'path': 'serpent_MLA_game.py', 'pluggable': 'Game'}
    plugin_file_path = "plugins\SerpentMLAGamePlugin\files\serpent_MLA_game.py"
    messages = ["SerpentMLAGame: 'after_launch' method should not appear in the class."]

    list(map(lambda m: install_messages.append("\n%s: %s" % (file_dict["path"], m)), messages))

    print(install_messages)



from serpent.utilities import SerpentError, Singleton

import ast
from serpent.Editlibrary.yl_offshoot.base import discover

from serpent.input_controller import InputController, InputControllers

from serpent.config import config
from redis import StrictRedis
class Pluggable:

    def __init__(self, **kwargs):
        pass

# class Game(offshoot.Pluggable):
class Game(Pluggable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = config.get(f"{self.__class__.__name__}Plugin", dict())

        self.platform = kwargs.get("platform")

        default_input_controller_backend = InputControllers.CLIENT
        self.input_controller = kwargs.get("input_controller") or default_input_controller_backend

        self.window_name = kwargs.get("window_name")


        self.redis_client = StrictRedis(**config["redis"])


        self.kwargs = kwargs


class SerpentMLAGame(Game, metaclass=Singleton):

    def __init__(self, **kwargs):
        kwargs["platform"] = "executable"

        kwargs["window_name"] = "WINDOW_NAME44444444444444"

        kwargs["executable_path"] = "EXECUTABLE_PATH5555555555"

# 运行游戏
def pluginDebug():
    file_path = r"plugins\SerpentMLAGamePlugin\files\serpent_MLA_game.py"
    game_name = "MLA"

    game_class_name = f"Serpent{game_name}Game"

    # print("game_class_mapping : ",game_class_mapping)

    Runm = 2

    if Runm == 1:
        # 导入信息:
        # from plugins.SerpentMLAGamePlugin.files.serpent_MLA_game import SerpentMLAGame
        # 导入信息:
        # from plugins.SerpentDNFGamePlugin.files.serpent_DNF_game import SerpentDNFGame

        import_statement = "from plugins.SerpentMLAGamePlugin.files.serpent_MLA_game import SerpentMLAGame"
        exec(import_statement)
        g = eval("SerpentMLAGame")
        print("g : ", g, type(g))
        # g :  <class 'plugins.SerpentMLAGamePlugin.files.serpent_MLA_game.SerpentMLAGame'> <class 'serpent.utilities.Singleton'>

        print(g.help())
        gs = g()
        print("gs : ", gs, type(gs))
        # gs :  <plugins.SerpentMLAGamePlugin.files.serpent_MLA_game.SerpentMLAGame object at 0x0000016246244850> <class 'plugins.SerpentMLAGamePlugin.files.serpent_MLA_game.SerpentMLAGame'>


        from plugins.SerpentMLAGamePlugin.files.serpent_MLA_game import SerpentMLAGame as dsds

        h = dsds()
        hs = dsds()
        print("h",h,type(h))
        # h     <plugins.SerpentMLAGamePlugin.files.serpent_MLA_game.SerpentMLAGame object at 0x00000234E716C2E0> <class 'plugins.SerpentMLAGamePlugin.files.serpent_MLA_game.SerpentMLAGame'>
        if g == h:
            print("两个类等同")
        else:
            print("两类不等同", type(g), type(h))
        return
    elif Runm == 2:
        game_class_mapping = discover("Game")
        game_class = game_class_mapping.get(game_class_name)

        if game_class is None:
            raise Exception(f"Game '{game_name}' wasn't found. Make sure the plugin is installed.")

        game = game_class()

        game.launch()

        print(" ------------- ")
        # print(game.window_name)
        # print(game.redis_client)
        # print(game.platform)

        return

def windows():
    windows_name = "VirtuaNESex - 超级马里奥兄弟 [F0REVERD汉化]"

    from plugins.SerpentMLAGamePlugin.files.serpent_MLA_game import SerpentMLAGame
    game = SerpentMLAGame()
    game.window_controller.locate_window(windows_name)

    adapter = game.window_controller._load_adapter()()
    print("adapter : ",game.game_name)
    print("adapter : ", game.window_name)
    # print("adapter : ", game.name)


import shlex
import subprocess
def subprocessPopen():
    executable_path = r"D:\BaiduNetdiskDownload\小霸王\小霸王游戏\FC全集\★★★FC模拟器★★★【打开模拟器，把游戏拖到模拟器运行】\VirtuaNESex.exe"

    print(shlex.split(executable_path))
    # subprocess.Popen(shlex.split(executable_path))
    subprocess.Popen(executable_path)


def run_plugin_init():
    from serpent.plugins.SerpentMLAGamePlugin.plugin import plugin_init
    plugin_init()


if __name__ == '__main__':
    # print("he,",sys.modules[m])
    # inspect.getmembers(sys.modules[m], inspect.isclass)
    print(" --- Debug 测试模块 --- ")
    # PluginTest()

    # activateplugin("SerpentMLAGamePlugin")

    # python_xg()
    # 测试运行游戏的脚本
    pluginDebug()
    # 测试cmd 打开游戏
    # subprocessPopen()
    # 测试获取窗口相关 系统
    # windows()

    # 运行 测试 exe 引导打开游戏
    # run_plugin_init()
