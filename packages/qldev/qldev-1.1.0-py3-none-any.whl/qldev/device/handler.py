import enum

class MessageType(enum.Enum):
    UDP = 'udp'
    TCP = 'tcp'
    SOCKET = 'socket'

class MessageParser(object):
    def __init__(self) -> None:
        pass

class MessageHandler(object):
    def __init__(self) -> None:
        print('MessageHandler __init__')

    def accept(self, message, address, type : MessageType = None):
        pass

    def add_client(self, client):
        pass

    def remove_client(self, client):
        pass

    