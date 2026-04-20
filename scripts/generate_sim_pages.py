#!/usr/bin/env python3
"""
Generate docs pages for each simulation from simulations/<sim>/README.md.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIM_ROOT = ROOT / "simulations"
DOCS_ROOT = ROOT / "docs"
SIM_DOCS_ROOT = DOCS_ROOT / "simulations"
ASSETS_ROOT = DOCS_ROOT / "assets" / "simulations"

SITE_TITLE = "KiCad Simulation Examples"
SIM_SECTION_TITLE = "Simulations"
REPO_URL = "https://github.com/feastorg/KiCad-Simulation-Examples"
DOWNLOAD_PDF_ZIP = "{{ site.baseurl }}/assets/downloads/schematics-pdf.zip"
DOWNLOAD_KIT_ZIP = "{{ site.baseurl }}/assets/downloads/schematics-kit.zip"

H1_RE = re.compile(r"^\s{0,3}#\s+(.+?)\s*$")


def die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def title_from_dir(name: str) -> str:
    return name.replace("_", " ").replace("-", " ").title()


def split_readme(readme_text: str, default_title: str) -> tuple[str, str]:
    lines = readme_text.splitlines()
    title = None
    body_start = 0
    for idx, line in enumerate(lines):
        m = H1_RE.match(line)
        if m:
            title = m.group(1).strip()
            body_start = idx + 1
            break
    if not title:
        title = default_title
        body_start = 0
    body = "\n".join(lines[body_start:]).lstrip()
    return title, body


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def render_sim_page(sim_name: str, title: str, body: str) -> str:
    image_path = f"{{{{ site.baseurl }}}}/assets/simulations/{sim_name}/schematic.png"
    download_pdf = DOWNLOAD_PDF_ZIP
    download_kit = DOWNLOAD_KIT_ZIP
    repo_link = f"{REPO_URL}/tree/main/simulations/{sim_name}"
    return (
        "---\n"
        "layout: default\n"
        f"title: {title}\n"
        f"parent: {SIM_SECTION_TITLE}\n"
        f"grand_parent: {SITE_TITLE}\n"
        "---\n\n"
        "<!-- AUTO-GENERATED: DO NOT EDIT BY HAND -->\n\n"
        f"> Download all schematics as PDFs: [{download_pdf}]({download_pdf})\n"
        f"> Or take the full kit with you (PDF + KiCad schematic + README): [{download_kit}]({download_kit})\n\n"
        f"![Schematic]({image_path})\n\n"
        f"[Open project folder on GitHub]({repo_link})\n\n"
        f"{body}\n"
    )


def render_sim_index(items: list[tuple[str, str, str]]) -> str:
    lines = [
        "---",
        "layout: default",
        f"title: {SIM_SECTION_TITLE}",
        f"parent: {SITE_TITLE}",
        "has_children: true",
        "nav_order: 3",
        "---",
        "",
        "<!-- AUTO-GENERATED: DO NOT EDIT BY HAND -->",
        "",
        "Browse individual simulation pages below. Each page includes a schematic and a short",
        "explanation of what the circuit demonstrates.",
        "",
        f"Download all schematics as PDFs: [{DOWNLOAD_PDF_ZIP}]({DOWNLOAD_PDF_ZIP})",
        f"Or take the full kit with you (PDF + KiCad schematic + README): [{DOWNLOAD_KIT_ZIP}]({DOWNLOAD_KIT_ZIP})",
        "",
        "Want to contribute a new simulation? See the contributor guide:",
        "[Contributing a Simulation](../contributing/).",
        "",
    ]
    for sim_name, title, blurb in items:
        img = f"<img src=\"{{{{ site.baseurl }}}}/assets/simulations/{sim_name}/schematic.png\" width=\"260\" />"
        link = f"{{{{ site.baseurl }}}}/simulations/{sim_name}/"
        lines.append(f"- [{title}]({link})  ")
        if blurb:
            lines.append(f"  {blurb}")
        lines.append(f"  {img}")
        lines.append("")
    return "\n".join(lines)


def render_site_index(items: list[tuple[str, str, str]]) -> str:
    intro = (
        "This is a collection of examples to display KiCad's integrated simulation "
        "capabilities. This builds off of the fantastic: "
        "[OJStuff/Schematics-Examples](https://github.com/OJStuff/Schematics-Examples) "
        "(last updated Dec 15, 2024; commit 41eb9bc)."
    )
    lines = [
        "---",
        "layout: default",
        f"title: {SITE_TITLE}",
        "has_children: true",
        "nav_order: 1",
        "---",
        "",
        "<!-- AUTO-GENERATED: DO NOT EDIT BY HAND -->",
        "",
        intro,
        "",
        f"Download all schematics as PDFs: [{DOWNLOAD_PDF_ZIP}]({DOWNLOAD_PDF_ZIP})",
        f"Or take the full kit with you (PDF + KiCad schematic + README): [{DOWNLOAD_KIT_ZIP}]({DOWNLOAD_KIT_ZIP})",
        "",
        "Contributing a new simulation? See:",
        "[Contributing a Simulation](contributing/).",
        "",
        "## Simulations",
        "",
    ]
    for sim_name, title, blurb in items:
        img = f"<img src=\"{{{{ site.baseurl }}}}/assets/simulations/{sim_name}/schematic.png\" width=\"260\" />"
        link = f"{{{{ site.baseurl }}}}/simulations/{sim_name}/"
        lines.append(f"- [{title}]({link})  ")
        if blurb:
            lines.append(f"  {blurb}")
        lines.append(f"  {img}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    if not SIM_ROOT.exists():
        die("simulations/ directory not found")

    sim_dirs = sorted(p for p in SIM_ROOT.iterdir() if p.is_dir())
    if not sim_dirs:
        die("no simulation directories found")

    missing_readmes = []
    items: list[tuple[str, str, str]] = []

    for sim_dir in sim_dirs:
        readme = sim_dir / "README.md"
        if not readme.exists():
            missing_readmes.append(sim_dir.name)
            continue

        text = readme.read_text(encoding="utf-8", errors="ignore")
        title, body = split_readme(text, title_from_dir(sim_dir.name))
        blurb = ""
        for line in body.splitlines():
            stripped = line.strip()
            if stripped:
                blurb = stripped
                break

        items.append((sim_dir.name, title, blurb))

        page = render_sim_page(sim_dir.name, title, body)
        out_path = SIM_DOCS_ROOT / sim_dir.name / "index.md"
        write_text(out_path, page)

    if missing_readmes:
        missing = ", ".join(sorted(missing_readmes))
        die(f"missing README.md in simulations: {missing}")

    items.sort(key=lambda x: x[1].lower())

    sim_index = render_sim_index(items)
    write_text(SIM_DOCS_ROOT / "index.md", sim_index)

    site_index = render_site_index(items)
    write_text(DOCS_ROOT / "index.md", site_index)


if __name__ == "__main__":
    main()
