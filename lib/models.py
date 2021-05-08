import sys, time
from PyQt5 import QtCore

class Particle(object):
    def __init__(self, real, fx):
        self.real = real
        self.fx = fx
        self.best_real = real
        self.best_fx = fx
        self.best_neighbour_real = -sys.maxsize
        self.best_neighbour_fx = -sys.maxsize
        self.vector = 0
        

    def __lt__(self, other):
        return self.fx > other.fx

    def __str__(self):
        return "real: % s, fx: % s, best_real: % s" % (self.real, self.fx, self.best_real)

class ThreadClass(QtCore.QThread):
    signal = QtCore.pyqtSignal(list)
    particles_list = []

    def __init__(self, parent = None):
        super(ThreadClass, self).__init__(parent)

    def run(self):
        for partices in self.particles_list:
            self.signal.emit(partices)
            time.sleep(0.02)