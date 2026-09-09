#!/usr/bin/env python3
"""
smoke_test.py -- verify the Basilisk install in the SilverSat codespace.

Builds the smallest useful simulation: one spacecraft in a SilverSat-like
500 km circular orbit under Earth point-mass gravity, propagated for one
orbit. Checks the integrated position against the analytic two-body solution
and that nothing in the import/build/run chain is broken.

Run:  python smoke_test.py
Exit status 0 on success, 1 on failure, so it can also be used in CI.
"""

import sys
import time

import numpy as np

try:
    from Basilisk import __path__ as bsk_path
    from Basilisk.simulation import spacecraft
    from Basilisk.utilities import (
        SimulationBaseClass,
        macros,
        orbitalMotion,
        simIncludeGravBody,
    )
except ImportError as exc:
    print(f"FAIL: could not import Basilisk ({exc})")
    print("      Is the 'bsk' package installed?  pip install \"bsk[all,examples]\"")
    sys.exit(1)

ORBIT_ALT_KM = 500.0          # SilverSat-ish altitude
CHECK_TOL_KM = 1.0            # allowed error vs. analytic two-body solution


def build_and_run():
    # --- simulation skeleton -------------------------------------------------
    sim = SimulationBaseClass.SimBaseClass()
    process = sim.CreateNewProcess("dynamicsProcess")
    dt = macros.sec2nano(10.0)                          # 10 s integration step
    process.addTask(sim.CreateNewTask("dynamicsTask", dt))

    # --- spacecraft ----------------------------------------------------------
    sc = spacecraft.Spacecraft()
    sc.ModelTag = "silversat"
    sc.hub.mHub = 4.0                                   # kg, roughly a 3U
    sc.hub.IHubPntBc_B = [[0.04, 0, 0], [0, 0.04, 0], [0, 0, 0.01]]
    sim.AddModelToTask("dynamicsTask", sc)

    # --- gravity -------------------------------------------------------------
    grav = simIncludeGravBody.gravBodyFactory()
    earth = grav.createEarth()
    earth.isCentralBody = True
    grav.addBodiesTo(sc)

    # --- initial orbit (500 km circular, ~ISS-like inclination) -------------
    oe = orbitalMotion.ClassicElements()
    oe.a = earth.radEquator + ORBIT_ALT_KM * 1000.0
    oe.e = 0.0005
    oe.i = 51.6 * macros.D2R
    oe.Omega = 30.0 * macros.D2R
    oe.omega = 0.0
    oe.f = 0.0
    r0, v0 = orbitalMotion.elem2rv(earth.mu, oe)
    sc.hub.r_CN_NInit = r0
    sc.hub.v_CN_NInit = v0
    period = 2 * np.pi * np.sqrt(oe.a ** 3 / earth.mu)

    # --- logging -------------------------------------------------------------
    log = sc.scStateOutMsg.recorder(macros.sec2nano(60.0))
    sim.AddModelToTask("dynamicsTask", log)

    # --- run one orbit -------------------------------------------------------
    sim.InitializeSimulation()
    sim.ConfigureStopTime(macros.sec2nano(period))
    t0 = time.perf_counter()
    sim.ExecuteSimulation()
    wall = time.perf_counter() - t0

    r_hist = np.array(log.r_BN_N)
    t_hist = np.array(log.times()) * macros.NANO2SEC

    # analytic two-body position at the final logged time
    n = np.sqrt(earth.mu / oe.a ** 3)
    M = n * t_hist[-1]
    E = orbitalMotion.M2E(M, oe.e)
    oe_end = orbitalMotion.ClassicElements()
    oe_end.a, oe_end.e, oe_end.i = oe.a, oe.e, oe.i
    oe_end.Omega, oe_end.omega = oe.Omega, oe.omega
    oe_end.f = orbitalMotion.E2f(E, oe.e)
    r_expected, _ = orbitalMotion.elem2rv(earth.mu, oe_end)
    return r_expected, r_hist, period, wall


def main():
    print(f"Basilisk import OK  ({bsk_path[0]})")
    r_expected, r_hist, period, wall = build_and_run()

    err_km = np.linalg.norm(r_hist[-1] - r_expected) / 1000.0
    alt_km = (np.linalg.norm(r_hist, axis=1).min() - 6378.1363e3) / 1000.0

    print(f"Orbit period      : {period / 60:.1f} min")
    print(f"Logged samples    : {len(r_hist)}")
    print(f"Min altitude      : {alt_km:.1f} km")
    print(f"Error vs. Kepler  : {err_km:.3f} km after one orbit")
    print(f"Wall-clock time   : {wall:.2f} s")

    if not np.all(np.isfinite(r_hist)):
        print("FAIL: non-finite state in trajectory")
        return 1
    if err_km > CHECK_TOL_KM:
        print(f"FAIL: error {err_km:.3f} km exceeds {CHECK_TOL_KM} km")
        return 1

    print("PASS: Basilisk is ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
