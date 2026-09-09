# Week 2 — Sensors lie

## Goal
Give a tumbling satellite the same sensors SilverSat 2 will fly — a
magnetometer, sun sensors, and a gyro — with realistic noise and bias, and
then work out which way it is pointing from their readings alone.

## What you'll use
- `magneticFieldWMM` — Earth's magnetic field along the orbit
- `magnetometer` — a noisy, biased measurement of that field
- `coarseSunSensor` — photodiodes that see the Sun (when it's not eclipsed)
- `imuSensor` — a gyro with drift
- Your own Python: the TRIAD algorithm to turn two vectors into an attitude

## Do this
1. Run the starter and plot the raw sensor outputs against the true values.
   Look at what noise and bias actually do to the signal.
2. Implement TRIAD using the magnetometer and sun-sensor vectors, and compare
   your attitude estimate to the truth from the simulation.
3. Watch what happens in eclipse.

## Done when
You have an attitude-error plot for a full orbit and can explain every place
it gets worse.

## Think about
Which sensor limits your accuracy? What would you do during eclipse? What
happens if the magnetometer is mounted 2 degrees off from where you think?
