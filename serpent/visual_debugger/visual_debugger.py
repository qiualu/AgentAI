from redis import StrictRedis

import skimage.io
import numpy as np

import pickle
import itertools

from serpent.config import config

# 调试过程中存储和检索图像数据
class VisualDebugger:

    def __init__(self, buckets=None):
        self.available_buckets = buckets or config["visual_debugger"]["available_buckets"]
        self.bucket_generator = itertools.cycle(self.available_buckets)

        self.redis_client = StrictRedis(**config["redis"])
        self.clear_image_data()

    # 存储图像数据的方法
    def store_image_data(self, image_data, image_shape, bucket="debug"):

        self.redis_client.lpush(f"{config['visual_debugger']['redis_key_prefix']}:{bucket}:SHAPE", pickle.dumps(image_shape))
        self.redis_client.lpush(f"{config['visual_debugger']['redis_key_prefix']}:{bucket}", image_data.tobytes())

    # 检索图像数据的方法
    def retrieve_image_data(self):
        bucket = next(self.bucket_generator)
        bucket_key = f"{config['visual_debugger']['redis_key_prefix']}:{bucket}"

        response = self.redis_client.rpop(bucket_key)

        if response is not None:
            bucket = bucket_key.split(":")[-1]

            image_shape = self.redis_client.rpop(f"{config['visual_debugger']['redis_key_prefix']}:{bucket}:SHAPE")
            image_shape = pickle.loads(image_shape)

            image_data = np.fromstring(response, dtype="float64").reshape(image_shape)

            return bucket, image_data

        return None
    # 保存图像数据的方法
    def save_image_data(self, bucket, image_data):
        if bucket in self.available_buckets:
            if image_data.dtype == "bool" or (image_data.dtype == "uint8" and 1 in np.unique(image_data)):
                image_data = image_data.astype("uint8") * 255

            skimage.io.imsave(f"{bucket}.png", image_data)
    # 清空图像数据的方法
    def clear_image_data(self):
        visual_debugger_keys = self.redis_client.keys(f"{config['visual_debugger']['redis_key_prefix']}*")

        for key in visual_debugger_keys:
            self.redis_client.delete(key.decode("utf-8"))
    # 获取指定存储桶中的队列长度的方法
    def get_bucket_queue_length(self, bucket):
        return self.redis_client.llen(f"{config['visual_debugger']['redis_key_prefix']}:{bucket}")
