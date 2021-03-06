from panda3d.core import *

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape, BulletSphereShape

from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import ZUp

class Player(object):

    #global playerNode
    #playerNode = NodePath('player')
    F_MOVE = 400.0
    
    def __init__(self, btWorld):
        self._attachControls()
        self._initPhysics(btWorld)
        self._loadModel()
        taskMgr.add(self.mouseUpdate, 'player-task')
        taskMgr.add(self.moveUpdate, 'player-task')
        
        self._vforce = Vec3(0,0,0)
        
        #ItemHandling(self.playerNode)

    def _attachControls(self):
        #base.accept( "s" , self.__setattr__,["walk",self.STOP] )
        base.accept("w", self.goForward)
        base.accept("w-up", self.nogoForward)
        base.accept("s", self.goBack)
        base.accept("s-up", self.nogoBack)
        base.accept("a", self.goLeft)
        base.accept("a-up", self.nogoLeft)
        base.accept("d", self.goRight)
        base.accept("d-up", self.nogoRight)
        base.accept("space", self.goUp)
        base.accept("space-up", self.nogoUp)
        
    def _loadModel(self):
        #self._model = loader.loadModel("../data/models/d1_sphere.egg")      
        #self._model.reparentTo(self.playerNode)
        
        pl = base.cam.node().getLens()
        pl.setNear(0.2)
        base.cam.node().setLens(pl)

    def _initPhysics(self, world):
        rad = 1
        shape = BulletSphereShape(rad)
        self._rb_node = BulletRigidBodyNode('Box')
        self._rb_node.setMass(80.0)
        self._rb_node.setFriction(1.8)
        self._rb_node.addShape(shape)
        self._rb_node.setAngularFactor(Vec3(0,0,0))
        self._rb_node.setDeactivationEnabled(False, True)
        self.playerNode = render.attachNewNode(self._rb_node)
        self.playerNode.setPos(0, 0, 4)
        self.playerNode.setHpr(0,0,0)
        world.attachRigidBody(self._rb_node)
        self.camNode = self.playerNode.attachNewNode("cam node")
        base.camera.reparentTo(self.camNode)
        self.camNode.setPos(self.camNode, 0, 0, 1.75-rad)
        
        #self.camNode.setPos(self.camNode, 0, -5,0.5)
        #self.camNode.lookAt(Point3(0,0,0),Vec3(0,1,0))
  
    def mouseUpdate(self,task):
        md = base.win.getPointer(0)
        dx = md.getX() - base.win.getXSize()/2.0
        dy = md.getY() - base.win.getYSize()/2.0
        
        yaw = dx/(base.win.getXSize()/2.0) * 90
        self.camNode.setHpr(self.camNode, -yaw, 0, 0)
        #base.camera.setHpr(base.camera, yaw, pith, roll)
        
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        return task.cont
        
    def moveUpdate(self,task):
        if (self._vforce.length() > 0):
            #self.rbNode.applyCentralForce(self._vforce)
            self._rb_node.applyCentralForce(self.playerNode.getRelativeVector(self.camNode, self._vforce))
        else:
            pass
        
        return task.cont
        
    def goForward(self):
        self._vforce.setY( self.F_MOVE)
    def nogoForward(self):
        self._vforce.setY( 0)
    def goBack(self):
        self._vforce.setY(-self.F_MOVE)
    def nogoBack(self):
        self._vforce.setY( 0)
    def goLeft(self):
        self._vforce.setX(-self.F_MOVE)
    def nogoLeft(self):
        self._vforce.setX( 0)
    def goRight(self):
        self._vforce.setX( self.F_MOVE)
    def nogoRight(self):
        self._vforce.setX( 0)
    def goUp(self):
        self._vforce.setZ( self.F_MOVE*1.4)
    def nogoUp(self):
        self._vforce.setZ( 0)

    def getRBNode(self):
        return self._rb_node
        

"""
class ItemHandling(object):
    def __init__(self, playerNode):
        taskMgr.add(self.setItemPosition, 'ItemPosition')

    def setItemPosition(self, task):
        return task.cont
"""