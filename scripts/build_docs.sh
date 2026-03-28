#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT"

python3 scripts/render_schematics.py
python3 scripts/generate_sim_pages.py
python3 scripts/bundle_pdfs.py

printf "\nDocs artifacts generated under docs/.\n"
