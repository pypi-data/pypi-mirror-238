from .crcutils import *
from .local import *

from enum import Enum 

class UDPCommand(Enum):
    NOTIFY = 0x9
    CONNECT = 0x10


class TCPCommand(Enum):
    GET_DEVICE_INFO = 0x10
    SIGNALS = 0X455
    TRIGGER = 0x501
    WAV_UPDATE_READY = 0X502
    WAV_UPDATE = 0X503
    WAV_UPDATE_FINISH = 0X504
    WAV_TRIGGER = 0X505