from gameState import GState
from gameStatePlaying import GameStatePlaying
from gameStateCredits import GameStateCredits
from gameStateInstructions import GameStateInstructions

import direct.directbase.DirectStart
from direct.gui.DirectGui import *

class GameStateMenu(GState):
    def start(self):
        self._menu_node = aspect2d.attachNewNode("menu-node")
        DirectButton(text = ("Play", "Play", "Play", "Play"),
            pos=(0, 0,  0.4), scale=.15, command=self._butPlay, parent=self._menu_node)
        DirectButton(text = ("Instructions", "Instructions", "Instructions", "Instructions"),
            pos=(0, 0,  0.15), scale=.15, command=self._butInstructions, parent=self._menu_node)
        DirectButton(text = ("Credits", "Credits", "Credits", "Credits"),
            pos=(0, 0, -0.15), scale=.15, command=self._butCredits, parent=self._menu_node)
        DirectButton(text = ("Exit", "Exit", "Exit", "Exit"),
            pos=(0, 0, -0.4), scale=.15, command=self._butExit, parent=self._menu_node)
            
    def stop(self):
        self._menu_node.removeNode()
        
    def _butPlay(self):
        print "but play"
        self._state_context.changeState(GameStatePlaying(self._state_context))
        
    def _butInstructions(self):
        print "but credits"
        self._state_context.changeState(GameStateInstructions(self._state_context))
        
    def _butCredits(self):
        print "but credits"
        self._state_context.changeState(GameStateCredits(self._state_context))
        
    def _butExit(self):
        print "but exit"
        self._state_context.exit()