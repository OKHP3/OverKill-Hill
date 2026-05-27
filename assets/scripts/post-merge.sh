#!/bin/bash
set -e

# OverKill Hill P³™ — post-merge setup
# Static HTML site — no build step required.
# Validates that the Python server module is importable and key files exist.

echo "Post-merge: verifying static site integrity..."

# Confirm server entry point exists
if [ ! -f "server.py" ]; then
  echo "ERROR: server.py not found" >&2
  exit 1
fi

# Confirm core HTML files are present
for f in index.html writings/first-diagram-is-a-liar/index.html assets/css/theme.css assets/js/app.js; do
  if [ ! -f "$f" ]; then
    echo "ERROR: required file missing: $f" >&2
    exit 1
  fi
done

echo "Post-merge: running MTB version consistency check..."
python3 assets/scripts/check-mtb-version.py
if [ $? -ne 0 ]; then
  echo "ERROR: MTB version check failed — stale version strings or roadmap drift detected." >&2
  exit 1
fi

echo "Post-merge: running full site validator..."
python3 assets/scripts/validate_site.py
if [ $? -ne 0 ]; then
  echo "ERROR: Site validation failed — stale or broken pages detected." >&2
  exit 1
fi

echo "Post-merge: all checks passed."
