#!/usr/bin/env python3
from pathlib import Path
import fnmatch


def load_ignore(dir_path: Path):
    ignore_file = dir_path / ".indexignore"
    patterns = []
    if ignore_file.exists():
        for line in ignore_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
    patterns.append("index.md")  # always ignore old indexes
    return patterns


def should_ignore(path: Path, patterns):
    return any(fnmatch.fnmatch(path.name, pat) for pat in patterns)


def make_index(dir_path: Path):
    patterns = load_ignore(dir_path)
    readme = dir_path / "README.md"
    index = dir_path / "index.md"
    parts = []

    # 1) README or fallback title
    if readme.exists() and not should_ignore(readme, patterns):
        parts.append(readme.read_text(encoding="utf-8"))
        parts.append("\n")
    else:
        title = dir_path.name.replace("_", " ").title() or "Documentation"
        parts.append(f"# {title}\n\n")

    parts.append("## Contents\n\n")

    # 2) List markdown files
    for md in sorted(dir_path.glob("*.md")):
        if should_ignore(md, patterns) or md.name.lower() in ("readme.md", "index.md"):
            continue
        title = md.stem.replace("_", " ").title()
        parts.append(f"- [{title}]({md.name})\n")
    parts.append("\n")

    # 3) Recurse into subdirectories
    for sub in sorted([d for d in dir_path.iterdir() if d.is_dir()]):
        if should_ignore(sub, patterns):
            continue
        make_index(sub)
        title = sub.name.replace("_", " ").title()
        parts.append(f"### [{title}]({sub.name}/index.html)\n")

    index.write_text("".join(parts), encoding="utf-8")
    print(f"Generated {index}")


if __name__ == "__main__":
    make_index(Path("docs"))
