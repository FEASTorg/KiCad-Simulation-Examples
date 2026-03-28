# Actuator PNP Switch LED

This example shows a PNP transistor used as a high-side switch to drive an LED load.

## Circuit Summary

The PNP emitter sits at VCC while the collector feeds an LED and resistor to ground.

## Expected Behavior

- LED turns on as the base is pulled below the emitter by ~0.7 V.
- Collector voltage rises toward VCC when the transistor saturates.

## How To Run

1. Open `Actuator-PNP-switch-LED.kicad_sch` in KiCad.
2. Click `Simulate` and run the configured analyses.
3. Add probes to the key nodes to view the expected behavior.

## Notes

- Base drive must pull low enough to turn the PNP fully on.
