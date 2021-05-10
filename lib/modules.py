import random
from math import pow, log2, cos, pi, sin
from copy import deepcopy, copy
import numpy
from time import time
import numba
from lib.models import Particle, Test
from random import random, randrange
import sys
from operator import attrgetter


@numba.jit(nopython=True, fastmath=True)
def random_real(range_a,  range_b,  precision):
    prec = pow(10, precision)
    return numpy.round(randrange(range_a * prec, (range_b) * prec + 1)/prec, precision)


@numba.jit(nopython=True, fastmath=True)
def func(real):
    return numpy.mod(real, 1) * (cos(20.0 * pi * real) - sin(real))


def get_individual(range_a, range_b, precision):
    real = random_real(range_a, range_b, precision)
    return Particle(real, func(real))


def new_individuals(range_a, range_b, precision, particles_number):
    particles = []
    for _ in range(particles_number):
        particles.append(get_individual(range_a, range_b, precision))
    return particles


def update_neighbours_best(particles, neighborhood_distance):
    for particle in particles:
        for neighbor in particles:
            if abs(neighbor.real - particle.real) <= neighborhood_distance and particle.fx > neighbor.best_neighbour_fx:
                neighbor.best_neighbour_real = particle.real
                neighbor.best_neighbour_fx = particle.fx


def get_vector(range_a, range_b, particle, c1_weight, c2_weight, c3_weight):
    factor = velocity_clamping_factor(range_a,  range_b)
    vector = c1_weight * random() * particle.vector + \
        c2_weight * random() * (particle.best_real - particle.real) + \
        c3_weight * random() * (particle.best_neighbour_real - particle.real)

    if vector > factor:
        vector = factor
    elif vector < -factor:
        particle.vector = -factor

    return vector


def velocity_clamping_factor(range_a,  range_b):
    return 0.1 * (range_b - range_a)


def are_close_enough(particles, precision):
    prec = pow(10, -precision)
    for particle in particles:
        if not all(list(map(lambda x: True if abs(x.real - particle.real) <= prec else False, particles))):
            return False
    return True


def evolution(range_a, range_b, precision, particles_number, iterations, c1_weight, c2_weight, c3_weight, neighborhood_distance, check_distance=True):
    best_fx = -sys.maxsize
    best_real = 0.0
    local_best = None
    particles_fx_list = []
    particles_lists = []
    best_fxs = []
    avg_fxs = []
    min_fxs = []

    particles = new_individuals(range_a, range_b, precision, particles_number)

    for _ in range(iterations):
        for particle in particles:
            particle.fx = func(particle.real)

            if particle.fx > particle.best_fx:
                particle.best_real = particle.real
                particle.best_fx = particle.fx

        particles_lists.append([particle.real for particle in particles])
        particles_fx_list = [particle.fx for particle in particles]
        local_best = max(particles)

        if local_best.fx > best_fx:
            best_fx = local_best.fx
            best_real = local_best.real

        best_fxs.append(best_fx)
        avg_fxs.append(sum(particles_fx_list) / particles_number)
        min_fxs.append(min(particles_fx_list))

        update_neighbours_best(particles, neighborhood_distance)

        for particle in particles:
            particle.vector = get_vector(
                range_a, range_b, particle, c1_weight, c2_weight, c3_weight)
            particle.real = round(particle.real + particle.vector, precision)

        if check_distance and are_close_enough(particles, precision):
            break

    return best_real, best_fx, best_fxs, avg_fxs, min_fxs, particles_lists


def test(range_a, range_b, precision):
    tests = []
    bests = []
    avg = 0

    for particles_number in range(10, 51, 10):
        for iterations in range(100, 501, 100):
            print(iterations)
            for c1 in numpy.around(numpy.arange(1, 2.01, 0.5), 1):
                for c2 in numpy.around(numpy.arange(c1, 2.01, 0.5), 1):
                    for c3 in numpy.around(numpy.arange(c2, 2.01, 0.5), 1):
                        for neighborhood in range(1, 6, 1):
                            avg = 0
                            for _ in range(0, 11):
                                best_real, best_fx, best_fxs, avg_fxs, min_fxs, particles = evolution(
                                    range_a, range_b, precision, particles_number, iterations, c1, c2, c3, neighborhood, False)
                                bests.append(best_fx)
                                avg += sum(avg_fxs) / len(avg_fxs)

                            tests.append(Test(
                                particles_number, iterations, c1, c2, c3, neighborhood, max(bests), avg / 10))    

    return tests
