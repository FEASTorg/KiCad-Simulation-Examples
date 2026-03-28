#!/usr/bin/env python3
"""Bundle schematic PDFs into a single zip for download."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIM_ASSETS = ROOT / "docs" / "assets" / "simulations"
OUT_DIR = ROOT / "docs" / "assets" / "downloads"
OUT_ZIP = OUT_DIR / "schematics.zip"


def die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    if not SIM_ASSETS.exists():
        die("expected docs/assets/simulations to exist; run render_schematics.py first")

    pdfs = sorted(SIM_ASSETS.glob("*/schematic.pdf"))
    if not pdfs:
        die("no schematic.pdf files found under docs/assets/simulations")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for pdf in pdfs:
            rel = pdf.relative_to(SIM_ASSETS)
            zf.write(pdf, rel.as_posix())

    print(f"✔ Wrote {OUT_ZIP}")


if __name__ == "__main__":
    main()
