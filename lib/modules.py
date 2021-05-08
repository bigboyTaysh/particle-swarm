import random
from math import pow, log2, cos, pi, sin
from copy import deepcopy, copy
import numpy
from time import time
import numba
from lib.models import Particle
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
    neighborhood = []
    for particle in particles:
        for neighbor in particles:
            if abs(neighbor.real - particle.real) <= neighborhood_distance and particle.fx > neighbor.best_neighbour_fx:
                neighbor.best_neighbour_real = particle.real
                neighbor.best_neighbour_fx = particle.fx


def get_vector(particle, c1_weight, c2_weight, c3_weight):
    return c1_weight * random() * particle.vector + \
        c2_weight * random() * (particle.best_real - particle.real) + \
        c3_weight * random() * (particle.best_neighbour_real - particle.real)


def are_close_enough(particles, precision):
    prec = pow(10, -precision)
    for particle in particles:
        if not all(list(map(lambda x: True if abs(x.real - particle.real) <= prec else False, particles))):
            return False
    return True


def evolution(range_a, range_b, precision, particles_number, iterations, c1_weight, c2_weight, c3_weight, neighborhood_distance):
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
        local_best = max(particles, key=attrgetter('fx'))

        if local_best.fx > best_fx:
            best_fx = local_best.fx
            best_real = local_best.real

        best_fxs.append(best_fx)
        avg_fxs.append(sum(particles_fx_list) / particles_number)
        min_fxs.append(min(particles_fx_list))

        update_neighbours_best(particles, neighborhood_distance)

        for particle in particles:
            particle.vector = get_vector(particle, c1_weight, c2_weight, c3_weight)
            particle.real = round(particle.real + particle.vector, precision)

        if are_close_enough(particles, precision):
            break

        

    for particle in particles: print(particle)
    print('')
    return best_real, best_fx, best_fxs, avg_fxs, min_fxs, particles_lists


'''
@numba.jit(nopython=True)
def evolution(range_a, range_b, precision, generations_number, checkMax = False):
    power = power_of_2(range_a, range_b, precision)
    best_binary = numpy.empty((generations_number,power), dtype=numpy.int32)
    best_reals = numpy.empty(generations_number, dtype=numpy.double)
    best_fxs = numpy.empty(generations_number, dtype=numpy.double)
    local_binary = numpy.empty((generations_number,power), dtype=numpy.int32)
    local_reals = numpy.empty(generations_number, dtype=numpy.double)
    local_fxs = []
    local_fxs_list = []
    new_individuals_bins = numpy.empty((power, power), dtype=numpy.int32)
    new_individuals_fxs = numpy.empty(power, dtype=numpy.double)
    new_individuals_reals = numpy.empty(power, dtype=numpy.double)

    local = False
    found = False
    iteration = 0
    
    while iteration < generations_number:
        local = False
        local_binary[iteration] = get_individual(range_a, range_b, precision, power)
        local_reals[iteration] = bin_to_real(local_binary[iteration], range_a, range_b, precision, power)
        local_fxs.append(func(local_reals[iteration]))

        while not local:
            new_individuals(local_binary[iteration], new_individuals_bins, new_individuals_reals, new_individuals_fxs, range_a, range_b, precision, power, generations_number)
            index = numpy.argmax(new_individuals_fxs)
            
            if local_fxs[-1] < new_individuals_fxs[index]:
                local_fxs.append(new_individuals_fxs[index])
                local_reals[iteration] = new_individuals_reals[index]
                local_binary[iteration] = new_individuals_bins[index]
            else:
                local = True

        local_fxs_list.append(local_fxs[:])

        if iteration == 0:
            best_binary[iteration] = local_binary[iteration]
            best_reals[iteration] = local_reals[iteration]
            best_fxs[iteration] = local_fxs[-1]
        elif best_fxs[iteration-1] < local_fxs[-1]:
            best_binary[iteration] = local_binary[iteration]
            best_reals[iteration] = local_reals[iteration]
            best_fxs[iteration] = local_fxs[-1]
        else:
            best_binary[iteration] = best_binary[iteration-1]
            best_reals[iteration] = best_reals[iteration-1]
            best_fxs[iteration] = best_fxs[iteration-1]

        if checkMax:
            if(best_reals[iteration] == 10.999):
                found = True
                break

        local_fxs.clear()
        iteration += 1

    return best_reals, best_binary, best_fxs, local_fxs_list, iteration, found


@numba.jit(nopython=True, fastmath=True)
def test_generation(range_a, range_b, precision, generations):
    result = numpy.zeros(generations, dtype=numpy.int32)

    for i in numpy.arange(100000):
        _, _, _, _, iteration, found = evolution(range_a, range_b, precision, generations, True)
        result[iteration] += 1 if found else 0

    return result

'''
