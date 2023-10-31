from time import sleep
from qldev.network import UDPProxy, TCPServer
from .client import *
from .handler import *
from .model import *

# 盒子服务端
class BoxServer(object): 
    def __init__(self, auto_search = False) -> None:
        self.__auto_search = auto_search
        self.__handler = BoxMessageHandler()
        self.__udp_port = 54366
        self.__tcp_port = 19128
        self.__udp_proxy = None
        self.__tcp_server = None
        self.__searching = False

    @property
    def clients(self):
        if self.__handler:
            return self.__handler.clients

        return None

    @property
    def broadcast_list(self):
        if self.__handler and self.__handler.broadcast_list:
            return self.__handler.broadcast_list.difference(self.__handler.connected_list)

        return None

    @property
    def connected_list(self):
        if self.__handler:
            return self.__handler.connected_list

        return None

    def start(self, udp_port = None, tcp_port = None):
        if udp_port:
            self.__udp_port = udp_port
        if tcp_port:
            self.__tcp_port = tcp_port
        
        self.__udp_listen()
        self.__tcp_listen()
        self.start_search()

        return self

    def __udp_listen(self):
        if self.__udp_proxy is None:
            self.__udp_proxy = UDPProxy(self.__udp_port)

        if self.__auto_search:
            self.__client_detect()

    # UDP消息监听-设备探测
    # 子线程
    def __client_detect(self):
        detect_thread = Thread(target=self.__udp_proxy.accept, args=(self.__udp_port, 512, self.__handler))
        detect_thread.setDaemon(True)
        detect_thread.start()

    def __tcp_listen(self):
        if self.__tcp_server is None:
            self.__tcp_server = TCPServer(self.__tcp_port)
        
        self.__client_accept()

    # 客户端连接请求
    # 子线程
    def __client_accept(self):
        accept_thread = Thread(target=self.__tcp_server.accept, args = (self.__handler,))
        accept_thread.setDaemon(True)
        accept_thread.start()

    # UDP消息发送-设备连接通知
    # 子线程
    def start_search(self, repeat = True):
        if self.__searching:
            logger.warning("重复的指令，搜寻设备任务已启动!")
            return
        self.__searching = True
        accept_thread = Thread(target=self.__search_all, args=(repeat,))
        accept_thread.setDaemon(True)
        accept_thread.start()

    def __search_all(self, repeat):
        while repeat and self.__searching:     
            if self.broadcast_list is None or len(self.broadcast_list) == 0:
                continue

            for idx, item in enumerate(self.broadcast_list):
                logger.debug(f"搜寻设备：{item}")
                try:
                    message = UDPMessage.get_message(item, tcp_port = self.__tcp_port)            
                    self.__udp_proxy.broadcast(message=message)
                except Exception as e:
                    logger.error(f"搜寻设备消息发送异常: {e}")
            # 广播间歇
            sleep(2)
        
    def add_search(self, devno):
        if devno:
            self.__handler.add_search(devno)

    # 获取可用的客户端（设备）
    def get_client(self, mac = None) -> BoxClient:
        if mac and mac in self.clients.keys():
            return self.clients[mac]
        elif len(self.clients) > 0:
            return list(self.clients.values())[0]
        else:
            return None

    def subscribe(self, callback, key = 'default', mac = None):
        client = self.get_client(mac)
        if client:
            consumer = BoxMessageQueue()
            client.subscribe(consumer = consumer, key = key)
            t = Thread(target=self.__consumer, args=(consumer, callback))
            t.setDaemon(True)
            t.start()
        else:
            raise Exception('没有可用的设备')

    def __consumer(self, consumer:BoxMessageQueue, callback):
        while True:
            if consumer.empty():
                sleep(0.1) ## sleep 100ms 
            else:
                callback(consumer.get())