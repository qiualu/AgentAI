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
    print("plugin_main 插件文件开始运行",command)
    executable_hook(SerpentMLAGamePlugin, command)


if __name__ == "__main__":
    offshoot.executable_hook(SerpentMLAGamePlugin)
