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


from panda3d.ode import OdeWorld, OdeSimpleSpace, OdeJointGroup
from panda3d.ode import OdeBody, OdeMass, OdeBoxGeom, OdePlaneGeom

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
        base.accept( "escape" , sys.exit)

        props = WindowProperties()
        #props.setCursorHidden(True)
        base.disableMouse()
        props.setMouseMode(WindowProperties.MRelative)
        base.win.requestProperties(props)
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        
        self._map_models = None
        self._cajas = None
        
        self._num_lvl = 1
        self._num_lvls = 1
        
        self.initODE()
        self.loadBkg()
        self.loadLevel()
        self.setAI()
        
        self._last_t = None
        self._last_t_space = 0
        
        self._player = Player(self.world, self.space)
        
    def initODE(self):
        # Setup our physics world
        self.world = OdeWorld()
        self.world.setGravity(0, 0, -9.81)
        
        # The surface table is needed for autoCollide
        self.world.initSurfaceTable(1)
        self.world.setSurfaceEntry(0, 0, 150, 0.0, 9.1, 0.9, 0.00001, 0.0, 0.002)
        
        # Create a space and add a contactgroup to it to add the contact joints
        self.space = OdeSimpleSpace()
        self.space.setAutoCollideWorld(self.world)
        self.contactgroup = OdeJointGroup()
        self.space.setAutoCollideJointGroup(self.contactgroup)
 
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
    
        self.environ1 = loader.loadModel("../data/models/groundPlane")      
        self.environ1.reparentTo(render)
        self.environ1.setPos(0,0,0)
        self.environ1.setScale(1)
        
        groundGeom = OdePlaneGeom(self.space, Vec4(0, 0, 1, 0))
        #groundGeom.setCollideBits(BitMask32(0x00000001))
        #groundGeom.setCategoryBits(BitMask32(0x00000002))
    def loadLevel(self):
        if (self._map_models != None):
            for m in self._map_models:
                m.remove()
        if (self._cajas != None):
            for c in self._cajas:
                c.model.remove()
        self._tp = TiledParser("map1")
        self._map_models = self._tp.load_models()
        self._cajas = self._tp.load_cajas()
      
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
        
        ##################
        
        self.space.autoCollide() # Setup the contact joints
        # Step the simulation and set the new positions
        if (task.frame > 1):
            self.world.quickStep(globalClock.getDt())
        #for np, body in boxes:
        #    np.setPosQuat(render, body.getPosition(), Quat(body.getQuaternion()))
        ##self._player.updatePos()
        self.contactgroup.empty() # Clear the contact joints
  
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

