"""Run the complete synthetic source-data generation and validation workflow."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(script_name: str) -> None:
    script = ROOT / script_name
    print(f"\n=== Running {script_name} ===")
    subprocess.run([sys.executable, str(script)], check=True)


def main() -> None:
    run("generate_reference_data.py")
    run("generate_activity_data.py")
    run("validate_generated_data.py")
    print("\nSynthetic enterprise source-data pipeline completed successfully.")


if __name__ == "__main__":
    main()
