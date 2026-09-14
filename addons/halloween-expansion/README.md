# Halloween Expansion

This folder holds the organized art and starter sprite drafts for the Halloween expansion mod.

## Asset Map

- `art/powerups/jackolantern_powerup_and_pumpkin_tux.jpg` for the Jack-O'-Lantern Helm collectible and Pumpkin Tux visual draft
- `art/enemies/phantom_bat_sheet.jpg` for the Phantom Bat
- `art/enemies/webweaver_sheet.jpg` for the Web-Weaver Spider
- `art/bosses/arachnia_boss_sheet.jpg` for Arachnia, Queen of the Web
- `art/enemies/wailing_phantoms_sheet.jpg` for the White Phantom, Green Wisp, and Blue Banshee
- `art/enemies/underworld_imp_sheet.jpg` for the Underworld Imp

## Legacy References

- `art/reference/ice_snortle_legacy_sheet.jpg`
- `art/reference/phantom_bat_legacy_sheet.jpg`

## Notes

- The player ability logic for Pumpkin Tux will need gameplay-side implementation; the sprite file here only prepares the visual state.
- Boss phases, web hazards, and enemy AI are prepared as sprite/state drafts and will need in-game testing in SuperTux.

## Test Order

1. Load the collectible sprite and confirm the hitbox and pickup art show correctly.
2. Check each enemy sprite loads without missing image references.
3. Verify mirrored facing states.
4. Test the boss sheet and the ghost trio after the basic enemies are stable.