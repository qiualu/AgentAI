from serpent.visual_debugger.visual_debugger import VisualDebugger

import numpy as np


class GameFrameBufferError(BaseException):
    pass


class GameFrameBuffer:

    def __init__(self, size=5):
        self.size = size
        self.frames = list()
    # 属性返回一个布尔值，检查 frames 列表是否已满。
    @property
    def full(self):
        return len(self.frames) >= self.size
    # 属性返回 frames 列表中最旧的一帧游戏帧，如果列表为空则返回 None。
    @property
    def previous_game_frame(self):
        return self.frames[0] if len(self.frames) else None
    # 方法用于将新的游戏帧添加到缓冲区中
    def add_game_frame(self, game_frame):
        if self.full:
            self.frames = [game_frame] + self.frames[:-1]
        else:
            self.frames = [game_frame] + self.frames
    # 方法用于将缓冲区中的游戏帧传递给 VisualDebugger 对象进行可视化调试
    def to_visual_debugger(self):
        visual_debugger = VisualDebugger()

        for i, game_frame in enumerate(self.frames):
            visual_debugger.store_image_data(
                np.array(game_frame.frame * 255, dtype="uint8"),
                game_frame.frame.shape,
                f"frame_{i + 1}"
            )
