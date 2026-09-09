"""
simple_earth_sun.py -- a tiny stand-in for SPICE.

Basilisk normally gets planet positions and Earth's rotation from NASA's
SPICE kernels (about 120 MB of downloads). For these exercises we only need
two things over the course of a day, and both have simple formulas:

  * Earth's rotation angle (Greenwich sidereal time), so the ground station
    moves under the orbit correctly, and
  * the direction to the Sun, so we know when the satellite is in shadow.

This file is also your first look at a *Python Basilisk module*: a class that
inherits from SysModel, gets called by the simulation every time step, and
writes messages that other modules read. Week 3's control law will use the
same pattern.

You don't need to read this to do Week 1. Come back to it in Week 3.
"""

import numpy as np

from Basilisk.architecture import sysModel, messaging

AU_M = 1.495978707e11
EARTH_ROT_RATE = 7.2921150e-5          # rad/s
OBLIQUITY = np.radians(23.439)


def _julian_date(year, month, day, hour=0.0, minute=0.0, second=0.0):
    """Julian date of a UTC calendar time (Meeus, good to a second here)."""
    if month <= 2:
        year -= 1
        month += 12
    a = year // 100
    b = 2 - a + a // 4
    jd = (int(365.25 * (year + 4716)) + int(30.6001 * (month + 1))
          + day + b - 1524.5)
    return jd + (hour + minute / 60.0 + second / 3600.0) / 24.0


def parse_utc(s):
    """'2026 SEP 21 12:00:00' -> Julian date."""
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
              "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    parts = s.replace("(UTC)", "").split()
    y, m, d = int(parts[0]), months.index(parts[1].upper()) + 1, int(parts[2])
    h, mi, se = (int(x) for x in parts[3].split(":"))
    return _julian_date(y, m, d, h, mi, se)


def gmst_rad(jd):
    """Greenwich mean sidereal time as an angle, from Julian date."""
    t = (jd - 2451545.0) / 36525.0
    gmst_s = (67310.54841 + (876600.0 * 3600 + 8640184.812866) * t
              + 0.093104 * t**2 - 6.2e-6 * t**3)
    return np.radians((gmst_s / 240.0) % 360.0)


def sun_direction_j2000(jd):
    """Unit vector from Earth to the Sun in the J2000 frame (low-precision,
    ~0.01 deg, from the Astronomical Almanac)."""
    n = jd - 2451545.0
    L = np.radians((280.460 + 0.9856474 * n) % 360.0)      # mean longitude
    g = np.radians((357.528 + 0.9856003 * n) % 360.0)      # mean anomaly
    lam = L + np.radians(1.915) * np.sin(g) + np.radians(0.020) * np.sin(2 * g)
    return np.array([np.cos(lam),
                     np.cos(OBLIQUITY) * np.sin(lam),
                     np.sin(OBLIQUITY) * np.sin(lam)])


class SimpleEarthSun(sysModel.SysModel):
    """Publishes Earth (at the origin, rotating) and Sun planet-state messages."""

    def __init__(self, start_utc):
        super().__init__()
        self.jd0 = parse_utc(start_utc)
        self.earthOutMsg = messaging.SpicePlanetStateMsg()
        self.sunOutMsg = messaging.SpicePlanetStateMsg()

    def Reset(self, CurrentSimNanos):
        self.UpdateState(CurrentSimNanos)

    def UpdateState(self, CurrentSimNanos):
        t = CurrentSimNanos * 1.0e-9
        jd = self.jd0 + t / 86400.0

        # --- Earth: fixed at the origin, rotating about +z --------------------
        th = gmst_rad(jd)
        c, s = np.cos(th), np.sin(th)
        dcm = [[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]]      # J2000 -> Earth-fixed
        w = EARTH_ROT_RATE
        dcm_dot = [[-s * w, c * w, 0.0], [-c * w, -s * w, 0.0], [0.0, 0.0, 0.0]]

        earth = messaging.SpicePlanetStateMsgPayload()
        earth.PlanetName = "earth"
        earth.PositionVector = [0.0, 0.0, 0.0]
        earth.VelocityVector = [0.0, 0.0, 0.0]
        earth.J20002Pfix = dcm
        earth.J20002Pfix_dot = dcm_dot
        earth.computeOrient = 1
        self.earthOutMsg.write(earth, CurrentSimNanos, self.moduleID)

        # --- Sun: 1 AU away in the current sun direction -----------------------
        sun = messaging.SpicePlanetStateMsgPayload()
        sun.PlanetName = "sun"
        sun.PositionVector = (AU_M * sun_direction_j2000(jd)).tolist()
        sun.VelocityVector = [0.0, 0.0, 0.0]
        sun.J20002Pfix = np.eye(3).tolist()
        sun.J20002Pfix_dot = np.zeros((3, 3)).tolist()
        sun.computeOrient = 0
        self.sunOutMsg.write(sun, CurrentSimNanos, self.moduleID)
