from gameState import GState
import gameStateMenu

import direct.directbase.DirectStart
from direct.gui.DirectGui import *
from panda3d.core import TextNode

class GameStateCredits(GState):
    def start(self):
        self._credits_node = aspect2d.attachNewNode("credits-node")
        text = TextNode('node name')
        text.setText("Videogame made by\n   David Ramirez Reina")
        textNodePath = self._credits_node.attachNewNode(text)
        textNodePath.setScale(0.07)
        
        DirectButton(text = ("Back", "Back", "Back", "Back"),
            pos=(0, 0, -0.8), scale=.15, command=self._butExit, parent=self._credits_node)
        
    def stop(self):
        self._credits_node.removeNode()
        
    def _butPlay(self):
        print "but play"
        self._state_context.changeState(gameStateMenu.GameStateMenu(self._state_context))
        
    def _butExit(self):
        print "but exit"
        self._state_context.exit()