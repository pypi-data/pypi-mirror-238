
import socket
import struct



class Bruce_socket_util():
    def is_port_ok(self):
        """
        查看端口是否有人占用
        """
        pass

    def is_ip_ok(self):
        """
        查看ip是否能ping通
        """
        pass

class Bruce_socket_client(Bruce_socket_util):
    def __init__(self, ip: str = "127.0.0.1", port: int = 8089):
        self.ip = ip
        self.port = port
        self.init_client()
        self._client=None
    def init_client(self):
        """
        初始化客户端
        """
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.on_content()
    def on_content(self):
        """
        客户端连接服务端
        """
        ip_port = (self.ip, self.port)
        res = self._client.connect_ex(ip_port)

    def send_msg(self,msg:str):
        """
        客户端发送消息
        """
        self._client.send(msg.encode('utf-8'))
    def wait_msg(self):
        """
        客户端等待服务端返回的消息
        """
        message = self._client.recv(1024).decode('utf-8')
        return message

    def close(self):
        """
        关闭客户端
        """
        self._client.close()










class Bruce_socket_server(Bruce_socket_util):
    def __init__(self, ip: str = "127.0.0.1", port: int = 8089,max_content:int=5):
        self.ip = ip
        self.port = port
        self.max_content=max_content
        self.init_server()
        self._server=None
    def init_server(self):
        """
        初始化服务端
        """
        ip_port = (self.ip, self.port)
        self._server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind(ip_port)
        self._server.listen( self.max_content)# 最大连接数默认为5


    def close(self):
        """
        关闭服务端
        """
        pass





"""
解决粘包的方法：
问题的根源在于，接收端不知道发送端将要传送的字节流的长度，所以解决粘包的方法就是围绕如何让发送端在发送数据前，把自己将要发送的字节流总大小让接收端知晓，然后接收端用一个死循环接收完所有数据；
"""


class Bruce_socket_error_server():

    """
    发生粘包的两种情况
    """
    def __init__(self,ip:str="127.0.0.1",port:int=8089):
        self.ip=ip
        self.port = port

    def error_one_socket_server(self):
        """
        1.发送端需要等缓冲区满才发送出去，造成粘包（发送数据时间间隔很短，数据了很小，会合到一起，产生粘包
        """
        ip_port = (self.ip, self.port)
        tcp_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket_server.bind(ip_port)
        tcp_socket_server.listen(5)
        conn, addr = tcp_socket_server.accept()
        data1 = conn.recv(10)
        data2 = conn.recv(10)
        print('----->', data1.decode('utf-8'))
        print('----->', data2.decode('utf-8'))
        conn.close()

    def error_two_socket_server(self):
        """
        2.接收方不及时接收缓冲区的包，造成多个包接收（客户端发送了一段数据，服务端只收了一小部分，服务端下次再收的时候还是从缓冲区拿上次遗留的数据，产生粘包）
        """
        self.error_one_socket_server()


class Bruce_socket_error_client():
    """
    发生粘包的两种情况
    """
    def __init__(self,ip:str="127.0.0.1",port:int=8089):
        self.ip=ip
        self.port=port

    def error_one_socket_client(self):
        """
        1.发送端需要等缓冲区满才发送出去，造成粘包（发送数据时间间隔很短，数据了很小，会合到一起，产生粘包
        """
        BUFSIZE = 1024
        ip_port = (self.ip, self.port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        res = s.connect_ex(ip_port)
        s.send('hello'.encode('utf-8'))
        s.send('feng'.encode('utf-8'))


    def error_two_socket_client(self):
        """
        2.接收方不及时接收缓冲区的包，造成多个包接收（客户端发送了一段数据，服务端只收了一小部分，服务端下次再收的时候还是从缓冲区拿上次遗留的数据，产生粘包）
        """
        BUFSIZE = 1024
        ip_port = (self.ip, self.port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        res = s.connect_ex(ip_port)
        s.send('hello1111111111111111111111111'.encode('utf-8'))
        s.send('feng'.encode('utf-8'))
        self.error_one_socket_client()


