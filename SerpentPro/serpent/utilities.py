import sys
import subprocess
import socket
import time
import enum

# ----Start 系统 属性 windows  ------
class SerpentError(BaseException):
    pass

class OperatingSystem(enum.Enum):
    LINUX = 0
    WINDOWS = 1

def operating_system():
    if sys.platform in ["linux", "linux2"]:
        return OperatingSystem.LINUX
    elif sys.platform == "win32":
        return OperatingSystem.WINDOWS

def is_linux():
    return operating_system().name == "LINUX"

def is_windows():
    return operating_system().name == "WINDOWS"
# ----End 系统 属性 windows  ------

# 清除屏幕
def clear_terminal():
    if is_linux():
        print("\033c")
    elif is_windows():
        subprocess.call(["cls"], shell=True)

# 打印一个logo
def display_serpent_logo():
    print("""
                         ▄▄▄▄█████▄▄▄
                     ▄█████████▀▀`  ,
                  ▄██████████",▄▄▄██  █ L
                ╓██████████▀╓█████▀  ██ ▌ j
               ▄██████████▀▄███▀▀ ▄███ █▌ ▐▌
              ▐██████████   ▄▄▄█████▀╓██  ██
              █████████▀▄▄███████▀`▄███` ██▌▐U
              ███████▀,███▀▀▀` ▄▄████▀ ,███ █`╒
              ▀▀▐▄▄   `     ╓██████▀  ▄███ ██ █
                          ▄████▀▀-  ▄███▀╓██-▐█
                      ^▀▀▀▀▀- ,▄██  ██▀,███`╒██
                            ▐████" ▀▀▄████ ▄██▌
                            ▐███▀ ,▄████▀ ▄██▌
                            ███▀ ╓████" ▄███▀
                           ▐██  ▄██▀ ,▄████▀
                          ▄█▀ ,▀▀ ▄▄█████▀
                        .▀   ,▄▄███████▀          ,    ,
                       ,▄▄▄█████████▀-           ███  ▐█
                 ,▄▄████████████▀▀              ██ █▌ ▐█
             ▄▄███████████▀▀▀                  ▄█▀▀▀█▄▐█
          ▄███████▀▀▀                          ``      `
       ,▄███▀▀'
      ▄██▀
     █▀`
    ▐▀
    `
    """)

def wait_for_crossbar():
    from config import config
    print(config["crossbar"]["host"], config["crossbar"]["port"])
    while True:
        s = socket.socket()

        try:
            s.connect((config["crossbar"]["host"], config["crossbar"]["port"]))
            s.close()
            break
        except Exception:
            print("Waiting for Crossbar server...")
            time.sleep(0.1)
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

