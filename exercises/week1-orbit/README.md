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
1. Run `week1_starter.py` in the terminal and read the summary it prints.
2. Create the file `week1.ipynb` in the `week1-orbit` directory, which will 
   open a Jupyter notebook. 
3. Open a code cell and run week1_starter.build_and_run(), assigning the output
   to a variable.
4. Add a line to call week1_starter.summarize() with the data you saved.
5. Plot the data using week1_starter.plot().
6. Work through the numbered TODOs at the bottom of the script. Write your
   answers in a `notes.md` in this folder; we'll compare as a group. Be 
   specific: say "Contact time drops to 22 minutes at 5 degree elevation",
   not simply "it went down."

> [!TIP]
> Imported Python modules are not reloaded automatically when edited (such as
> entering new values for your orbital parameters). If you change the 
> week1_starter.py module and don't reload it, your data won't change.
>
> To avoid confusion and frustration, add these lines at the top of
> your code cell.
>
> ```
> %load_ext autoreload
> %autoreload 2
> ```

## Done when
You can say, with numbers, how many minutes per day we can talk to the
satellite and what fraction of each orbit is dark — and explain what changes
when you move the altitude, the inclination, or the station's minimum
elevation.

## Think about
Passes are a few minutes long and there are a handful per day, often
clustered. What does that mean for how the satellite has to behave when
nobody is listening?
