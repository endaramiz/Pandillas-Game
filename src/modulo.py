from panda3d.core import Vec3


#from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

class Modulo(object):
    def __init__(self, world, x, y, w, h):
        self._model = None
        self._initPhysics(world, x, y, w, h)
        self._loadModel(x, y)
        
    def remove(self):
        if self._model is not None:
            self._model.remove()
            
    def _loadModel(self, x, y):
        self._model = loader.loadModel("../data/models/cube.egg")      
        self._model.reparentTo(self._modulo_node)
        
    def _initPhysics(self, world, x, y, w, h):
        shape = BulletBoxShape(Vec3(w,w,h))
        self._rb_node = BulletRigidBodyNode('Box')
        self._rb_node.setMass(0)
        self._rb_node.addShape(shape)
        #self._rb_node.setAngularFactor(Vec3(0,0,0))
        #self._rb_node.setDeactivationEnabled(False, True)
        world.attachRigidBody(self._rb_node)
        
        self._modulo_node = render.attachNewNode(self._rb_node)
        self._modulo_node.setPos(x, y, 0)
        