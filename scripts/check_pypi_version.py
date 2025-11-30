"""Checks whether the local package version exists on TestPyPI or PyPI.

This script extracts the local package version from the project's __init__.py
and compares it against versions published on TestPyPI or PyPI. It supports a
command-line flag to toggle between the test and production repositories, and a
stage parameter to enforce version rules for deployed vs. deploying.
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path
from typing import List, Optional
from packaging.version import Version

PACKAGE_NAME = "latlng_to_state"
PACKAGE_PATH = "latlng_to_state"

TEST_PYPI_URL = "https://test.pypi.org/pypi"
PROD_PYPI_URL = "https://pypi.org/pypi"


def get_local_version() -> str:
    """Extracts the package version from <package>/__init__.py."""
    init_path = Path(PACKAGE_PATH) / "__init__.py"
    text = init_path.read_text()

    version_line = next(
        (line for line in text.splitlines() if line.startswith("__version__")),
        None,
    )

    if not version_line:
        print("ERROR: __version__ not found in __init__.py", file=sys.stderr)
        sys.exit(1)

    return version_line.split("=")[1].strip().strip("\"'")


def fetch_versions(base_url: str, package_name: str) -> List[str]:
    """Fetches all published versions for a package from PyPI or TestPyPI."""
    url = f"{base_url}/{package_name}/json"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            return list(data.get("releases", {}).keys())
    except Exception:
        return []


def get_latest_version(versions: List[str]) -> Optional[str]:
    """Returns the highest semantic version in a list."""
    if not versions:
        return None
    try:
        return str(max((Version(v) for v in versions)))
    except Exception:
        return versions[-1]


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments including repo choice and stage."""
    parser = argparse.ArgumentParser(
        description="Compare the local package version with PyPI/TestPyPI."
    )

    repo_group = parser.add_mutually_exclusive_group()
    repo_group.add_argument(
        "--prod",
        action="store_true",
        help="Check against production PyPI.",
    )
    repo_group.add_argument(
        "--test",
        action="store_true",
        help="Check against TestPyPI (default).",
    )

    parser.add_argument(
        "--stage",
        choices=["deploying", "deployed"],
        default="deploying",
        help=(
            "Version rule mode:\n"
            "  deploying → local version must NOT exist remotely\n"
            "  deployed  → local version MUST already exist remotely"
        ),
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Determine repo
    if args.prod:
        base_url = PROD_PYPI_URL
        repo_name = "PyPI"
    else:
        base_url = TEST_PYPI_URL
        repo_name = "TestPyPI"

    print(f"Checking against: {repo_name}")
    print(f"Stage: {args.stage}")

    local_version = get_local_version()
    published_versions = fetch_versions(base_url, PACKAGE_NAME)
    latest_version = get_latest_version(published_versions)

    print(f"Local version: {local_version}")
    print(f"{repo_name} published versions: {published_versions or 'None'}")

    if latest_version:
        print(f"Latest {repo_name} version: {latest_version}")
    else:
        print(f"Latest {repo_name} version: None")

    if args.stage == "deploying":
        # Must NOT exist yet
        if local_version in published_versions:
            print(
                f"""❌ ERROR: Version {local_version} already
                    exists on {repo_name}."""
            )
            sys.exit(1)

        print(f"✅ Version {local_version} is new. Safe to publish.")
        sys.exit(0)

    elif args.stage == "deployed":
        # Must already exist
        if local_version not in published_versions:
            print(
                f"""❌ ERROR: Version {local_version} does NOT
                    exist on {repo_name}."""
            )
            sys.exit(1)

        print(f"""✅ Version {local_version} is correctly
                published on {repo_name}.""")

        sys.exit(0)


if __name__ == "__main__":
    main()
