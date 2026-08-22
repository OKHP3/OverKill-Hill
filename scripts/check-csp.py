#!/usr/bin/env python3
"""CI guard against missing, drifted, or weakened page CSP policies."""
import runpy
import sys


if __name__ == "__main__":
    sys.argv = ["scripts/generate-csp.py", "--check"]
    runpy.run_path("scripts/generate-csp.py", run_name="__main__")