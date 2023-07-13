
import inspect

import sys
import serpent.game
# m = "serpent.game"
# exec("import %s" % m)

# classes = inspect.getmembers(sys.modules[m], inspect.isclass)
# print("classes", classes)


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


if __name__ == '__main__':
    # print("he,",sys.modules[m])
    # inspect.getmembers(sys.modules[m], inspect.isclass)
    print("HHH")
    # PluginTest()

    # activateplugin("SerpentMLAGamePlugin")

    python_xg()
