#from base.graphics.image import Image
#from base.graphics.graphics import Graphics

from xml.dom import minidom
from math import ceil
import sys

from caja import Caja
from modulo import Modulo
from panel import Panel

class Layer(object):
    def __init__(self, xml_layer):
        #print xml_layer.toxml()
        self._data = list()
        self._name = xml_layer.getAttribute("name")
        self._w = int(xml_layer.getAttribute("width"))
        self._h = int(xml_layer.getAttribute("height"))
        j = 0
        row = list()
        for tile in xml_layer.getElementsByTagName("tile"):
            row.append(int(tile.getAttribute("gid")))
            j += 1
            if j >= self._w:
                j = 0
                self._data.append(row)
                row = list()
        #print self._data
                
    def name(self):
        return self._name
        
    def data(self):
        return self._data
        
    def get(self, i, j):
        return self._data[i][j]
        
    def h(self):
        return self._h
        
    def w(self):
        return self._w

class TiledParser(object):
    def __init__(self, tilemap_name):
        xml_doc = minidom.parse("../data/tiles/maps/"+tilemap_name+".tmx")
        self._layer = Layer(xml_doc.getElementsByTagName("layer")[0])
        
    def load_models(self, world):
        #models = list()
        modulos = list()
        paneles = list()
        for i in range(self._layer.h()):
            for j in range(self._layer.w()):
                v = self._layer.get(i, j)
                #s = 8
                w = 2.5
                h = 2
                x = j*w
                y = -i*w
                if (v == 5):
                    modulo = Modulo(world, x, y, w, h)
                    modulos.append(modulo)
                elif (1 <= v and v <= 4):
                    modulo = Modulo(world, x, y, w, h)
                    modulos.append(modulo)
                    panel = Panel(world, x, y, w, h, (v-1)*90)
                    paneles.append(panel)
                    """
                elif (6 <= v and v <= 9):
                    model = loader.loadModel("../data/models/my/mybflecha_mag.egg")      
                    model.reparentTo(render)
                    model.setPos(j*s,-i*s,0)
                    model.setScale(s/2.)
                    model.setHpr(-(v-5)*90,0,0)
                    models.append(model)
                elif (13 <= v and v <= 16):
                    model = loader.loadModel("../data/models/my/mybflecha_roj.egg")      
                    model.reparentTo(render)
                    model.setPos(j*s,-i*s,0)
                    model.setScale(s/2.)
                    model.setHpr(-(v-12)*90,0,0)
                    models.append(model)
                elif (v == 17):
                    model = loader.loadModel("../data/models/my/mybpoint_green.egg")      
                    model.reparentTo(render)
                    model.setPos(j*s,-i*s,0)
                    model.setScale(s/2.)
                    models.append(model)
                elif (v == 18):
                    model = loader.loadModel("../data/models/my/mybpoint_red.egg")      
                    model.reparentTo(render)
                    model.setPos(j*s,-i*s,0)
                    model.setScale(s/2.)
                    models.append(model)
                    """
        return modulos, paneles
        return models
                    
    def load_cajas(self):
        cajas = list()
        for i in range(self._layer.h()):
            for j in range(self._layer.w()):
                v = self._layer.get(i, j)
                dirs = [[-1,0], [0,1], [1,0], [0,-1]]
                s = 8
                if (13 <= v and v <= 16):
                    caja_model = loader.loadModel("../data/models/my/mybox.egg")                     
                    caja_model.reparentTo(render)
                    caja_model.setPos(j*s,-i*s, 0)
                    caja_model.setScale(s/2.)
                    caja_model.setHpr(-v*90,0,0)
                    caja = Caja(i, j, dirs[v-13][0], dirs[v-13][1], caja_model)
                    cajas.append(caja)
        return cajas
        
    def get_dir(self, i, j, desvio_activated=False):
        v = self._layer.get(i, j)
        dirs = [[-1,0], [0,1], [1,0], [0,-1]]
        if (1 <= v and v <= 4):
            return dirs[v-1]
        if (6 <= v and v <= 9 and desvio_activated):
            return dirs[v-6]
        return None
        
    def entregada(self, i, j):
        v = self._layer.get(i, j)
        return v == 17
        
    def perdida(self, i, j):
        v = self._layer.get(i, j)
        return v == 18
        