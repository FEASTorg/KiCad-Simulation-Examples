#!/usr/bin/env python3
"""Bundle PDFs + KiCad schematics + READMEs into a single zip."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIM_ROOT = ROOT / "simulations"
OUT_DIR = ROOT / "docs" / "assets" / "downloads"
OUT_ZIP = OUT_DIR / "schematics-kit.zip"

MODEL_EXTS = {".lib", ".spice", ".cir", ".txt"}


def die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def iter_files(sim_dir: Path) -> list[Path]:
    files = []
    files.extend(sim_dir.glob("*.kicad_sch"))
    files.extend(sim_dir.glob("README.md"))
    for p in sim_dir.iterdir():
        if p.is_file() and p.suffix.lower() in MODEL_EXTS:
            files.append(p)
    return sorted({p.resolve() for p in files})


def main() -> None:
    if not SIM_ROOT.exists():
        die("simulations directory not found")

    sim_dirs = sorted([p for p in SIM_ROOT.iterdir() if p.is_dir()])
    if not sim_dirs:
        die("no simulation directories found")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for sim_dir in sim_dirs:
            files = iter_files(sim_dir)
            if not files:
                continue
            for file in files:
                rel = file.relative_to(SIM_ROOT)
                zf.write(file, rel.as_posix())

    print(f"✔ Wrote {OUT_ZIP}")


if __name__ == "__main__":
    main()
