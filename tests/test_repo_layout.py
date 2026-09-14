from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover - environment dependent
    Image = None


REPO_ROOT = Path(__file__).resolve().parents[1]
SUPERTUX_SOURCE_ROOT = Path("/Users/brian/Documents/Projects/SuperTux-v0.7.0-Source")
SPRITE_IMAGE_BLOCK_PATTERN = re.compile(r'\(images(?P<body>.*?)\)', re.DOTALL)
DISALLOWED_ROOT_SUFFIXES = {".sprite", ".png", ".jpg", ".jpeg", ".webp"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


class RepoLayoutTests(unittest.TestCase):
    def _sprite_image_refs(self, sprite_path: Path) -> list[str]:
        content = sprite_path.read_text(encoding="utf-8")
        refs: list[str] = []
        for block in SPRITE_IMAGE_BLOCK_PATTERN.finditer(content):
            refs.extend(re.findall(r'"([^"]+)"', block.group("body")))
        return refs

    def _load_manifest(self) -> dict:
        manifest_path = REPO_ROOT / "addons" / "manifest.json"
        return json.loads(manifest_path.read_text(encoding="utf-8"))

    def test_no_floating_asset_files_at_repo_root(self) -> None:
        floating = [
            path.name
            for path in REPO_ROOT.iterdir()
            if path.is_file() and path.suffix.lower() in DISALLOWED_ROOT_SUFFIXES
        ]
        self.assertEqual(
            floating,
            [],
            f"unexpected loose asset files at repo root: {floating}",
        )

    def test_manifest_exists_and_is_valid_json(self) -> None:
        manifest_path = REPO_ROOT / "addons" / "manifest.json"
        self.assertTrue(manifest_path.exists())
        manifest = self._load_manifest()
        self.assertEqual(manifest.get("version"), 1)
        self.assertIsInstance(manifest.get("assetSets"), list)

    def test_manifest_asset_sets_have_expected_keys(self) -> None:
        manifest = self._load_manifest()
        for asset_set in manifest["assetSets"]:
            self.assertIn("name", asset_set)
            self.assertIn("kind", asset_set)
            self.assertTrue("sprite" in asset_set or "spriteDir" in asset_set)
            self.assertIn("requiredFiles", asset_set)

    def test_manifest_declared_files_exist(self) -> None:
        manifest = self._load_manifest()
        missing: list[str] = []
        for asset_set in manifest["assetSets"]:
            for relative_path in asset_set.get("requiredFiles", []):
                if not (REPO_ROOT / "addons" / relative_path).exists():
                    missing.append(relative_path)
            for sprite_name in asset_set.get("requiredSprites", []):
                sprite_dir = REPO_ROOT / "addons" / asset_set["spriteDir"]
                sprite_path = sprite_dir / sprite_name
                if not sprite_path.exists():
                    missing.append(str(sprite_path.relative_to(REPO_ROOT / "addons")))

        self.assertEqual(missing, [], f"manifest references missing files: {missing}")

    def test_manifest_expected_sprite_roots_match_repo(self) -> None:
        manifest = self._load_manifest()
        roots = {asset_set["name"]: asset_set for asset_set in manifest["assetSets"]}
        self.assertEqual(roots["base-snortle"]["sprite"], "enemies/snortle.sprite")
        self.assertEqual(roots["ice-snortle"]["sprite"], "enemies/ice_snortle.sprite")
        self.assertEqual(roots["projectile-template"]["sprite"], "projectiles/projectile.sprite")
        self.assertEqual(roots["looping-animation-template"]["sprite"], "effects/looping_animation.sprite")

    def test_super_tux_source_checkout_looks_valid(self) -> None:
        self.assertTrue(SUPERTUX_SOURCE_ROOT.exists(), f"missing SuperTux source checkout: {SUPERTUX_SOURCE_ROOT}")
        self.assertTrue((SUPERTUX_SOURCE_ROOT / "CMakeLists.txt").exists())
        self.assertTrue((SUPERTUX_SOURCE_ROOT / "src").is_dir())
        self.assertTrue((SUPERTUX_SOURCE_ROOT / "data").is_dir())

    def test_all_images_open_successfully(self) -> None:
        if Image is None:
            self.skipTest("Pillow is not installed in this Python environment")

        broken: list[str] = []
        for image_path in REPO_ROOT.rglob("*"):
            if image_path.is_file() and image_path.suffix.lower() in IMAGE_SUFFIXES:
                try:
                    with Image.open(image_path) as image:
                        image.verify()
                except Exception as exc:  # pragma: no cover - surfaced via assertion
                    broken.append(f"{image_path.relative_to(REPO_ROOT)} -> {exc}")

        self.assertEqual(broken, [], "broken image files:\n" + "\n".join(broken))

    def test_all_pngs_have_pixels_and_dimensions(self) -> None:
        if Image is None:
            self.skipTest("Pillow is not installed in this Python environment")

        problems: list[str] = []
        for image_path in REPO_ROOT.rglob("*.png"):
            with Image.open(image_path) as opened:
                width, height = opened.size
                if width <= 0 or height <= 0:
                    problems.append(f"{image_path.relative_to(REPO_ROOT)} has invalid size {opened.size}")
                if opened.getbbox() is None:
                    problems.append(f"{image_path.relative_to(REPO_ROOT)} is fully transparent or empty")

        self.assertEqual(problems, [], "png problems:\n" + "\n".join(problems))

    def test_snortle_pngs_have_transparency(self) -> None:
        if Image is None:
            self.skipTest("Pillow is not installed in this Python environment")

        problems: list[str] = []
        for image_path in (REPO_ROOT / "addons" / "enemies" / "snortle" / "frames").glob("*.png"):
            with Image.open(image_path) as opened:
                image = opened.convert("RGBA")
                try:
                    alpha_min, alpha_max = image.getchannel("A").getextrema()
                    if alpha_min == alpha_max == 255:
                        problems.append(f"{image_path.relative_to(REPO_ROOT)} is fully opaque")
                finally:
                    image.close()

        self.assertEqual(problems, [], "snortle transparency problems:\n" + "\n".join(problems))

    def test_ice_snortle_pngs_have_transparency(self) -> None:
        if Image is None:
            self.skipTest("Pillow is not installed in this Python environment")

        problems: list[str] = []
        for image_path in (REPO_ROOT / "addons" / "enemies" / "ice_snortle" / "frames").glob("*.png"):
            with Image.open(image_path) as opened:
                image = opened.convert("RGBA")
                try:
                    alpha_min, alpha_max = image.getchannel("A").getextrema()
                    if alpha_min == alpha_max == 255:
                        problems.append(f"{image_path.relative_to(REPO_ROOT)} is fully opaque")
                finally:
                    image.close()

        self.assertEqual(problems, [], "ice snortle transparency problems:\n" + "\n".join(problems))

    def test_enemy_sprite_files_live_in_enemy_root(self) -> None:
        enemy_root = REPO_ROOT / "addons" / "enemies"
        top_level_sprites = sorted(path.name for path in enemy_root.glob("*.sprite"))
        nested_sprites = sorted(
            path.relative_to(enemy_root).as_posix()
            for subdir in enemy_root.iterdir()
            if subdir.is_dir()
            for path in subdir.rglob("*.sprite")
        )

        self.assertEqual(
            top_level_sprites,
            ["ice_snortle.sprite", "snortle.sprite", "walker.sprite"],
        )
        self.assertEqual(
            nested_sprites,
            [],
            f"enemy sprite files should stay at the enemy root, not in subdirectories: {nested_sprites}",
        )

    def test_enemy_sprite_files_have_expected_headers(self) -> None:
        for sprite_name in ["snortle.sprite", "ice_snortle.sprite", "walker.sprite"]:
            sprite_path = REPO_ROOT / "addons" / "enemies" / sprite_name
            content = sprite_path.read_text(encoding="utf-8").lstrip()
            self.assertTrue(content.startswith("(supertux-sprite"), sprite_name)
            self.assertEqual(content.count("("), content.count(")"), f"unbalanced parentheses in {sprite_name}")
            self.assertGreaterEqual(content.count("(action"), 1, f"{sprite_name} needs at least one action")

    def test_enemy_sprite_action_names_are_unique(self) -> None:
        action_name_pattern = re.compile(r'\(name\s+"([^"]+)"\)')
        for sprite_name in ["snortle.sprite", "ice_snortle.sprite", "walker.sprite"]:
            sprite_path = REPO_ROOT / "addons" / "enemies" / sprite_name
            names = action_name_pattern.findall(sprite_path.read_text(encoding="utf-8"))
            self.assertEqual(len(names), len(set(names)), f"duplicate action names in {sprite_name}: {names}")

    def test_projectile_template_sprite_is_organized(self) -> None:
        projectile_root = REPO_ROOT / "addons" / "projectiles"
        self.assertTrue((projectile_root / "projectile.sprite").exists())
        nested_sprites = sorted(path.relative_to(projectile_root).as_posix() for path in projectile_root.rglob("*.sprite") if path.name != "projectile.sprite")
        self.assertEqual(nested_sprites, [])

    def test_projectile_template_sprite_has_expected_structure(self) -> None:
        sprite_path = REPO_ROOT / "addons" / "projectiles" / "projectile.sprite"
        content = sprite_path.read_text(encoding="utf-8")
        self.assertTrue(content.lstrip().startswith("(supertux-sprite"))
        self.assertEqual(content.count("("), content.count(")"))
        self.assertIn('(images "projectile.png")', content)

    def test_effects_template_sprite_is_organized(self) -> None:
        effects_root = REPO_ROOT / "addons" / "effects"
        self.assertTrue((effects_root / "looping_animation.sprite").exists())
        nested_sprites = sorted(path.relative_to(effects_root).as_posix() for path in effects_root.rglob("*.sprite") if path.name != "looping_animation.sprite")
        self.assertEqual(nested_sprites, [])

    def test_effects_template_sprite_has_expected_structure(self) -> None:
        sprite_path = REPO_ROOT / "addons" / "effects" / "looping_animation.sprite"
        content = sprite_path.read_text(encoding="utf-8")
        self.assertTrue(content.lstrip().startswith("(supertux-sprite"))
        self.assertEqual(content.count("("), content.count(")"))
        self.assertIn('(images', content)

    def test_snortle_folder_inventory_is_clean(self) -> None:
        snortle_root = REPO_ROOT / "addons" / "enemies" / "snortle"
        self.assertEqual(
            sorted(path.name for path in snortle_root.iterdir()),
            ["README.md", "base_snortle_sheet.jpg", "frames"],
        )

    def test_ice_snortle_folder_inventory_is_clean(self) -> None:
        ice_root = REPO_ROOT / "addons" / "enemies" / "ice_snortle"
        self.assertEqual(
            sorted(path.name for path in ice_root.iterdir()),
            ["README.md", "frames", "ice_snortle_sheet.jpg"],
        )

    def _assert_sprite_image_refs_exist(self, sprite_path: Path) -> None:
        missing: list[str] = []
        for image_ref in self._sprite_image_refs(sprite_path):
            image_path = (sprite_path.parent / image_ref).resolve()
            if not image_path.exists():
                missing.append(f"{sprite_path.relative_to(REPO_ROOT)} -> {image_ref}")

        self.assertEqual(
            missing,
            [],
            "missing image references:\n" + "\n".join(missing),
        )

    def test_base_snortle_sprite_references_exist(self) -> None:
        self._assert_sprite_image_refs_exist(REPO_ROOT / "addons" / "enemies" / "snortle.sprite")

    def test_base_snortle_sprite_uses_expected_frames(self) -> None:
        self.assertEqual(
            self._sprite_image_refs(REPO_ROOT / "addons" / "enemies" / "snortle.sprite"),
            [
                "snortle/frames/crawl-0.png",
                "snortle/frames/crawl-1.png",
                "snortle/frames/windup.png",
                "snortle/frames/fire.png",
                "snortle/frames/squished.png",
            ],
        )

    def test_ice_snortle_sprite_references_exist(self) -> None:
        self._assert_sprite_image_refs_exist(REPO_ROOT / "addons" / "enemies" / "ice_snortle.sprite")

    def test_ice_snortle_sprite_uses_expected_frames(self) -> None:
        self.assertEqual(
            self._sprite_image_refs(REPO_ROOT / "addons" / "enemies" / "ice_snortle.sprite"),
            [
                "ice_snortle/frames/ice-snortle-crawl-0.png",
                "ice_snortle/frames/ice-snortle-crawl-1.png",
                "ice_snortle/frames/ice-snortle-windup.png",
                "ice_snortle/frames/ice-snortle-fire.png",
                "ice_snortle/frames/ice-snortle-squished.png",
            ],
        )

    def test_halloween_expansion_sprite_references_exist(self) -> None:
        expansion_sprites = sorted((REPO_ROOT / "addons" / "halloween-expansion" / "sprites").glob("*.sprite"))
        self.assertGreater(len(expansion_sprites), 0)
        for sprite_path in expansion_sprites:
            self._assert_sprite_image_refs_exist(sprite_path)

    def test_halloween_expansion_sprites_have_valid_structure(self) -> None:
        expansion_sprites = sorted((REPO_ROOT / "addons" / "halloween-expansion" / "sprites").glob("*.sprite"))
        for sprite_path in expansion_sprites:
            content = sprite_path.read_text(encoding="utf-8")
            self.assertTrue(content.lstrip().startswith("(supertux-sprite"), sprite_path.name)
            self.assertEqual(content.count("("), content.count(")"), f"unbalanced parentheses in {sprite_path.name}")
            self.assertGreaterEqual(content.count("(action"), 1, f"{sprite_path.name} needs at least one action")

    def test_halloween_expansion_sprite_inventory_is_complete(self) -> None:
        expansion_root = REPO_ROOT / "addons" / "halloween-expansion" / "sprites"
        self.assertEqual(
            sorted(path.name for path in expansion_root.glob("*.sprite")),
            [
                "arachnia_boss.sprite",
                "ghost_blue.sprite",
                "ghost_green.sprite",
                "ghost_white.sprite",
                "jackolantern_powerup.sprite",
                "phantom_bat.sprite",
                "pumpkin_tux.sprite",
                "underworld_imp.sprite",
                "webweaver.sprite",
            ],
        )

    def test_halloween_expansion_sprite_inventory_matches_manifest(self) -> None:
        manifest = self._load_manifest()
        halloween = next(asset_set for asset_set in manifest["assetSets"] if asset_set["name"] == "halloween-expansion")
        expected = sorted(halloween["requiredSprites"])
        actual = sorted(path.name for path in (REPO_ROOT / "addons" / "halloween-expansion" / "sprites").glob("*.sprite"))
        self.assertEqual(actual, expected)

    def test_snortle_assets_are_organized(self) -> None:
        base_dir = REPO_ROOT / "addons" / "enemies" / "snortle"
        ice_dir = REPO_ROOT / "addons" / "enemies" / "ice_snortle"

        self.assertTrue((base_dir / "base_snortle_sheet.jpg").exists())
        self.assertTrue((base_dir / "frames").is_dir())
        self.assertEqual(
            sorted(path.name for path in (base_dir / "frames").glob("*.png")),
            [
                "crawl-0.png",
                "crawl-1.png",
                "fire.png",
                "squished.png",
                "windup.png",
            ],
        )

        self.assertTrue((ice_dir / "ice_snortle_sheet.jpg").exists())
        self.assertTrue((ice_dir / "frames").is_dir())
        self.assertEqual(
            sorted(path.name for path in (ice_dir / "frames").glob("*.png")),
            [
                "ice-snortle-crawl-0.png",
                "ice-snortle-crawl-1.png",
                "ice-snortle-fire.png",
                "ice-snortle-squished.png",
                "ice-snortle-windup.png",
            ],
        )

    def test_halloween_asset_inventory_matches_readme(self) -> None:
        art_root = REPO_ROOT / "addons" / "halloween-expansion" / "art"
        expected_files = {
            art_root / "bosses" / "arachnia_boss_sheet.jpg",
            art_root / "enemies" / "phantom_bat_sheet.jpg",
            art_root / "enemies" / "underworld_imp_sheet.jpg",
            art_root / "enemies" / "wailing_phantoms_sheet.jpg",
            art_root / "enemies" / "webweaver_sheet.jpg",
            art_root / "powerups" / "jackolantern_powerup_and_pumpkin_tux.jpg",
            art_root / "reference" / "phantom_bat_legacy_sheet.jpg",
            art_root / "reference" / "ice_snortle_legacy_sheet.jpg",
        }

        missing = sorted(str(path.relative_to(REPO_ROOT)) for path in expected_files if not path.exists())
        self.assertEqual(missing, [], f"missing halloween expansion assets: {missing}")


if __name__ == "__main__":
    unittest.main()