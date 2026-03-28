# RC Lowpass

Demonstrates a first-order RC low-pass filter.

## Circuit Summary

A series resistor feeds a capacitor to ground; the output is across the capacitor.

## Expected Behavior

- AC sweep shows a -3 dB cutoff at 1/(2πRC).
- Transient response smooths fast edges.

## How To Run

1. Open `RC-Lowpass.kicad_sch` in KiCad.
2. Click `Simulate` and run the configured analyses.
3. Add probes to the key nodes to view the expected behavior.

## Notes

- Increase R or C to lower the cutoff frequency.
