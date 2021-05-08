import sys

class Particle(object):
    def __init__(self, real, fx, best_neighbour=-sys.maxsize):
        self.real = real
        self.fx = fx
        self.best_real = fx
        self.best_neighbour = best_neighbour
        

    def __lt__(self, other):
        return self.fx > other.fx

    def __str__(self):
        return "real: % s, fx: % s, best_real: % s" % (self.real, self.fx, self.best_real)