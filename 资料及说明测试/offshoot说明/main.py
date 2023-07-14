#!/usr/bin/env python
import sys
import os

import subprocess

import offshoot

valid_commands = ["init", "install", "uninstall"]


def execute():
    print("len(sys.argv) : ", len(sys.argv), sys.argv)

    if len(sys.argv) == 2:

        command = sys.argv[1]

        if command not in valid_commands:
            raise Exception("'%s' is not a valid Offshoot command." % command)

        if command == "init":
            init()
    elif len(sys.argv) > 2:
        command, args = sys.argv[1], sys.argv[2:]
        print(command, args)
        if command not in valid_commands:
            raise Exception("'%s' is not a valid Offshoot command." % command)

        if command == "install":
            install(args[0])
        elif command == "uninstall":
            uninstall(args[0])


def install(plugin):
    print("OFFSHOOT: Attempting to install %s..." % plugin)
    # 读取 offshoot.yml 中的PLUGIN_HOME 配置项
    plugin_directory = offshoot.config.get("file_paths").get("plugins")
    # plugins\SerpentMLAGamePlugin\plugin.py 插件路径
    plugin_path = "%s/%s/plugin.py".replace("/", os.sep) % (plugin_directory, plugin)
    # 执行 install 命令
    # plugins.SerpentMLAGamePlugin.plugin
    plugin_module_string = plugin_path.replace(os.sep, ".").replace(".py", "")

    print(plugin_module_string)
    print("os.sep : ",os.sep) # os.sep :  \
    print("sys.executable.split(os.sep): ", sys.executable.split(os.sep))
    # sys.executable.split(os.sep):  ['C:', 'Users', 'yl', '.conda', 'envs', 'AgentAI', 'python.exe']
    print([sys.executable.split(os.sep)[-1], "-m", "%s" % plugin_module_string, "install"])
    # ['python.exe', '-m', 'plugins.SerpentMLAGamePlugin.plugin', 'install']
    return

    subprocess.call([sys.executable.split(os.sep)[-1], "-m", "%s" % plugin_module_string, "install"])


def uninstall(plugin):
    print("OFFSHOOT: Attempting to uninstall %s..." % plugin)

    plugin_directory = offshoot.config.get("file_paths").get("plugins")
    plugin_path = "%s/%s/plugin.py".replace("/", os.sep) % (plugin_directory, plugin)

    plugin_module_string = plugin_path.replace(os.sep, ".").replace(".py", "")

    print("plugin_directory : ",plugin_directory)
    print("plugin_path : ", plugin_path)
    print("plugin_module_string : ", plugin_module_string)
    print([sys.executable.split(os.sep)[-1], "-m", "%s" % plugin_module_string, "uninstall"])

    # plugin_directory: plugins
    # plugin_path: plugins\SerpentMLAGamePlugin\plugin.py
    # plugin_module_string: plugins.SerpentMLAGamePlugin.plugin
    # ['python.exe', '-m', 'plugins.SerpentMLAGamePlugin.plugin', 'uninstall']

    return
    subprocess.call([sys.executable.split(os.sep)[-1], "-m", "%s" % plugin_module_string, "uninstall"])


def init():
    import warnings
    warnings.filterwarnings("ignore")

    print("OFFSHOOT: Generating configuration file...")
    offshoot.generate_configuration_file()
    print("OFFSHOOT: Initialized successfully!")


if __name__ == "__main__":
    # sys.argv = [r"E:\Projece\python\SerpentAI\函数案例说明\offshoot说明", 'install', 'SerpentMLAGamePlugin']
    sys.argv = [r"E:\Projece\python\SerpentAI\函数案例说明\offshoot说明", 'uninstall', 'SerpentMLAGamePlugin']

    execute()
