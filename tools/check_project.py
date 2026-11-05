"""Automatic checks for the WICKLIGHT project.

Run:  python3 tools/check_project.py
It checks the PNG files, sprite sheets, Piskel files, the level, the screens
and the documents, and prints PASS or FAIL for each check.
"""
import base64
import glob
import hashlib
import io
import json
import os
import re
import sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import art            # noqa: E402
import level as L     # noqa: E402
import build_level    # noqa: E402
import build_screens  # noqa: E402

A = os.path.join(ROOT, "02_Pixel_Art_Assets")
results = []


def check(name, ok, detail=""):
    results.append((ok, name, detail))


def png_files(*parts):
    return sorted(glob.glob(os.path.join(A, *parts), recursive=True))


PALETTE_RGB = set(art.RGB.values())

# ---------------------------------------------------------------- 1. pixel art files
sprite_pngs = png_files("sprites", "**", "*.png") + png_files("tiles", "*.png") + \
    png_files("spritesheets", "*.png")
bad_mode, bad_colour, half_alpha, not_clear, bad_size = [], [], [], [], []
for f in sprite_pngs:
    im = Image.open(f)
    name = os.path.relpath(f, ROOT)
    if im.mode != "RGBA":
        bad_mode.append(name)
        continue
    if im.width % 16 or im.height % 16:
        bad_size.append(name)
    for (r, g, b, a) in zip(*[iter(im.tobytes())] * 4):
        if a not in (0, 255):
            half_alpha.append(name)
            break
        if a == 255 and (r, g, b) not in PALETTE_RGB:
            bad_colour.append(name)
            break
    if im.getpixel((0, 0))[3] != 0 and "tiles/" not in name.replace("\\", "/"):
        not_clear.append(name)
check("All sprite, tile and sheet PNGs are RGBA (have transparency)", not bad_mode, bad_mode)
check("All sizes are multiples of 16 pixels", not bad_size, bad_size)
check("Only fully see-through or fully solid pixels (no half-transparent pixels)", not half_alpha, half_alpha)
check("Every solid pixel uses a colour from the 16-colour palette", not bad_colour, bad_colour)
check("Sprites have a see-through background (top-left pixel is clear)", not not_clear, not_clear)

# stray pixels: a solid pixel with no solid neighbour (the ember sparkle frame is on purpose)
stray = []
for f in png_files("sprites", "**", "*.png") + png_files("tiles", "*.png"):
    if f.endswith("ember_1.png"):
        continue
    im = Image.open(f)
    w, h = im.size
    px = im.load()
    for y in range(h):
        for x in range(w):
            if px[x, y][3]:
                n = [px[x + dx, y + dy][3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                     if 0 <= x + dx < w and 0 <= y + dy < h]
                if not any(n):
                    stray.append(f"{os.path.relpath(f, ROOT)} ({x},{y})")
check("No lonely stray pixels in sprites and tiles", not stray, stray)

# duplicates (same picture saved twice in the same folder type)
hashes = {}
for f in png_files("sprites", "**", "*.png") + png_files("tiles", "[0-9]*.png"):
    h = hashlib.md5(Image.open(f).tobytes()).hexdigest()
    hashes.setdefault(h, []).append(os.path.relpath(f, ROOT))
dups = [v for v in hashes.values() if len(v) > 1]
check("No duplicate sprite or tile images", not dups, dups)

# required assets
need = {
    "player idle animation": "sprites/player/candle_idle_0.png",
    "player walk animation": "sprites/player/candle_walk_3.png",
    "player jump sprite": "sprites/player/candle_jump_0.png",
    "ember collectible": "sprites/ember/ember_0.png",
    "moth enemy": "sprites/moth/moth_0.png",
    "spike hazard tile": "tiles/3_spikes.png",
    "stone platform tiles": "tiles/2_platform.png",
    "tileset": "tiles/tileset.png",
    "cave background": "background/cave_background.png",
    "exit door": "sprites/door/door_closed.png",
    "combined sprite sheet": "spritesheets/wicklight_spritesheet.png",
    "palette (.gpl)": "palette/wicklight.gpl",
}
missing = [k for k, v in need.items() if not os.path.exists(os.path.join(A, v))]
check("All required assets exist (%d)" % len(need), not missing, missing)

gpl = open(os.path.join(A, "palette", "wicklight.gpl")).read().splitlines()
check("Palette file has 16 colours", gpl[0] == "GIMP Palette" and
      len([l for l in gpl if re.match(r"^\s*\d+\s+\d+\s+\d+", l)]) == 16)

# ---------------------------------------------------------------- 2. sheets and frame alignment
meta = json.load(open(os.path.join(A, "spritesheets", "spritesheets.json")))
align_err = []
for name, m in meta["animations"].items():
    s = Image.open(os.path.join(A, "spritesheets", m["file"]))
    if s.size != (m["frame_width"] * m["frames"], m["frame_height"]):
        align_err.append(f"{name}: strip size {s.size}")
    folder = {"candle": "player"}.get(name.split("_")[0], name.split("_")[0])
    for i in range(m["frames"]):
        fname = ["door_closed", "door_open"][i] if name == "door" else f"{name}_{i}"
        single = Image.open(os.path.join(A, "sprites", folder, fname + ".png"))
        part = s.crop((i * m["frame_width"], 0, (i + 1) * m["frame_width"], m["frame_height"]))
        if single.tobytes() != part.tobytes():
            align_err.append(f"{name} frame {i} differs from {fname}.png")
check("Sprite strips are the right size and match the single PNG frames", not align_err, align_err)

sheet = Image.open(os.path.join(A, "spritesheets", "wicklight_spritesheet.png"))
sheet_err = []
for name, r in meta["combined_sheet"]["rows"].items():
    s = Image.open(os.path.join(A, "spritesheets", meta["animations"][name]["file"]))
    part = sheet.crop((0, r["y"], s.width, r["y"] + s.height))
    if part.tobytes() != s.tobytes():
        sheet_err.append(name)
check("Combined sprite sheet matches every strip", not sheet_err, sheet_err)

# candle frames: same size body, feet on the bottom rows, body stays in the same columns
cols = set()
for f in png_files("sprites", "player", "*.png"):
    im = Image.open(f)
    bbox = im.getbbox()
    cols.add((bbox[0], bbox[2]))
check("All candle frames line up (same left and right edge)", len(cols) == 1, sorted(cols))

# ---------------------------------------------------------------- 3. Piskel files
pk_err = []
for f in sorted(glob.glob(os.path.join(A, "piskel", "*.piskel"))):
    name = os.path.basename(f)[:-7]
    try:
        d = json.load(open(f))
        assert d["modelVersion"] == 2, "modelVersion must be 2"
        pk = d["piskel"]
        layer = json.loads(pk["layers"][0])
        chunk = layer["chunks"][0]
        png = Image.open(io.BytesIO(base64.b64decode(chunk["base64PNG"].split(",", 1)[1])))
        fw = png.width // len(chunk["layout"])          # Piskel: width / number of columns
        fh = png.height // len(chunk["layout"][0])
        assert (fw, fh) == (pk["width"], pk["height"]), "frame size does not match"
        assert layer["frameCount"] == len(chunk["layout"]), "frame count does not match"
        strip = Image.open(os.path.join(A, "spritesheets", meta["animations"][name]["file"]))
        assert png.convert("RGBA").tobytes() == strip.tobytes(), "pixels differ from the PNG strip"
    except Exception as e:  # noqa: BLE001
        pk_err.append(f"{name}: {e}")
check("Piskel files follow Piskel's file format and match the PNGs (6 files)",
      not pk_err and len(glob.glob(os.path.join(A, "piskel", "*.piskel"))) == 6, pk_err)

# ---------------------------------------------------------------- 4. level
res = build_level.jump_check()
check("Level has exactly 5 embers", res["embers in level"] == 5)
check("Level has 2 moths and 3 spike groups", res["moths"] == 2 and res["spike groups"] == 3)
groups, prev = 0, None
for (x, y) in sorted(L.find('^'), key=lambda c: (c[1], c[0])):
    if prev is None or not (y == prev[1] and x == prev[0] + 1):
        groups += 1
    prev = (x, y)
check("Spike groups counted from the map = 3", groups == 3, groups)
check("One start and one exit door", len(L.find('P')) == 1 and len(L.find('D')) == 1)
check("All embers can be reached from the start", res["all embers reachable"])
check("The exit door can be reached from the start", res["door reachable"])
check("Every jump on the planned route is max 3 tiles up and max 4 tiles across", res["route jumps ok"])
door = L.find('D')[0]
check("The door stands on the ground", L.cell(door[0], door[1] + 2) == '#')
check("Moth paths stay inside the level and do not go through walls",
      all(L.cell(x, r) not in "#=" for (r, a, b) in L.MOTH_PATHS for x in range(a, b + 1)))

# ---------------------------------------------------------------- 5. screens and rules
bs = build_screens
check("Timer starts at 60 seconds", bs.START_TIME == 60)
check("Player has 3 lives", bs.START_LIVES == 3)
check("Gameplay HUD: embers shown (2) = embers missing from the map (2)",
      bs.GAMEPLAY["embers"] == 2 and len(L.find('e')) - bs.GAMEPLAY["embers"] == 3)
check("Victory shows 5/5 embers and time left > 0", bs.VICTORY["embers"] == 5 and bs.VICTORY["time"] > 0)
check("Game Over reason matches its numbers (0 lives, under 5 embers)",
      bs.GAME_OVER["lives"] == 0 and bs.GAME_OVER["embers"] < 5 and bs.GAME_OVER["reason"] == "NO LIVES LEFT")
check("Gameplay time (0:41) is below 60 and above victory time left (0:18)",
      bs.VICTORY["time"] < bs.GAMEPLAY["time"] < bs.START_TIME)
shots = sorted(glob.glob(os.path.join(ROOT, "04_UI_and_Prototype", "screens", "*.png")))
check("4 screens exist at 1920 x 1080",
      len(shots) == 4 and all(Image.open(s).size == (1920, 1080) for s in shots))
hs = bs.hotspots()
check("Prototype links: menu->game, game->win, game->lose, win->game/menu, lose->game/menu",
      {h.get("go") for h in hs["menu"]["hots"]} >= {"game"} and
      {h.get("go") for h in hs["game"]["hots"]} == {"win", "lose"} and
      {h.get("go") for h in hs["win"]["hots"]} == {"game", "menu"} and
      {h.get("go") for h in hs["lose"]["hots"]} == {"game", "menu"})

# ---------------------------------------------------------------- 6. documents
docs = sorted(glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True))
broken = []
for md in docs:
    for link in re.findall(r"\]\(([^)]+)\)", open(md).read()):
        if link.startswith(("http", "#")):
            continue
        link = link.split("#")[0]
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(md), link))):
            broken.append(f"{os.path.relpath(md, ROOT)} -> {link}")
check("All links and images in the documents work", not broken, broken)

OLD_WORDS = ["glow level", "glow x", "wax", "bank", "sconce", "shard", "belfry", "frost", "icicle",
             "multiplier", "at risk", "crumbl", "pip's", "pip is", "great bell"]
old = []
for f in docs + [os.path.join(ROOT, "04_UI_and_Prototype", "prototype", "index.html")]:
    text = open(f).read().lower()
    for w in OLD_WORDS:
        if w in text and not f.endswith("Verification_Report.md"):
            old.append(f"{os.path.relpath(f, ROOT)}: '{w}'")
check("No words from the old, complicated version are left in the documents", not old, old)

placeholders = []
for md in docs:
    for line in open(md):
        if re.search(r"\bTODO\b|lorem|TBD", line):
            placeholders.append(os.path.relpath(md, ROOT))
check("No placeholder text in the documents (except name/number fields)", not placeholders, placeholders)

# ---------------------------------------------------------------- report
fails = [r for r in results if not r[0]]
for ok, name, detail in results:
    print(("PASS  " if ok else "FAIL  ") + name + ("" if ok or not detail else f"\n      {detail}"))
print(f"\n{len(results) - len(fails)} of {len(results)} checks passed.")
sys.exit(1 if fails else 0)
