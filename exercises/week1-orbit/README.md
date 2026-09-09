# Week 1 — Where am I, and when can I talk?

## Goal
Propagate a SilverSat-like orbit for one day and answer two questions the
flight software will care about every single orbit:

- When is the satellite in Earth's shadow? (No sun means no solar power.)
- When is it above our ground station? (The only time we can send commands
  or get data down.)

## What you'll use
- `spacecraft` — the satellite's position, velocity and attitude
- `eclipse` — is the Sun blocked by Earth right now?
- `groundLocation` — is the satellite above the horizon at our station?
- `simple_earth_sun.py` — a small helper that tells the sim where the Sun is
  and how far Earth has rotated (you don't need to read it this week)

## Do this
1. Run `python week1_starter.py` and read the summary it prints.
2. Open `week1.png` (or run it in a notebook to see the plots inline).
3. Work through the numbered TODOs at the bottom of the script. Write your
   answers in a `notes.md` in this folder; we'll compare as a group.

## Done when
You can say, with numbers, how many minutes per day we can talk to the
satellite and what fraction of each orbit is dark — and explain what changes
when you move the altitude, the inclination, or the station's minimum
elevation.

## Think about
Passes are a few minutes long and there are a handful per day, often
clustered. What does that mean for how the satellite has to behave when
nobody is listening?
