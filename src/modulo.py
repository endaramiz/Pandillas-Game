from panda3d.core import Vec3


#from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

class Modulo(object):
    def __init__(self, world, x, y, w, h):
        self._model = None
        self._initPhysics(world, x, y, w, h)
        self._loadModel(x, y, h)
        
    def remove(self):
        if self._model is not None:
            self._model.remove()
            
    def _loadModel(self, x, y, h):
        self._model = loader.loadModel("../data/models/cube.egg")
        self._model.setPos(0,0,-h/2)
        self._model.reparentTo(self._modulo_node)
        
    def _initPhysics(self, world, x, y, w, h):
        print Vec3(w*0.5,w*0.5,h*0.5)
        shape = BulletBoxShape(Vec3(w*0.5,w*0.5,h*0.5))
        self._rb_node = BulletRigidBodyNode('Box')
        self._rb_node.setMass(0)
        self._rb_node.addShape(shape)
        #self._rb_node.setAngularFactor(Vec3(0,0,0))
        #self._rb_node.setDeactivationEnabled(False, True)
        world.attachRigidBody(self._rb_node)
        
        self._modulo_node = render.attachNewNode(self._rb_node)
        self._modulo_node.setPos(x, y, h/2.0)
        