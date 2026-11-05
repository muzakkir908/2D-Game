"""Level 1 - "The Drowned Belfry": data + rendering helpers.

Legend
  #  stone (auto top/fill)     =  wooden plank (one-way)   %  crumbling stone
  ^  iron spikes (hazard)      ~  water surface (hazard)   w  deep water
  c  hanging chain (decor)     P  player start             e  ember
  d  wax drop                  b  bell shard               M  frost moth
  I  icicle (ceiling hazard)   S  sconce checkpoint        G  great bell (2x2, top-left)
"""
from PIL import Image, ImageDraw
import random
import wl
from build_assets import TILE_INDEX

# Each section is 24 columns x 14 rows. Jump budget: 3 tiles up, 4 tiles across.
S1_WICK_ROOM = [
    "########################",
    "########################",
    "#                       ",
    "#                       ",
    "#     c                 ",
    "#     c                 ",
    "#     c            e    ",
    "#     c          e   e  ",
    "#      e        =====   ",
    "#     e e    e          ",
    "#  P e                S ",
    "######  #####   ########",
    "######~~#####~~~########",
    "######ww#####www########",
]
S2_MOTH_GALLERY = [
    "########################",
    "########################",
    "                        ",
    "              M         ",
    "          e e e     b   ",
    "        =========  ===  ",
    "                        ",
    "    e                   ",
    "   ===                  ",
    "                        ",
    "  d    e  ^^^   e   e   ",
    "########################",
    "########################",
    "########################",
]
S3_FLOODED_NAVE = [
    "########################",
    "########################",
    "        I   I   I       ",
    "                        ",
    "                        ",
    "                   M    ",
    "            b e         ",
    "                        ",
    "          e     e       ",
    "           %%  %%       ",
    "  S     d             e ",
    "####~~~##~~~~~~~~~~~####",
    "####www##wwwwwwwwwww####",
    "####www##wwwwwwwwwww####",
]
S4_BELL_CLIMB = [
    "########################",
    "########################",
    "               I       #",
    "           eM   b      #",
    "          e    e    G  #",
    "         ###  ===      #",
    "                   #####",
    "      de         M  ####",
    "     ###            ####",
    "                    ####",
    " S e     ^^^^^^^^^^^####",
    "########################",
    "########################",
    "########################",
]
SECTIONS = [
    ("THE WICK-ROOM", "TEACH", S1_WICK_ROOM),
    ("MOTH GALLERY", "CHOOSE", S2_MOTH_GALLERY),
    ("FLOODED NAVE", "PRESSURE", S3_FLOODED_NAVE),
    ("BELL CLIMB", "EXAM", S4_BELL_CLIMB),
]
for _, _, sec in SECTIONS:
    assert len(sec) == 14 and all(len(r) == 24 for r in sec), [len(r) for r in sec]

ROWS = ["".join(sec[y] for _, _, sec in SECTIONS) for y in range(14)]
W, H = len(ROWS[0]), len(ROWS)
ENTITY = set("PedbMISG")

# background decoration (columns that get windows / pillars)
WINDOWS = [10, 30, 41, 54, 66, 79]
PILLARS = [17, 47, 71]


def cell(x, y):
    if 0 <= x < W and 0 <= y < H:
        return ROWS[y][x]
    return '#'


def terrain_tile(x, y):
    c = cell(x, y)
    if c == '#':
        return 'stone_top' if cell(x, y - 1) not in '#' else 'stone'
    return {'=': 'plank', '%': 'crumble', '^': 'spikes', '~': 'water_surface_0',
            'w': 'water_fill', 'c': 'chain'}.get(c)


def bg_tile(x, y):
    if y < 2:
        return None
    if x in WINDOWS and y in (3, 4):
        return 'window_top' if y == 3 else 'window_bottom'
    if x in PILLARS and 2 <= y <= 10:
        return 'pillar'
    return 'stone_bg'


def entities():
    out = []
    for y, row in enumerate(ROWS):
        for x, ch in enumerate(row):
            if ch in ENTITY:
                out.append((ch, x, y))
    return out


def count(ch):
    return sum(r.count(ch) for r in ROWS)


def render(x0=0, x1=W, frame=0, lit_sconces=(), player=None, show_start=True,
           moth_offsets=None, bg_shade=True):
    """Render columns [x0,x1) of the level at 1x. Returns RGBA image."""
    tiles = {n: t for n, t, _ in __import__('build_assets').TILESET}
    tiles['water_surface_0'] = wl.tile_water(frame % 2)
    im = Image.new("RGBA", ((x1 - x0) * 16, H * 16), wl.rgba('N'))
    # far background: dark arches silhouette
    d = ImageDraw.Draw(im)
    for x in range(x0, x1):
        for y in range(H):
            t = bg_tile(x, y)
            if t:
                im.alpha_composite(tiles[t], ((x - x0) * 16, y * 16))
    if bg_shade:  # push the background back: darken with navy veil
        veil = Image.new("RGBA", im.size, wl.rgba('N', 120))
        im.alpha_composite(veil)
    # moonlight shafts from windows
    shaft = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shaft)
    for wx in WINDOWS:
        if x0 - 6 <= wx < x1:
            bx = (wx - x0) * 16 + 3
            sd.polygon([(bx, 64), (bx + 10, 64), (bx + 58, 176), (bx + 34, 176)],
                       fill=wl.rgba('F', 22))
    im.alpha_composite(shaft)
    for x in range(x0, x1):
        for y in range(H):
            t = terrain_tile(x, y)
            if t:
                im.alpha_composite(tiles[t], ((x - x0) * 16, y * 16))
    ember = wl.ember_frames()
    wax = wl.wax_frames()
    shard = wl.shard_frames()
    moth = wl.moth_frames()
    ice = wl.icicle_frames()
    sconce = wl.sconce_frames()
    for i, (ch, x, y) in enumerate(entities()):
        if not (x0 - 2 <= x < x1):
            continue
        px, py = (x - x0) * 16, y * 16
        if ch == 'e':
            im.alpha_composite(ember[(frame + x) % 4], (px, py))
        elif ch == 'd':
            im.alpha_composite(wax[(frame + x) % 2], (px, py))
        elif ch == 'b':
            im.alpha_composite(shard[(frame + x) % 4], (px, py))
        elif ch == 'M':
            ox, oy = (moth_offsets or {}).get((x, y), (0, 0))
            im.alpha_composite(moth[(frame + x) % 2], (px + ox, py + oy))
        elif ch == 'I':
            im.alpha_composite(ice[(frame + x) % 2], (px, py))
        elif ch == 'S':
            im.alpha_composite(sconce[1 + frame % 2] if x in lit_sconces else sconce[0], (px, py))
        elif ch == 'G':
            im.alpha_composite(wl.bell(False), (px, py))
        elif ch == 'P' and show_start and player is None:
            im.alpha_composite(wl.pip_anim('idle')[0], (px, py))
    if player:
        sprite, ppx, ppy = player
        im.alpha_composite(sprite, (ppx - x0 * 16, ppy))
    return im
