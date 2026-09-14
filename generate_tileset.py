from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ModuleNotFoundError as exc:  # pragma: no cover - dependency is optional in some environments
    raise SystemExit(
        "Pillow is required to generate the haunted tileset. Install it with: python3 -m pip install pillow"
    ) from exc

REPO_ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = REPO_ROOT / "addons" / "halloween-expansion" / "art" / "tilesets" / "haunted_tiles.png"


def build_haunted_tileset() -> Image.Image:
    tile_size = 32
    cols = 4
    rows = 1
    tileset = Image.new("RGBA", (tile_size * cols, tile_size * rows), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tileset)

    # Tile 0: Spooky stone brick wall
    draw.rectangle([0, 0, 31, 31], fill=(45, 50, 60))
    draw.line([0, 16, 31, 16], fill=(25, 30, 35), width=1)  # Horizontal mortar
    draw.line([16, 0, 16, 16], fill=(25, 30, 35), width=1)  # Vertical mortar top
    draw.line([8, 16, 8, 31], fill=(25, 30, 35), width=1)  # Vertical mortar bottom
    draw.line([24, 16, 24, 31], fill=(25, 30, 35), width=1)

    # Tile 1: Rotting wooden floorboards
    draw.rectangle([32, 0, 63, 31], fill=(60, 40, 30))
    draw.line([48, 0, 48, 31], fill=(35, 20, 15), width=1)  # Plank split
    draw.line([40, 0, 40, 31], fill=(80, 55, 40), width=1)  # Highlight
    draw.line([56, 0, 56, 31], fill=(80, 55, 40), width=1)

    # Tile 2: Haunted roof slate
    draw.rectangle([64, 0, 95, 31], fill=(30, 30, 40))
    for x in range(64, 96, 8):
        draw.arc([x, 4, x + 8, 16], start=0, end=180, fill=(50, 50, 65), width=1)
        draw.arc([x + 4, 16, x + 12, 28], start=0, end=180, fill=(50, 50, 65), width=1)

    # Tile 3: Cobweb corner overlay
    draw.rectangle([96, 0, 127, 31], fill=(0, 0, 0, 0))
    draw.line([96, 0, 127, 31], fill=(200, 200, 210), width=1)
    draw.line([96, 8, 119, 0], fill=(180, 180, 190), width=1)
    draw.line([104, 31, 127, 8], fill=(180, 180, 190), width=1)

    return tileset


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    tileset = build_haunted_tileset()
    tileset.save(OUTPUT_PATH)
    print(f"Haunted house tileset generated at {OUTPUT_PATH}")


if __name__ == "__main__":
    main()