"""
Reads .github/deploy_config.json and outputs whether deployment is enabled.

This script MUST exit 0 for both deploy_true and deploy_false so that the
workflow remains green unless the config file is missing or invalid.
"""

import json
import sys
from pathlib import Path
from os import environ


CONFIG_PATH = Path(".github/deployment.json")

def main() -> None:
    if not CONFIG_PATH.exists():
        print("ERROR: deployment.json not found in .github/", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(CONFIG_PATH.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if "deploy_enabled" not in data:
        print(
            "ERROR: 'deploy_enabled' missing in deployment.json",
            file=sys.stderr,
        )
        sys.exit(1)

    deploy_enabled = bool(data["deploy_enabled"])

    # Modern GitHub Actions output using $GITHUB_OUTPUT
    output_file = Path(environ["GITHUB_OUTPUT"])
    output_file.write_text(
        f"deploy_enabled={str(deploy_enabled).lower()}\n"
    )

    if deploy_enabled:
        print("✅ Deployment ENABLED via deployment.json")
    else:
        print(
            "🚫 Deployment DISABLED via deployment.json "
            "(early exit after tests)"
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
