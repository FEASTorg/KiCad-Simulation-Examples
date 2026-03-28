---
layout: default
title: Introduction to Simulation in KiCad
parent: KiCad Simulation Examples
nav_order: 2
---

KiCad includes an embedded circuit simulator that uses ngspice as its simulation engine and
exposes simulation through the schematic editor UI. You build a simulation schematic, assign
models to symbols, and run analyses to plot results.

## What KiCad’s Simulator Is

- **A graphical front end to ngspice**: KiCad integrates the open‑source ngspice engine and
  provides simulation tools directly in the schematic editor.
- **Schematic‑driven**: You can run simulations from standard KiCad schematics once models
  are assigned and simulation directives are configured.

## Core Analysis Types

KiCad’s simulator exposes the standard ngspice analysis modes most commonly used in
teaching and design:

- **Operating Point (OP)**
- **DC Sweep / DC Transfer**
- **AC Sweep**
- **Transient**

Custom analysis directives are also supported for advanced use cases.

## Practical Tips and Common Pitfalls

- **Assign models before running**: KiCad ships SPICE‑oriented symbols, but you still need
  to attach appropriate SPICE models for many devices.
- **Use probes or save settings**: If you don’t save all voltages/currents, you must probe
  or explicitly save the signals you want to plot.
- **Bring your own third‑party models**: KiCad doesn’t bundle commercial SPICE libraries,
  but you can use manufacturer‑supplied models.

## References

- KiCad Simulation (official overview):
  - https://www.kicad.org/discover/spice/
- ngspice User’s Manual:
  - http://ngspice.sourceforge.net/docs/ngspice-manual.pdf
