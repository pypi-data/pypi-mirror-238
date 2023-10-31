from cmath import log
from ipaddress import ip_address
from socket import *
from time import strftime
from loguru import logger

from qldev.device import MessageParser
from qldev.device.handler import MessageHandler, MessageType

class UDPSender(object):
    def __init__(self, ip = "255.255.255.255", port = 54366) :
        self._address = (ip, port)
        self._socket = None
        self.socket()
    
    def socket(self):
        if self._socket is None:
            self._socket = socket(AF_INET, SOCK_DGRAM)
            self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        
        return self._socket
        
    def send(self, message):
        try:
            self._socket.sendto(message, self._address)
        except Exception as e:
            logger.error("Exception on UDPSender send.")
            logger.error(e)
    
    def close(self):
        if self._socket :
            self._close()


class UDPProxy(object):
    def __init__(self, port=54366):
        self.__port = port
        self.__Listening = {}
        self.__socket = socket(AF_INET, SOCK_DGRAM)

    def close(self):
        if self.__socket:
            self.__socket.close()
            logger.info(f"关闭端口{self.__port}的连接")
        else:
            logger.warning(f"未监听端口{self.__port}的UDP消息")
    
    def accept(self, port: None, bufsize: int = 1024, handler:MessageHandler = None):
        if port is None:
            port = self.__port
        if port is None:
            logger.error(f"未设置UDP消息监听端口！")
            return
        if port in self.__Listening.keys():
            logger.warning(f"请不要重复监听端口{port}消息")

        self.__socket.bind(('', port)) 
        logger.debug(f"开始监听端口({port})的UDP消息")
        self.__Listening[port] = True

        while self.__Listening[port]:
            buffer = self.__socket.recvfrom(bufsize) 
            if buffer and handler:
                handler.accept(buffer[0], buffer[1], MessageType.UDP)
        
        self.__Listening[port] = False
        
    def broadcast(self, message, port = None):
        if port is None:
            port = self.__port
        address = ('255.255.255.255', port)
        self.__socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        try:
            self.__socket.sendto(message, address)
        except Exception as e:
            logger.error("发送UDP消息异常：")
            logger.error(e)

        
