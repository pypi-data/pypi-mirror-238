from .solver import FiberSolver
from PyFiberModes import Mode, ModeFamily
from math import sqrt, isnan, isinf
import numpy
from scipy.special import jn, jn_zeros, kn, j0, j1, k0, k1, jvp, kvp
from PyFiberModes.constants import Y0
import logging


class Cutoff(FiberSolver):
    """
    Cutoff for standard step-index fiber.
    """

    logger = logging.getLogger(__name__)

    def __call__(self, mode):
        nu = mode.nu
        m = mode.m

        if mode.family is ModeFamily.LP:
            if nu == 0:
                nu, m = 1, -1

            else:
                nu -= 1
        elif mode.family is ModeFamily.HE:
            if nu == 1:
                m -= 1
            else:
                return self._findHEcutoff(mode)

        return jn_zeros(nu, m)[m - 1]

    def _cutoffHE(self, V0, nu):
        wavelength = self.fiber.V0_to_wavelength(V0)
        n02 = self.fiber.get_maximum_index(0, wavelength)**2 / self.fiber.get_minimum_index(1, wavelength)**2
        return (1 + n02) * jn(nu - 2, V0) - (1 - n02) * jn(nu, V0)

    def _findHEcutoff(self, mode):
        if mode.m > 1:
            pm = Mode(mode.family, mode.nu, mode.m - 1)
            lowbound = self.fiber.cutoff(pm)
            if isnan(lowbound) or isinf(lowbound):
                raise AssertionError("_findHEcutoff: no previous cutoff for"
                                     "{} mode".format(str(mode)))
            delta = 1 / lowbound if lowbound else self._MCD
            lowbound += delta
        else:
            lowbound = delta = self._MCD
        ipoints = numpy.concatenate((jn_zeros(mode.nu, mode.m),
                                     jn_zeros(mode.nu - 2, mode.m)))
        ipoints.sort()
        ipoints = list(ipoints[ipoints > lowbound])
        co = self._findFirstRoot(self._cutoffHE,
                                 args=(mode.nu,),
                                 lowbound=lowbound,
                                 ipoints=ipoints,
                                 delta=delta)
        if isnan(co):
            self.logger.error("_findHEcutoff: no cutoff found for "
                              "{} mode".format(str(mode)))
            return 0
        return co


class Neff(FiberSolver):
    """
    Effective index for standard step-index fiber
    """

    def __call__(self, wavelength: float, mode, delta, lowbound):
        epsilon = 1e-12

        co = self.fiber.cutoff(mode=mode)
        if self.fiber.get_V0(wavelength=wavelength) < co:
            return float("nan")

        nco = self.fiber.get_maximum_index(0, wavelength)
        r = self.fiber.get_outer_radius(0)
        highbound = sqrt(nco**2 - (co / (r * wavelength.k0))**2) - epsilon

        if mode.family is ModeFamily.LP:
            nm = Mode(ModeFamily.LP, mode.nu + 1, mode.m)
        elif mode.family is ModeFamily.HE:
            nm = Mode(ModeFamily.LP, mode.nu, mode.m)
        elif mode.family is ModeFamily.EH:
            nm = Mode(ModeFamily.LP, mode.nu + 2, mode.m)
        else:
            nm = Mode(ModeFamily.LP, 1, mode.m + 1)
        co = self.fiber.cutoff(nm)
        try:
            lowbound = max(sqrt(nco**2 - (co / (r * wavelength.k0))**2) + epsilon,
                           self.fiber.get_minimum_index(-1, wavelength) + epsilon)
        except ValueError:
            lowbound = nco

        fct = {ModeFamily.LP: self._lpceq,
               ModeFamily.TE: self._teceq,
               ModeFamily.TM: self._tmceq,
               ModeFamily.HE: self._heceq,
               ModeFamily.EH: self._ehceq
               }

        return self._findBetween(fct[mode.family], lowbound, highbound,
                                 args=(wavelength, mode.nu))

    def _lpfield(self, wavelength, nu, neff, r):
        rho = self.fiber.get_outer_radius(0)
        k = wavelength.k0
        nco2 = self.fiber.get_maximum_index(0, wavelength)**2
        ncl2 = self.fiber.get_minimum_index(1, wavelength)**2
        u = rho * k * sqrt(nco2 - neff**2)
        w = rho * k * sqrt(neff**2 - ncl2)

        if r < rho:
            ex = j0(u * r / rho) / j0(u)
        else:
            ex = k0(w * r / rho) / k0(w)
        hy = neff * Y0 * ex  # Snyder & Love uses nco, but Bures uses neff

        return numpy.array((ex, 0, 0)), numpy.array((0, hy, 0))

    def _tefield(self, wavelength, nu, neff, r):
        rho = self.fiber.get_outer_radius(0)
        k = wavelength.k0
        nco2 = self.fiber.get_maximum_index(0, wavelength)**2
        ncl2 = self.fiber.get_minimum_index(1, wavelength)**2
        u = rho * k * sqrt(nco2 - neff**2)
        w = rho * k * sqrt(neff**2 - ncl2)

        if r < rho:
            hz = -Y0 * u / (k * rho) * j0(u * r / rho) / j1(u)
            ephi = -j1(u * r / rho) / j1(u)
        else:
            hz = Y0 * w / (k * rho) * k0(w * r / rho) / k1(w)
            ephi = -k1(w * r / rho) / k1(w)
        hr = -neff * Y0 * ephi

        return numpy.array((0, ephi, 0)), numpy.array((hr, 0, hz))

    def _tmfield(self, wavelength, nu, neff, r):
        rho = self.fiber.get_outer_radius(0)
        k = wavelength.k0
        nco2 = self.fiber.get_maximum_index(0, wavelength)**2
        ncl2 = self.fiber.get_minimum_index(1, wavelength)**2
        u = rho * k * sqrt(nco2 - neff**2)
        w = rho * k * sqrt(neff**2 - ncl2)

        if r < rho:
            ez = -u / (k * neff * rho) * j0(u * r / rho) / j1(u)
            er = j1(u * r / rho) / j1(u)
            hphi = Y0 * nco2 / neff * er
        else:
            ez = nco2 / ncl2 * w / (k * neff * rho) * k0(w * r / rho) / k1(w)
            er = nco2 / ncl2 * k1(w * r / rho) / k1(w)
            hphi = Y0 * nco2 / ncl2 * k1(w * r / rho) / k1(w)

        return numpy.array((er, 0, ez)), numpy.array((0, hphi, 0))

    def _hefield(self, wavelength, nu, neff, r):
        rho = self.fiber.get_outer_radius(0)
        k = wavelength.k0
        nco2 = self.fiber.get_maximum_index(0, wavelength)**2
        ncl2 = self.fiber.get_minimum_index(1, wavelength)**2
        u = rho * k * sqrt(nco2 - neff**2)
        w = rho * k * sqrt(neff**2 - ncl2)
        v = rho * k * sqrt(nco2 - ncl2)

        jnu = jn(nu, u)
        knw = kn(nu, w)

        Delta = (1 - ncl2 / nco2) / 2
        b1 = jvp(nu, u) / (u * jnu)
        b2 = kvp(nu, w) / (w * knw)
        F1 = (u * w / v)**2 * (b1 + (1 - 2 * Delta) * b2) / nu
        F2 = (v / (u * w))**2 * nu / (b1 + b2)
        a1 = (F2 - 1) / 2
        a2 = (F2 + 1) / 2
        a3 = (F1 - 1) / 2
        a4 = (F1 + 1) / 2
        a5 = (F1 - 1 + 2 * Delta) / 2
        a6 = (F1 + 1 - 2 * Delta) / 2

        if r < rho:
            jmur = jn(nu - 1, u * r / rho)
            jpur = jn(nu + 1, u * r / rho)
            jnur = jn(nu, u * r / rho)
            er = -(a1 * jmur + a2 * jpur) / jnu
            ephi = -(a1 * jmur - a2 * jpur) / jnu
            ez = u / (k * neff * rho) * jnur / jnu
            hr = Y0 * nco2 / neff * (a3 * jmur - a4 * jpur) / jnu
            hphi = -Y0 * nco2 / neff * (a3 * jmur + a4 * jpur) / jnu
            hz = Y0 * u * F2 / (k * rho) * jnur / jnu
        else:
            kmur = kn(nu - 1, w * r / rho)
            kpur = kn(nu + 1, w * r / rho)
            knur = kn(nu, w * r / rho)
            er = -u / w * (a1 * kmur - a2 * kpur) / knw
            ephi = -u / w * (a1 * kmur + a2 * kpur) / knw
            ez = u / (k * neff * rho) * knur / knw
            hr = Y0 * nco2 / neff * u / w * (a5 * kmur + a6 * kpur) / knw
            hphi = -Y0 * nco2 / neff * u / w * (a5 * kmur - a6 * kpur) / knw
            hz = Y0 * u * F2 / (k * rho) * knur / knw

        return numpy.array((er, ephi, ez)), numpy.array((hr, hphi, hz))

    _ehfield = _hefield

    def _uw(self, wavelength, neff):
        r = self.fiber.get_outer_radius(0)
        rk0 = r * wavelength.k0
        return (rk0 * sqrt(self.fiber.get_maximum_index(0, wavelength)**2 - neff**2),
                rk0 * sqrt(neff**2 - self.fiber.get_minimum_index(1, wavelength)**2))

    def _lpceq(self, neff, wavelength, nu):
        u, w = self._uw(wavelength, neff)
        return (u * jn(nu - 1, u) * kn(nu, w) +
                w * jn(nu, u) * kn(nu - 1, w))

    def _teceq(self, neff, wavelength, nu):
        u, w = self._uw(wavelength, neff)
        return u * j0(u) * k1(w) + w * j1(u) * k0(w)

    def _tmceq(self, neff, wavelength, nu):
        u, w = self._uw(wavelength, neff)
        nco = self.fiber.get_maximum_index(0, wavelength)
        ncl = self.fiber.get_minimum_index(1, wavelength)
        return (u * j0(u) * k1(w) * ncl**2 +
                w * j1(u) * k0(w) * nco**2)

    def _heceq(self, neff, wavelength, nu):
        u, w = self._uw(wavelength, neff)
        v2 = u**2 + w**2
        nco = self.fiber.get_maximum_index(0, wavelength)
        ncl = self.fiber.get_minimum_index(1, wavelength)
        delta = (1 - ncl**2 / nco**2) / 2
        jnu = jn(nu, u)
        knu = kn(nu, w)
        kp = kvp(nu, w)

        return (jvp(nu, u) * w * knu +
                kp * u * jnu * (1 - delta) +
                jnu * sqrt((u * kp * delta)**2 +
                           ((nu * neff * v2 * knu) /
                            (nco * u * w))**2))

    def _ehceq(self, neff, wl, nu):
        u, w = self._uw(wl, neff)
        v2 = u**2 + w**2
        nco = self.fiber.get_maximum_index(0, wl)
        ncl = self.fiber.get_minimum_index(1, wl)
        delta = (1 - ncl**2 / nco**2) / 2
        jnu = jn(nu, u)
        knu = kn(nu, w)
        kp = kvp(nu, w)

        return (jvp(nu, u) * w * knu +
                kp * u * jnu * (1 - delta) -
                jnu * sqrt((u * kp * delta)**2 +
                           ((nu * neff * v2 * knu) /
                            (nco * u * w))**2))
