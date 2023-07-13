from serpent.game_launcher import GameLauncher, GameLauncherException
from serpent.utilities import is_linux, is_windows

import shlex
import subprocess


class ExecutableGameLauncher(GameLauncher):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def launch(self, **kwargs):
        executable_path = kwargs.get("executable_path")
        # exe 的路径
        # print("executable_path",executable_path)
        # return
        if executable_path is None:
            raise GameLauncherException("An 'executable_path' kwarg is required...")
        try:
            if is_linux():
                subprocess.Popen(shlex.split(executable_path))
            elif is_windows():
                subprocess.Popen(shlex.split(executable_path))
        except:
            print("y except : 启动exe  serpent/game_launchers/executable_game_launcher.py")
            if is_linux():
                subprocess.Popen(executable_path)
            elif is_windows():
                subprocess.Popen(executable_path)