from panda3d.core import *

from panda3d.ode import *

class Player(object):

    global playerNode
    playerNode = NodePath('player')
    F_MOVE = 1000.0
    
    def __init__(self, ode_world, ode_space):
        self._loadModel()
        self._initCamera()
        self._attachControls()
        self._initPhysics(ode_world, ode_space)
        taskMgr.add(self.mouseUpdate, 'mouse-task')
        taskMgr.add(self.moveUpdate, 'move-task')
        
        self._vforce = Vec3(0,0,0)
        
        ItemHandling(playerNode)
        
    def _loadModel(self):
        playerNode.reparentTo(render)
        playerNode.setPos(0,0,14)
        #playerNode.setScale(.05)
   
    def _initCamera(self):
        pl = base.cam.node().getLens()
        pl.setFov(70)
        base.cam.node().setLens(pl)
        base.camera.reparentTo(playerNode)

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
       # Create the body and set the mass
  
    def _initPhysics(self, world, space):
        radius = 0.25
        length = 2
        self._ode_body = OdeBody(world)
        M = OdeMass()
        #M.setBox(50, 1, 1, 1)
        M.set_cylinder_total(100, 3, radius, length)
        self._ode_body.setMass(M)
        self._ode_body.setPosition(playerNode.getPos())
        self._ode_body.setQuaternion(playerNode.getQuat())
        # Create a BoxGeom
        boxGeom = OdeCappedCylinderGeom(space, radius, length)
        #boxGeom = OdeBoxGeom(space, 1, 1, 1)
        #boxGeom.setCollideBits(BitMask32(0x00000002))
        #boxGeom.setCategoryBits(BitMask32(0x00000001))
        boxGeom.setBody(self._ode_body)
        #boxes.append((boxNP, boxBody))
        
        j1 = OdeAMotorJoint(world)
        #j1.setAnchor(0,0,0)
        j1.attach(self._ode_body, None)
        j1.setParamVel(0, 30)
        j1.setParamVel(1, 0)
        j1.setParamVel(2, 0)
        #j1.setParamHiStop(0, 0)
        #j1.setParamHiStop(1, 0)
        #j1.setParamHiStop(2, 0)
        #j1.setParamLoStop(0, 0)
        #j1.setParamLoStop(1, 0)
        #j1.setParamLoStop(2, 0)
        #self._ode_body.attach(j1, None)
  
    def mouseUpdate(self,task):
        md = base.win.getPointer(0)
        dx = md.getX() - base.win.getXSize()/2.0
        dy = md.getY() - base.win.getYSize()/2.0
        
        yaw = dx/(base.win.getXSize()/2.0) * 90
        playerNode.setHpr(playerNode, -yaw, 0, 0)
        #base.camera.setHpr(base.camera, yaw, pith, roll)
        
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        return task.cont
        
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
       
        cameray = base.camera.getP() - (y - base.win.getYSize()/2)*0.12
        if base.win.movePointer(0, base.win.getXSize()/2, base.win.getYSize()/2):
           playerNode.setH(playerNode.getH() -  (x - base.win.getXSize()/2)*0.12)
           if cameray<-80:
               cameray = -80
           if cameray>90:
               cameray = 90
           base.camera.setP(cameray)
        return task.cont
     
    def moveUpdate(self,task):
        #playerNode.setPos(playerNode,self._vspeed*globalClock.getDt())
        ###playerNode.setPosQuat(render, self._ode_body.getPosition(), Quat(self._ode_body.getQuaternion()))
        playerNode.setPos(render, self._ode_body.getPosition())
        
        if (self._vforce.length() > 0):
            print self._vforce, render.getRelativeVector(playerNode, self._vforce)
            self._ode_body.setForce(render.getRelativeVector(playerNode, self._vforce))
        else:
            pass
        #self._vforce = Vec3(0,0,0)
        
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
        self._vforce.setZ( self.F_MOVE)
    def nogoUp(self):
        self._vforce.setZ( 0)

class ItemHandling(object):
    def __init__(self, playerNode):
        taskMgr.add(self.setItemPosition, 'ItemPosition')

    def setItemPosition(self, task):
        return task.cont
        