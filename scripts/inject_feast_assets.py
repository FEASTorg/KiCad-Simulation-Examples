#!/usr/bin/env python3
"""
Inject FEAST theme assets (_sass and _includes) into docs/ when
color_scheme: feast is specified in docs/_config.yml.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml

CONFIG_PATH = Path("docs/_config.yml")
TEMP_CLONE_DIR = Path("_feast_temp")
REMOTE_REPO_URL = "https://github.com/feastorg/feastorg.github.io.git"
WANTED_COLOR_SCHEME = "feast"
RETRY_ATTEMPTS = 3
RETRY_DELAY = 5


def log(message: str) -> None:
    print(message)


def load_color_scheme(config_path: Path) -> str | None:
    if not config_path.exists():
        return None
    try:
        with config_path.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        return str(config.get("color_scheme", "")).strip().lower()
    except (yaml.YAMLError, OSError):
        return None


def clone_theme_repo(retries: int = RETRY_ATTEMPTS, delay: int = RETRY_DELAY) -> bool:
    log(f"Cloning theme repo to {TEMP_CLONE_DIR}...")
    for attempt in range(1, retries + 1):
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", REMOTE_REPO_URL, str(TEMP_CLONE_DIR)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            log(f"Clone successful on attempt {attempt}")
            return True
        except subprocess.CalledProcessError as exc:
            log(f"Clone attempt {attempt} failed.\n{exc.output.decode(errors='ignore')}")
            if attempt < retries:
                log(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                log("All attempts to clone the theme repo failed.")
    return False


def copy_theme_assets() -> None:
    for folder in ["_sass", "_includes"]:
        src = TEMP_CLONE_DIR / folder
        dst = Path("docs") / folder
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)


def safe_rmtree(path: Path) -> bool:
    try:
        shutil.rmtree(path)
        return True
    except (PermissionError, OSError) as exc:
        log(f"Could not delete '{path}': {exc}")
        return False


def verify_assets() -> bool:
    success = True
    for folder in ["_sass", "_includes"]:
        path = Path("docs") / folder
        if not path.exists() or not any(path.iterdir()):
            log(f"Missing or empty: docs/{folder}/ — injection likely failed.")
            success = False
        else:
            log(f"Verified: docs/{folder}/ has {len(list(path.iterdir()))} items.")
    return success


def main() -> None:
    if not CONFIG_PATH.exists():
        log(f"Missing: {CONFIG_PATH} — cannot determine color_scheme.")
        sys.exit(1)

    color_scheme = load_color_scheme(CONFIG_PATH)
    if color_scheme != WANTED_COLOR_SCHEME:
        log(f"color_scheme is '{color_scheme}', skipping injection.")
        return

    if TEMP_CLONE_DIR.exists():
        if not safe_rmtree(TEMP_CLONE_DIR):
            log(f"Failed to clean temp dir '{TEMP_CLONE_DIR}'. Aborting.")
            sys.exit(1)

    if not clone_theme_repo():
        sys.exit(1)

    copy_theme_assets()
    safe_rmtree(TEMP_CLONE_DIR)

    if not verify_assets():
        log("Asset verification failed. Please inspect logs.")
        sys.exit(1)

    log("Theme assets injected and verified successfully.")


if __name__ == "__main__":
    main()
