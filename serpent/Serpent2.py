#!/usr/bin/env python
import os
import sys
import shutil
import subprocess
import shlex
import time

#  添加包目录

import os

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)

import sys
sys.path.append(parent_directory)



import offshoot

from serpent.utilities import clear_terminal, display_serpent_logo, is_linux, is_windows, wait_for_crossbar

# clear_terminal, \ 清空控制台
# display_serpent_logo, \ 打印一个logo
# is_linux, is_windows, \ 是否是这个系统
# wait_for_crossbar  连接tcp服务器


from serpent.window_controller import WindowController

# WindowController 操控窗口

# Add the current working directory to sys.path to discover user plugins!
sys.path.insert(0, os.getcwd())

# On Windows, disable the Fortran CTRL-C handler that gets installed with SciPyc
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = 'T' # 表示禁用 Fortran 的 Ctrl+C 处理程序。


VERSION = "2023.7.10"

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
    print(f"\nSerpent 的版本:  v{VERSION} ")
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


    if module is None:
        setup_base()
    elif module == "ocr":
        setup_ocr()
    elif module == "gui":
        setup_gui()
    elif module == "ml":
        setup_ml()
    elif module == "dashboard":
        setup_dashboard()
    else:
        print(f"Invalid Setup Module: {module}")


def setup_gui():
    if is_linux():
        print("Before continuing with the GUI module setup, please read and perform the installation steps from the wiki: https://github.com/SerpentAI/SerpentAI/wiki/Linux-Installation-Guide#gui")
    elif is_windows():
        print("Before continuing with the GUI module setup, please read and perform the installation steps from the wiki: https://github.com/SerpentAI/SerpentAI/wiki/Windows-Installation-Guide#gui")

    print("")
    input("Press Enter to continue...")

    if is_linux():
        subprocess.call(shlex.split("pip install Kivy==1.10.0"))
    elif is_windows():
        subprocess.call(shlex.split("pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew"))
        subprocess.call(shlex.split("pip install Kivy==1.10.0"))

    print("")
    print("GUI module setup complete!")


def setup_ml():
    if is_linux():
        print("Before continuing with the ML module setup, please read and perform the installation steps from the wiki: https://github.com/SerpentAI/SerpentAI/wiki/Linux-Installation-Guide#ml")
    elif is_windows():
        print("Before continuing with the ML module setup, please read and perform the installation steps from the wiki: https://github.com/SerpentAI/SerpentAI/wiki/Windows-Installation-Guide#ml")

    print("")
    input("Press Enter to continue...")

    # Decide on CPU or GPU Tensorflow
    tensorflow_backend = input("\nWhich backend do you plan to use for Tensorflow (One of: 'CPU', 'GPU' - Note: GPU backend can only be used on NVIDIA GTX 600 series and up): \n")

    if tensorflow_backend not in ["CPU", "GPU"]:
        tensorflow_backend = "CPU"

    if tensorflow_backend == "GPU":
        subprocess.call(shlex.split("pip install tensorflow-gpu==1.5.1"))
    elif tensorflow_backend == "CPU":
        subprocess.call(shlex.split("pip install tensorflow==1.5.1"))

    subprocess.call(shlex.split("pip install Keras tensorforce==0.3.5.1"))

    print("")
    print("ML module setup complete!")


def setup_dashboard():
    if is_linux():
        print("Before continuing with the Dashboard module setup, please read and perform the installation steps from the wiki: https://github.com/SerpentAI/SerpentAI/wiki/Linux-Installation-Guide#dashboard")
    elif is_windows():
        print("Before continuing with the Dashboard module setup, please read and perform the installation steps from the wiki: https://github.com/SerpentAI/SerpentAI/wiki/Windows-Installation-Guide#dashboard")

    print("")
    input("Press Enter to continue...")

    # Copy the base dashboard directory to the install location
    shutil.copytree(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard"),
        os.path.join(os.getcwd(), "dashboard")
    )

    # Copy the WAMP components to the install location dashboard directory
    shutil.copy(
        os.path.join(os.path.dirname(__file__), "wamp_components", "analytics_component.py"),
        os.path.join(os.getcwd(), "dashboard", "analytics_component.py")
    )

    shutil.copy(
        os.path.join(os.path.dirname(__file__), "wamp_components", "dashboard_api_component.py"),
        os.path.join(os.getcwd(), "dashboard", "dashboard_api_component.py")
    )

    # Install Kivy
    if is_linux():
        subprocess.call(shlex.split("pip install Kivy==1.10.0"))
    elif is_windows():
        subprocess.call(shlex.split("pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew"))
        subprocess.call(shlex.split("pip install Kivy==1.10.0"))

    # Install CEFPython
    subprocess.call(shlex.split("pip install cefpython3==57.1"))

    # Install Pony ORM
    subprocess.call(shlex.split("pip install pony==0.7.3"))


# TODO: Bring this up to date for dev branch
def update():
    clear_terminal()
    display_serpent_logo()
    print("")

    print("Updating Serpent.AI to the latest version...")

    subprocess.call(shlex.split("pip install --upgrade SerpentAI"))

    if is_linux():
        shutil.copy(
            os.path.join(os.path.dirname(__file__), "requirements.linux.txt"),
            os.path.join(os.getcwd(), "requirements.txt")
        )
    elif is_windows():
        shutil.copy(
            os.path.join(os.path.dirname(__file__), "requirements.win32.txt"),
            os.path.join(os.getcwd(), "requirements.txt")
        )

    subprocess.call(shlex.split("pip install -r requirements.txt"))

    import yaml

    with open(os.path.join(os.path.dirname(__file__), "config", "config.yml"), "r") as f:
        serpent_config = yaml.safe_load(f) or {}

    with open(os.path.join(os.getcwd(), "config", "config.yml"), "r") as f:
        user_config = yaml.safe_load(f) or {}

    config_changed = False

    for key, value in serpent_config.items():
        if key not in user_config:
            user_config[key] = value
            config_changed = True

    if config_changed:
        with open(os.path.join(os.getcwd(), "config", "config.yml"), "w") as f:
            f.write(yaml.dump(user_config))


def modules():
    import importlib
    exists = importlib.util.find_spec

    serpent_modules = {
        "OCR": (exists("tesserocr") or exists("pytesseract")) is not None,
        "GUI": exists("kivy") is not None,
        "ML": exists("keras") is not None and exists("tensorforce") is not None,
        "DASHBOARD": exists("kivy") is not None and exists("cefpython3") is not None and exists("pony") is not None
    }

    clear_terminal()
    display_serpent_logo()
    print("")

    print("Installed Serpent.AI Modules:")
    print("")

    print(f"OCR => {'Yes' if serpent_modules['OCR'] else 'No; Install with `serpent setup ocr` if needed'}")
    print(f"GUI => {'Yes' if serpent_modules['GUI'] else 'No; Install with `serpent setup gui` if needed'}")
    print(f"ML => {'Yes' if serpent_modules['ML'] else 'No; Install with `serpent setup ml` if needed'}")
    print(f"DASHBOARD => {'Yes' if serpent_modules['DASHBOARD'] else 'No; Install with `serpent setup dashboard` if needed'}")

    print("")


def grab_frames(width, height, x_offset, y_offset, pipeline_string=None):
    from serpent.frame_grabber import FrameGrabber

    frame_grabber = FrameGrabber(
        width=int(width),
        height=int(height),
        x_offset=int(x_offset),
        y_offset=int(y_offset),
        pipeline_string=pipeline_string
    )

    frame_grabber.start()


def activate(plugin_name):
    subprocess.call(shlex.split(f"offshoot install {plugin_name}"))


def deactivate(plugin_name):
    subprocess.call(shlex.split(f"offshoot uninstall {plugin_name}"))


def plugins():
    plugin_names = set()

    for root, directories, files in os.walk(offshoot.config['file_paths']['plugins']):
        if root != offshoot.config['file_paths']['plugins']:
            break

        for directory in directories:
            plugin_names.add(directory)

    manifest_plugin_names = set()

    for plugin_name in offshoot.Manifest().list_plugins().keys():
        manifest_plugin_names.add(plugin_name)

    active_plugins = plugin_names & manifest_plugin_names
    inactive_plugins = plugin_names - manifest_plugin_names

    print("\nACTIVE Plugins:\n")
    print("\n".join(active_plugins or ["No active plugins..."]))

    print("\nINACTIVE Plugins:\n")
    print("\n".join(inactive_plugins or ["No inactive plugins..."]))


def launch(game_name):
    game = initialize_game(game_name)
    game.launch()


def play(game_name, game_agent_name, frame_handler=None):
    game = initialize_game(game_name)
    game.launch(dry_run=True)

    game_agent_class_mapping = offshoot.discover("GameAgent", selection=game_agent_name)
    game_agent_class = game_agent_class_mapping.get(game_agent_name)

    if game_agent_class is None:
        raise Exception(f"Game Agent '{game_agent_name}' wasn't found. Make sure the plugin is installed.")

    game.play(game_agent_class_name=game_agent_name, frame_handler=frame_handler)


def record(game_name, game_agent_name, frame_count=4, frame_spacing=4):
    game = initialize_game(game_name)
    game.launch(dry_run=True)

    game.play(
        game_agent_class_name=game_agent_name,
        frame_handler="RECORD",
        frame_count=int(frame_count),
        frame_spacing=int(frame_spacing)
    )




def train(training_type, *args):
    if training_type == "context":
        train_context(*args)
    elif training_type == "object":
        train_object(*args)


def capture(capture_type, game_name, interval=1, extra=None, extra_2=None):
    game = initialize_game(game_name)
    game.launch(dry_run=True)

    if capture_type not in ["frame", "context", "region"]:
        raise Exception("Invalid capture command.")

    if capture_type == "frame":
        game.play(frame_handler="COLLECT_FRAMES", interval=float(interval))
    elif capture_type == "context":
        game.play(frame_handler="COLLECT_FRAMES_FOR_CONTEXT", interval=float(interval), context=extra, screen_region=extra_2)
    elif capture_type == "region":
        game.play(frame_handler="COLLECT_FRAME_REGIONS", interval=float(interval), region=extra)


def visual_debugger(*buckets):
    from serpent.visual_debugger.visual_debugger_app import VisualDebuggerApp
    VisualDebuggerApp(buckets=buckets or None).run()


def window_name():
    clear_terminal()
    print("Open the Game manually.")

    input("\nPress Enter and then focus the game window...")

    window_controller = WindowController()

    time.sleep(5)

    focused_window_name = window_controller.get_focused_window_name()

    print(f"\nGame Window Detected! Please set the kwargs['window_name'] value in the Game plugin to:")
    print("\n" + focused_window_name + "\n")


def record_inputs():
    from serpent.input_recorder import InputRecorder

    input_recorder = InputRecorder()

    input_recorder.start()


def dashboard(width=None, height=None):
    if width is not None and height is not None:
        width = int(width)
        height = int(height)

    wait_for_crossbar()

    from serpent.dashboard.dashboard_app import DashboardApp
    DashboardApp(width=width, height=height).run()


def object_recognition(game_agent_name, model_name):
    model_path = f"plugins/{game_agent_name}Plugin/files/ml_models/object_recognition/{model_name}"

    from serpent.machine_learning.object_recognition.object_recognizer import ObjectRecognizer
    object_recognizer = ObjectRecognizer(model_name, model_path=model_path)

    object_recognizer.predict_directory("datasets/collect_frames")




# 创建一个游戏插件
def generate(plugin_type):
    print("generate")
    if plugin_type == "game" or plugin_type == "游戏":
        generate_game_plugin()
    elif plugin_type == "game_agent" or plugin_type == "游戏代理":
        generate_game_agent_plugin()
    else:
        # raise Exception(f"'{plugin_type}' is not a valid plugin type...")
        raise Exception(f" 创建游戏插件  '{plugin_type}'  不是插件类型... 请输入game 或者 game_agent")


def train(training_type, *args):
    if training_type == "context":
        train_context(*args)
    elif training_type == "object":
        train_object(*args)


def capture(capture_type, game_name, interval=1, extra=None, extra_2=None):
    game = initialize_game(game_name)
    game.launch(dry_run=True)

    if capture_type not in ["frame", "context", "region"]:
        raise Exception("Invalid capture command.")

    if capture_type == "frame":
        game.play(frame_handler="COLLECT_FRAMES", interval=float(interval))
    elif capture_type == "context":
        game.play(frame_handler="COLLECT_FRAMES_FOR_CONTEXT", interval=float(interval), context=extra, screen_region=extra_2)
    elif capture_type == "region":
        game.play(frame_handler="COLLECT_FRAME_REGIONS", interval=float(interval), region=extra)


def visual_debugger(*buckets):
    from serpent.visual_debugger.visual_debugger_app import VisualDebuggerApp
    VisualDebuggerApp(buckets=buckets or None).run()


def window_name():
    clear_terminal()
    print("Open the Game manually.")

    input("\nPress Enter and then focus the game window...")

    window_controller = WindowController()

    time.sleep(5)

    focused_window_name = window_controller.get_focused_window_name()

    print(f"\nGame Window Detected! Please set the kwargs['window_name'] value in the Game plugin to:")
    print("\n" + focused_window_name + "\n")


def record_inputs():
    from serpent.input_recorder import InputRecorder

    input_recorder = InputRecorder()

    input_recorder.start()


def dashboard(width=None, height=None):
    if width is not None and height is not None:
        width = int(width)
        height = int(height)

    wait_for_crossbar()

    from serpent.dashboard.dashboard_app import DashboardApp
    DashboardApp(width=width, height=height).run()


def object_recognition(game_agent_name, model_name):
    model_path = f"plugins/{game_agent_name}Plugin/files/ml_models/object_recognition/{model_name}"

    from serpent.machine_learning.object_recognition.object_recognizer import ObjectRecognizer
    object_recognizer = ObjectRecognizer(model_name, model_path=model_path)

    object_recognizer.predict_directory("datasets/collect_frames")


def generate_game_plugin():
    clear_terminal()
    display_serpent_logo()
    print("")

    game_name = input("输入游戏名字 \n")
    game_platform = input("游戏是如何发行的?(其中之一:'steam'， 'executable'， 'web_browser','custom'): \n")

    # game_name = "DNF"
    # game_platform = "2"

    if game_name in [None, ""]:
        raise Exception("Invalid game name.")

    if game_platform  in ["1", "2", "3","4"]:
        if game_platform == "1":
            game_platform = 'steam'
        elif game_platform == "2":
            game_platform = 'executable'
        elif game_platform == "3":
            game_platform = 'web_browser'
        elif game_platform == "4":
            game_platform = 'custom'

    if game_platform not in ["steam", "executable", "web_browser","custom"]:
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

    prepare_game_agent_plugin(game_agent_name)

    subprocess.call(shlex.split(f"serpent activate Serpent{game_agent_name}GameAgentPlugin"))


def prepare_game_plugin(game_name, game_platform):
    plugin_destination_path = f"{offshoot.config['file_paths']['plugins']}/Serpent{game_name}GamePlugin".replace("/",
                                                                                                                 os.sep)

    shutil.copytree(
        os.path.join(os.path.dirname(__file__), "templates/SerpentGamePlugin".replace("/", os.sep)),
        plugin_destination_path
    )

    # Plugin Definition
    with open(f"{plugin_destination_path}/plugin.py".replace("/", os.sep), "r") as f:
        contents = f.read()

    contents = contents.replace("SerpentGamePlugin", f"Serpent{game_name}GamePlugin")
    contents = contents.replace("serpent_game.py", f"serpent_{game_name}_game.py")

    with open(f"{plugin_destination_path}/plugin.py".replace("/", os.sep), "w") as f:
        f.write(contents)

    shutil.move(f"{plugin_destination_path}/files/serpent_game.py".replace("/", os.sep),
                f"{plugin_destination_path}/files/serpent_{game_name}_game.py".replace("/", os.sep))

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


def prepare_game_agent_plugin(game_agent_name):
    plugin_destination_path = f"{offshoot.config['file_paths']['plugins']}/Serpent{game_agent_name}GameAgentPlugin".replace(
        "/", os.sep)

    shutil.copytree(
        os.path.join(os.path.dirname(__file__), "templates/SerpentGameAgentPlugin".replace("/", os.sep)),
        plugin_destination_path
    )

    with open(f"{plugin_destination_path}/plugin.py", "r") as f:
        contents = f.read()

    contents = contents.replace("SerpentGameAgentPlugin", f"Serpent{game_agent_name}GameAgentPlugin")
    contents = contents.replace("serpent_game_agent.py", f"serpent_{game_agent_name}_game_agent.py")

    with open(f"{plugin_destination_path}/plugin.py", "w") as f:
        f.write(contents)

    shutil.move(f"{plugin_destination_path}/files/serpent_game_agent.py",
                f"{plugin_destination_path}/files/serpent_{game_agent_name}_game_agent.py")

    with open(f"{plugin_destination_path}/files/serpent_{game_agent_name}_game_agent.py", "r") as f:
        contents = f.read()

    contents = contents.replace("SerpentGameAgent", f"Serpent{game_agent_name}GameAgent")

    with open(f"{plugin_destination_path}/files/serpent_{game_agent_name}_game_agent.py", "w") as f:
        f.write(contents)


def train_context(epochs=3, validate=True, autosave=False):
    if validate not in [True, "True", False, "False"]:
        raise ValueError("'validate' should be True or False")

    if autosave not in [True, "True", False, "False"]:
        raise ValueError("'autosave' should be True or False")

    from serpent.machine_learning.context_classification.context_classifier import ContextClassifier
    ContextClassifier.executable_train(epochs=int(epochs), validate=argv_is_true(validate),
                                       autosave=argv_is_true(autosave))


def train_object(name, algorithm, *classes):
    from serpent.machine_learning.object_recognition.object_recognizer import ObjectRecognizer, ObjectRecognizers

    backend = "luminoth"

    backend_mapping = {
        "luminoth": ObjectRecognizers.LUMINOTH
    }

    object_recognizer = ObjectRecognizer(
        name,
        backend=backend_mapping[backend],
        algorithm=algorithm,
        classes=classes
    )

    import signal
    signal.signal(signal.SIGINT, object_recognizer.on_interrupt)

    object_recognizer.train()


def initialize_game(game_name):
    game_class_name = f"Serpent{game_name}Game"

    game_class_mapping = offshoot.discover("Game")
    game_class = game_class_mapping.get(game_class_name)

    if game_class is None:
        raise Exception(f"Game '{game_name}' wasn't found. Make sure the plugin is installed.")

    game = game_class()

    return game


def argv_is_true(arg):
    return arg in [True, "True"]


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

    print("Serpent start YL 55")
    execute()
