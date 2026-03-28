---
layout: default
title: Contributing a Simulation
parent: KiCad Simulation Examples
nav_order: 4
---

Thanks for helping expand the KiCad Simulation Examples library. This site is built directly
from the contents of each simulation folder, so a clean structure and a clear README are the
most important parts of a good contribution.

## Required Files

Each simulation must live under `simulations/<name>/` and include:

- `*.kicad_sch` schematic (single file preferred, name matches the folder if multiple)
- `README.md` with a single H1 title and a short first paragraph
- Any required SPICE models (`.lib`, `.spice`, etc.) stored alongside the schematic

## README Template

Use this as a starting point for each simulation README:

```markdown
# Title of Simulation

One short paragraph describing the goal of the simulation.

## Circuit Summary

Describe the topology and the key components.

## Expected Behavior

Explain what plots or behaviors to look for when running the simulation.

## How To Run

1. Open `<schematic>.kicad_sch` in KiCad.
2. Click `Simulate` and run the configured analyses.
3. Add probes for the key nodes to view expected behavior.

## Notes

Any modeling assumptions, limitations, or tips.
```

## Naming

- Use lowercase kebab-case for folder names (for example: `rc-lowpass`).
- Keep names short but descriptive.

## Assets

Schematics are rendered in CI. If you need additional images or plots, include them in the
README with relative paths under the same simulation directory.
