"""Builds 03_Level_Design/: maps, annotated design sheet, Tiled export, CSV/ASCII data."""
import csv
import json
import os
from PIL import Image, ImageDraw
import wl
import level as L
from build_assets import TILE_INDEX, TILESET, TS_COLS

OUT = os.path.join(os.path.dirname(__file__), "..", "03_Level_Design")
os.makedirs(os.path.join(OUT, "data"), exist_ok=True)

MAIN_ROUTE = [(3, 10), (5, 10), (6.5, 8.6), (8, 10), (12, 10), (14, 8.4), (16, 10), (22, 10),
              (26, 10), (33, 10), (35, 8.2), (37, 10), (47, 10), (51, 10), (53, 8.8), (55.5, 10),
              (57.5, 7.4), (59.5, 8), (61.5, 6.6), (63.5, 8), (66, 7.2), (68, 9), (70, 10),
              (73, 10), (75.5, 7.8), (78, 7), (80, 5.2), (82, 4), (84, 3.2), (87, 4), (89.5, 3.6),
              (92, 5)]
RISK_ROUTES = [
    [(16, 10), (16.5, 7.4), (17, 7), (21, 7), (22, 8.5), (22.5, 10)],
    [(25, 10), (26.5, 8), (28, 7), (29.5, 5.2), (32, 4), (40, 4), (42, 3.2), (44, 4), (45, 4),
     (46, 6.5), (47, 10)],
]
CALLOUTS = [
    (3, 10, "START", "Flat, safe runway. Learn to move with zero threat."),
    (5, 10, "FIRST EMBER", "Lies in your path. Glow rises to x2 on pickup."),
    (6.5, 9, "FIRST GAP", "2-tile water gap. Embers trace the jump arc."),
    (14, 9, "WIDER GAP", "3-tile gap. Same lesson, less margin."),
    (18, 7, "OPTIONAL SHELF", "3 bonus embers, no enemy: practise greed."),
    (22, 10, "SCONCE 1", "Checkpoint + BANK, taught right after greed."),
    (28, 8, "THE FORK", "Low road: safe, few embers. High road: rich."),
    (38, 3, "FIRST MOTH", "Guards the high road. More glow = more aggro."),
    (35, 10, "SPIKE PIT", "The low road still asks for one clean jump."),
    (44, 4, "BELL SHARD 1", "Prize at the end of the high road. +250."),
    (50, 10, "SCONCE 2", "Bank before the hardest section."),
    (56, 10, "PILLAR + WAX", "Refuel the wax timer before the water."),
    (60, 9, "CRUMBLE + ICE", "Stones fall 0.6s after landing. Shard 2 above."),
    (67, 5, "MOTH OVER WATER", "A hit here knocks you into the water."),
    (73, 10, "SCONCE 3", "Final bank. Wise players cash in here."),
    (78, 8, "THE CLIMB", "3-tile steps = max jump. Spikes punish misses."),
    (84, 3, "MOTH + ICICLE", "Both threats at once: the final exam."),
    (88, 3, "BELL SHARD 3", "Floats in the moth's airspace. Greed test."),
    (92, 4, "GREAT BELL", "Touch it to ring the bell. Level complete!"),
]
DIFFICULTY = [(0, 1), (5, 1), (6, 2), (12, 2), (13, 3), (16, 2), (21, 1), (24, 2), (32, 3),
              (36, 5), (40, 5), (44, 4), (48, 2), (52, 3), (57, 6), (62, 7), (66, 7), (70, 5),
              (72, 2), (76, 6), (80, 7), (84, 9), (89, 9), (92, 10), (96, 10)]


def tc(x, y):
    return int(x * 16 + 8), int(y * 16 + 8)


def dashed(d, pts, color, width=1, dash=6, gap=4):
    import math
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        dist = math.hypot(bx - ax, by - ay)
        n = max(1, int(dist / (dash + gap)))
        for i in range(n):
            t0 = i / n
            t1 = min(1, t0 + dash / max(dist, 1))
            d.line([ax + (bx - ax) * t0, ay + (by - ay) * t0,
                    ax + (bx - ax) * t1, ay + (by - ay) * t1], fill=color, width=width)


def route(img, pts, color):
    d = ImageDraw.Draw(img)
    P = [tc(x, y) for x, y in pts]
    dashed(d, P, wl.rgba('K'), width=4)
    dashed(d, P, wl.rgba(color), width=2)
    ex, ey = P[-1]
    d.polygon([(ex - 4, ey - 4), (ex + 4, ey), (ex - 4, ey + 4)], fill=wl.rgba(color),
              outline=wl.rgba('K'))


def badge(img, n, x, y, col='A'):
    d = ImageDraw.Draw(img)
    cx, cy = tc(x, y)
    cy -= 14
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=wl.rgba('K'))
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=wl.rgba(col))
    d.line([cx, cy + 7, cx, cy + 11], fill=wl.rgba('K'), width=1)
    wl.draw_text(img, str(n), cx + 1, cy - 3, color='K', outline=None, shadow=False, anchor='c')


def section_header(img, y):
    d = ImageDraw.Draw(img)
    cols = ['G', 'P', 'u', 'R']
    for i, (name, role, _) in enumerate(L.SECTIONS):
        x0 = i * 24 * 16
        d.rectangle([x0, y, x0 + 24 * 16 - 2, y + 15], fill=wl.rgba('K'))
        d.rectangle([x0 + 1, y + 1, x0 + 24 * 16 - 3, y + 14], fill=wl.rgba(cols[i]))
        wl.draw_text(img, f"{i + 1}. {name}", x0 + 6, y + 4, color='W')
        wl.draw_text(img, role, x0 + 24 * 16 - 8, y + 4, color='K', outline=None, shadow=False,
                     anchor='r')


def main():
    full = L.render(lit_sconces=())
    full.save(os.path.join(OUT, "level_01_map_1x.png"))
    wl.scale(full, 3).save(os.path.join(OUT, "level_01_map_clean_x3.png"))

    # ---------------- grid / coordinate map
    g = wl.scale(full, 2)
    gd = ImageDraw.Draw(g, "RGBA")
    for x in range(L.W + 1):
        gd.line([x * 32, 0, x * 32, g.height], fill=(255, 255, 255, 40 if x % 4 else 90))
    for y in range(L.H + 1):
        gd.line([0, y * 32, g.width, y * 32], fill=(255, 255, 255, 40))
    grid = Image.new("RGBA", (g.width + 40, g.height + 40), wl.rgba('K'))
    grid.alpha_composite(g, (40, 40))
    for x in range(0, L.W, 2):
        wl.draw_text(grid, str(x), 40 + x * 32 + 16, 14, color='C', sc=2, anchor='c', shadow=False)
    for y in range(L.H):
        wl.draw_text(grid, str(y), 20, 40 + y * 32 + 9, color='C', sc=2, anchor='c', shadow=False)
    grid.save(os.path.join(OUT, "level_01_map_grid_coords.png"))

    # ---------------- annotated design sheet (built at 1x then scaled x2)
    top, mapy = 34, 52
    legend_y = mapy + 224 + 64
    sheet = Image.new("RGBA", (L.W * 16, legend_y + 5 * 26 + 16), wl.rgba('N'))
    wl.draw_text(sheet, "LEVEL 1 - THE DROWNED BELFRY  |  ANNOTATED LAYOUT", 8, 8, sc=2,
                 grad=('Y', 'O'))
    wl.draw_text(sheet, "96 X 14 TILES (16PX)   EMBERS %d   WAX %d   SHARDS %d   MOTHS %d   "
                 "ICICLES %d   CHECKPOINTS %d" % (L.count('e'), L.count('d'), L.count('b'),
                                                  L.count('M'), L.count('I'), L.count('S')),
                 L.W * 16 - 8, 12, color='H', anchor='r')
    section_header(sheet, top)
    mp = L.render(lit_sconces=())
    sheet.alpha_composite(mp, (0, mapy))
    layer = Image.new("RGBA", (L.W * 16, 224), (0, 0, 0, 0))
    for r in RISK_ROUTES:
        route(layer, r, 'R')
    route(layer, MAIN_ROUTE, 'A')
    for i, (x, y, *_r) in enumerate(CALLOUTS):
        badge(layer, i + 1, x, y, col='F' if 'SCONCE' in _r[0] else ('Y' if 'SHARD' in _r[0] or
                                                                     'BELL' in _r[0] else 'A'))
    sheet.alpha_composite(layer, (0, mapy))
    # section dividers
    d = ImageDraw.Draw(sheet)
    for i in range(1, 4):
        x = i * 24 * 16
        for yy in range(mapy, mapy + 224, 6):
            d.line([x, yy, x, yy + 2], fill=wl.rgba('W'))

    # difficulty curve
    gy = mapy + 224 + 8
    gh = 40
    d.rectangle([0, gy, L.W * 16, gy + gh], fill=wl.rgba('K'))
    for v in range(0, 11, 5):
        yy = gy + gh - 4 - v * 3.2
        d.line([0, yy, L.W * 16, yy], fill=wl.rgba('D'))
    pts = [(x * 16, gy + gh - 4 - v * 3.2) for x, v in DIFFICULTY]
    poly = pts + [(L.W * 16, gy + gh), (0, gy + gh)]
    d.polygon(poly, fill=wl.rgba('R', 90))
    d.line(pts, fill=wl.rgba('O'), width=2)
    wl.draw_text(sheet, "DIFFICULTY", 6, gy + 4, color='O')
    for name, x in (("BANK", 22), ("BANK", 50), ("BANK", 73)):
        d.line([x * 16 + 8, gy, x * 16 + 8, gy + gh], fill=wl.rgba('F'))
        wl.draw_text(sheet, "CHECKPOINT - RELIEF", x * 16 + 12, gy + 4, color='F', shadow=False)
    wl.draw_text(sheet, "PEAK - FINAL EXAM", 88 * 16, gy + 4, color='Y', anchor='c')

    # key
    ky = gy + gh + 6
    route(sheet, [(0.1, (ky - 8) / 16 + 0.0), (1.6, (ky - 8) / 16)], 'A')
    wl.draw_text(sheet, "MAIN (SAFE) ROUTE", 36, ky - 3, color='A')
    route(sheet, [(9, (ky - 8) / 16), (10.5, (ky - 8) / 16)], 'R')
    wl.draw_text(sheet, "OPTIONAL RISK ROUTE (MORE EMBERS / SHARDS)", 180, ky - 3, color='R')
    wl.draw_text(sheet, "ORANGE = LESSON/THREAT   BLUE = CHECKPOINT   GOLD = REWARD/GOAL", 560, ky - 3,
                 color='H')

    # legend columns
    col_w = L.W * 16 // 4
    for i, (x, y, title, desc) in enumerate(CALLOUTS):
        c, r = i // 5, i % 5
        lx, ly = c * col_w + 8, legend_y + 10 + r * 26
        dd = ImageDraw.Draw(sheet)
        dd.ellipse([lx, ly, lx + 12, ly + 12], fill=wl.rgba('A'), outline=wl.rgba('K'))
        wl.draw_text(sheet, str(i + 1), lx + 7, ly + 3, color='K', outline=None, shadow=False,
                     anchor='c')
        wl.draw_text(sheet, title, lx + 18, ly, color='Y')
        wl.draw_text(sheet, desc.upper(), lx + 18, ly + 10, color='C', shadow=False, outline=None)
    wl.scale(sheet, 2).save(os.path.join(OUT, "level_01_annotated_design_x2.png"))

    # ---------------- per-section close-ups (x4) for the document
    for i, (name, role, _) in enumerate(L.SECTIONS):
        x0 = i * 24
        crop = sheet.crop((x0 * 16, mapy, (x0 + 24) * 16, mapy + 224))
        wl.scale(crop, 3).save(os.path.join(OUT, f"section_{i + 1}_{name.lower().replace(' ', '_').replace('-', '_')}_x3.png"))

    # ---------------- data exports
    with open(os.path.join(OUT, "data", "level_01.txt"), "w") as f:
        f.write(L.__doc__.split("Legend")[1].strip("\n") + "\n\n")
        f.write("\n".join(L.ROWS) + "\n")
    terrain = [[TILE_INDEX.get(L.terrain_tile(x, y), -1) if L.terrain_tile(x, y) else -1
                for x in range(L.W)] for y in range(L.H)]
    bg = [[TILE_INDEX[L.bg_tile(x, y)] if L.bg_tile(x, y) else -1 for x in range(L.W)]
          for y in range(L.H)]
    for name, grid_ in (("terrain", terrain), ("background", bg)):
        with open(os.path.join(OUT, "data", f"level_01_{name}.csv"), "w", newline="") as f:
            csv.writer(f).writerows(grid_)
    ent_names = {'P': 'player_start', 'e': 'ember', 'd': 'wax_drop', 'b': 'bell_shard',
                 'M': 'frost_moth', 'I': 'icicle', 'S': 'sconce_checkpoint', 'G': 'great_bell'}
    objs = []
    for i, (ch, x, y) in enumerate(L.entities()):
        w = h = 32 if ch == 'G' else 16
        objs.append({"id": i + 1, "name": ent_names[ch], "type": ent_names[ch],
                     "x": x * 16, "y": y * 16, "width": w, "height": h, "rotation": 0,
                     "visible": True, "properties": [
                         {"name": "tile_x", "type": "int", "value": x},
                         {"name": "tile_y", "type": "int", "value": y}]})
    with open(os.path.join(OUT, "data", "level_01_entities.json"), "w") as f:
        json.dump(objs, f, indent=1)

    def tl(name, data):
        return {"type": "tilelayer", "name": name, "width": L.W, "height": L.H, "x": 0, "y": 0,
                "opacity": 1, "visible": True,
                "data": [v + 1 if v >= 0 else 0 for row in data for v in row]}
    tmj = {
        "type": "map", "version": "1.10", "tiledversion": "1.10.2", "orientation": "orthogonal",
        "renderorder": "right-down", "width": L.W, "height": L.H, "tilewidth": 16,
        "tileheight": 16, "infinite": False, "nextlayerid": 4, "nextobjectid": len(objs) + 1,
        "backgroundcolor": "#1a1a2e",
        "tilesets": [{
            "firstgid": 1, "name": "wicklight_tileset",
            "image": "../../02_Pixel_Art_Assets/tileset/wicklight_tileset.png",
            "imagewidth": TS_COLS * 16, "imageheight": 32, "tilewidth": 16, "tileheight": 16,
            "columns": TS_COLS, "tilecount": len(TILESET), "margin": 0, "spacing": 0,
            "tiles": [{"id": i, "type": k, "properties": [{"name": "name", "type": "string",
                                                            "value": n}]}
                      for i, (n, _, k) in enumerate(TILESET)]}],
        "layers": [dict(tl("Background", bg), id=1), dict(tl("Terrain", terrain), id=2),
                   {"type": "objectgroup", "id": 3, "name": "Entities", "opacity": 1,
                    "visible": True, "x": 0, "y": 0, "draworder": "topdown", "objects": objs}],
    }
    with open(os.path.join(OUT, "data", "level_01.tmj"), "w") as f:
        json.dump(tmj, f)


if __name__ == "__main__":
    main()
