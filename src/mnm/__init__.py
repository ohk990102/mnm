saved_socket = None

def enable_socket_fragmentation(timeout=0.1, interval=0):
    '''
    This is a hack to fragment each packet to 1 byte.
    This is useful for testing with a firewall like iptables.
    Should be used on linux only.

    :param timeout: timeout for each flush (default: 0.1)
    :param interval: interval between checking if the socket is flushed (default: 0)
    :return:
    '''
    global saved_socket
    if saved_socket:
        return
    import socket


    def flush_socket(sock: socket.socket) -> bool:
        from ctypes import c_ulong
        from time import sleep
        from termios import TIOCOUTQ
        from fcntl import ioctl
        import time
        
        cu = time.time()

        while time.time() - cu < timeout and sock.fileno() != -1: # if fd is -1, then it has been probably close()'d
            remaining = c_ulong.from_buffer_copy(
                ioctl(sock.fileno(), TIOCOUTQ, bytearray(8), False)).value

            if remaining == 0:
                # all data has been sent and ACKed
                return True

            # wait a bit before retrying,
            # sleep(0) was meant like yield current thread,
            # but will probably be close to busy-waiting,
            # feel free to change it to fit your needs
            sleep(interval)

        # not all data has been sent
        return False

    def send(self, data, flags=0):
        nbytes = 0
        for i in range(0, len(data), 1):
            nbytes += super(socket.socket, self).send(data[i:i+1], flags)
            flush_socket(self)
        return nbytes

    def sendall(self, data, flags=0):
        for i in range(0, len(data), 1):
            super(socket.socket, self).sendall(data[i:i+1], flags)
            flush_socket(self)
        return None

    saved_socket = {
        'send': socket.socket.send,
        'sendall': socket.socket.sendall
    }

    socket.socket.send = send
    socket.socket.sendall = sendall

def disable_socket_fragmentation():
    global saved_socket
    import socket
    if saved_socket:
        socket.socket.send = saved_socket['send']
        socket.socket.sendall = saved_socket['sendall']

    saved_socket = None

saved_requests = None

def enable_header_mocking():
    global saved_requests
    try:
        import requests.utils
        import requests.sessions
    except ImportError:
        raise Exception('requests module is not installed')

    def wrap_default_headers():
        import requests.structures
        return requests.structures.CaseInsensitiveDict({
            'Sec-Ch-Ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US;q=0.8,en;q=0.7',
        })

    saved_requests = {
        'utils.default_headers': requests.utils.default_headers,
        'sessions.default_headers': requests.sessions.default_headers
    }
    requests.utils.default_headers = wrap_default_headers
    requests.sessions.default_headers = wrap_default_headers

def disable_header_mocking():
    global saved_requests
    try:
        import requests.utils
        import requests.sessions
    except ImportError:
        raise Exception('requests module is not installed')
    
    if saved_requests:
        requests.utils.default_headers = saved_requests['utils.default_headers']
        requests.sessions.default_headers = saved_requests['sessions.default_headers']

    saved_requests = None
