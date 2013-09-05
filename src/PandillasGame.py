# Author: Ryan Myers
# Models: Jeff Styers, Reagan Heller

#from panda3d.core import loadPrcFileData
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")

# Last Updated: 6/13/2005
#
# This tutorial provides an example of creating a character
# and having it walk around on uneven terrain, as well
# as implementing a fully rotatable camera.

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

#import os
#os.chdir("../")

from TiledParser import TiledParser
from caja import Caja
from player import Player

#************************GLOBAL**********************************************
speed = 0.75

# Figure out what directory this program is in.
MYDIR=os.path.abspath(sys.path[0])
MYDIR=Filename.fromOsSpecific(MYDIR).getFullpath()

font = loader.loadFont("cmss12")

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1), font = font,
                        pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1,1,1,1), font = font,
                        pos=(1.3,-0.95), align=TextNode.ARight, scale = .07)

class World(DirectObject):

    def __init__(self):
        self.keyMap = {"left":0, "right":0, "up":0, "down":0}
        
        self.title = addTitle("Awesome Panda3D Game!")
        #self.inst1 = addInstructions(0.95, "[ESC]: Quit")
        #self.inst2 = addInstructions(0.90, "[Enter]: Start Pathfinding")
        
        #base.disableMouse()
        #base.useDrive()
        #base.useTrackball()
        #base.oobe()
        #base.cam.setPosHpr(0,-210,135,0,327,0)
        #base.cam.setPos(-5, 3, 16)
        #base.cam.lookAt(0,0,0)
        base.accept( "escape" , sys.exit)

        props = WindowProperties()
        #props.setCursorHidden(True)
        base.disableMouse()
        props.setMouseMode(WindowProperties.MRelative)
        base.win.requestProperties(props)
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        
        self._map_models = None
        self._cajas = None
        self._modulos = None
        self._paneles = None
        
        self._num_lvl = 1
        self._num_lvls = 1
        
        self.initBullet()
        self.loadBkg()
        self.loadLevel()
        self.setAI()
        
        self._last_t = None
        self._last_t_space = 0
        
        self._player = Player(self.world)
        
    def initBullet(self):
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
 
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
        
        groundShape = BulletPlaneShape(Vec3(0, 0, 1), 0)
        groundNode = BulletRigidBodyNode('Ground')
        groundNode.addShape(groundShape)
        self.world.attachRigidBody(groundNode)
        
    def loadLevel(self):
        if (self._map_models != None):
            for m in self._map_models:
                m.remove()
        if (self._cajas != None):
            for c in self._cajas:
                c.model.remove()
        if (self._modulos is not None):
            for m in self._modulos:
                m.remove()
        if (self._paneles is not None):
            for p in self._paneles:
                p.remove()
                
        self._tp = TiledParser("map1")
        #self._map_models = self._tp.load_models()
        self._cajas = self._tp.load_cajas()
        self._modulos, self._paneles = self._tp.load_models(self.world)
      
    def setAI(self):
        self._LogicTickTime = 1####
        self.accept("space", self.actionSpace)
        
        #taskMgr.doMethodLater(self._LogicTickTime, self.updateCajasPos, 'Update Cajas Pos')
        taskMgr.add(self.updateCajasSoftPos, 'Update Cajas Soft Pos')

    def updateCajasPos(self):
        for caja in self._cajas:
            caja.i += caja.di
            caja.j += caja.dj
            caja.model.setPos(caja.j*8,-caja.i*8, 0)
            time = globalClock.getFrameTime()
            #print "Space", time, self._last_t_space
            dir = self._tp.get_dir(caja.i, caja.j, time - self._last_t_space < 0.3)
            if (dir != None):
                caja.di = dir[0]
                caja.dj = dir[1]
            elif (self._tp.entregada(caja.i, caja.j)):
                caja.entregada = True
                caja.di = 0
                caja.dj = 0
            elif (self._tp.perdida(caja.i, caja.j)):
                caja.perdida = True
                caja.di = 0
                caja.dj = 0
        
        todas_entregadas = True
        for c in self._cajas:
            if not c.entregada:
                todas_entregadas = False
                break
        if todas_entregadas: self.nextLevel()
        
        for c in self._cajas:
            if c.perdida: self.gameOver()
            
    def updateCajasSoftPos(self, task):
        """
        if (self._last_t == None):
            self._last_t = task.time
        if (math.floor(task.time) != math.floor(self._last_t)):
            self.updateCajasPos()
        else:
            f = math.modf(task.time)[0]
            if (f != 0):
                for caja in self._cajas:
                    caja.model.setPos(caja.j*8 + caja.dj*f*8,-caja.i*8 - caja.di*f*8, 0)
        self._last_t = task.time
        """ 
        ##################
        
        # Step the simulation and set the new positions
        if (task.frame > 1):
            self.world.doPhysics(globalClock.getDt())
        
        for panel in self._paneles:
            contact = self.world.contactTestPair(self._player.getRBNode(), panel.getRBNode())
            if contact.getNumContacts() > 0:
                panel.manipulate()
                
        brokens = 0
        for panel in self._paneles:
            if panel.isBroken():
                brokens += 1
        print brokens
  
        return task.cont
        
    def actionSpace(self):
        new_t = globalClock.getFrameTime()
        if (new_t - self._last_t_space > 0.3):
            self._last_t_space = new_t
        #print self._last_t_space

    def gameOver(self):
        self.loadLevel()
        print "Game Over"
        
    def nextLevel(self):
        self.loadLevel()
        print "Next Level"
        
w = World()
run()

