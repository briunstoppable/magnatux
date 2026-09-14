# magnatux
Add Ons for SuperTux

[![Nightly Validator](https://github.com/briunstoppable/magnatux/actions/workflows/nightly-validator.yml/badge.svg)](https://github.com/briunstoppable/magnatux/actions/workflows/nightly-validator.yml)
[![Validation Status](https://img.shields.io/badge/validation-passing-brightgreen)](https://github.com/briunstoppable/magnatux/actions/workflows/nightly-validator.yml)

This repository is the holding place for all SuperTux addons and mods we build over time.

## Verification

- Run `.venv/bin/python -m unittest discover -s tests` from the repo root for the full manifest, asset inventory, and sprite-reference checks.
- Run `./test_magnatux.sh` for the local preflight; it prefers the repo venv when available and also checks the downloaded SuperTux source checkout at `/Users/brian/Documents/Projects/SuperTux-v0.7.0-Source` when present.
- Run `./run_supertux_local.sh` when you want to validate MagnaTux and then launch SuperTux for map-editor testing; it expects a source-built binary first and only tries the copied app bundle if you set `SUPERTUX_ALLOW_APP_BUNDLE=1`.

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
