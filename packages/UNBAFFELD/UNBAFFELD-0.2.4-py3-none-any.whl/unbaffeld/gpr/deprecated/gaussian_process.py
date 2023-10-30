"""gaussian_process2.py

This script calculates the log of the evidence on a grid of sigma_x, sigma_y
I assume flat priors for sigmax, sigmay
"""

import numpy as np
import random
import math as m


def model_function(x, a, b, c, d):
    """This function returns the value of model function"""
    return a * m.pow(x, 3) + b * m.pow(x, 2) + c * m.pow(x, 1) + d


def data_signal(y):
    """This function returns the perfect data signal"""
    da = 12
    db = 0
    return da * y + db


def noisey_signal(x, noise, a, b, c, d):
    """Return a noisey signal at x"""
    y = model_function(x, a, b, c, d)
    ly = data_signal(y)
    return random.gauss(ly, noise)


def kernel(x1, x2, sigmaf, sigmax):
    """Return the kernel for x1,x2"""
    return m.pow(sigmaf, 2) * m.exp(-0.5 * m.pow((x2 - x1) / sigmax, 2))


def kss(x1, x2, sigmaf, sigmax):
    """Return k** for x1,x2"""
    return kernel(x1, x2, sigmaf, sigmax)


def kls(x1, x2, sigmaf, sigmax, a, b, c, d):
    """Return the kl* for x1,x2"""
    lx1 = data_signal(model_function(x1, a, b, c, d))
    return kernel(lx1, x2, sigmaf, sigmax)


def kll(x1, x2, sigmaf, sigmax, a, b, c, d):
    """Return the kll for x1,x2"""
    lx1 = data_signal(model_function(x1, a, b, c, d))
    lx2 = data_signal(model_function(x2, a, b, c, d))
    return data_signal(data_signal(kernel(lx1, lx2, sigmaf, sigmax)))


def gaussian_sample(mat_mean, mat_l, points):
    """A sample from a normal distribution with mean mat_mat and L is the
    'square root' of the covariance matrix"""
    x_vec = np.zeros(points)
    for ix, xx in enumerate(x_vec):
        x_vec[ix] = random.gauss(0, 1)
    u_vec = mat_mean + np.dot(mat_l, x_vec)
    return u_vec
