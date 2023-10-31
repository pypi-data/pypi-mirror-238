import enum
from queue import Queue
import time
import numpy as np
from loguru import logger

class Acc(enum.Enum):
    X = 0
    Y = 1
    Z = 2

class BoxPacket(object):
    def __init__(self, id, points) -> None:
        self.__id = id
        self.__eeg, self.__acc = BoxPacket.parse(points)
        
    def __lt__(self, other):
        return self.__id < other.__id

    def __gt__(self, other):
        return self.__id > other.__id

    def __eq__(self, other):
        return self.__id == other.__id

    @property
    def id(self):
        return self.__id

    # 一维数组
    @property
    def eeg(self):
        return self.__eeg

    # 一维数组/二维数组
    @property
    def acc(self, dim : Acc = None):
        if dim :
            return self.__acc[dim.value]
        
        return self.__acc
        
    @staticmethod
    def parse(data):
        # 1, 2 数据相同（只有一通道数据)
        eegs = []
        # x, y, z
        acc = [[],[],[]]
        for i in range(0, 200, 4):
            eegs.append(int.from_bytes(data[i : i + 2], 'little'))
        for i in range(200, 230, 6):
            acc[0].append(int.from_bytes(data[i : i + 2], 'little'))
            acc[1].append(int.from_bytes(data[i + 2 : i + 4], 'little'))
            acc[2].append(int.from_bytes(data[i + 4 : i + 6], 'little'))

        # 数字信号转换为电压值(mv)
        eegs = (np.array(eegs) -32768) * (2500000 / 48 / 4 / 32768)
        return eegs, acc

class BoxMessageQueue(Queue):
    def __init__(self, maxsize: int = 0) -> None:
        super().__init__(maxsize)
        self.__uid = int(time.time() * 1000000)
        self.__latest_id = None
        self.__total = 0

    def put(self, v:BoxPacket):
        super().put(v)
        self.__latest_id = v.id
        self.__total += 1
        if self.qsize() >= 3000 and self.qsize() % 1000 == 0:
            logger.warning(f'队列（{self.__uid}）已有{self.__total}条数据未消费，请关注。')

    @classmethod
    def unique_id(self, key):
        self.__uid = key

    @property
    def latest_id(self):
        return self.__latest_id

    @property
    def total(self):
        return self.__total