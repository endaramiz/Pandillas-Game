
class GState(object):
    def __init__(self, state_context):
        self._state_context = state_context
    def start(self):
        raise NotImplementedError
    def stop(self):
        raise NotImplementedError
        
