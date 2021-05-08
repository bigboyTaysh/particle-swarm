import random
from math import pow, log2, cos, pi, sin
from copy import deepcopy, copy
import numpy
from time import time
import numba
from lib.models import Particle


@numba.jit(nopython=True, fastmath=True)
def random_real(range_a,  range_b,  precision):
    prec = pow(10, precision)
    return numpy.round(random.randrange(range_a * prec, (range_b) * prec + 1)/prec, precision)

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


def evolution(range_a, range_b, precision, particles_number, iterations, c1_weight, c2_weight, c3_weight, neighborhood_distance):
    particles = new_individuals(range_a, range_b, precision, particles_number)
    for _ in range(iterations):
        print(particle) 


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
