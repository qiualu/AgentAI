import warnings
warnings.simplefilter("ignore")

import offshoot

import subprocess
import signal
import shlex
import time
import os, os.path
import atexit

from serpent.game_agent import GameAgent

from serpent.game_launchers import *

from serpent.window_controller import WindowController

from serpent.input_controller import InputController, InputControllers

from serpent.frame_grabber import FrameGrabber
from serpent.game_frame_limiter import GameFrameLimiter

from serpent.sprite import Sprite

from serpent.utilities import clear_terminal, is_windows, SerpentError

import skimage.io
import skimage.color

import numpy as np

from redis import StrictRedis

from serpent.config import config


class GameError(BaseException):
    pass


class Game(offshoot.Pluggable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = config.get(f"{self.__class__.__name__}Plugin", dict())

        self.platform = kwargs.get("platform")

        default_input_controller_backend = InputControllers.CLIENT
        self.input_controller = kwargs.get("input_controller") or default_input_controller_backend

        self.window_id = None
        self.window_name = kwargs.get("window_name")
        self.window_geometry = None

        self.dashboard_window_id = None

        self.window_controller = WindowController()

        self.is_launched = False

        self.frame_grabber_process = None
        self.frame_transformation_pipeline_string = None

        self.crossbar_process = None
        self.input_controller_process = None

        self.game_frame_limiter = GameFrameLimiter(fps=self.config.get("fps", 30))

        self.api_class = None
        self.api_instance = None

        self.environments = dict()
        self.environment_data = dict()

        self.sprites = self._discover_sprites()

        self.redis_client = StrictRedis(**config["redis"])

        self.pause_callback_fired = False

        self.kwargs = kwargs

    @property
    @offshoot.forbidden
    def game_name(self):
        return self.__class__.__name__.replace("Serpent", "").replace("Game", "")

    @property
    @offshoot.forbidden
    def game_launcher(self):
        return self.game_launchers.get(self.platform)

    @property
    @offshoot.forbidden
    def game_launchers(self):
        return {
            "steam": SteamGameLauncher,
            "executable": ExecutableGameLauncher,
            "web_browser": WebBrowserGameLauncher
        }

    @property
    @offshoot.expected
    def screen_regions(self):
        raise NotImplementedError()

    @property
    @offshoot.forbidden
    def api(self):
        if self.api_instance is None:
            self.api_instance = self.api_class(game=self)
        else:
            return self.api_instance

    @property
    @offshoot.forbidden
    def is_focused(self):
        return self.window_controller.is_window_focused(self.window_id)

    @offshoot.forbidden
    def launch(self, dry_run=False):
        self.before_launch()

        if not dry_run:
            self.game_launcher().launch(**self.kwargs)

        self.after_launch()

    @offshoot.forbidden
    def relaunch(self, before_relaunch=None, after_relaunch=None):
        clear_terminal()
        print("")
        print("Relaunching the game...")

        self.stop_frame_grabber()

        time.sleep(1)

        if before_relaunch is not None:
            before_relaunch()

        time.sleep(1)

        subprocess.call(shlex.split(f"serpent launch {self.game_name}"))
        self.launch(dry_run=True)

        self.start_frame_grabber()
        self.redis_client.delete(config["frame_grabber"]["redis_key"])

        while self.redis_client.llen(config["frame_grabber"]["redis_key"]) == 0:
            time.sleep(0.1)

        self.window_controller.focus_window(self.window_id)

        if after_relaunch is not None:
            after_relaunch()

    def before_launch(self):
        pass

    def after_launch(self):
        self.is_launched = True

        current_attempt = 1

        while current_attempt <= 100:
            self.window_id = self.window_controller.locate_window(self.window_name)

            if self.window_id not in [0, "0"]:
                break

            time.sleep(0.1)

        time.sleep(3)

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

    def play(self, game_agent_class_name="GameAgent", frame_handler=None, **kwargs):
        if not self.is_launched:
            raise GameError(f"Game '{self.__class__.__name__}' is not running...")

        self.start_crossbar()
        time.sleep(3)

        self.start_input_controller()

        game_agent_class = offshoot.discover("GameAgent", selection=game_agent_class_name).get(game_agent_class_name, GameAgent)

        if game_agent_class is None:
            raise GameError("The provided Game Agent class name does not map to an existing class...")

        game_agent = game_agent_class(
            game=self,
            input_controller=InputController(game=self, backend=self.input_controller),
            **kwargs
        )

        # Look if we need to auto-append PNG to frame transformation pipeline based on given frame_handler
        png_frame_handlers = ["RECORD"]

        if frame_handler in png_frame_handlers and self.frame_transformation_pipeline_string is not None:
            if not self.frame_transformation_pipeline_string.endswith("|PNG"):
                self.frame_transformation_pipeline_string += "|PNG"

        self.start_frame_grabber()
        self.redis_client.delete(config["frame_grabber"]["redis_key"])

        while self.redis_client.llen(config["frame_grabber"]["redis_key"]) == 0:
            time.sleep(0.1)

        self.window_controller.focus_window(self.window_id)

        # Override FPS Config?
        if frame_handler == "RECORD":
            self.game_frame_limiter = GameFrameLimiter(fps=10)

        try:
            while True:
                self.game_frame_limiter.start()

                game_frame, game_frame_pipeline = self.grab_latest_frame()

                try:
                    if self.is_focused:
                        self.pause_callback_fired = False
                        game_agent.on_game_frame(game_frame, game_frame_pipeline, frame_handler=frame_handler, **kwargs)
                    else:
                        if not self.pause_callback_fired:
                            print("PAUSED\n")

                            game_agent.on_pause(frame_handler=frame_handler, **kwargs)
                            self.pause_callback_fired = True

                        time.sleep(1)
                except Exception as e:
                    raise e
                    # print(e)
                    # time.sleep(0.1)

                self.game_frame_limiter.stop_and_delay()
        except Exception as e:
            raise e
        finally:
            self.stop_frame_grabber()
            self.stop_input_controller()
            self.stop_crossbar()
            
    @offshoot.forbidden
    def extract_window_geometry(self):
        if self.is_launched:
            return self.window_controller.get_window_geometry(self.window_id)

        return None

    @offshoot.forbidden
    def start_frame_grabber(self, pipeline_string=None):
        if not self.is_launched:
            raise GameError(f"Game '{self.__class__.__name__}' is not running...")

        if self.frame_grabber_process is not None:
            self.stop_frame_grabber()

        frame_grabber_command = f"serpent grab_frames {self.window_geometry['width']} {self.window_geometry['height']} {self.window_geometry['x_offset']} {self.window_geometry['y_offset']}"

        pipeline_string = pipeline_string or self.frame_transformation_pipeline_string

        if pipeline_string is not None:
            frame_grabber_command += f" {pipeline_string}"

        self.frame_grabber_process = subprocess.Popen(shlex.split(frame_grabber_command))

        signal.signal(signal.SIGINT, self._handle_signal_frame_grabber)
        signal.signal(signal.SIGTERM, self._handle_signal_frame_grabber)

        atexit.register(self._handle_signal_frame_grabber, 15, None, False)

    @offshoot.forbidden
    def stop_frame_grabber(self):
        if self.frame_grabber_process is None:
            return None

        self.frame_grabber_process.kill()
        self.frame_grabber_process = None

        atexit.unregister(self._handle_signal_frame_grabber)

    @offshoot.forbidden
    def grab_latest_frame(self):
        game_frame_buffer, game_frame_buffer_pipeline = FrameGrabber.get_frames_with_pipeline([0])

        return game_frame_buffer.frames[0], game_frame_buffer_pipeline.frames[0]

    @offshoot.forbidden
    def start_crossbar(self):
        if self.crossbar_process is not None:
            self.stop_crossbar()

        crossbar_command = f"crossbar start --config crossbar.json"

        self.crossbar_process = subprocess.Popen(shlex.split(crossbar_command))

        signal.signal(signal.SIGINT, self._handle_signal_crossbar)
        signal.signal(signal.SIGTERM, self._handle_signal_crossbar)

        atexit.register(self._handle_signal_crossbar, 15, None, False)

    @offshoot.forbidden
    def stop_crossbar(self):
        if self.crossbar_process is None:
            return None

        self.crossbar_process.kill()
        self.crossbar_process = None

        atexit.unregister(self._handle_signal_crossbar)

    @offshoot.forbidden
    def start_input_controller(self):
        if self.input_controller_process is not None:
            self.stop_input_controller()

        self.redis_client.set("SERPENT:GAME", self.__class__.__name__)

        input_controller_command = f"python -m serpent.wamp_components.input_controller_component"

        self.input_controller_process = subprocess.Popen(shlex.split(input_controller_command))

        signal.signal(signal.SIGINT, self._handle_signal_input_controller)
        signal.signal(signal.SIGTERM, self._handle_signal_input_controller)

        atexit.register(self._handle_signal_input_controller, 15, None, False)

    @offshoot.forbidden
    def stop_input_controller(self):
        if self.input_controller_process is None:
            return None

        self.input_controller_process.kill()
        self.input_controller_process = None

        atexit.unregister(self._handle_signal_input_controller)

    def _discover_sprites(self):
        plugin_path = offshoot.config["file_paths"]["plugins"]
        sprites = dict()

        sprite_path = f"{plugin_path}/{self.__class__.__name__}Plugin/files/data/sprites"

        if os.path.isdir(sprite_path):
            files = os.scandir(sprite_path)

            for file in files:
                if file.name.endswith(".png"):
                    sprite_name = "_".join(file.name.split("/")[-1].split("_")[:-1]).replace(".png", "").upper()

                    sprite_image_data = skimage.io.imread(f"{sprite_path}/{file.name}")
                    sprite_image_data = sprite_image_data[..., np.newaxis]

                    if sprite_name not in sprites:
                        sprite = Sprite(sprite_name, image_data=sprite_image_data)
                        sprites[sprite_name] = sprite
                    else:
                        sprites[sprite_name].append_image_data(sprite_image_data)

        return sprites

    def _handle_signal_frame_grabber(self, signum=15, frame=None, do_exit=True):
        if self.frame_grabber_process is not None:
            if self.frame_grabber_process.poll() is None:
                self.frame_grabber_process.send_signal(signum)

                if do_exit:
                    exit()

    def _handle_signal_crossbar(self, signum=15, frame=None, do_exit=True):
        if self.crossbar_process is not None:
            if self.crossbar_process.poll() is None:
                self.crossbar_process.send_signal(signum)

                if do_exit:
                    exit()

    def _handle_signal_input_controller(self, signum=15, frame=None, do_exit=True):
        if self.input_controller_process is not None:
            if self.input_controller_process.poll() is None:
                self.input_controller_process.send_signal(signum)

                if do_exit:
                    exit()
