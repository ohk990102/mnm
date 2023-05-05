import socket
from .wrapper import MnmWrapper

class SocketFragmentation(MnmWrapper):
    def __init__(self, timeout=0.1, interval=0.01, slice=1):
        super().__init__()
        self.timeout = timeout
        self.interval = interval
        self.slice = slice

    def enable(self):
        if self.saved_state:
            return

        def flush_socket(sock: socket.socket) -> bool:
            from sys import platform
            import time
            if platform == 'linux' or platform == 'linux2':
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

        def send(s, data, flags=0):
            nbytes = 0
            for i in range(0, len(data), self.slice):
                nbytes += super(socket.socket, s).send(data[i:i+self.slice], flags)
                flush_socket(s)
            return nbytes

        def sendall(s, data, flags=0):
            for i in range(0, len(data), self.slice):
                super(socket.socket, s).sendall(data[i:i+self.slice], flags)
                flush_socket(s)
            return None

        self.saved_state = {
            'send': socket.socket.send,
            'sendall': socket.socket.sendall
        }

        socket.socket.send = send
        socket.socket.sendall = sendall

    def disable(self):
        import socket
        if self.saved_state:
            socket.socket.send = self.saved_state['send']
            socket.socket.sendall = self.saved_state['sendall']

        self.saved_state = None
