# NMOS Amplifier Cs

Shows the gain and inversion of a common-source NMOS amplifier.

## Circuit Summary

A bias network sets the NMOS operating point, with a drain resistor converting current changes to voltage.

## Expected Behavior

- Small-signal output is inverted relative to the input.
- Gain depends on bias point and drain resistor value.

## How To Run

1. Open `NMOS-Amplifier-CS.kicad_sch` in KiCad.
2. Click `Simulate` and run the configured analyses.
3. Add probes to the key nodes to view the expected behavior.

## Notes

- Sweep the gate bias to explore linear vs. cutoff regions.
