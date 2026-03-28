# NPN Amplifier Ce

Shows the gain and inversion of a common-emitter NPN amplifier.

## Circuit Summary

A bias network sets the transistor operating point, with a collector resistor producing voltage gain.

## Expected Behavior

- Output is inverted relative to the input.
- Gain changes with collector resistor and emitter degeneration.

## How To Run

1. Open `NPN-Amplifier-CE.kicad_sch` in KiCad.
2. Click `Simulate` and run the configured analyses.
3. Add probes to the key nodes to view the expected behavior.

## Notes

- Check bias stability by varying beta in the model.
