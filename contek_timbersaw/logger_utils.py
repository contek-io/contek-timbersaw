import time
import threading
import pandas as pd
from loguru import logger
import json


class LoggingModule:
    def __init__(
        self,
        path: str,  # path to write on disk
        format: str,  # written format
        rotation: str | int,  # the condition of new file
        retention: str | int,  # default: keep some log files
    ):
        self.logger = logger.bind(id=id(self))
        self.path = path
        self.format = format
        self.rotation = rotation
        self.retention = retention
        self.added = self.add()

    def add(self) -> int:
        return self.logger.add(
            sink=self.path,
            format=self.format,
            rotation=self.rotation,
            retention=self.retention,
            filter=lambda record: record["extra"].get("id") == id(self),
        )

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            assert hasattr(self, key), f"{key} is not exist in {self}"
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.logger.remove(self.added)
        self.added = self.add()


class HeartbeatLoggger(LoggingModule):
    def __init__(
        self,
        path: str,
        task: str,
        interval: str,
        rotation: str | int = "500 MB",
        retention: str | int = 3,
        format: str = "[{time:YYYY-MM-DDTHH:mm:ss.SSS}] {message}",
    ):
        super().__init__(path, format, rotation, retention)
        self.task = task
        self.interval = interval
        self.sequence = 0
        self.lock = threading.Lock()

    def one_beat(self):
        self.lock.acquire()
        self.logger.info(f"[{self.task}] [{self.interval}] [{self.sequence}]")
        self.sequence += 1
        self.lock.release()

    def timer_beat(self):
        while True:
            self.one_beat()
            time.sleep(pd.Timedelta(self.interval).total_seconds())

    def start(self):
        thread = threading.Thread(target=self.timer_beat)
        thread.start()


class JsonLogger(LoggingModule):
    def __init__(
        self,
        path: str,
        rotation: str | int = "500 MB",
        retention: str | int = 3,
        format: str = "{extra[serialized]}",
    ):
        super().__init__(path, format, rotation, retention)

    @staticmethod
    def serializer(record):
        record_cp = record["extra"].copy()
        record_cp.pop("id")
        serialized = json.dumps({**record_cp})
        record["extra"]["serialized"] = serialized

    def log(self, **kwargs):
        self.logger.bind(**kwargs).patch(JsonLogger.serializer).info(f"{kwargs}")


if __name__ == "__main__":
    heartbeat_logger = HeartbeatLoggger("heartbeat.log", "task", "5s")
    heartbeat_logger.one_beat()
    heartbeat_logger.update(task="task007")
    heartbeat_logger.one_beat()
    heartbeat_logger.start()

    json_logger = JsonLogger("json.log")
    json_logger.log(json=True, a=1, b=2, c="c", d=1.2)

    with json_logger.logger.contextualize(category="111111"):
        json_logger.log(cnt=1)
    json_logger.log(cnt=2)
