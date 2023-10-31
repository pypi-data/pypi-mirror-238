import socket
from loguru import logger

from qldev.device import MessageHandler, MessageType

class TCPServer(object):
    def __init__(self, port, callback=None) :
        self.__port = port
        self._callback = callback
        self._run = False
        self._socket = None
        self.clients = {}
        self._start()

    def is_run(self):
        return self._run
    
    def exists(self, devno):
        return not self.get_client(devno)
    
    def accept(self, handler : MessageHandler = None):

        while self._run:
            # 等待新的客户端连接
            client_socket, client_address= self._socket.accept()
            logger.info(f"收到新的设备连接: {client_address}")
            if handler:
                handler.accept(client_socket, client_address, MessageType.SOCKET)

    def client_handler(self, socket, addr):
        logger.info(f"new client socket {addr[0]}:{addr[1]} connected.")


    def _start(self):
        if self.is_run():
            return

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 本地信息
        address = ('', self.__port)
        # 绑定
        self._socket.bind(address)

        self._socket.listen(128)
        logger.info(f'开始监听端口{self.__port}的TCP消息')

        self._run = True
    
    def get_client(self, devno = None):   
        if len(self.clients) == 0:
            logger.warning("TCP server has no client connection.")
            return None

        if devno:
            return self.clients[devno]
        else:
            # 默认返回一个设备
            key = random.sample(self.clients.keys(), 1)[0]
            return self.clients[key]

        
def client_listen(socket, callback):
    while True:
        try:
            # 接收对方发送过来的数据
            recv_data = socket.recv(1024)  # 接收1024个字节
            if recv_data:
                msg = recv_data.decode('utf-8')
                logger.debug(f'receive -> {msg}')
                callback     
        except Exception as e:
            logger.error("Exception on client_listen")
            logger.error(e)
            break

class ServerContainer(object):
    def __init__(self) :
        self.servers = {}
        
    def add_listen(self, port):
        if self.exists(port):
            logger.warning(f"server[{port}] exists already.")
            return
        tcp_server = TCPServer(port)
        self.servers[port] = tcp_server

        return tcp_server

        
    def exists(self, port):
        if self.servers[port]:
            return True
        return False

