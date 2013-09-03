from panda3d.core import *

class Player(object):
    speed = 100
    #FORWARD = Vec3(0,2,0)
    #BACK = Vec3(0,-1,0)
    #LEFT = Vec3(-1,0,0)
    #RIGHT = Vec3(1,0,0)
    #STOP = Vec3(0)
    #walk = STOP
    #strafe = STOP
    #readyToJump = False
    #jump = 0

    global playerNode
    playerNode = NodePath('player')
    
    
    def __init__(self):
        self._loadModel()
        self._setUpCamera()
        self._attachControls()
        taskMgr.add(self.mouseUpdate, 'mouse-task')
        taskMgr.add(self.moveUpdate, 'move-task')

        ItemHandling(playerNode)
        
        self._vspeed = Vec3(0,0,0)
        
    def _loadModel(self):
        playerNode.reparentTo(render)
        playerNode.setPos(0,0,4)
        playerNode.setScale(.05)
   
    def _setUpCamera(self):
        pl = base.cam.node().getLens()
        pl.setFov(70)
        base.cam.node().setLens(pl)
        base.camera.reparentTo(playerNode)

    def _attachControls(self):
        #base.accept( "s" , self.__setattr__,["walk",self.STOP] )
        base.accept("w", self.goForward)
        base.accept("s", self.goBack)
        base.accept("a", self.goLeft)
        base.accept("d", self.goRight)
       
    def mouseUpdate(self,task):
        md = base.win.getPointer(0)
        dx = md.getX() - base.win.getXSize()/2.0
        dy = md.getY() - base.win.getYSize()/2.0
        
        print dx
        
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
        #playerNode.setPos(playerNode,self.walk*globalClock.getDt()*self.speed)
        #playerNode.setPos(playerNode,self.strafe*globalClock.getDt()*self.speed)
        playerNode.setPos(playerNode,self._vspeed*globalClock.getDt())
        return task.cont
        
    def goForward(self):
        self._vspeed.setY( self.speed)
    def goBack(self):
        self._vspeed.setY(-self.speed)
    def goLeft(self):
        self._vspeed.setX(-self.speed)
    def goRight(self):
        self._vspeed.setX( self.speed)

class ItemHandling(object):
    def __init__(self, playerNode):
        taskMgr.add(self.setItemPosition, 'ItemPosition')

    def setItemPosition(self, task):
        return task.cont
        