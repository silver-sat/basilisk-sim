# basilisk-sim
Basilisk simulation for SilverSat 2 — Satellite Simulator Exercises

This repository is the home for the SilverSat 2 simulation exercises. Over a
few weeks we will use [Basilisk](https://avslab.github.io/basilisk/), an
open-source spacecraft simulation framework from CU Boulder, to get a feel for
the problems our flight software has to solve before we write it for real:
knowing where the satellite is, figuring out which way it is pointing,
controlling that, and coping when sensors and actuators misbehave.

Everything runs in the cloud in a GitHub Codespace. You do not need to
install anything on your laptop.

## Getting started

1. Make sure you have a GitHub account and have accepted the invitation to the
   Silver-Sat organization.
2. On this repository's page, click the green **Code** button, choose the
   **Codespaces** tab, and click **Create codespace on main**.
3. Wait for VS Code to open in your browser (usually under a minute). A
   terminal appears at the bottom; if it doesn't, use **Terminal → New
   Terminal**.
4. In the terminal, run:

   ```
   python smoke_test.py
   ```

   You should see a few lines of output ending in `PASS: Basilisk is ready.`
   If you see anything else, tell a mentor.

That's it. Your codespace keeps your files between sessions; the next time
you open the repo, choose the existing codespace rather than creating a new
one.

### Prefer the desktop app?

The browser version is full VS Code, and it's what the exercises assume. If
you already use VS Code on your laptop and want to keep your shortcuts, install
the **GitHub Codespaces** extension, sign in, and open the same codespace from
there. Nothing else changes.

## What's in the repo

| Path | What it is |
|---|---|
| `smoke_test.py` | A minimal one-orbit simulation that confirms Basilisk works. Also a good first read: every exercise uses the same skeleton. |
| `exercises/` | One folder per week. Each has a starter script, a short README describing the goal, and a place for your work. |
| `.devcontainer/` | The definition of the cloud environment. Mentors maintain this. |
| `README.md` | This document. |
| `.gitignore` | Reduces repository clutter for temporary and work files. |
| `LICENSE` | SilverSat open sources our code. |

## The exercises

Each week builds on the last. Details are in each folder's README.

1. **Where am I, and when can I talk?** Propagate a SilverSat-like orbit for a
   day and plot eclipse periods and ground-station passes.
2. **Sensors lie.** Add a magnetometer, sun sensors, and a gyro with realistic
   noise, then work out attitude from their readings and compare to truth.
3. **Detumble.** Bring a tumbling satellite to rest using only magnetorquers.
4. **Point at something and keep pointing.** Hold a target attitude and deal
   with the momentum that builds up.
5. **Things break.** Add a mode manager and see what happens when sensors drop
   out or an actuator sticks.

## Working in Basilisk

- Basilisk simulations are Python scripts. Run them from the terminal with
  `python yourscript.py`, or paste the code into a Jupyter notebook to get
  plots inline. The notebook route is usually easier for plotting.
- Scripts that call `plt.show()` won't pop up a window in the cloud. Either
  use a notebook, or save figures with `plt.savefig("name.png")` and open the
  PNG in the editor.
- The [Basilisk documentation](https://avslab.github.io/basilisk/) has a page
  for every module. The **Examples** section is the fastest way to see how
  something is wired up.

## Saving your work

Your codespace is yours, but it is not backed up. Commit and push regularly:

```
git add .
git commit -m "Week 2: completed tasks"
git push
```

Work in a branch named after you (`git switch -c yourname`) so that pushes
don't collide with other students. Mentors will show you how to open a pull
request when you have something to share.

## Codespace housekeeping

- Keep **one** codespace for this repo. Extra ones use up your storage quota.
- Codespaces pause after 30 minutes idle and resume where you left off.
- If something is badly broken, **Command Palette → Codespaces: Rebuild
  Container** gives you a fresh environment without losing committed work.
- Free accounts get 60 hours a month on the default machine. That is plenty
  for our sessions plus some time at home, but don't leave a simulation
  running overnight.

## Getting help

Ask in the SilverSat channel, use email, or grab a mentor during a session. If Basilisk
itself does something surprising, the project's
[GitHub Discussions](https://github.com/AVSLab/basilisk/discussions) are
friendly and searchable.
