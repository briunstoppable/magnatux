# magnatux
Add Ons for SuperTux

[![Nightly Validator](https://github.com/briunstoppable/magnatux/actions/workflows/nightly-validator.yml/badge.svg)](https://github.com/briunstoppable/magnatux/actions/workflows/nightly-validator.yml)
[![Validation Status](https://img.shields.io/badge/validation-passing-brightgreen)](https://github.com/briunstoppable/magnatux/actions/workflows/nightly-validator.yml)

This repository is the clean, Linux-first home for SuperTux addons and mods we build over time.

## Environment requirements

This project expects a Python environment with Pillow installed for image validation and tileset generation.

- Create or reuse the repo venv: `python3 -m venv .venv`
- Activate it: `source .venv/bin/activate`
- Install dependencies: `python -m pip install -r requirements.txt`
- If you are not using the repo venv, make sure `Pillow` is available in the interpreter you run the validation scripts with.

## Verification

- Run `.venv/bin/python -m unittest discover -s tests` from the repo root for the full manifest, asset inventory, and sprite-reference checks.
- Run `./test_magnatux.sh` for the local preflight; it prefers the repo venv when available and looks for a SuperTux source checkout via `SUPERTUX_SOURCE_ROOT` or common Linux install locations.
- Run `./run_supertux_local.sh` when you want to validate MagnaTux and then attempt to launch a locally built SuperTux binary. It is intentionally Linux-safe and no longer relies on macOS app bundles, quarantine handling, or `codesign`.

## Linux-first workflow

- Keep the SuperTux source tree in a standard Linux path such as `~/SuperTux-v0.7.0-Source` or `~/src/SuperTux-v0.7.0-Source`.
- Export `SUPERTUX_SOURCE_ROOT=/path/to/SuperTux-source` before running validation or the local launcher.
- Copy the organized addon tree into SuperTux's user addon directory, typically `~/.local/share/supertux2/addons/` or the equivalent data directory used by your local build.

## Active Expansion

- `addons/halloween-expansion/` contains the organized Halloween mod assets, sprite drafts, and test notes.

## Project Areas

- `addons/` contains reusable addon work and expansion-specific assets.
- `mods/` is reserved for larger standalone mod projects.

## Current Layout

- `addons/projectiles/` for projectile-based sprite drafts
- `addons/enemies/` for enemy sprite drafts
- `addons/effects/` for general animation or effect drafts

The organized addon files live under `addons/`, and the original generated source drafts are archived in `addons/source/`.

## Local addon copying

When testing in a Linux SuperTux build, mirror the repo's structure under the game data directory, for example:

```text
~/.local/share/supertux2/addons/
  enemies/
    snortle.sprite
    ice_snortle.sprite
    snortle/
      base_snortle_sheet.jpg
      frames/
        crawl-0.png
        crawl-1.png
        windup.png
        fire.png
        squished.png
    ice_snortle/
      ice_snortle_sheet.jpg
      frames/
        ice-snortle-crawl-0.png
        ice-snortle-crawl-1.png
        ice-snortle-windup.png
        ice-snortle-fire.png
        ice-snortle-squished.png
```

This keeps the file paths consistent with the repo manifest and avoids loose asset files at the repo root.
