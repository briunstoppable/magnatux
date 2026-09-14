#!/bin/bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="$REPO_ROOT/.venv/bin/python"
SUPERTUX_SOURCE_ROOT="${SUPERTUX_SOURCE_ROOT:-/Users/brian/Documents/Projects/SuperTux-v0.7.0-Source}"

if [ ! -d "$REPO_ROOT/addons" ]; then
    echo "Error: $REPO_ROOT/addons not found. Please verify the MagnaTux repo path."
    exit 1
fi

echo "Running repo validation..."
if [ -x "$PYTHON_BIN" ]; then
    "$PYTHON_BIN" -m unittest discover -s "$REPO_ROOT/tests"
elif command -v python3 >/dev/null 2>&1; then
    python3 -m unittest discover -s "$REPO_ROOT/tests"
else
    echo "python3 not found; skipping tests"
fi

echo
if [ -d "$SUPERTUX_SOURCE_ROOT" ]; then
    echo "Found SuperTux source at: $SUPERTUX_SOURCE_ROOT"
    if [ -f "$SUPERTUX_SOURCE_ROOT/CMakeLists.txt" ] && [ -d "$SUPERTUX_SOURCE_ROOT/src" ] && [ -d "$SUPERTUX_SOURCE_ROOT/data" ]; then
        echo "SuperTux source layout looks valid."
    else
        echo "SuperTux source directory exists, but it does not look like a complete checkout."
    fi
else
    echo "SuperTux source not found at: $SUPERTUX_SOURCE_ROOT"
fi

echo
echo "MagnaTux validation complete."