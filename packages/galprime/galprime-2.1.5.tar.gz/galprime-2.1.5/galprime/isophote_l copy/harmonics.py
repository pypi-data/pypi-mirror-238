# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This module provides tools for computing and fitting harmonic functions.
"""

import numpy as np

__all__ = ['first_and_second_harmonic_function',
           'fit_first_and_second_harmonics', 'fit_upper_harmonic']


def _least_squares_fit(optimize_func, parameters):
    # call the least squares fitting
    # function and handle the result.
    from scipy.optimize import leastsq
    solution = leastsq(optimize_func, parameters, full_output=True)

    if solution[4] > 4:
        raise RuntimeError("Error in least squares fit: " + solution[3])

    # return coefficients and covariance matrix
    return (solution[0], solution[1])


def first_and_second_harmonic_function(phi, c):

    return (c[0] + c[1]*np.sin(phi) + c[2]*np.cos(phi) + c[3]*np.sin(2*phi) +
            c[4]*np.cos(2*phi))


def fit_first_and_second_harmonics(phi, intensities):

    a1 = b1 = a2 = b2 = 1.

    def optimize_func(x):
        return first_and_second_harmonic_function(
            phi, np.array([x[0], x[1], x[2], x[3], x[4]])) - intensities

    return _least_squares_fit(optimize_func, [np.nanmean(intensities), a1, b1,
                                              a2, b2])


def fit_upper_harmonic(phi, intensities, order):

    an = bn = 1.

    def optimize_func(x):
        return (x[0] + x[1]*np.sin(order*phi) + x[2]*np.cos(order*phi) -
                intensities)

    return _least_squares_fit(optimize_func, [np.nanmean(intensities), an, bn])
