from loguru import logger
from qldev.box.client import BoxClient
from qldev.box.message import UDPMessage

from qldev.device import MessageHandler, MessageType

class BoxMessageHandler(MessageHandler):
    def __init__(self) -> None:
        super().__init__()
        self.clients = {}
        self.__broadcast_list = set([])
        self.__connected_list = set([])
        self.__temp = {}

    @property
    def broadcast_list(self):
        return self.__broadcast_list

    @property
    def connected_list(self):
        return self.__connected_list

    def accept(self, message, address, type : MessageType = MessageType.TCP):
        logger.trace(f"new {type.value} message received.")
        if type == MessageType.UDP:
            devinfo = UDPMessage.parse(message)
            logger.trace(devinfo)
            if devinfo and UDPMessage.MAC in devinfo.keys():
                self.add_search(devinfo[UDPMessage.MAC])

            return

        if type == MessageType.SOCKET:
            self.__add_socket(message, address)
            return

        if type == MessageType.TCP:
            return

    def __add_socket(self, socket, address):
        logger.trace(socket)
        logger.trace(address)
        key = f'{address[0]}_{address[1]}'
        client = BoxClient(socket, address, self)
        self.__temp[key] = client
        # 启动消息处理，并发送消息问询设备信息
        client.listen().ask()

    def add_client(self, client):
        
        logger.info(f"添加设备到客户端列表（{client.mac} - {client.address}）")

        if client.mac:
            self.clients[client.mac] = client
            self.connected_list.add(client.mac)
            logger.info(f"添加完成，客户端列表当前设备数量：{len(self.clients)}")


    def remove_client(self, client):
        logger.info(f"从客户端列表中移除设备（{client.mac} - {client.address}）")
        if client.mac and client.mac in self.clients.keys():
            self.clients.pop(client.mac)
            self.connected_list.remove(client.mac)
            logger.info(f"移除完成，客户端列表当前设备数量：{len(self.clients)}")
        if client.key and client.key in self.clients.keys():
            self.__temp.pop(client.key)

        # 删除对象
        del client
        

    def add_search(self, devno):
        if devno and not (devno in self.__broadcast_list):
            self.__broadcast_list.add(devno)
            logger.info(f"发现新设备（{devno}）并加入搜寻列表")