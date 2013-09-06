from gameState import GState

#for directx window and functions
import direct.directbase.DirectStart
#for most bus3d stuff
from pandac.PandaModules import *
#for directx object support
from direct.showbase.DirectObject import DirectObject
#for intervals
from direct.interval.IntervalGlobal import *
#for FSM
from direct.fsm import FSM
from direct.fsm import State
#for tasks
from direct.task import Task
#for Actors
from direct.actor.Actor import Actor
#for math
import math
#for system commands
import random, sys, os, math
#for directGUI
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText

#for Pandai
from panda3d.ai import *


from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText

from TiledParser import TiledParser
from player import Player


# Figure out what directory this program is in.
MYDIR=os.path.abspath(sys.path[0])
MYDIR=Filename.fromOsSpecific(MYDIR).getFullpath()

#import os
#os.chdir("../")

class GameStatePlaying(GState):
    VIDAS = 3
    LEVEL_TIME = 10#0
    
    def start(self):
        self.keyMap = {"left":0, "right":0, "up":0, "down":0}
        
        base.accept( "escape" , sys.exit)

        props = WindowProperties()
        props.setCursorHidden(True)
        base.disableMouse()
        props.setMouseMode(WindowProperties.MRelative)
        base.win.requestProperties(props)
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        
        self._modulos = None
        self._paneles = None
        
        self._num_lvl = 1
        self._num_lvls = 2
        
        self.loadLevel()
        self.loadGUI()
        self.loadBkg()
        
        self._last_t = None
        self._last_t_space = 0
        
    def stop(self):
        pass
        
    def loadLevel(self):
        self._level_time = self.LEVEL_TIME
        self.initBullet()
        self._player = Player(self.world)
        self.loadMap()
        self.setAI()
        
    def initBullet(self):
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        
        groundShape = BulletPlaneShape(Vec3(0, 0, 1), 0)
        groundNode = BulletRigidBodyNode('Ground')
        groundNode.addShape(groundShape)
        self.world.attachRigidBody(groundNode)
 
    def loadBkg(self):
        self.environ1 = loader.loadModel("../data/models/skydome")      
        self.environ1.reparentTo(render)
        self.environ1.setPos(0,0,0)
        self.environ1.setScale(1)
        
        self.environ2 = loader.loadModel("../data/models/skydome")      
        self.environ2.reparentTo(render)
        self.environ2.setP(180)
        self.environ2.setH(270)
        self.environ2.setScale(1)
        
        self.dirnlight1 = DirectionalLight("dirn_light1")
        self.dirnlight1.setColor(Vec4(1.0,1.0,1.0,1.0))
        self.dirnlightnode1 = render.attachNewNode(self.dirnlight1)
        self.dirnlightnode1.setHpr(0,317,0)
        render.setLight(self.dirnlightnode1)
        
        self.alight = AmbientLight('alight')
        self.alight.setColor(VBase4(0.05, 0.05, 0.05, 1))
        self.alight_node = render.attachNewNode(self.alight)
        render.setLight(self.alight_node)
    
        self.environ1 = loader.loadModel("../data/models/groundPlane")      
        self.environ1.reparentTo(render)
        self.environ1.setPos(0,0,0)
        self.environ1.setScale(1)
        
        
    def loadGUI(self):
        self.vidas_imgs = list()
        w = 0.24
        for i in range(self.VIDAS):
            image_warning = OnscreenImage(image = '../data/Texture/signal_warning.png', pos=(-1 + i*w, 0, 0.85))
            image_warning.setScale(0.1)
            image_warning.setTransparency(TransparencyAttrib.MAlpha)
            image_warning.hide()
            
            image_ok = OnscreenImage(image = '../data/Texture/signal_ok.png', pos=(-1 + i*w, 0, 0.85))
            image_ok.setScale(0.1)
            image_ok.setTransparency(TransparencyAttrib.MAlpha)
            image_ok.show()
            self.vidas_imgs.append((image_ok, image_warning))
            
        self._level_time_O = OnscreenText(text = '', pos = (0, 0.85), scale = 0.14, fg=(1.0, 1.0, 1.0, 1.0), bg=(0.0, 0.0, 0.0, 1.0))
        
        
    def loadMap(self):
        if (self._modulos is not None):
            for m in self._modulos:
                m.remove()
        if (self._paneles is not None):
            for p in self._paneles:
                p.remove()
                
        self._tp = TiledParser("map"+str(self._num_lvl))
        self._cajas = self._tp.load_cajas()
        self._modulos, self._paneles = self._tp.load_models(self.world)
      
    def setAI(self):
        taskMgr.add(self.update, 'Update')
            
    def update(self, task):
        if (task.frame > 1):
            self.world.doPhysics(globalClock.getDt())
            self._level_time -= globalClock.getDt()
            self._level_time_O.setText(str(int(self._level_time)))
        
        for panel in self._paneles:
            contact = self.world.contactTestPair(self._player.getRBNode(), panel.getRBNode())
            if contact.getNumContacts() > 0:
                panel.manipulate()
                
        brokens = 0
        for panel in self._paneles:
            if panel.isBroken():
                brokens += 1
        #print brokens
        
        for i, vida_imgs in enumerate(self.vidas_imgs):
            if i < len(self.vidas_imgs) - brokens:
                vida_imgs[0].show()
                vida_imgs[1].hide()
            else:
                vida_imgs[0].hide()
                vida_imgs[1].show()
            
        if brokens > self.VIDAS:
            self.gameOver()
            return task.done
            
        if self._level_time <= 0:
            self._num_lvl += 1
            if self._num_lvl <= self._num_lvls:
                self.nextLevel()
            else:
                self.theEnd()
            return task.done
        return task.cont

    def gameOver(self):
        taskMgr.remove('player-task')
        taskMgr.remove('panel-task')
        self._mission_text_O = OnscreenText(text = 'Game Over', pos = (0, 0), scale = 0.5, fg=(1.0, 1.0, 1.0, 1.0), bg=(0.0, 0.0, 0.0, 1.0))
        taskMgr.add(self.gameOverTransition, 'game-over-transition')
        #self.loadLevel()
        print "Game Over"
        
    def gameOverTransition(self, task):
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        if task.time > 3.0:
            self._mission_text_O.hide()
            props = WindowProperties()
            props.setCursorHidden(False)
            base.win.requestProperties(props)
            print "MENU"
            return task.done

        return task.cont
        
    def nextLevel(self):
        taskMgr.remove('player-task')
        taskMgr.remove('panel-task')
        self._mission_text_O = OnscreenText(text = 'Mission\nComplete', pos = (0, 0), scale = 0.5, fg=(1.0, 1.0, 1.0, 1.0), bg=(0.0, 0.0, 0.0, 1.0))
        taskMgr.add(self.nextLevelTransition, 'next-Level-transition')
        print "Mission Complete"
        
    def nextLevelTransition(self, task):
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        if task.time > 3.0:
            print "Next Level"
            self._mission_text_O.hide()
            self.loadLevel()
            return task.done

        return task.cont
        
    def theEnd(self):
        taskMgr.remove('player-task')
        taskMgr.remove('panel-task')
        self._mission_text_O = OnscreenText(text = '.       The End       .', pos = (0, 0), scale = 0.5, fg=(1.0, 1.0, 1.0, 1.0), bg=(0.0, 0.0, 0.0, 1.0))
        taskMgr.add(self.theEndTransition, 'theEnd-transition')
        #self.loadLevel()
        print "Mission Complete"
        
    def theEndTransition(self, task):
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        if task.time > 3.0:
            self._mission_text_O.hide()
            props = WindowProperties()
            props.setCursorHidden(False)
            base.win.requestProperties(props)
            print "The End"
            return task.done

        return task.cont
