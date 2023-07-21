import skimage.color
import skimage.measure
import skimage.transform
import skimage.filters
import skimage.morphology

import numpy as np

import io

from PIL import Image


class GameFrameError(BaseException):
    pass


class GameFrame:
    # 初始化方法，接受帧数据、帧变体、时间戳和其他参数作为输入。
    def __init__(self, frame_data, frame_variants=None, timestamp=None, **kwargs):
        if isinstance(frame_data, bytes):
            self.frame_bytes = frame_data
            self.frame_array = None
        elif isinstance(frame_data, np.ndarray):
            self.frame_bytes = None
            self.frame_array = frame_data

        self.frame_variants = frame_variants or dict()

        self.timestamp = timestamp

        self.offset_x = kwargs.get("offset_x") or 0
        self.offset_y = kwargs.get("offset_y") or 0

        self.resize_order = kwargs.get("resize_order") or 1
    # 返回帧数据（字节数组或数组）。
    @property
    def frame(self):
        return self.frame_array if self.frame_array is not None else self.frame_bytes
    # 返回帧的四分之一大小的版本（宽度减半，高度减半）。
    @property
    def half_resolution_frame(self):
        """ A quarter-sized version of the frame (half-width, half-height)"""

        if "half" not in self.frame_variants:
            self.frame_variants["half"] = self._to_half_resolution()

        return self.frame_variants["half"]
    # 返回帧的十六分之一大小的版本（宽度四分之一，高度四分之一）。
    @property
    def quarter_resolution_frame(self):
        """ A sixteenth-sized version of the frame (quarter-width, quarter-height)"""

        if "quarter" not in self.frame_variants:
            self.frame_variants["quarter"] = self._to_quarter_resolution()

        return self.frame_variants["quarter"]
    # 返回帧的1/32大小的版本（宽度八分之一，高度八分之一）。
    @property
    def eighth_resolution_frame(self):
        """ A 1/32-sized version of the frame (eighth-width, eighth-height)"""

        if "eighth" not in self.frame_variants:
            self.frame_variants["eighth"] = self._to_eighth_resolution()

        return self.frame_variants["eighth"]
    # 返回帧的1/32大小的灰度版本（宽度八分之一，高度八分之一）。
    @property
    def eighth_resolution_grayscale_frame(self):
        """ A 1/32-sized, grayscale version of the frame (eighth-width, eighth-height)"""

        if "eighth_grayscale" not in self.frame_variants:
            self.frame_variants["eighth_grayscale"] = self._to_eighth_grayscale_resolution()

        return self.frame_variants["eighth_grayscale"]
    # 返回帧的全尺寸灰度版本。
    @property
    def grayscale_frame(self):
        """ A full-size grayscale version of the frame"""

        if "grayscale" not in self.frame_variants:
            self.frame_variants["grayscale"] = self._to_grayscale()

        return self.frame_variants["grayscale"]
    # 返回用于SSIM的100x100灰度帧。
    @property
    def ssim_frame(self):
        """ A 100x100 grayscale frame to be used for SSIM"""

        if "ssim" not in self.frame_variants:
            self.frame_variants["ssim"] = self._to_ssim()

        return self.frame_variants["ssim"]
    # 返回最常见的颜色。
    @property
    def top_color(self):
        height, width, channels = self.eighth_resolution_frame.shape
        values, counts = np.unique(self.eighth_resolution_frame.reshape(width * height, channels), axis=0, return_counts=True)

        return [int(i) for i in values[np.argsort(counts)[::-1][0]]]
    # 计算当前帧与前一帧之间的结构相似性。
    def compare_ssim(self, previous_game_frame):
        return skimage.measure.compare_ssim(previous_game_frame.ssim_frame, self.ssim_frame)
    # 计算当前帧与前一帧之间的差异。
    def difference(self, previous_game_frame):
        current = skimage.filters.gaussian(self.grayscale_frame, 8)
        previous = skimage.filters.gaussian(previous_game_frame.grayscale_frame, 8)

        return current - previous
    # 将帧转换为PIL图像对象。
    def to_pil(self):
        return Image.fromarray(self.frame)
    # 将帧转换为PNG字节数组。
    def to_png_bytes(self):
        pil_frame = Image.fromarray(skimage.util.img_as_ubyte(self.frame))

        if len(self.frame.shape) == 3:
            pil_frame = pil_frame.convert("RGB")

        png_frame = io.BytesIO()

        pil_frame.save(png_frame, format="PNG", compress_level=3)
        png_frame.seek(0)

        return png_frame.read()

    # 将帧缩小到四分之一大小的内部方法。
    # TODO: Refactor Fraction of Resolution Frames...
    def _to_half_resolution(self):
        shape = (
            self.frame_array.shape[0] // 2,
            self.frame_array.shape[1] // 2
        )

        return np.array(skimage.transform.resize(self.frame_array, shape, mode="reflect", order=self.resize_order) * 255, dtype="uint8")
    # 将帧缩小到十六分之一大小的内部方法。
    def _to_quarter_resolution(self):
        shape = (
            self.frame_array.shape[0] // 4,
            self.frame_array.shape[1] // 4
        )

        return np.array(skimage.transform.resize(self.frame_array, shape, mode="reflect", order=self.resize_order) * 255, dtype="uint8")
    # 将帧缩小到1/32大小的内部方法。
    def _to_eighth_resolution(self):
        shape = (
            self.frame_array.shape[0] // 8,
            self.frame_array.shape[1] // 8
        )

        return np.array(skimage.transform.resize(self.frame_array, shape, mode="reflect", order=self.resize_order) * 255, dtype="uint8")
    # 将帧缩小到1/32大小的灰度版本的内部方法。
    def _to_eighth_grayscale_resolution(self):
        shape = (
            self.frame_array.shape[0] // 8,
            self.frame_array.shape[1] // 8
        )

        return np.array(skimage.transform.resize(self.grayscale_frame, shape, mode="reflect", order=self.resize_order) * 255, dtype="uint8")
    # 将帧转换为灰度版本的内部方法。
    def _to_grayscale(self):
        return np.array(skimage.color.rgb2gray(self.frame_array) * 255, dtype="uint8")
    # 将帧缩放为100x100大小的灰度版本的内部方法。
    def _to_ssim(self):
        grayscale = self.grayscale_frame
        return skimage.transform.resize(grayscale, (100, 100), mode="reflect", order=0)
