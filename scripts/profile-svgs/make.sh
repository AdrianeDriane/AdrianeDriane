#!/bin/bash
# Rebuild header.svg + footer.svg (repo root) at their exact rendered heights.
#
# Edit content/styles in build_profile.py, then run:
#   bash scripts/profile-svgs/make.sh
#
# Needs python3 and Google Chrome (headless, used to measure the heights).
# Set CHROME to point at a different Chrome/Chromium binary.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-$(cd "$HERE/../.." && pwd)}"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

python3 -I "$HERE/build_profile.py" "$HERE/icons" measure "$TMP/measure.html"
HEIGHTS=$("$CHROME" --headless=new --disable-gpu --user-data-dir="$TMP/chrome" \
  --dump-dom "file://$TMP/measure.html" 2>/dev/null | grep -o 'H=[0-9]*,[0-9]*' | cut -d= -f2)
[ -n "$HEIGHTS" ] || { echo "Could not measure heights (is Chrome at \$CHROME?)" >&2; exit 1; }
python3 -I "$HERE/build_profile.py" "$HERE/icons" build "$OUT" ${HEIGHTS/,/ }
