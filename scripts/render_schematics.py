#!/usr/bin/env python3
"""
Render schematic images for each simulation using KiBot.

Outputs:
  docs/assets/simulations/<sim>/schematic.svg
  docs/assets/simulations/<sim>/schematic.png
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIM_ROOT = ROOT / "simulations"
OUT_ROOT = ROOT / "docs" / "assets" / "simulations"
KIBOT_CFG = ROOT / "kibot" / "schematic-export.kibot.yaml"


def die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def pick_schematic(sim_dir: Path) -> Path:
    sch_files = sorted(sim_dir.glob("*.kicad_sch"))
    if not sch_files:
        die(f"no .kicad_sch found in {sim_dir}")
    if len(sch_files) == 1:
        return sch_files[0]
    for sch in sch_files:
        if sch.stem == sim_dir.name:
            return sch
    names = ", ".join(p.name for p in sch_files)
    die(f"multiple schematics in {sim_dir}, none matching dir name: {names}")
    raise RuntimeError("unreachable")


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        die(f"missing required tool: {name}")


def render_sim(sim_dir: Path) -> None:
    sim_name = sim_dir.name
    sch = pick_schematic(sim_dir)
    out_dir = OUT_ROOT / sim_name
    out_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "kibot",
            "-c",
            str(KIBOT_CFG),
            "-e",
            str(sch),
            "-d",
            str(out_dir),
        ],
        check=True,
    )

    svg_path = out_dir / "schematic.svg"
    pdf_path = out_dir / "schematic.pdf"
    if not svg_path.exists():
        die(f"expected output not found: {svg_path}")
    if not pdf_path.exists():
        die(f"expected output not found: {pdf_path}")

    png_path = out_dir / "schematic.png"
    if shutil.which("rsvg-convert"):
        subprocess.run(["rsvg-convert", str(svg_path), "-o", str(png_path)], check=True)
    elif shutil.which("inkscape"):
        subprocess.run(
            [
                "inkscape",
                str(svg_path),
                "--export-type=png",
                f"--export-filename={png_path}",
            ],
            check=True,
        )
    elif shutil.which("convert"):
        subprocess.run(["convert", str(svg_path), str(png_path)], check=True)
    else:
        die("no SVG-to-PNG converter found (rsvg-convert, inkscape, or convert)")


def main() -> None:
    if not SIM_ROOT.exists():
        die("simulations/ directory not found")
    if not KIBOT_CFG.exists():
        die(f"KiBot config not found: {KIBOT_CFG}")

    require_tool("kibot")

    sim_dirs = sorted(p for p in SIM_ROOT.iterdir() if p.is_dir())
    if not sim_dirs:
        die("no simulation directories found")

    missing_schematics: list[str] = []
    multi_schematics: list[tuple[str, list[str]]] = []
    for sim_dir in sim_dirs:
        sch_files = sorted(sim_dir.glob("*.kicad_sch"))
        if not sch_files:
            missing_schematics.append(sim_dir.name)
            continue
        if len(sch_files) > 1 and not any(s.stem == sim_dir.name for s in sch_files):
            multi_schematics.append((sim_dir.name, [s.name for s in sch_files]))

    if missing_schematics or multi_schematics:
        if missing_schematics:
            missing = ", ".join(sorted(missing_schematics))
            print(f"error: missing .kicad_sch in simulations: {missing}", file=sys.stderr)
        if multi_schematics:
            for sim, files in multi_schematics:
                names = ", ".join(files)
                print(
                    f"error: multiple schematics in {sim}, none matching dir name: {names}",
                    file=sys.stderr,
                )
        sys.exit(1)

    for sim_dir in sim_dirs:
        render_sim(sim_dir)


if __name__ == "__main__":
    main()
