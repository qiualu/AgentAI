import offshoot


class SerpentDNFGamePlugin(offshoot.Plugin):
    name = "SerpentDNFGamePlugin"
    version = "0.1.0"

    libraries = []

    files = [
        {"path": "serpent_DNF_game.py", "pluggable": "Game"}
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



def plugin_main():
    print("plugin_main 插件文件开始运行")
    # executable_hook(SerpentGamePlugin)

if __name__ == "__main__":
    offshoot.executable_hook(SerpentDNFGamePlugin)
