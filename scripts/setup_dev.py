#!/usr/bin/env python3
"""Setup script for development environment."""

import os
import subprocess
import sys


def main() -> None:
    """Install pre-commit hooks and development dependencies."""
    print("Setting up development environment...")

    # Install development requirements
    print("Installing development dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements/local.txt"])

    # Install pre-commit hooks
    print("Installing pre-commit hooks...")
    subprocess.check_call(["pre-commit", "install"])

    print("\nDevelopment environment setup complete!")
    print("\nYou can now run pre-commit manually with:")
    print("  pre-commit run --all-files")


if __name__ == "__main__":
    # Change to the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    main()
