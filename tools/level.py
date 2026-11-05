"""WICKLIGHT - The Little Candle: the level.

The level is 24 x 12 tiles (384 x 192 pixels). It fits on one screen.
One letter = one tile:
  #  stone (ground)     =  stone platform     ^  spikes
  P  start              e  ember              M  moth (start spot)
  D  exit door (2 tiles tall, this is the top half)
  .  empty
"""
from PIL import Image
import art

ROWS = [
    "########################",
    "#......................#",
    "#......................#",
    "#......................#",
    "#.............e.M......#",
    "#............===.......#",
    "#.........e.......e....#",
    "#........===.....===...#",
    "#.....................D#",
    "#.P.e.^^....^^^.^...Me.#",
    "########################",
    "########################",
]
W, H = 24, 12
assert len(ROWS) == H and all(len(r) == W for r in ROWS), [len(r) for r in ROWS]

# Each moth flies left and right between two columns (on one row).
MOTH_PATHS = [  # (row, left column, right column)
    (4, 12, 16),
    (9, 17, 20),
]

# Player movement (used to check every jump in the level).
JUMP_UP_TILES = 3       # highest jump: 3 tiles
JUMP_ACROSS_TILES = 4   # widest gap: 4 tiles


def cell(x, y):
    if 0 <= x < W and 0 <= y < H:
        return ROWS[y][x]
    return '#'


def tile_name(x, y):
    c = cell(x, y)
    if c == '#':
        return 'ground_top' if cell(x, y - 1) != '#' else 'ground'
    return {'=': 'platform', '^': 'spikes'}.get(c)


def find(ch):
    return [(x, y) for y in range(H) for x in range(W) if ROWS[y][x] == ch]


def render(ember_taken=(), moths=None, player=None, door_open=False, show_start=False):
    """Draw the level (384 x 192). moths = list of (pixel x, pixel y, frame)."""
    tiles = {n: art.from_map(m, 16, 16) for n, m, _ in art.TILES}
    img = art.background().crop((0, 24, 384, 216))
    for y in range(H):
        for x in range(W):
            t = tile_name(x, y)
            if t:
                img.alpha_composite(tiles[t], (x * 16, y * 16))
    ember = art.from_map(art.EMBER_A, 16, 16)
    for (x, y) in find('e'):
        if (x, y) not in ember_taken:
            img.alpha_composite(ember, (x * 16, y * 16))
    dx, dy = find('D')[0]
    img.alpha_composite(art.from_map(art.door_rows(door_open)), (dx * 16, dy * 16))
    moth_imgs = [art.from_map(art.MOTH_UP, 16, 16), art.from_map(art.MOTH_DOWN, 16, 16)]
    if moths is None:
        moths = [(x * 16, y * 16, 0) for (x, y) in find('M')]
    for (mx, my, f) in moths:
        img.alpha_composite(moth_imgs[f], (mx, my))
    if show_start:
        sx, sy = find('P')[0]
        img.alpha_composite(art.candle_frames()["candle_idle"][0], (sx * 16, sy * 16))
    if player:
        sprite, px, py = player
        img.alpha_composite(sprite, (px, py))
    return img
