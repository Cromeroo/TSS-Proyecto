#!/usr/bin/env python
"""Entry point - convierte PDF a audio MP3."""

import sys

from src.cli import main

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)
