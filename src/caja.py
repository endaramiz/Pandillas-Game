
class Caja(object):
    def __init__(self, i, j, di, dj, model):
        self.i = i
        self.j = j
        self.di = di
        self.dj = dj
        self.model = model
        self.entregada = False
        self.perdida = False