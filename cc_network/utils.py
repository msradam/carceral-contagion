import numpy
from enum import Enum


def generate_sentence(race):
    a = 1.2
    if race == 'black':
        b = a / 17.0
    if race == 'white':
        b = a / 14.0
    gam = numpy.random.gamma(a, 1.0 / b)
    sentence = numpy.random.poisson(gam)
    return sentence
