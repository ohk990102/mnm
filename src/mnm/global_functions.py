from .socket_fragmentation import SocketFragmentation
from .header_mocking import HeaderMocking

from ._internal_utils import deprecated

_global_socket_fragmentation = SocketFragmentation()
_global_header_mocking = HeaderMocking()

@deprecated
def enable_socket_fragmentation():
    global _global_socket_fragmentation
    _global_socket_fragmentation.enable()

@deprecated
def disable_socket_fragmentation():
    global _global_socket_fragmentation
    _global_socket_fragmentation.disable()

@deprecated
def enable_header_mocking():
    global _global_header_mocking
    _global_header_mocking.enable()
    
@deprecated
def disable_header_mocking():
    global _global_header_mocking
    _global_header_mocking.disable()