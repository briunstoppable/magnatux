# Enemy Drafts

The snortle is the first enemy prepared for testing.

## Current Status

- `snortle.sprite` is the base enemy contract to validate first.
- `ice_snortle.sprite` is the variant that should be tested after the base enemy is stable.
- The green snortle is the base template; its rendered frames live in `snortle/frames/`.
- The ice snortle stays in `ice_snortle/` as its own asset set.
- The ice variant frame exports now live in `ice_snortle/frames/` with `ice-snortle-*` names.

## Next Step

Load the base snortle in SuperTux first, then compare the ice variant against it once the shared animation setup is working.