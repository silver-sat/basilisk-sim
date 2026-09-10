#!/usr/bin/env python3
"""
Week 1 -- Where am I, and when can I talk?

Propagate a SilverSat-like orbit for one day and find out:
  * how much of each orbit is spent in Earth's shadow (no sun = no power), and
  * when the satellite is above our ground station (the only time we can talk).

Run it as-is first:   python week1_starter.py
Then work through the TODOs at the bottom of this file.

Everything you need is already here. The structure is the same one every
Basilisk simulation uses:

    build the sim -> add models -> wire messages -> add recorders -> run -> plot
"""

import numpy as np
import matplotlib.pyplot as plt

from Basilisk.simulation import spacecraft, groundLocation, eclipse
from simple_earth_sun import SimpleEarthSun
from Basilisk.architecture import astroConstants
from Basilisk.utilities import (
    SimulationBaseClass,
    macros,
    orbitalMotion,
    simIncludeGravBody,
)

# ---------------------------------------------------------------------------
# Parameters you will be asked to change. Start with these.
# ---------------------------------------------------------------------------
ALTITUDE_KM      = 500.0                  # circular orbit altitude
INCLINATION_DEG  = 51.6                   # 51.6 is ISS-like; SilverSat 1 was deployed from the ISS
START_TIME_UTC   = "2026 SEP 21 12:00:00 (UTC)"
SIM_DURATION_H   = 24.0

"""
We will use Silver Spring, MD as the ground-station coordinates for this exercise. For the flight,
we'll use the location of the ground station.
"""

GS_NAME          = "SilverSat ground station"
GS_LAT_DEG       = 39.00                  # placeholder: Silver Spring, MD
GS_LON_DEG       = -77.03
GS_ALT_M         = 100.0
GS_MIN_ELEV_DEG  = 10.0                   # below this the antenna can't see us

STEP_S           = 10.0                   # integration and logging step


def build_and_run(altitude_km=None, inclination_deg=None, duration_h=None,
                  gs_lat_deg=None, gs_lon_deg=None, gs_min_elev_deg=None):
    altitude_km     = ALTITUDE_KM     if altitude_km     is None else altitude_km
    inclination_deg = INCLINATION_DEG if inclination_deg is None else inclination_deg
    duration_h      = SIM_DURATION_H  if duration_h      is None else duration_h
    gs_lat_deg      = GS_LAT_DEG      if gs_lat_deg      is None else gs_lat_deg
    gs_lon_deg      = GS_LON_DEG      if gs_lon_deg      is None else gs_lon_deg
    gs_min_elev_deg = GS_MIN_ELEV_DEG if gs_min_elev_deg is None else gs_min_elev_deg
    """Build the simulation, run it, and return the logged data as a dict."""

    # --- 1. simulation skeleton ---------------------------------------------
    sim = SimulationBaseClass.SimBaseClass()
    proc = sim.CreateNewProcess("dynProcess")
    dt = macros.sec2nano(STEP_S)
    proc.addTask(sim.CreateNewTask("dynTask", dt))

    # --- 2. spacecraft -------------------------------------------------------
    sc = spacecraft.Spacecraft()
    sc.ModelTag = "silversat"
    sc.hub.mHub = 4.0                                        # kg
    sc.hub.IHubPntBc_B = [[0.04, 0, 0], [0, 0.04, 0], [0, 0, 0.01]]  # kg m^2

    # --- 3. gravity, plus Earth rotation and Sun direction -------------------
    grav = simIncludeGravBody.gravBodyFactory()
    earth = grav.createEarth()
    earth.isCentralBody = True
    grav.addBodiesTo(sc)
    sim.AddModelToTask("dynTask", sc, 1)

    # Where is the Sun, and which way has Earth turned? (see simple_earth_sun.py)
    ephem = SimpleEarthSun(START_TIME_UTC)
    ephem.ModelTag = "earthSun"
    earthMsg = ephem.earthOutMsg
    sunMsg   = ephem.sunOutMsg
    sim.AddModelToTask("dynTask", ephem, 2)      # priority 2: runs before the spacecraft

    # --- 4. initial orbit ----------------------------------------------------
    oe = orbitalMotion.ClassicElements()
    oe.a = astroConstants.REQ_EARTH * 1e3 + altitude_km * 1e3
    oe.e = 0.0005
    oe.i = inclination_deg * macros.D2R
    oe.Omega = 40.0 * macros.D2R
    oe.omega = 0.0
    oe.f = 0.0
    r0, v0 = orbitalMotion.elem2rv(earth.mu, oe)
    sc.hub.r_CN_NInit = r0
    sc.hub.v_CN_NInit = v0
    period_s = 2 * np.pi * np.sqrt(oe.a ** 3 / earth.mu)

    # --- 5. eclipse model ----------------------------------------------------
    ecl = eclipse.Eclipse()
    ecl.ModelTag = "eclipse"
    ecl.addSpacecraftToModel(sc.scStateOutMsg)
    ecl.addPlanetToModel(earthMsg)
    ecl.sunInMsg.subscribeTo(sunMsg)
    sim.AddModelToTask("dynTask", ecl)

    # --- 6. ground station ---------------------------------------------------
    gs = groundLocation.GroundLocation()
    gs.ModelTag = "groundStation"
    gs.planetRadius = astroConstants.REQ_EARTH * 1e3
    gs.specifyLocation(np.radians(gs_lat_deg), np.radians(gs_lon_deg), GS_ALT_M)
    gs.planetInMsg.subscribeTo(earthMsg)
    gs.minimumElevation = np.radians(gs_min_elev_deg)
    gs.maximumRange = 1e9
    gs.addSpacecraftToModel(sc.scStateOutMsg)
    sim.AddModelToTask("dynTask", gs)

    # --- 7. recorders (these are what we plot) -------------------------------
    scLog  = sc.scStateOutMsg.recorder()
    eclLog = ecl.eclipseOutMsgs[0].recorder()
    gsLog  = gs.accessOutMsgs[0].recorder()
    for log in (scLog, eclLog, gsLog):
        sim.AddModelToTask("dynTask", log)

    # --- 8. run --------------------------------------------------------------
    sim.InitializeSimulation()
    sim.ConfigureStopTime(macros.hour2nano(duration_h))
    sim.ExecuteSimulation()

    t = np.array(scLog.times()) * macros.NANO2SEC
    return {
        "t_s":        t,
        "r_N":        np.array(scLog.r_BN_N),          # position, m, inertial
        "shadow":     np.array(eclLog.shadowFactor),   # 1 = full sun, 0 = full shadow
        "access":     np.array(gsLog.hasAccess),       # 1 when above min elevation
        "elev_deg":   np.degrees(gsLog.elevation),
        "range_km":   np.array(gsLog.slantRange) / 1e3,
        "period_s":   period_s,
        "min_elev_deg": gs_min_elev_deg,
    }


# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------
def find_intervals(flag, t):
    """Return a list of (t_start, t_end) for each run where flag is truthy."""
    flag = np.asarray(flag).astype(bool)
    edges = np.diff(flag.astype(int))
    starts = np.where(edges == 1)[0] + 1
    ends   = np.where(edges == -1)[0] + 1
    if flag[0]:
        starts = np.r_[0, starts]
    if flag[-1]:
        ends = np.r_[ends, len(flag) - 1]
    return list(zip(t[starts], t[ends]))


def summarize(d):
    t, period = d["t_s"], d["period_s"]
    print(f"Orbit period       : {period / 60:.1f} min  ({24 * 3600 / period:.1f} orbits/day)")

    eclipses = find_intervals(d["shadow"] < 0.5, t)
    ecl_total = sum(e - s for s, e in eclipses)
    print(f"Eclipses           : {len(eclipses)} in 24 h, "
          f"avg {ecl_total / max(len(eclipses), 1) / 60:.1f} min each, "
          f"{100 * ecl_total / t[-1]:.0f}% of the day in shadow")

    passes = find_intervals(d["access"] > 0.5, t)
    print(f"Ground passes      : {len(passes)} above {d['min_elev_deg']:.0f} deg elevation")
    print("   #   start (h)   length (min)   max elev (deg)   min range (km)")
    for k, (s, e) in enumerate(passes, 1):
        m = (t >= s) & (t <= e)
        print(f"  {k:2d}   {s / 3600:7.2f}     {(e - s) / 60:6.1f}         "
              f"{d['elev_deg'][m].max():6.1f}          {d['range_km'][m].min():7.0f}")
    print(f"Total contact time : {sum(e - s for s, e in passes) / 60:.1f} min per day")


def plot(d, save_as="week1.png"):
    t_h = d["t_s"] / 3600.0
    fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    ax[0].plot(t_h, np.linalg.norm(d["r_N"], axis=1) / 1e3 - astroConstants.REQ_EARTH)
    ax[0].set_ylabel("altitude (km)")

    ax[1].fill_between(t_h, 0, 1 - d["shadow"], step="mid", alpha=0.6, label="in shadow")
    ax[1].set_ylabel("eclipse")
    ax[1].set_ylim(0, 1.1)
    ax[1].legend(loc="upper right")

    ax[2].plot(t_h, d["elev_deg"], lw=0.8)
    ax[2].axhline(d['min_elev_deg'], color="r", ls="--", lw=0.8, label="min elevation")
    ax[2].fill_between(t_h, -90, 90, where=d["access"] > 0.5, alpha=0.2, label="in contact")
    ax[2].set_ylim(-90, 90)
    ax[2].set_ylabel("elevation (deg)")
    ax[2].set_xlabel("time (hours)")
    ax[2].legend(loc="upper right")

    fig.suptitle(f"{ALTITUDE_KM:.0f} km, {INCLINATION_DEG:.1f} deg orbit vs. {GS_NAME}")
    fig.tight_layout()
    fig.savefig(save_as, dpi=120)
    print(f"Saved {save_as}")
    return fig


if __name__ == "__main__":
    data = build_and_run()
    summarize(data)
    plot(data)
    plt.show()

# ---------------------------------------------------------------------------
# TODOs -- do these in order, in a notebook or by editing the constants above.
# Write down what you find; we'll compare answers as a group.
#
# 1. Run the script and read the pass table. How many minutes a day can we
#    actually talk to the satellite? Is that more or less than you expected?
#
# 2. Change GS_MIN_ELEV_DEG to 5 and then 20. How much contact time do we gain
#    or lose? (Real antennas near buildings and trees rarely see below ~10 deg.)
#
# 3. Change ALTITUDE_KM to 400 and to 600. What happens to the orbit period,
#    the eclipse length, and the passes? Which altitude would you pick for
#    talking, and which for staying up longer? (Hint: SilverSat 1 reentered.)
#
# 4. Change INCLINATION_DEG to 97.5 (a polar, sun-synchronous-ish orbit). How
#    do the passes change? Why?
#
# 5. Stretch: the eclipse fraction changes through the year. Change
#    START_TIME_UTC to a date in June and one in December and compare.
#    (Ask: what does the flight software need to know about this?)
#
# 6. Stretch: build_and_run() accepts arguments. Write a loop that runs it for
#    several altitudes and plots contact minutes per day vs. altitude.
# ---------------------------------------------------------------------------
