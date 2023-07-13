from serpent.game import Game

from .api.api import MLAAPI

from serpent.utilities import SerpentError, Singleton



import time


class SerpentMLAGame(Game, metaclass=Singleton):

    def __init__(self, **kwargs):



        kwargs["platform"] = "executable"

        kwargs["window_name"] = "WINDOW_NAME44444444444444"

        
        
        kwargs["executable_path"] = "EXECUTABLE_PATH5555555555"
        
        print("脚本当中 kwargs ", kwargs)

        super().__init__(**kwargs)

        self.api_class = MLAAPI
        self.api_instance = None

        self.environments = dict()
        self.environment_data = dict()

    @property  # 装饰器 可以把函数变成直接读取 s = self.area
    def screen_regions(self):
        regions = {
            "SAMPLE_REGION": (0, 0, 0, 0)
        }

        return regions

    # Not  after_launch
    def _after_launch(self):
        self.is_launched = True

        current_attempt = 1

        while current_attempt <= 100:
            self.window_id = self.window_controller.locate_window(self.window_name)

            if self.window_id not in [0, "0"]:
                break

            time.sleep(0.1)

        time.sleep(0.5)

        if self.window_id in [0, "0"]:
            raise SerpentError("Game window not found...")

        self.window_controller.move_window(self.window_id, 0, 0)

        self.dashboard_window_id = self.window_controller.locate_window("Serpent.AI Dashboard")

        # TODO: Test on Linux
        if self.dashboard_window_id is not None and self.dashboard_window_id not in [0, "0"]:
            self.window_controller.bring_window_to_top(self.dashboard_window_id)

        self.window_controller.focus_window(self.window_id)

        self.window_geometry = self.extract_window_geometry()

        print(self.window_geometry)
