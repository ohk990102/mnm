class MnmWrapper(object):
    def __init__(self):
        self.saved_state = None
    
    def enable(self):
        raise NotImplementedError
    
    def disable(self):
        raise NotImplementedError

    def __enter__(self):
        self.enable()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable()
