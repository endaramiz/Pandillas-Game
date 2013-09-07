from gameStateMenu import GameStateMenu

import sys

class StateManager(object):
    def __init__(self):
        self._state = None
        self.changeState(GameStateMenu(self))
        run()
        
    def changeState(self, state):
        if self._state is not None:
            self._state.stop()
        self._state = state
        self._state.start()
        
    def exit(self):
        print "EXIT"
        self._state.stop()
        sys.exit()
               
e = StateManager()
run()
