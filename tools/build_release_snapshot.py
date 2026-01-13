import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-id", required=True)
    args = parser.parse_args()

    release_id = args.release_id
    release_root = ROOT / "data" / "snapshots" / "releases"
    release_root.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["SNAPSHOT_ID"] = release_id
    env["SNAPSHOT_ROOT"] = str(release_root)

    subprocess.run([sys.executable, "tools/build_index.py"], check=True, env=env, cwd=ROOT)
    subprocess.run([sys.executable, "tools/build_snapshot.py"], check=True, env=env, cwd=ROOT)

    print(f"Release snapshot built: {release_root / release_id}")


if __name__ == "__main__":
    main()
