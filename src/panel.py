from panda3d.core import Vec3


#from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletBoxShape

class Panel(object):
    def __init__(self, world, x, y, w, h, adir):
        self._model = None
        self._initPhysics(world, x, y, w, h, adir)
        self._loadModel(x, y, h)
        
    def remove(self):
        if self._model is not None:
            self._model.remove()
            
    def _loadModel(self, x, y, h):
        self._model = loader.loadModel("../data/models/panel_green.egg")
        #self._model.setPos(0,0,-h/2)
        self._model.reparentTo(self._modulo_node)
        
    def _initPhysics(self, world, x, y, w, h, adir):
        shape = BulletBoxShape(Vec3(w/4.0, w/4.0, h/4.0))
        self._g_node = BulletGhostNode('Box')
        #self._rb_node.setMass(0)
        self._g_node.addShape(shape)
        #self._rb_node.setAngularFactor(Vec3(0,0,0))
        #self._rb_node.setDeactivationEnabled(False, True)
        world.attachGhost(self._g_node)
        
        self._modulo_node = render.attachNewNode(self._g_node)
        self._modulo_node.setPos(x, y, h/2.0)
        self._modulo_node.setHpr(adir, 0, 0)
        self._modulo_node.setPos(self._modulo_node, 0, w/2.0, 0)
        
    def getRBNode(self):
        return self._g_node