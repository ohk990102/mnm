import socket
import ssl
import time
from sys import platform
from .wrapper import MnmWrapper

class SocketFragmentation(MnmWrapper):
    def __init__(self, timeout=0.1, interval=0.01, slice=1, linux_ack_check=True):
        super().__init__()
        self.timeout = timeout
        self.interval = interval
        self.slice = slice
        self.linux_ack_check = linux_ack_check

    def enable(self):
        if self.saved_state:
            return

        def flush_socket(sock: socket.socket) -> bool:
            
            if self.linux_ack_check and platform == 'linux' or platform == 'linux2':
                from ctypes import c_ulong
                from termios import TIOCOUTQ
                from fcntl import ioctl
                
                cu = time.time()

                while time.time() - cu < self.timeout and sock.fileno() != -1:
                    remaining = c_ulong.from_buffer_copy(
                        ioctl(sock.fileno(), TIOCOUTQ, bytearray(8), False)).value

                    if remaining == 0:
                        return True

                    time.sleep(self.interval)
            else:
                time.sleep(self.timeout)

            # not all data has been sent
            return False

        def _socket_send(s, data, flags=0):
            nbytes = 0
            for i in range(0, len(data), self.slice):
                nbytes += self.saved_state['socket.send'](s, data[i:i+self.slice], flags)
                flush_socket(s)
            return nbytes

        def _socket_sendall(s, data, flags=0):
            for i in range(0, len(data), self.slice):
                self.saved_state['socket.sendall'](s, data[i:i+self.slice], flags)
                flush_socket(s)
            return None

        def _sslsocket_send(s: ssl.SSLSocket, data, flags=0):
            nbytes = 0
            for i in range(0, len(data), self.slice):
                nbytes += self.saved_state['SSLSocket.send'](s, data[i:i+self.slice], flags)
                flush_socket(s)
            return nbytes

        def _sslsocket_sendall(s: ssl.SSLSocket, data, flags=0):
            for i in range(0, len(data), self.slice):
                self.saved_state['SSLSocket.sendall'](s, data[i:i+self.slice], flags)
                flush_socket(s)
            return None

        self.saved_state = {
            'socket.send': socket.socket.send,
            'socket.sendall': socket.socket.sendall,
            'SSLSocket.send': ssl.SSLSocket.send,
            'SSLSocket.sendall': ssl.SSLSocket.sendall
        }

        socket.socket.send = _socket_send
        socket.socket.sendall = _socket_sendall
        ssl.SSLSocket.send = _sslsocket_send
        ssl.SSLSocket.sendall = _sslsocket_sendall

    def disable(self):
        if self.saved_state:
            socket.socket.send = self.saved_state['socket.send']
            socket.socket.sendall = self.saved_state['socket.sendall']
            ssl.SSLSocket.send = self.saved_state['SSLSocket.send']
            ssl.SSLSocket.sendall = self.saved_state['SSLSocket.sendall']

        self.saved_state = None
