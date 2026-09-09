# Week 4 — Point at something and keep pointing

## Goal
Hold a commanded attitude (sun-pointing for power, or nadir for a camera)
and keep holding it while the disturbances that never stop try to push the
satellite off.

## What you'll use
- `reactionWheelStateEffector` — reaction wheels (if SilverSat 2 flies them)
  or `mtbEffector` alone (if not — we'll decide before this week)
- `mrpFeedback` — Basilisk's standard attitude controller
- `mtbMomentumManagement` — using torquers to unload the wheels
- Disturbances: gravity gradient, aerodynamic drag, residual magnetic dipole

## Do this
1. Command sun-pointing and plot pointing error over an orbit.
2. Add disturbances and watch reaction-wheel momentum grow.
3. Add momentum management and watch it stop growing.
4. Tune the controller gains. Find the point where it goes unstable.

## Done when
Pointing error stays under 5 degrees for a full day with wheel speeds staying
inside their limits.

## Think about
Two actuators had to cooperate for the "easy" case. Which one is in charge?
What if the wheels are off and only torquers remain — what pointing accuracy
can you get?
