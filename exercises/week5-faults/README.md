# Week 5 — Things break

## Goal
Real flight software is mostly mode logic and fault handling, not control
math. Take last week's pointing sim, wrap it in a mode manager, and then
break things on purpose.

## What you'll use
- Everything from weeks 1–4
- A Python mode manager you write: detumble → safe/sun-point → nominal, with
  rules for moving between them
- Basilisk's Monte Carlo support for running many cases at once

## Do this
1. Write the mode manager. Start in detumble from a tumbling state and let it
   promote itself to nominal pointing when it is safe to.
2. Inject faults, one at a time: sun sensors go dark (eclipse), a torquer
   sticks on, the magnetometer reports stale values, a wheel stops.
3. For each fault, decide what the satellite *should* do and make it happen.
4. Run a small Monte Carlo over initial tumble rates and sensor biases. Does
   the satellite always end up in nominal mode? How long does it take?

## Done when
You have a mode-transition diagram, a table of faults with the response you
chose, and a Monte Carlo plot showing time-to-nominal across many runs.

## Think about
Which of these decisions can the satellite make alone, and which need a
human in the loop — given what you learned in Week 1 about how rarely we can
talk to it?
