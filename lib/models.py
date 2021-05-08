import sys

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