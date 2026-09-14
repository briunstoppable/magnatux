#!/bin/bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="$REPO_ROOT/.venv/bin/python"
SUPERTUX_SOURCE_ROOT="${SUPERTUX_SOURCE_ROOT:-}"

find_supertux_source_root() {
    if [ -n "$SUPERTUX_SOURCE_ROOT" ] && [ -d "$SUPERTUX_SOURCE_ROOT" ]; then
        printf '%s\n' "$SUPERTUX_SOURCE_ROOT"
        return 0
    fi

    for candidate in \
        "$HOME/SuperTux-v0.7.0-Source" \
        "$HOME/src/SuperTux-v0.7.0-Source" \
        "$HOME/Documents/Projects/SuperTux-v0.7.0-Source" \
        /opt/SuperTux-v0.7.0-Source \
        /usr/local/share/SuperTux-v0.7.0-Source
    do
        if [ -d "$candidate" ]; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done

    return 1
}

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
if SOURCE_ROOT="$(find_supertux_source_root 2>/dev/null)"; then
    echo "Found SuperTux source at: $SOURCE_ROOT"
    if [ -f "$SOURCE_ROOT/CMakeLists.txt" ] && [ -d "$SOURCE_ROOT/src" ] && [ -d "$SOURCE_ROOT/data" ]; then
        echo "SuperTux source layout looks valid."
    else
        echo "SuperTux source directory exists, but it does not look like a complete checkout."
    fi
else
    echo "SuperTux source not found. Set SUPERTUX_SOURCE_ROOT=/path/to/SuperTux-source and rerun this check."
fi

echo
echo "MagnaTux validation complete."