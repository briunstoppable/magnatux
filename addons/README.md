# Addons

This folder holds the organized SuperTux addon drafts.

The repo root is the long-term home for all addon and mod work; this folder covers the addon side of that effort.

## Active Work

- `halloween-expansion/` is the current expansion workspace.

## Folders

- `projectiles/` for projectile assets and sprite definitions
- `enemies/` for enemy assets and sprite definitions
- `effects/` for animation-only or reusable visual drafts

## Draft Inventory

- `projectiles/projectile.sprite`
- `enemies/snortle.sprite`
- `enemies/ice_snortle.sprite`
- `enemies/walker.sprite`
- `effects/looping_animation.sprite`

## SuperTux Test Notes

- `snortle.sprite` is the first test target.
- `snortle/frames/` is the reusable green base template.
- `ice_snortle/` is the separate blue variant asset folder.
- Put the enemy sprite files where SuperTux expects addon sprites.
- Confirm the crawling, windup, fire, and squished states all load.
- Verify the mirrored right-facing actions display correctly.
- Check both the normal and ice variants in-game before tuning hitboxes.
- Keep the exported PNGs under `snortle/frames/` for the green base snortle and under `ice_snortle/` for the blue variant.