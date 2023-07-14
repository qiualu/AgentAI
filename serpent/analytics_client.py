from redis import StrictRedis
from datetime import datetime
from pprint import pprint

from serpent.config import config

import json


class AnalyticsClientError(BaseException):
    pass

# 类用于跟踪分析事件，并将事件发送到 Redis 列表中。类的主要方法和属性包括：
class AnalyticsClient:

    def __init__(self, project_key=None):
        if project_key is None:
            raise AnalyticsClientError("'project_key' kwarg is expected...")

        self.project_key = project_key   # 设置项目密钥
        self.redis_client = StrictRedis(**config["redis"])  # 创建 Redis 客户端连接

        self.broadcast = config["analytics"].get("broadcast", False)  # 获取广播配置，默认为 False
        self.debug = config["analytics"].get("debug", False)  # 获取调试配置，默认为 False

        self.event_whitelist = config["analytics"].get("event_whitelist")  # 获取事件白名单配置

    @property
    def redis_key(self):
        return f"SERPENT:{self.project_key}:EVENTS"  # 返回 Redis 键的名称

    def track(self, event_key=None, data=None, timestamp=None, is_persistable=True):
        if self.event_whitelist is None or event_key in self.event_whitelist:
            event = {
                "project_key": self.project_key,   # 设置项目密钥
                "event_key": event_key,  # 设置事件密钥
                "data": data,  # 设置数据
                "timestamp": timestamp if timestamp is not None else datetime.utcnow().isoformat(),  # 设置时间戳
                "is_persistable": is_persistable  # 设置是否可持久化
            }

            if self.debug:
                pprint(event) # 调试模式下打印事件信息

            if self.broadcast:
                self.redis_client.lpush(self.redis_key, json.dumps(event))   # 将事件推送到 Redis 列表中
