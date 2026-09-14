#!/bin/bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="$REPO_ROOT/.venv/bin/python"
SUPERTUX_SOURCE_ROOT="${SUPERTUX_SOURCE_ROOT:-}"
SUPERTUX_BUILD_EXE="${SUPERTUX_BUILD_EXE:-}"

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

run_validation() {
    echo "Running MagnaTux validation..."
    if [ -x "$PYTHON_BIN" ]; then
        "$PYTHON_BIN" -m unittest discover -s "$REPO_ROOT/tests"
    elif command -v python3 >/dev/null 2>&1; then
        python3 -m unittest discover -s "$REPO_ROOT/tests"
    else
        echo "python3 not found; skipping tests"
    fi
}

launch_source_build() {
    local build_exe="$1"
    if [ ! -x "$build_exe" ]; then
        return 1
    fi

    echo "Launching SuperTux executable: $build_exe"
    "$build_exe" &
}

run_validation

echo
if [ -n "$SUPERTUX_BUILD_EXE" ] && [ -x "$SUPERTUX_BUILD_EXE" ]; then
    launch_source_build "$SUPERTUX_BUILD_EXE"
    exit 0
fi

if SOURCE_ROOT="$(find_supertux_source_root 2>/dev/null)"; then
    if [ -x "$SOURCE_ROOT/build/supertux2" ]; then
        launch_source_build "$SOURCE_ROOT/build/supertux2"
        exit 0
    elif [ -x "$SOURCE_ROOT/build/supertux" ]; then
        launch_source_build "$SOURCE_ROOT/build/supertux"
        exit 0
    fi

    echo "SuperTux source checkout found at: $SOURCE_ROOT"
    if command -v cmake >/dev/null 2>&1; then
        echo "No built executable detected yet. Build it with:"
        echo "  cmake -S \"$SOURCE_ROOT\" -B \"$SOURCE_ROOT/build\""
        echo "  cmake --build \"$SOURCE_ROOT/build\""
        echo "Then rerun this script or set SUPERTUX_BUILD_EXE to the resulting binary."
    else
        echo "cmake is not installed, so this machine cannot build SuperTux from source yet."
        echo "Install the build tools from the SuperTux INSTALL.md, then rerun this script."
    fi
    exit 1
fi

echo "No local SuperTux source checkout found."
echo "Set SUPERTUX_SOURCE_ROOT to the SuperTux source directory or clone the project before running this script."
exit 1