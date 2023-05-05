from .socket_fragmentation import SocketFragmentation
from .header_mocking import HeaderMocking
from .wrapper import MnmWrapper
from typing import Tuple

def mixed(*mnms: MnmWrapper):
    if len(mnms) == 0:
        mnms: Tuple[MnmWrapper] = (SocketFragmentation(), HeaderMocking())
    def _decorator(func):
        def _wrapper(*args, **kwargs):
            for mnm in mnms:
                mnm.enable()
            try:
                result = func(*args, **kwargs)
            finally:
                for mnm in reversed(mnms):
                    mnm.disable()
            return result
        return _wrapper
    return _decorator