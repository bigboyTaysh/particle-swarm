import sys
import time
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
        return self.fx < other.fx

    def __str__(self):
        return "real: % s, fx: % s, best_real: % s" % (self.real, self.fx, self.best_real)

class Test(object):
    def __init__(self, particles, iterations, c1, c2, c3, neighborhood, fmax, fave):
        self.particles = particles
        self.iterations = iterations
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.neighborhood = neighborhood
        self.fmax = fmax
        self.fave = fave


class ThreadClass(QtCore.QThread):
    signal = QtCore.pyqtSignal(list)
    particles_list = []

    def __init__(self, parent=None):
        super(ThreadClass, self).__init__(parent)

    def run(self):
        for partices in self.particles_list:
            self.signal.emit(partices)
            time.sleep(0.01)
