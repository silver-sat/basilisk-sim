# Week 3 — Detumble

## Goal
The satellite leaves the deployer spinning a few degrees per second on every
axis. Bring it to rest using nothing but magnetorquers and a magnetometer.

## What you'll use
- `mtbEffector` — magnetic torque bars (coils) that push against Earth's field
- `magnetometer` — from last week
- A Python Basilisk module you write yourself: the B-dot control law.
  `week1-orbit/simple_earth_sun.py` shows the pattern (a class with
  `Reset` and `UpdateState` that reads and writes messages).

## Do this
1. Run the starter with the controller stubbed out and watch the tumble
   persist.
2. Implement B-dot: torque against the *rate of change* of the measured field.
   It is about ten lines.
3. Plot body rates over several orbits. How long does detumble take?
4. Break it: give the magnetometer a dead axis, then a large bias, and see
   what your controller does.

## Done when
Body rates fall below 0.1 deg/s from a 5 deg/s start, and you can say how
many orbits it took and why it can't be faster.

## Think about
Why does the rate drop faster on some axes than others? What would the
flight software need to check before deciding "detumble is finished"?
