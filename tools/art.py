"""WICKLIGHT - The Little Candle: art library.

All pixel art in the project is made here.
Every sprite and tile is written as a small text map:
one letter = one pixel, and '.' = a see-through pixel.
The letters are the colour keys in PALETTE below.

To make all the PNG files again, run:  python3 tools/build_all.py
"""
from PIL import Image, ImageDraw
import font

# --------------------------------------------------------------------------
# PALETTE (16 colours)
# --------------------------------------------------------------------------
PALETTE = {
    'K': ("Outline",        (27, 20, 35)),
    'N': ("Cave Dark",      (36, 30, 51)),
    'B': ("Cave Rock",      (51, 41, 74)),
    'D': ("Stone Dark",     (63, 74, 94)),
    'M': ("Stone",          (94, 107, 128)),
    'L': ("Stone Light",    (139, 152, 168)),
    'C': ("Candle",         (243, 230, 200)),
    'S': ("Candle Shadow",  (205, 179, 140)),
    'R': ("Flame Red",      (194, 64, 58)),
    'O': ("Flame Orange",   (240, 138, 60)),
    'Y': ("Flame Yellow",   (255, 211, 92)),
    'W': ("Flame White",    (255, 247, 217)),
    'P': ("Moth Purple",    (122, 95, 168)),
    'F': ("Moth Wing",      (201, 182, 240)),
    'n': ("Wood",           (107, 68, 48)),
    'l': ("Wood Light",     (160, 106, 63)),
}
RGB = {k: v[1] for k, v in PALETTE.items()}
TILE = 16


def rgba(key, a=255):
    return RGB[key] + (a,)


def from_map(rows, w=None, h=None):
    """Turn a text map into an RGBA image."""
    w = w or max(len(r) for r in rows)
    h = h or len(rows)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in RGB:
                img.putpixel((x, y), rgba(ch))
    return img


def scale(img, s):
    return img.resize((img.width * s, img.height * s), Image.NEAREST)


# --------------------------------------------------------------------------
# PLAYER: the little candle (16 x 16)
# --------------------------------------------------------------------------
FLAME_A = [
    "......KK........",
    ".....KOOK.......",
    ".....KOYOK......",
    "....KOYWYOK.....",
    "....KOYWYOK.....",
    ".....KRORK......",
]
FLAME_B = [
    ".......K........",
    "......KOK.......",
    ".....KOYOK......",
    ".....KYWYK......",
    "....KOYWYOK.....",
    ".....KRORK......",
]
FLAME_WALK = [                 # the flame leans back when walking
    ".....KK.........",
    "....KOOK........",
    ".....KOYOK......",
    "....KOYWYOK.....",
    "....KOYWYOK.....",
    ".....KRORK......",
]
BODY = [
    "....KCCKKCCK....",
    "....KCCCCCSK....",
    "....KCKCCKSK....",
    "....KCKCCKSK....",
    "....KCCCCCSK....",
    "....KCCCCSSK....",
    "....KSSSSSSK....",
    "....KKKKKKKK....",
]
BODY_LOOK_UP = [
    "....KCCKKCCK....",
    "....KCKCCKSK....",
    "....KCKCCKSK....",
    "....KCCCCCSK....",
    "....KCCCCCSK....",
    "....KCCCCSSK....",
    "....KSSSSSSK....",
    "....KKKKKKKK....",
]
FEET_STAND = ".....KK..KK....."
FEET_STEP = "....KK....KK...."
FEET_PASS = "......KKKK......"
FEET_TUCK = "................"


def candle(flame, body, feet, up=0):
    """Build one 16x16 candle frame. up=1 lifts the body by 1 pixel."""
    rows = flame + body + [feet]          # 6 + 8 + 1 = 15 rows
    rows = (["................"] if not up else []) + rows + (["................"] if up else [])
    return from_map(rows, 16, 16)


def candle_frames():
    return {
        "candle_idle": [candle(FLAME_A, BODY, FEET_STAND),
                        candle(FLAME_B, BODY, FEET_STAND)],
        "candle_walk": [candle(FLAME_WALK, BODY, FEET_STEP),
                        candle(FLAME_WALK, BODY, FEET_PASS, up=1),
                        candle(FLAME_A, BODY, FEET_STEP),
                        candle(FLAME_B, BODY, FEET_PASS, up=1)],
        "candle_jump": [candle(FLAME_B, BODY_LOOK_UP, FEET_TUCK, up=1)],
    }


# --------------------------------------------------------------------------
# EMBER (collectible), MOTH (enemy), DOOR (exit)
# --------------------------------------------------------------------------
EMBER_A = [
    "................",
    "................",
    "................",
    ".......KK.......",
    "......KYYK......",
    ".....KYWWYK.....",
    "....KOYWWYOK....",
    "....KOYYYYOK....",
    ".....KOOOOK.....",
    "......KRRK......",
    ".......KK.......",
    "................",
    "................",
    "................",
    "................",
    "................",
]
EMBER_B = [                    # second frame: little sparkles
    "................",
    "................",
    "...Y........Y...",
    ".......KK.......",
    "......KYYK......",
    ".....KYWWYK.....",
    "....KOYWWYOK....",
    "....KOYYYYOK....",
    ".....KOOOOK.....",
    "......KRRK......",
    ".......KK.......",
    "...Y........Y...",
    "................",
    "................",
    "................",
    "................",
]
MOTH_UP = [                    # wings up
    "................",
    "................",
    "KKK..........KKK",
    "KFFKK......KKFFK",
    "KFPFFK.KK.KFFPFK",
    "KFFFPFKPPKFPFFFK",
    ".KFFFFKYYKFFFFK.",
    "..KKFFKPPKFFKK..",
    "....KKKPPKKK....",
    "......KPPK......",
    ".......KK.......",
    "................",
    "................",
    "................",
    "................",
    "................",
]
MOTH_DOWN = [                  # wings down
    "................",
    "................",
    "................",
    "................",
    ".......KK.......",
    "......KPPK......",
    "......KYYK......",
    "..KKKKKPPKKKKK..",
    ".KFFFFKPPKFFFFK.",
    "KFPFFFK..KFFFPFK",
    "KFFPFK....KFPFFK",
    "KFFKK......KKFFK",
    "KKK..........KKK",
    "................",
    "................",
    "................",
]


def door_rows(open_):
    """Exit door, 16 x 32 (two tiles tall). Closed = wood. Open = warm light."""
    rows = [
        "....KKKKKKKK....",
        "..KKLLLLLLLLKK..",
        ".KLLMMMMMMMMLLK.",
        ".KLMKKKKKKKKMLK.",
    ]
    for y in range(4, 31):
        if open_:
            inside = "KYYWWYYK" if 10 <= y <= 24 else "KOYYYYOK"
        elif y in (10, 22):
            inside = "KKKKKKKK"
        elif y == 16:
            inside = "KlnnlnYK"          # Y = door handle
        else:
            inside = "KlnnlnnK"
        rows.append(".KLM" + inside + "MLK.")
    rows.append(".KKKKKKKKKKKKKK.")
    return rows


# --------------------------------------------------------------------------
# TILES (16 x 16): ground top, ground, platform, spikes
# --------------------------------------------------------------------------
GROUND = [
    "MMMMMMMDMMMMMMMM",
    "MMMMMMMDMMMMMMMM",
    "MMLMMMMDMMMMLMMM",
    "MMMMMMMDMMMMMMMM",
    "MMMMMMMDMMMMMMMM",
    "MMMMMMMDMMMMMMMM",
    "MMMMMMMDMMMMMMMM",
    "DDDDDDDDDDDDDDDD",
    "MMMDMMMMMMMMMMMM",
    "MMMDMMMMMMMLMMMM",
    "MMMDMMMMMMMMMMMM",
    "MMMDMMMMMMMMMMMM",
    "MMMDMMLMMMMMMMMM",
    "MMMDMMMMMMMMMMMM",
    "MMMDMMMMMMMMMMMM",
    "DDDDDDDDDDDDDDDD",
]
GROUND_TOP = ["LLLLLLLLLLLLLLLL", "MLLLMMLLLLLMLLLM"] + GROUND[2:]
PLATFORM = [
    "LLLLLLLLLLLLLLLL",
    "MLLLMMLLLLLMLLLM",
    "MMMMMMMDMMMMMMMM",
    "MMLMMMMDMMMMLMMM",
    "MMMMMMMDMMMMMMMM",
    "DDDDDDDDDDDDDDDD",
    ".DDDDDDDDDDDDDD.",
    "..KKKKKKKKKKKK..",
] + ["................"] * 8
SPIKES = ["................"] * 7 + [
    "..R....R....R...",
    "..L....L....L...",
    ".LLM..LLM..LLM..",
    ".LMD..LMD..LMD..",
    "LLMMDLLMMDLLMMD.",
    "LMMDDLMMDDLMMDD.",
    "LMMDDLMMDDLMMDD.",
    "DDDDDDDDDDDDDDDD",
    "KKKKKKKKKKKKKKKK",
]
TILES = [  # tileset order
    ("ground_top", GROUND_TOP, "solid"),
    ("ground", GROUND, "solid"),
    ("platform", PLATFORM, "solid (stand on top)"),
    ("spikes", SPIKES, "hazard"),
]


# --------------------------------------------------------------------------
# CAVE BACKGROUND (384 x 216)
# Made from simple shapes so it is easy to read and easy to redraw.
# --------------------------------------------------------------------------
BG_W, BG_H = 384, 216
STALACTITES = [(20, 14, 30), (70, 10, 18), (118, 18, 40), (176, 12, 22), (230, 16, 34),
               (290, 10, 20), (338, 18, 38), (372, 10, 16)]          # (x, width, length)
ROCKS = [(40, 216, 70, 40), (150, 222, 60, 26), (260, 216, 80, 44), (370, 210, 50, 36)]
#        (cx, cy, rx, ry) = rock mounds along the bottom
DOTS = [(30, 90), (64, 150), (130, 70), (170, 160), (210, 100), (250, 60), (300, 150),
        (350, 80), (90, 40), (200, 30), (280, 120), (24, 180)]


def bg_pixel(x, y):
    """Colour key of the cave background at pixel (x, y)."""
    for (sx, w, ln) in STALACTITES:
        half = w // 2
        if y < ln and abs(x - sx) <= half - (y * half) // ln:
            return 'B'
    for (cx, cy, rx, ry) in ROCKS:
        if ((x - cx) * (x - cx)) * ry * ry + ((y - cy) * (y - cy)) * rx * rx <= rx * rx * ry * ry:
            return 'B'
    for (dx, dy) in DOTS:
        if (x, y) in ((dx, dy), (dx + 1, dy)):
            return 'D'
    return 'N'


def background():
    img = Image.new("RGBA", (BG_W, BG_H), rgba('N'))
    px = img.load()
    for y in range(BG_H):
        for x in range(BG_W):
            k = bg_pixel(x, y)
            if k != 'N':
                px[x, y] = rgba(k)
    return img


# --------------------------------------------------------------------------
# UI PIECES
# --------------------------------------------------------------------------
HEART = [".KK.KK.", "KRRKRRK", "KRWRRRK", "KRRRRRK", ".KRRRK.", "..KRK..", "...K..."]
HEART_EMPTY = [".KK.KK.", "KDDKDDK", "KDDDDDK", "KDDDDDK", ".KDDDK.", "..KDK..", "...K..."]
ICON_EMBER = ["..K..", ".KYK.", "KYWYK", "KOYOK", ".KRK.", "..K.."]
ICON_EMBER_EMPTY = ["..K..", ".KDK.", "KDMDK", "KDDDK", ".KDK.", "..K.."]
ICON_CLOCK = [".KKK.", "KCKCK", "KCKKK", "KCCCK", ".KKK."]


def draw_text(img, s, x, y, color='W', sc=1, anchor='l', shadow=True):
    """Pixel text with a dark outline and shadow."""
    m = font.text_mask(s, sc)
    if anchor == 'c':
        x -= m.width // 2
    elif anchor == 'r':
        x -= m.width
    o = max(1, sc // 2)
    k = Image.new("RGBA", m.size, rgba('K'))
    if shadow:
        img.paste(k, (x + o, y + o), m)
    for dx in (-o, 0, o):
        for dy in (-o, 0, o):
            if dx or dy:
                img.paste(k, (x + dx, y + dy), m)
    img.paste(Image.new("RGBA", m.size, rgba(color)), (x, y), m)
    return m.width


def panel(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill=rgba('K'))
    d.rectangle([1, 1, w - 2, h - 2], fill=rgba('D'))
    d.rectangle([3, 3, w - 4, h - 4], fill=rgba('N'))
    return im


def button(label, w=100, selected=False):
    h = 17
    im = Image.new("RGBA", (w, h + 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    face, top, text = ('O', 'Y', 'K') if selected else ('D', 'M', 'C')
    d.rectangle([0, 2, w - 1, h + 1], fill=rgba('K'))        # shadow
    d.rectangle([0, 0, w - 1, h - 1], fill=rgba('K'))        # outline
    d.rectangle([1, 1, w - 2, h - 2], fill=rgba(face))
    d.line([1, 1, w - 2, 1], fill=rgba(top))
    m = font.text_mask(label)
    im.paste(Image.new("RGBA", m.size, rgba(text)), (w // 2 - m.width // 2, 5), m)
    return im
