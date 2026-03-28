# Actuator NPN Switch LED

This example shows an NPN transistor used as a low-side switch to drive an LED load.

## Circuit Summary

A base resistor controls the NPN transistor, sinking current from an LED and series resistor tied to VCC.

## Expected Behavior

- LED current rises sharply once V_BE exceeds ~0.7 V.
- Collector voltage drops near ground when the transistor saturates.

## How To Run

1. Open `Actuator-NPN-switch-LED.kicad_sch` in KiCad.
2. Click `Simulate` and run the configured analyses.
3. Add probes to the key nodes to view the expected behavior.

## Notes

- Compare base current to LED current to see saturation margin.
