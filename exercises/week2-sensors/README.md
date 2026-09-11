# Week 2 — Sensors lie

## Goal
Last week the simulation told us exactly where the satellite was. The real
satellite doesn't get that. It gets a handful of noisy readings and has to
work out for itself which way the sun is, whether it's in the dark, and how
fast it's spinning.

You'll write four small pieces of that software.

## What you'll use
- Six **coarse sun sensors** — photodiodes on each face, brighter the more
  directly they face the sun
- A **magnetometer** — measures Earth's magnetic field
- A **gyro** — measures how fast the satellite is spinning
- Your own Python, in `week2_starter.py`

## Do this
1. Run `python week2_starter.py`. It works, plots the sensors, and reports
   that all four tasks are unwritten. Look at the plot first.
2. Do the tasks in order. Each is a function near the top of the file with a
   `TODO` and a sketch of the answer. Run the file after each one — it
   checks your work and prints how you did.
   - **Task A** — which way is the sun?
   - **Task B** — am I in the dark? (and how to stop the answer flickering)
   - **Task C** — can I trust the gyro?
   - **Task D** (stretch) — smoothing a noisy signal
3. Answer the questions at the bottom of the file in a `notes.md`.

The only math you need: subtraction, division, square root, comparison, and
adding up a list.

## Done when
All four checks report sensible numbers, and you can explain — without
looking at the code — why the gyro is useless after a few minutes and why
the sun sensors are useless for a third of every orbit.

## Think about
Every sensor here fails in some situation. The magnetometer is the only one
that works everywhere. Keep that in mind next week, when you have to detumble
the satellite with nothing else to go on.
