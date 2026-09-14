#!/bin/bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="$REPO_ROOT/.venv/bin/python"
SUPERTUX_APP_PATH="${SUPERTUX_APP_PATH:-/Applications/SuperTux.app}"
SUPERTUX_SOURCE_ROOT="${SUPERTUX_SOURCE_ROOT:-/Users/brian/Documents/Projects/SuperTux-v0.7.0-Source}"
SUPERTUX_BUILD_EXE="${SUPERTUX_BUILD_EXE:-}"
LOCAL_SUPERTUX_APP_PATH="${LOCAL_SUPERTUX_APP_PATH:-${TMPDIR:-/tmp}/MagnaTux-SuperTux.app}"
SUPERTUX_ALLOW_APP_BUNDLE="${SUPERTUX_ALLOW_APP_BUNDLE:-0}"

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

clear_quarantine() {
    local target="$1"
    if xattr -p com.apple.quarantine "$target" >/dev/null 2>&1; then
        echo "Removing quarantine from: $target"
        if ! xattr -d com.apple.quarantine "$target"; then
            echo "Warning: could not remove quarantine from $target"
        fi
    fi
}

launch_app_bundle() {
    local app_path="$1"
    if [ ! -d "$app_path" ]; then
        return 1
    fi

    rm -rf "$LOCAL_SUPERTUX_APP_PATH"
    echo "Copying SuperTux to a local writable path: $LOCAL_SUPERTUX_APP_PATH"
    ditto "$app_path" "$LOCAL_SUPERTUX_APP_PATH"

    clear_quarantine "$LOCAL_SUPERTUX_APP_PATH"

    echo "Ad-hoc signing local copy: $LOCAL_SUPERTUX_APP_PATH"
    if ! codesign --force --deep --sign - "$LOCAL_SUPERTUX_APP_PATH" >/dev/null 2>&1; then
        echo "Warning: ad-hoc signing the local copy failed, but launch will still be attempted."
    fi

    echo "Verifying local copy signature..."
    if ! codesign --verify --deep --strict --verbose=4 "$LOCAL_SUPERTUX_APP_PATH" >/dev/null 2>&1; then
        echo "Error: the local SuperTux copy is still code-signature invalid."
        echo "This downloaded app bundle is not suitable for direct local launching on this machine."
        echo "Build SuperTux from source or use a trusted nightly/release binary instead."
        return 1
    fi

    echo "Launching SuperTux app bundle: $LOCAL_SUPERTUX_APP_PATH"
    open "$LOCAL_SUPERTUX_APP_PATH"
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
elif [ -d "$SUPERTUX_SOURCE_ROOT" ] && [ -x "$SUPERTUX_SOURCE_ROOT/build/supertux2" ]; then
    launch_source_build "$SUPERTUX_SOURCE_ROOT/build/supertux2"
elif [ -d "$SUPERTUX_SOURCE_ROOT" ]; then
    echo "SuperTux source checkout found at: $SUPERTUX_SOURCE_ROOT"
    if command -v cmake >/dev/null 2>&1; then
        echo "No built executable detected yet. Build it with:"
        echo "  cmake -S \"$SUPERTUX_SOURCE_ROOT\" -B \"$SUPERTUX_SOURCE_ROOT/build\""
        echo "  cmake --build \"$SUPERTUX_SOURCE_ROOT/build\""
        echo "Then rerun this script, or set SUPERTUX_BUILD_EXE to the resulting binary."
    else
        echo "cmake is not installed, so this machine cannot build SuperTux from source yet."
        echo "Install the build tools from SuperTux's INSTALL.md, then rerun this script."
    fi
    if [ "$SUPERTUX_ALLOW_APP_BUNDLE" = "1" ] && launch_app_bundle "$SUPERTUX_APP_PATH"; then
        :
    else
        exit 1
    fi
else
    echo "No local SuperTux source checkout found at $SUPERTUX_SOURCE_ROOT."
    exit 1
fi

echo
echo "SuperTux launch attempted. Use this for local MagnaTux map-editor validation."