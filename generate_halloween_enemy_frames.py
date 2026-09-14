from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

REPO_ROOT = Path(__file__).resolve().parent


def _save_frames(base_dir: Path, frames: list[tuple[str, Image.Image]]) -> None:
    base_dir.mkdir(parents=True, exist_ok=True)
    for name, image in frames:
        path = base_dir / f"{name}.png"
        image.save(path)


def _draw_phantom_bat(image: Image.Image, wing_offset: int) -> None:
    draw = ImageDraw.Draw(image)
    body = (8, 10, 22, 24)
    draw.ellipse(body, fill=(76, 64, 110), outline=(36, 24, 52), width=2)
    draw.polygon([(5, 14), (0, 8), (6, 16), (1, 22)], fill=(76, 64, 110))
    draw.polygon([(25, 14), (31, 8), (26, 16), (30, 22)], fill=(76, 64, 110))
    draw.polygon([(8, 14), (10, 4), (18, 10), (16, 18)], fill=(76, 64, 110))
    draw.polygon([(20, 14), (21, 4), (26, 10), (23, 18)], fill=(76, 64, 110))
    draw.ellipse((13, 14, 17, 18), fill=(255, 80, 80))
    draw.line((15, 18, 15, 22), fill=(180, 50, 50), width=2)
    draw.line((9, 22, 22, 22), fill=(40, 28, 52), width=2)
    draw.line((15, 24, 15 + wing_offset, 28), fill=(120, 100, 150), width=2)
    draw.line((15, 24, 15 - wing_offset, 28), fill=(120, 100, 150), width=2)


def _draw_underworld_imp(image: Image.Image, pose: str) -> None:
    draw = ImageDraw.Draw(image)
    if pose == "taunt":
        draw.ellipse((8, 8, 24, 22), fill=(200, 70, 40), outline=(90, 25, 20), width=2)
        draw.line((16, 22, 16, 30), fill=(120, 35, 25), width=3)
        draw.line((16, 14, 10, 10), fill=(120, 35, 25), width=2)
        draw.line((16, 14, 22, 10), fill=(120, 35, 25), width=2)
        draw.ellipse((13, 15, 18, 19), fill=(255, 120, 80))
    elif pose == "leap":
        draw.ellipse((8, 10, 24, 24), fill=(210, 80, 45), outline=(100, 30, 20), width=2)
        draw.line((16, 24, 12, 29), fill=(130, 45, 25), width=2)
        draw.line((16, 24, 20, 29), fill=(130, 45, 25), width=2)
        draw.line((8, 15, 5, 10), fill=(120, 35, 25), width=2)
        draw.line((24, 15, 27, 10), fill=(120, 35, 25), width=2)
        draw.ellipse((13, 15, 18, 19), fill=(255, 120, 80))
    else:
        draw.ellipse((10, 12, 22, 22), fill=(180, 70, 40), outline=(90, 25, 20), width=2)
        draw.line((16, 22, 16, 28), fill=(120, 35, 25), width=3)
        draw.line((11, 15, 15, 14), fill=(255, 120, 80), width=2)
        draw.line((17, 15, 21, 14), fill=(255, 120, 80), width=2)
        draw.ellipse((13, 15, 18, 18), fill=(255, 120, 80))


def _draw_webweaver(image: Image.Image, pose: str) -> None:
    draw = ImageDraw.Draw(image)
    draw.ellipse((9, 12, 22, 23), fill=(52, 90, 42), outline=(28, 42, 22), width=2)
    draw.line((16, 23, 16, 29), fill=(45, 70, 36), width=2)
    draw.line((11, 18, 5, 16), fill=(55, 90, 45), width=2)
    draw.line((21, 18, 27, 16), fill=(55, 90, 45), width=2)
    draw.line((8, 21, 4, 29), fill=(45, 70, 36), width=2)
    draw.line((24, 21, 28, 29), fill=(45, 70, 36), width=2)
    if pose == "spit":
        draw.line((22, 16, 30, 8), fill=(220, 220, 220), width=2)
        draw.line((23, 17, 32, 10), fill=(200, 200, 200), width=2)
    elif pose == "defeated":
        draw.ellipse((8, 18, 24, 24), fill=(95, 120, 90), outline=(50, 72, 58), width=2)
        draw.line((16, 24, 16, 30), fill=(60, 80, 70), width=2)
    draw.ellipse((13, 15, 18, 18), fill=(255, 80, 80))


def _draw_ghost(image: Image.Image, color: tuple[int, int, int], glow: tuple[int, int, int], drift: int) -> None:
    draw = ImageDraw.Draw(image)
    body = [(8, 10), (12, 6), (20, 6), (24, 10), (24, 22), (20, 26), (12, 26), (8, 22)]
    draw.polygon(body, fill=color, outline=(200, 200, 220), width=1)
    draw.line((12, 18, 16, 18), fill=(240, 240, 240), width=2)
    draw.line((16, 18, 20, 18), fill=(240, 240, 240), width=2)
    draw.ellipse((12, 16, 14, 18), fill=(255, 255, 255))
    draw.ellipse((18, 16, 20, 18), fill=(255, 255, 255))
    draw.line((12, 22, 12 + drift, 28), fill=glow, width=2)
    draw.line((20, 22, 20 - drift, 28), fill=glow, width=2)


def _draw_arachnia(image: Image.Image, phase: str) -> None:
    draw = ImageDraw.Draw(image)
    if phase == "hang":
        draw.ellipse((10, 8, 22, 20), fill=(90, 80, 110), outline=(45, 42, 60), width=2)
        draw.line((11, 20, 8, 26), fill=(60, 50, 100), width=2)
        draw.line((21, 20, 24, 26), fill=(60, 50, 100), width=2)
        draw.ellipse((13, 12, 18, 16), fill=(255, 80, 80))
    elif phase == "rearing":
        draw.ellipse((8, 10, 24, 22), fill=(100, 85, 120), outline=(50, 42, 68), width=2)
        draw.line((16, 22, 16, 30), fill=(60, 50, 100), width=2)
        draw.line((14, 12, 8, 6), fill=(60, 50, 100), width=2)
        draw.line((18, 12, 24, 6), fill=(60, 50, 100), width=2)
        draw.ellipse((13, 15, 18, 19), fill=(255, 80, 80))
    elif phase == "lunge":
        draw.ellipse((8, 12, 24, 24), fill=(100, 85, 120), outline=(50, 42, 68), width=2)
        draw.line((16, 24, 16, 30), fill=(60, 50, 100), width=2)
        draw.line((14, 12, 8, 8), fill=(60, 50, 100), width=2)
        draw.line((18, 12, 24, 8), fill=(60, 50, 100), width=2)
        draw.line((16, 26, 28, 28), fill=(60, 50, 100), width=2)
        draw.ellipse((13, 15, 18, 19), fill=(255, 80, 80))
    elif phase == "slam":
        draw.ellipse((10, 13, 22, 25), fill=(90, 80, 110), outline=(45, 42, 60), width=2)
        draw.line((14, 25, 14, 30), fill=(60, 50, 100), width=2)
        draw.line((18, 25, 18, 30), fill=(60, 50, 100), width=2)
        draw.ellipse((12, 16, 18, 20), fill=(255, 80, 80))
    else:
        draw.ellipse((10, 14, 22, 22), fill=(90, 80, 110), outline=(45, 42, 60), width=2)
        draw.line((16, 22, 16, 28), fill=(60, 50, 100), width=2)
        draw.ellipse((13, 17, 18, 20), fill=(255, 80, 80))


def generate_indexed_frames() -> None:
    # Phantom bat
    bat_dir = REPO_ROOT / "addons" / "halloween-expansion" / "art" / "enemies" / "phantom_bat" / "frames"
    bat_frames = []
    for idx in range(2):
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        _draw_phantom_bat(img, 4 + idx)
        bat_frames.append((f"hang-{idx}", img.copy()))
    for idx in range(2):
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        _draw_phantom_bat(img, 6 + idx)
        bat_frames.append((f"swoop-{idx}", img.copy()))
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    _draw_phantom_bat(img, 3)
    bat_frames.append(("defeated", img.copy()))
    _save_frames(bat_dir, bat_frames)

    # Underworld imp
    imp_dir = REPO_ROOT / "addons" / "halloween-expansion" / "art" / "enemies" / "underworld_imp" / "frames"
    imp_frames = []
    for pose in ["taunt", "leap", "defeated"]:
        for idx in range(2):
            img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
            _draw_underworld_imp(img, pose if pose != "leap" or idx == 0 else "leap")
            imp_frames.append((f"{pose}-{idx}", img.copy()))
    _save_frames(imp_dir, imp_frames)

    # Webweaver
    web_dir = REPO_ROOT / "addons" / "halloween-expansion" / "art" / "enemies" / "webweaver" / "frames"
    web_frames = []
    for idx in range(2):
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        _draw_webweaver(img, "crawl")
        web_frames.append((f"crawl-{idx}", img.copy()))
    for idx in range(2):
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        _draw_webweaver(img, "spit")
        web_frames.append((f"spit-web-{idx}", img.copy()))
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    _draw_webweaver(img, "defeated")
    web_frames.append(("defeated", img.copy()))
    _save_frames(web_dir, web_frames)

    # Wailing phantoms
    ghost_dir = REPO_ROOT / "addons" / "halloween-expansion" / "art" / "enemies" / "wailing_phantoms" / "frames"
    ghost_frames = []
    for color, accent in [("white", (220, 220, 220)), ("green", (110, 255, 120)), ("blue", (120, 180, 255))]:
        for idx in range(2):
            img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
            _draw_ghost(img, (220, 220, 220) if color == "white" else (120, 255, 120) if color == "green" else (120, 180, 255), accent, idx)
            ghost_frames.append((f"{color}-{idx}", img.copy()))
    _save_frames(ghost_dir, ghost_frames)

    # Arachnia boss
    arach_dir = REPO_ROOT / "addons" / "halloween-expansion" / "art" / "bosses" / "arachnia" / "frames"
    arach_frames = []
    for phase, idxs in {"hang": 2, "rearing": 2, "lunge": 2, "slam": 1, "defeated": 1}.items():
        for idx in range(idxs):
            img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            _draw_arachnia(img, phase)
            arach_frames.append((f"{phase}-{idx}", img.copy()))
    _save_frames(arach_dir, arach_frames)


if __name__ == "__main__":
    generate_indexed_frames()
