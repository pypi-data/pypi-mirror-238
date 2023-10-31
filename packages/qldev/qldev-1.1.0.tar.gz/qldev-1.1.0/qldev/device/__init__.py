from .handler import *

class Device(object):
    def __init__(self) -> None:
        pass

class QLDevice(Device):
    def __init__(self, handler: MessageHandler = None) -> None:
        super().__init__()
        self.__handler = handler

    @property
    def handler(self):
        return self.__handler