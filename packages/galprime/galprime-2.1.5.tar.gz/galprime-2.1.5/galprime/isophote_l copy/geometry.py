# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This module provides a container class to store parameters for the
geometry of an ellipse.
"""

import math

from astropy import log
import numpy as np

__all__ = ['EllipseGeometry']


IN_MASK = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

OUT_MASK = [
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
]


def _area(sma, eps, phi, r):
    """
    Compute elliptical sector area.
    """

    aux = r * math.cos(phi) / sma
    signal = aux / abs(aux)
    if abs(aux) >= 1.:
        aux = signal
    return abs(sma**2 * (1.-eps) / 2. * math.acos(aux))


class EllipseGeometry:

    def __init__(self, x0, y0, sma, eps, pa, astep=0.1, linear_growth=False,
                 fix_center=False, fix_pa=False, fix_eps=False):
        self.x0 = x0
        self.y0 = y0
        self.sma = sma
        self.eps = eps
        self.pa = pa

        self.astep = astep
        self.linear_growth = linear_growth

        # Fixed parameters are flagged in here. Note that the
        # ordering must follow the same ordering used in the
        # fitter._CORRECTORS list.
        self.fix = np.array([fix_center, fix_center, fix_pa, fix_eps])

        # limits for sector angular width
        self._phi_min = 0.05
        self._phi_max = 0.2

        # variables used in the calculation of the sector angular width
        sma1, sma2 = self.bounding_ellipses()
        inner_sma = min((sma2 - sma1), 3.)
        self._area_factor = (sma2 - sma1) * inner_sma

        # sma can eventually be zero!
        if self.sma > 0.:
            self.sector_angular_width = max(min((inner_sma / self.sma),
                                                self._phi_max), self._phi_min)
            self.initial_polar_angle = self.sector_angular_width / 2.
            self.initial_polar_radius = self.radius(self.initial_polar_angle)

    def find_center(self, image, threshold=0.1, verbose=True):

        self._centerer_mask_half_size = len(IN_MASK) / 2
        self.centerer_threshold = threshold

        # number of pixels in each mask
        sz = len(IN_MASK)
        self._centerer_ones_in = np.ma.masked_array(np.ones(shape=(sz, sz)),
                                                    mask=IN_MASK)
        self._centerer_ones_out = np.ma.masked_array(np.ones(shape=(sz, sz)),
                                                     mask=OUT_MASK)
        self._centerer_in_mask_npix = np.sum(self._centerer_ones_in)
        self._centerer_out_mask_npix = np.sum(self._centerer_ones_out)

        # Check if center coordinates point to somewhere inside the frame.
        # If not, set then to frame center.
        shape = image.shape
        _x0 = self.x0
        _y0 = self.y0
        if (_x0 is None or _x0 < 0 or _x0 >= shape[1] or _y0 is None or
                _y0 < 0 or _y0 >= shape[0]):
            _x0 = shape[1] / 2
            _y0 = shape[0] / 2

        max_fom = 0.
        max_i = 0
        max_j = 0

        # scan all positions inside window
        window_half_size = 5
        for i in range(int(_x0 - window_half_size),
                       int(_x0 + window_half_size) + 1):
            for j in range(int(_y0 - window_half_size),
                           int(_y0 + window_half_size) + 1):

                # ensure that it stays inside image frame
                i1 = int(max(0, i - self._centerer_mask_half_size))
                j1 = int(max(0, j - self._centerer_mask_half_size))
                i2 = int(min(shape[1] - 1, i + self._centerer_mask_half_size))
                j2 = int(min(shape[0] - 1, j + self._centerer_mask_half_size))

                window = image[j1:j2, i1:i2]

                # averages in inner and outer regions.
                inner = np.ma.masked_array(window, mask=IN_MASK)
                outer = np.ma.masked_array(window, mask=OUT_MASK)
                inner_avg = np.sum(inner) / self._centerer_in_mask_npix
                outer_avg = np.sum(outer) / self._centerer_out_mask_npix

                # standard deviation and figure of merit
                inner_std = np.std(inner)
                outer_std = np.std(outer)
                stddev = np.sqrt(inner_std**2 + outer_std**2)

                fom = (inner_avg - outer_avg) / stddev

                if fom > max_fom:
                    max_fom = fom
                    max_i = i
                    max_j = j

        # figure of merit > threshold: update geometry with new coordinates.
        if max_fom > threshold:
            self.x0 = float(max_i)
            self.y0 = float(max_j)

            if verbose:
                log.info("Found center at x0 = {0:5.1f}, y0 = {1:5.1f}"
                         .format(self.x0, self.y0))
        else:
            if verbose:
                log.info('Result is below the threshold -- keeping the '
                         'original coordinates.')

    def radius(self, angle):

        return (self.sma * (1. - self.eps) /
                np.sqrt(((1. - self.eps) * np.cos(angle))**2 +
                        (np.sin(angle))**2))

    def initialize_sector_geometry(self, phi):

        # These polar radii bound the region between the inner
        # and outer ellipses that define the sector.
        sma1, sma2 = self.bounding_ellipses()
        eps_ = 1. - self.eps

        # polar vector at one side of the elliptical sector
        self._phi1 = phi - self.sector_angular_width / 2.
        r1 = (sma1 * eps_ / math.sqrt((eps_ * math.cos(self._phi1))**2
                                      + (math.sin(self._phi1))**2))
        r2 = (sma2 * eps_ / math.sqrt((eps_ * math.cos(self._phi1))**2
                                      + (math.sin(self._phi1))**2))

        # polar vector at the other side of the elliptical sector
        self._phi2 = phi + self.sector_angular_width / 2.
        r3 = (sma2 * eps_ / math.sqrt((eps_ * math.cos(self._phi2))**2
                                      + (math.sin(self._phi2))**2))

        r4 = (sma1 * eps_ / math.sqrt((eps_ * math.cos(self._phi2))**2
                                      + (math.sin(self._phi2))**2))

        # sector area
        sa1 = _area(sma1, self.eps, self._phi1, r1)
        sa2 = _area(sma2, self.eps, self._phi1, r2)
        sa3 = _area(sma2, self.eps, self._phi2, r3)
        sa4 = _area(sma1, self.eps, self._phi2, r4)
        self.sector_area = abs((sa3 - sa2) - (sa4 - sa1))

        # angular width of sector. It is calculated such that the sectors
        # come out with roughly constant area along the ellipse.
        self.sector_angular_width = max(min((self._area_factor / (r3 - r4) /
                                             r4), self._phi_max),
                                        self._phi_min)

        # compute the 4 vertices that define the elliptical sector.
        vertex_x = np.zeros(shape=4, dtype=float)
        vertex_y = np.zeros(shape=4, dtype=float)

        # vertices are labelled in counterclockwise sequence
        vertex_x[0:2] = np.array([r1, r2]) * math.cos(self._phi1 + self.pa)
        vertex_x[2:4] = np.array([r4, r3]) * math.cos(self._phi2 + self.pa)
        vertex_y[0:2] = np.array([r1, r2]) * math.sin(self._phi1 + self.pa)
        vertex_y[2:4] = np.array([r4, r3]) * math.sin(self._phi2 + self.pa)
        vertex_x += self.x0
        vertex_y += self.y0

        return vertex_x, vertex_y

    def bounding_ellipses(self):

        if self.linear_growth:
            a1 = self.sma - self.astep / 2.
            a2 = self.sma + self.astep / 2.
        else:
            a1 = self.sma * (1. - self.astep / 2.)
            a2 = self.sma * (1. + self.astep / 2.)

        return a1, a2

    def polar_angle_sector_limits(self):
        return self._phi1, self._phi2

    def to_polar(self, x, y):

        # We split in between a scalar version and a
        # vectorized version. This is necessary for
        # now so we don't pay a heavy speed penalty
        # that is incurred when using vectorized code.

        # The split in two separate functions helps in
        # the profiling analysis: most of the time is
        # spent in the scalar function.

        if isinstance(x, (int, float)):
            return self._to_polar_scalar(x, y)
        else:
            return self._to_polar_vectorized(x, y)

    def _to_polar_scalar(self, x, y):

        x1 = x - self.x0
        y1 = y - self.y0

        radius = x1**2 + y1**2
        if radius > 0.0:
            radius = math.sqrt(radius)
            angle = math.asin(abs(y1) / radius)
        else:
            radius = 0.
            angle = 1.

        if x1 >= 0. and y1 < 0.:
            angle = 2*np.pi - angle
        elif x1 < 0. and y1 >= 0.:
            angle = np.pi - angle
        elif x1 < 0. and y1 < 0.:
            angle = np.pi + angle

        pa1 = self.pa
        if self.pa < 0.:
            pa1 = self.pa + 2*np.pi
        angle = angle - pa1
        if angle < 0.:
            angle = angle + 2*np.pi

        return radius, angle

    def _to_polar_vectorized(self, x, y):

        x1 = np.atleast_2d(x) - self.x0
        y1 = np.atleast_2d(y) - self.y0

        radius = x1**2 + y1**2
        angle = np.ones(radius.shape)

        imask = (radius > 0.0)
        radius[imask] = np.sqrt(radius[imask])
        angle[imask] = np.arcsin(np.abs(y1[imask]) / radius[imask])
        radius[~imask] = 0.
        angle[~imask] = 1.

        idx = (x1 >= 0.) & (y1 < 0)
        angle[idx] = 2*np.pi - angle[idx]
        idx = (x1 < 0.) & (y1 >= 0.)
        angle[idx] = np.pi - angle[idx]
        idx = (x1 < 0.) & (y1 < 0.)
        angle[idx] = np.pi + angle[idx]

        pa1 = self.pa
        if self.pa < 0.:
            pa1 = self.pa + 2*np.pi
        angle = angle - pa1
        angle[angle < 0] += 2*np.pi

        return radius, angle

    def update_sma(self, step):
        """
        Calculate an updated value for the semimajor axis, given the
        current value and the step value.

        The step value must be managed by the caller to support both
        modes: grow outwards and shrink inwards.

        Parameters
        ----------
        step : float
            The step value.

        Returns
        -------
        sma : float
            The new semimajor axis length.
        """

        if self.linear_growth:
            sma = self.sma + step
        else:
            sma = self.sma * (1. + step)
        return sma

    def reset_sma(self, step):
        """
        Change the direction of semimajor axis growth, from outwards to
        inwards.

        Parameters
        ----------
        step : float
            The current step value.

        Returns
        -------
        sma, new_step : float
            The new semimajor axis length and the new step value to
            initiate the shrinking of the semimajor axis length. This is
            the step value that should be used when calling the
            :meth:`~photutils.isophote.EllipseGeometry.update_sma`
            method.
        """

        if self.linear_growth:
            sma = self.sma - step
            step = -step
        else:
            aux = 1. / (1. + step)
            sma = self.sma * aux
            step = aux - 1.

        return sma, step
