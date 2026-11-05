"""WICKLIGHT shared art library.

Everything visual in the project is generated from this file so the style stays
consistent: one master palette, one 16x16 grid, one bitmap font, one outline colour.
Run `python3 tools/build_all.py` to regenerate every PNG in the project.
"""
from PIL import Image, ImageDraw
import random

TILE = 16

# --------------------------------------------------------------------------
# MASTER PALETTE  (28 colours)  key -> (name, rgb)
# --------------------------------------------------------------------------
PALETTE = {
    'K': ("Soot Outline",     (13, 11, 26)),
    'N': ("Abyss Navy",       (26, 26, 46)),
    'D': ("Stone Dark",       (38, 50, 74)),
    'M': ("Stone Mid",        (59, 77, 107)),
    'L': ("Stone Light",      (90, 115, 148)),
    'H': ("Stone Highlight",  (138, 162, 191)),
    't': ("Deep Water",       (20, 57, 74)),
    'u': ("Water",            (31, 111, 120)),
    'v': ("Water Light",      (79, 179, 169)),
    'f': ("Foam",             (168, 230, 207)),
    'g': ("Moss Dark",        (62, 107, 58)),
    'G': ("Moss Light",       (110, 162, 75)),
    'b': ("Wood Dark",        (74, 44, 42)),
    'n': ("Wood Mid",         (122, 74, 53)),
    'l': ("Wood Light",       (168, 113, 74)),
    'R': ("Flame Red",        (184, 59, 59)),
    'O': ("Flame Orange",     (240, 123, 63)),
    'A': ("Flame Amber",      (255, 184, 77)),
    'Y': ("Flame Yellow",     (255, 224, 138)),
    'W': ("White Hot",        (255, 246, 214)),
    'C': ("Wax",              (239, 227, 200)),
    'S': ("Wax Shadow",       (201, 180, 143)),
    'F': ("Frost Light",      (191, 233, 255)),
    'I': ("Frost Mid",        (127, 184, 224)),
    'P': ("Moth Violet",      (107, 90, 158)),
    'p': ("Moth Dusk",        (61, 50, 99)),
    'Z': ("Bronze Dark",      (140, 106, 47)),
    'z': ("Bronze",           (201, 151, 58)),
}
RGB = {k: v[1] for k, v in PALETTE.items()}


def rgba(key, a=255):
    r, g, b = RGB[key]
    return (r, g, b, a)


def from_map(rows, w=None, h=None, ox=0, oy=0, img=None):
    """Convert a list of palette-key strings into an RGBA image ('.' / ' ' = transparent)."""
    w = w or max(len(r) for r in rows)
    h = h or len(rows)
    img = img or Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in RGB and 0 <= x + ox < img.width and 0 <= y + oy < img.height:
                px[x + ox, y + oy] = rgba(ch)
    return img


def mirror_half(rows):
    return [r + r[::-1] for r in rows]


def recolor(img, mapping):
    """Swap palette colours, mapping = {'O':'I', ...}."""
    out = img.copy()
    px = out.load()
    lut = {RGB[a]: RGB[b] for a, b in mapping.items()}
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a and (r, g, b) in lut:
                px[x, y] = lut[(r, g, b)] + (a,)
    return out


def scale(img, s):
    return img.resize((img.width * s, img.height * s), Image.NEAREST)


# --------------------------------------------------------------------------
# PLAYER: "PIP" the candle-wick (16x16)
# --------------------------------------------------------------------------
FLAME = {
    'idle0': [
        ".......KK.......",
        "......KOAK......",
        "......KAYK......",
        ".....KOYWAK.....",
        ".....KAYWYK.....",
        "....KOAYWYOK....",
        "....KRAYYAOK....",
        ".....KROORK.....",
    ],
    'idle1': [
        "........K.......",
        ".......KOK......",
        "......KOAK......",
        ".....KOAYAK.....",
        ".....KAYWYK.....",
        "....KOAYWYAK....",
        "....KRAYYAOK....",
        ".....KROORK.....",
    ],
    'run': [
        "...KK...........",
        "...KOKK.........",
        "....KAOKK.......",
        "....KOAYAK......",
        "....KOAYWAK.....",
        "....KOAYWYOK....",
        "....KRAYYAOK....",
        ".....KROORK.....",
    ],
    'jump': [
        ".......KK.......",
        "......KOAK......",
        "......KAYK......",
        "......KYWK......",
        ".....KAYWAK.....",
        ".....KAYWYK.....",
        "....KRAYYAOK....",
        ".....KROORK.....",
    ],
    'fall': [
        "................",
        "....K......K....",
        "....KO....OK....",
        "....KOK..KAK....",
        ".....KAKKAYK....",
        "....KOAYWYOK....",
        "....KRAYYAOK....",
        ".....KROORK.....",
    ],
}
BODY = {
    'open': [
        "....KCCKKCSK....",
        "....KCCCCCSK....",
        "....KCCKCCKK....",
        "....KCCKCCKK....",
        "....KCOCCCOK....",
        "....KSCCCSSK....",
        "....KKKKKKKK....",
    ],
    'look_up': [
        "....KCCKKCSK....",
        "....KCCKCCKK....",
        "....KCCKCCKK....",
        "....KCCCCCSK....",
        "....KCOCCCOK....",
        "....KSCCCSSK....",
        "....KKKKKKKK....",
    ],
    'shut': [
        "....KCCKKCSK....",
        "....KCCCCCSK....",
        "....KCCCCCSK....",
        "....KCKKCKKK....",
        "....KCOCCCOK....",
        "....KSCCCSSK....",
        "....KKKKKKKK....",
    ],
}
FEET = {
    'stand': ".....KK..KK.....",
    'stride': "....KK....KK....",
    'pass': "......KKKK......",
    'tuck': "................",
}


def pip_frame(flame='idle0', body='open', feet='stand', bob=0, hurt=False):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    rows = FLAME[flame] + BODY[body] + [FEET[feet]]
    from_map(rows, 16, 16, 0, bob, img)
    if feet == 'tuck':  # little tucked feet tight under body
        from_map(["......KK.KK....."], 16, 16, 0, 15 + bob - 1 + 1, img)
    if hurt:
        img = recolor(img, {'O': 'I', 'A': 'F', 'Y': 'F', 'R': 'P', 'W': 'F'})
    return img


PIP_ANIMS = {
    'idle': [dict(flame='idle0'), dict(flame='idle1')],
    'run': [dict(flame='run', feet='stride'), dict(flame='run', feet='pass', bob=-1),
            dict(flame='idle1', feet='stride'), dict(flame='run', feet='pass', bob=-1)],
    'jump': [dict(flame='fall', body='look_up', feet='tuck')],
    'fall': [dict(flame='jump', body='open', feet='stride')],
    'hurt': [dict(flame='idle0', body='shut', feet='pass', hurt=True)],
}


def pip_anim(name):
    return [pip_frame(**kw) for kw in PIP_ANIMS[name]]


# --------------------------------------------------------------------------
# COLLECTIBLES
# --------------------------------------------------------------------------
EMBER = [
    "...KK...",
    "..KYAK..",
    ".KYWAOK.",
    "KAWYAOOK",
    "KOYAORRK",
    ".KOORRK.",
    "..KRRK..",
    "...KK...",
]
WAX = [
    "....K...",
    "...KCK..",
    "...KCK..",
    "..KCWCK.",
    "..KCWSK.",
    ".KCWCCSK",
    ".KCCCCSK",
    ".KCCCSSK",
    "..KSSSK.",
    "...KKK..",
]
SHARD = [
    "......KK..",
    ".....KYzK.",
    "....KzYzK.",
    "...KZzYzK.",
    "..KZzzzzK.",
    "..KZzWzK..",
    ".KZZzzzK..",
    ".KZZzzK...",
    "..KZZK....",
    "...KK.....",
]


def ember_frames():
    frames = []
    sparks = [(3, 2), (12, 4), (12, 11), (3, 11)]
    for i, bob in enumerate([0, -1, -1, 0]):
        im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        from_map(EMBER, ox=4, oy=4 + bob, img=im)
        sx, sy = sparks[i]
        im.putpixel((sx, sy + bob), rgba('Y'))
        frames.append(im)
    return frames


def wax_frames():
    out = []
    for bob in (0, -1):
        im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        from_map(WAX, ox=4, oy=4 + bob, img=im)
        out.append(im)
    return out


def shard_frames():
    out = []
    glints = [(5, 1), (6, 3), (5, 5), (4, 7)]
    for i, (gx, gy) in enumerate(glints):
        im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        bob = [0, -1, -1, 0][i]
        from_map(SHARD, ox=3, oy=3 + bob, img=im)
        im.putpixel((3 + gx, 3 + gy + bob), rgba('W'))
        out.append(im)
    return out


# --------------------------------------------------------------------------
# ENEMIES / HAZARDS
# --------------------------------------------------------------------------
MOTH_BODY = [
    "................",
    "................",
    "......K..K......",
    ".......KK.......",
    "......KPPK......",
    ".....KWPPWK.....",
    "......KppK......",
    "......KPpK......",
    "......KppK......",
    ".......KK.......",
]
WING_UP = mirror_half([
    "KKK.....",
    "KFFKK...",
    "KFIIFK..",
    "KFIPIFK.",
    ".KFIIIKK",
    "..KKFIK.",
    "....KK..",
])
WING_DOWN = mirror_half([
    "........",
    "........",
    "........",
    "........",
    "........",
    "..KKKKKK",
    ".KFFIIKK",
    "KFIPIIK.",
    "KFIIIK..",
    "KFFKK...",
    ".KK.....",
])


def moth_frames():
    out = []
    for wing in (WING_UP, WING_DOWN):
        im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        from_map(wing, 16, 16, 0, 2, im)
        from_map(MOTH_BODY, 16, 16, 0, 2, im)
        out.append(im)
    return out


ICICLE = [
    ".KKKKKKKKKKKKKK.",
    ".KFFFFIFFFFFIIK.",
    "..KFFIKKFFIIKK..",
    "..KFIK.KFIIK....",
    "...KIK.KFIK.....",
    "...KK..KFIK.....",
    ".......KFIK.....",
    ".......KIK......",
    ".......KIK......",
    "........K.......",
]


def icicle_frames():
    a = from_map(ICICLE, 16, 16)
    b = from_map(ICICLE, 16, 16)
    b.putpixel((8, 10), rgba('F'))  # forming drip
    b.putpixel((8, 11), rgba('I'))
    return [a, b]


# --------------------------------------------------------------------------
# OBJECTS
# --------------------------------------------------------------------------
SCONCE = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "......KKKK......",
    "......KCSK......",
    "......KCSK......",
    "...KKKKKKKKKK...",
    "...KYzzzzzzZK...",
    "....KZzzzzZK....",
    "......KZZK......",
    "......KzZK......",
    ".....KKKKKK.....",
]
SCONCE_FLAME = [
    [".......K", "......KOK", "......KAK", ".....KAYAK", ".....KAWAK", "......KRK"],
    ["........", ".......KK", "......KOK", ".....KAYK", ".....KAWAK", "......KRK"],
]


def sconce_frames():
    unlit = from_map(SCONCE, 16, 16)
    unlit = recolor(unlit, {'Y': 'z'})
    unlit.putpixel((7, 6), rgba('K'))
    unlit.putpixel((8, 5), rgba('M'))  # smoke wisp
    lit = []
    for f in SCONCE_FLAME:
        im = from_map(SCONCE, 16, 16)
        from_map(f, 16, 16, 1, 1, im)
        lit.append(im)
    return [unlit] + lit


def bell(ringing=False):
    """32x32 Great Bell exit (procedural so the curve is smooth)."""
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    px = im.load()
    # wooden yoke beam
    for x in range(2, 30):
        for y in range(0, 4):
            c = 'n' if y in (1, 2) else 'b'
            if y == 1 and x % 6 == 0:
                c = 'l'
            px[x, y] = rgba(c)
        px[x, 0] = rgba('K')
        px[x, 4] = rgba('K')
    for y in range(0, 5):
        px[1, y] = rgba('K'); px[30, y] = rgba('K')
    # crown
    for y in range(5, 8):
        for x in range(13, 19):
            px[x, y] = rgba('Z' if x > 16 else 'z')
        px[12, y] = rgba('K'); px[19, y] = rgba('K')
    # bell body: half-width per row
    hw = {}
    for i, y in enumerate(range(8, 27)):
        t = i / 18
        hw[y] = int(5 + 3 * t + 5 * t ** 3)
    hw[27] = 14; hw[28] = 14
    cx = 15.5
    for y, w in hw.items():
        x0, x1 = int(cx - w), int(cx + w)
        for x in range(x0, x1 + 1):
            rel = (x - x0) / max(1, (x1 - x0))
            if rel < 0.18: c = 'z'
            elif rel < 0.32: c = 'Y' if y < 24 else 'z'
            elif rel < 0.7: c = 'z'
            elif rel < 0.86: c = 'Z'
            else: c = 'b'
            if y in (22, 23): c = {'z': 'Z', 'Y': 'z', 'Z': 'b', 'b': 'b'}[c]  # engraved band
            if y >= 27: c = 'Z' if rel > 0.5 else 'z'
            px[x, y] = rgba(c)
        px[x0 - 1, y] = rgba('K'); px[x1 + 1, y] = rgba('K')
    for x in range(int(cx - 5) - 1, int(cx + 5) + 2):
        px[x, 7] = rgba('K')
    for x in range(1, 31):
        px[x, 29] = rgba('K')
    # rune glyph on the band
    for x in (11, 13, 15, 17, 19):
        px[x, 22] = rgba('A' if ringing else 'Y')
    # crack
    for (x, y) in [(20, 12), (21, 13), (20, 14), (21, 15), (22, 16)]:
        px[x, y] = rgba('K')
    # clapper
    for y in (29, 30):
        for x in (14, 15, 16, 17):
            px[x, y] = rgba('K')
    px[15, 30] = rgba('Z'); px[16, 30] = rgba('Z')
    px[15, 31] = rgba('K'); px[16, 31] = rgba('K')
    if ringing:
        for (x, y) in [(0, 12), (0, 13), (1, 11), (1, 14), (31, 12), (31, 13), (30, 11), (30, 14),
                       (3, 16), (3, 17), (28, 16), (28, 17)]:
            px[x, y] = rgba('W')
    return im


# --------------------------------------------------------------------------
# TILES (procedural with fixed seeds so output is deterministic)
# --------------------------------------------------------------------------
def _bricks(face, face2, mortar, hi, seed):
    rnd = random.Random(seed)
    im = Image.new("RGBA", (16, 16), rgba(mortar))
    px = im.load()
    for row in range(4):
        y0 = row * 4
        off = 0 if row % 2 == 0 else 4
        for bx in range(-1, 3):
            x0 = bx * 8 + off
            for y in range(y0, y0 + 3):
                for x in range(x0, x0 + 7):
                    if 0 <= x < 16:
                        c = face if rnd.random() > 0.18 else face2
                        if y == y0 or x == x0:
                            c = hi
                        px[x, y] = rgba(c)
    return im


def tile_stone():
    return _bricks('M', 'D', 'K', 'L', 3)


def tile_stone_top():
    im = _bricks('M', 'D', 'K', 'L', 3)
    px = im.load()
    moss = ["GGGGGGGGGGGGGGGG", "gGGgGGGggGGGgGGg", "g.gg.gg..gg.g.gg", "..g...g...g....g"]
    for y, row in enumerate(moss):
        for x, ch in enumerate(row):
            if ch != '.':
                px[x, y] = rgba(ch)
    for x in range(16):
        if x % 5 == 2:
            px[x, 0] = rgba('f')  # dew catching light
    return im


def tile_stone_bg():
    im = _bricks('D', 'N', 'K', 'M', 11)
    return im


def tile_window_top():
    im = tile_stone_bg()
    px = im.load()
    for y in range(4, 16):
        for x in range(3, 13):
            r = ((x - 7.5) ** 2) / 25 + ((y - 9) ** 2) / 25
            if y >= 9 or r < 1:
                px[x, y] = rgba('t')
    for y in range(4, 16):
        for x in range(2, 14):
            if px[x, y][:3] != RGB['t'] and any(
                    0 <= x + dx < 16 and px[x + dx, y][:3] == RGB['t'] for dx in (-1, 1)):
                px[x, y] = rgba('K')
    for y in range(6, 16):
        px[7, y] = rgba('K'); px[8, y] = rgba('K')
    px[5, 8] = rgba('F'); px[10, 12] = rgba('f')  # stars
    return im


def tile_window_bottom():
    im = tile_stone_bg()
    px = im.load()
    for y in range(0, 12):
        for x in range(3, 13):
            px[x, y] = rgba('t')
        px[2, y] = rgba('K'); px[13, y] = rgba('K')
        px[7, y] = rgba('K'); px[8, y] = rgba('K')
    for x in range(1, 15):
        px[x, 12] = rgba('H'); px[x, 13] = rgba('L'); px[x, 14] = rgba('K')
    px[4, 3] = rgba('I'); px[11, 6] = rgba('F')
    return im


def tile_plank():
    rows = [
        "KKKKKKKKKKKKKKKK",
        "llllllllllllllll",
        "nnnlnnnnnnnnlnnn",
        "nKnnnnnnnnKnnnnn",
        "bbbbbbbbbbbbbbbb",
        "KKKKKKKKKKKKKKKK",
        "..KbK......KbK..",
        "..KbK......KbK..",
        "...K........K...",
    ]
    return from_map(rows, 16, 16)


def tile_crumble(stage=0):
    im = _bricks('L', 'M', 'K', 'H', 21)
    px = im.load()
    cracks = [(3, 2), (4, 3), (4, 4), (5, 5), (10, 1), (11, 2), (11, 3), (12, 4), (8, 9), (7, 10),
              (7, 11), (8, 12), (13, 10), (12, 11)]
    for (x, y) in cracks[: 8 + stage * 6]:
        px[x, y] = rgba('K')
    if stage:
        for (x, y) in [(0, 15), (1, 15), (15, 15), (6, 15), (14, 14)]:
            px[x, y] = (0, 0, 0, 0)
        for x in range(16):
            if x % 4 == 1:
                px[x, 15] = (0, 0, 0, 0)
    return im


def tile_spikes():
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    spike = ["..F..", "..K..", ".KHK.", ".KHK.", ".KHDK", "KHLDK", "KHLDK", "KHLDK", "KHLDK"]
    for i in range(3):
        from_map(spike, 16, 16, i * 5 + 1, 3, im)
    base = ["KKKKKKKKKKKKKKKK", "KMLMMLMMLMMLMMLK", "KDDDDDDDDDDDDDDK", "KKKKKKKKKKKKKKKK"]
    from_map(base, 16, 16, 0, 12, im)
    for x in (1, 6, 11):
        im.putpixel((x + 2, 2), rgba('F'))
    return im


def tile_water(frame=0, surface=True):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = im.load()
    top = 4 if surface else 0
    for y in range(top, 16):
        for x in range(16):
            depth = y - top
            c = 'u' if (surface and depth < 3) else 't'
            if surface and depth > 2 and (x + y * 3 + frame * 5) % 11 == 0:
                c = 'u'
            px[x, y] = rgba(c, 235)
    if surface:
        for x in range(16):
            wave = (x + frame * 4) % 8
            yy = top + (0 if wave < 4 else 1)
            px[x, yy] = rgba('f')
            px[x, yy + 1] = rgba('v')
    return im


def tile_chain():
    rows = [
        "......KK........",
        ".....KHLK.......",
        ".....KLDK.......",
        "......KK........",
        "......KLK.......",
        "......KHK.......",
        "......KDK.......",
        "......KK........",
        ".....KHLK.......",
        ".....KLDK.......",
        "......KK........",
        "......KLK.......",
        "......KHK.......",
        "......KDK.......",
        "......KK........",
        ".....KHLK.......",
    ]
    return from_map(rows, 16, 16)


def tile_pillar():
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = im.load()
    for y in range(16):
        for x in range(3, 13):
            c = 'L' if x < 6 else ('M' if x < 10 else 'D')
            if x == 4: c = 'H'
            if y % 8 == 0: c = 'K'
            px[x, y] = rgba(c)
        px[2, y] = rgba('K'); px[13, y] = rgba('K')
    return im


# --------------------------------------------------------------------------
# BITMAP FONT  "Belfry 5x7"
# --------------------------------------------------------------------------
GLYPHS = {
    'A': [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'B': ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    'C': [" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "],
    'D': ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    'E': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    'F': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    'G': [" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ####"],
    'H': ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'I': ["###", " # ", " # ", " # ", " # ", " # ", "###"],
    'J': ["  ###", "   # ", "   # ", "   # ", "#  # ", "#  # ", " ##  "],
    'K': ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    'L': ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    'M': ["#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"],
    'N': ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    'O': [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'P': ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    'Q': [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    'R': ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    'S': [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    'U': ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'V': ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    'W': ["#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"],
    'X': ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    'Y': ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    'Z': ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    '0': [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    '1': [" # ", "## ", " # ", " # ", " # ", " # ", "###"],
    '2': [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    '3': ["#### ", "    #", "    #", " ### ", "    #", "    #", "#### "],
    '4': ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    '5': ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    '6': [" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "],
    '7': ["#####", "    #", "   # ", "  #  ", "  #  ", "  #  ", "  #  "],
    '8': [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    '9': [" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "],
    ':': [" ", "#", " ", " ", " ", "#", " "],
    '.': [" ", " ", " ", " ", " ", " ", "#"],
    ',': ["  ", "  ", "  ", "  ", "  ", " #", "# "],
    '!': ["#", "#", "#", "#", "#", " ", "#"],
    '?': [" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "],
    '-': ["   ", "   ", "   ", "###", "   ", "   ", "   "],
    '+': ["     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "],
    '/': ["    #", "   # ", "   # ", "  #  ", " #   ", " #   ", "#    "],
    "'": ["#", "#", " ", " ", " ", " ", " "],
    'x': ["     ", "     ", "#   #", " # # ", "  #  ", " # # ", "#   #"],
    '%': ["##  #", "##  #", "   # ", "  #  ", " #   ", "#  ##", "#  ##"],
    '(': [" #", "# ", "# ", "# ", "# ", "# ", " #"],
    ')': ["# ", " #", " #", " #", " #", " #", "# "],
    '>': ["#   ", " #  ", "  # ", "   #", "  # ", " #  ", "#   "],
    '<': ["   #", "  # ", " #  ", "#   ", " #  ", "  # ", "   #"],
    '&': [" ##  ", "#  # ", " ##  ", " ## #", "#  # ", "#  # ", " ## #"],
    '=': ["    ", "    ", "####", "    ", "####", "    ", "    "],
    '|': ["#", "#", "#", "#", "#", "#", "#"],
    '#': [" # # ", "#####", " # # ", " # # ", "#####", " # # ", "     "],
    ' ': ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
}


def text_width(s, sc=1, spacing=1):
    w = 0
    for ch in s:
        g = GLYPHS.get(ch.upper() if ch != 'x' else ch, GLYPHS[' '])
        w += (len(g[0]) + spacing) * sc
    return max(0, w - spacing * sc)


def text_mask(s, sc=1, spacing=1):
    w, h = text_width(s, sc, spacing), 7 * sc
    m = Image.new("L", (max(1, w), h), 0)
    px = m.load()
    x = 0
    for ch in s:
        g = GLYPHS.get(ch.upper() if ch != 'x' else ch, GLYPHS[' '])
        for gy, row in enumerate(g):
            for gx, c in enumerate(row):
                if c == '#':
                    for dy in range(sc):
                        for dx in range(sc):
                            px[x + gx * sc + dx, gy * sc + dy] = 255
        x += (len(g[0]) + spacing) * sc
    return m


def draw_text(img, s, x, y, color='W', sc=1, outline='K', shadow=True, grad=None, spacing=1,
              anchor='l'):
    """Pixel text with 1px (scaled) outline + drop shadow. grad=(top_key, bottom_key) for 2-band fill."""
    m = text_mask(s, sc, spacing)
    if anchor == 'c':
        x = x - m.width // 2
    elif anchor == 'r':
        x = x - m.width
    o = max(1, sc // 2) if sc > 1 else 1
    if shadow:
        sh = Image.new("RGBA", m.size, rgba('K'))
        img.paste(sh, (x + o, y + o * 2), m)
    if outline:
        ol = Image.new("RGBA", m.size, rgba(outline))
        for dx in (-o, 0, o):
            for dy in (-o, 0, o):
                if dx or dy:
                    img.paste(ol, (x + dx, y + dy), m)
    if grad:
        fill = Image.new("RGBA", m.size, rgba(grad[1]))
        top = Image.new("RGBA", (m.width, m.height // 2 + (sc if sc > 1 else 0)), rgba(grad[0]))
        fill.paste(top, (0, 0))
        if len(grad) > 2:  # highlight line
            hl = Image.new("RGBA", (m.width, max(1, sc // 2)), rgba(grad[2]))
            fill.paste(hl, (0, 0))
        img.paste(fill, (x, y), m)
    else:
        img.paste(Image.new("RGBA", m.size, rgba(color)), (x, y), m)
    return m.width


# --------------------------------------------------------------------------
# UI PIECES
# --------------------------------------------------------------------------
def panel(w, h, style='stone'):
    """9-slice style framed panel."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if style == 'stone':
        fill, inner, hi, lo = 'N', 'D', 'L', 'K'
    elif style == 'frost':
        fill, inner, hi, lo = 'N', 'p', 'I', 'K'
    else:  # wood
        fill, inner, hi, lo = 'b', 'n', 'l', 'K'
    d.rectangle([1, 0, w - 2, h - 1], fill=rgba('K'))
    d.rectangle([0, 1, w - 1, h - 2], fill=rgba('K'))
    d.rectangle([1, 1, w - 2, h - 2], fill=rgba(inner))
    d.rectangle([3, 3, w - 4, h - 4], fill=rgba(fill, 235))
    d.line([2, 1, w - 3, 1], fill=rgba(hi))
    d.line([1, 2, 1, h - 3], fill=rgba(hi))
    d.line([2, h - 2, w - 3, h - 2], fill=rgba(lo))
    # bronze corner rivets
    for (cx, cy) in [(3, 3), (w - 5, 3), (3, h - 5), (w - 5, h - 5)]:
        d.rectangle([cx, cy, cx + 1, cy + 1], fill=rgba('z'))
        im.putpixel((cx, cy), rgba('Y'))
    return im


def button(label, w=104, selected=False, sc=1):
    h = 17
    im = Image.new("RGBA", (w, h + 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    base, top, edge = ('O', 'A', 'Y') if selected else ('D', 'M', 'L')
    d.rectangle([1, 2, w - 2, h + 1], fill=rgba('K'))  # drop shadow
    d.rectangle([1, 0, w - 2, h - 1], fill=rgba('K'))
    d.rectangle([0, 1, w - 1, h - 2], fill=rgba('K'))
    d.rectangle([1, 1, w - 2, h - 2], fill=rgba(base))
    d.rectangle([1, 1, w - 2, h // 2 - 1], fill=rgba(top))
    d.line([2, 1, w - 3, 1], fill=rgba(edge))
    d.line([2, h - 2, w - 3, h - 2], fill=rgba('R' if selected else 'N'))
    tcol = 'K' if selected else 'C'
    draw_text(im, label, w // 2, 5, color=tcol, outline=None if selected else 'K',
              shadow=False, anchor='c')
    return im


HEART = [
    ".KK.KK.",
    "KRAKORK",
    "KAWAOOK",
    "KOAOORK",
    ".KOORK.",
    "..KRK..",
    "...K...",
]
HEART_EMPTY = [
    ".KK.KK.",
    "KDDKDDK",
    "KDMDDDK",
    "KDDDDDK",
    ".KDDDK.",
    "..KDK..",
    "...K...",
]
ICON_EMBER = [
    "..K..",
    ".KYK.",
    "KYWAK",
    "KAOOK",
    ".KRK.",
    "..K..",
]
ICON_SHARD = [
    "...KK",
    "..KYK",
    ".KzYK",
    "KZzzK",
    "KZzK.",
    ".KK..",
]
ICON_SHARD_EMPTY = [
    "...KK",
    "..KMK",
    ".KDMK",
    "KDDDK",
    "KDDK.",
    ".KK..",
]
ICON_CLOCK = [
    ".KKK.",
    "KCKCK",
    "KCKKK",
    "KCCCK",
    ".KKK.",
]
