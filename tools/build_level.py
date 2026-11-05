"""Makes the level files in 03_Level_Design/ and checks that every jump is possible."""
import json
import os
import math
from PIL import Image, ImageDraw
import art
import level as L
import font

OUT = os.path.join(os.path.dirname(__file__), "..", "03_Level_Design")
TILE_INDEX = {n: i for i, (n, _, _) in enumerate(art.TILES)}

# The planned route (tile x, tile y). Arcs are jumps.
ROUTE = [(2, 9), (4, 9), (5, 9), (6.5, 7.4), (8, 9), (8.6, 6.6), (10, 6), (11, 6), (12, 3.4),
         (13, 4), (14, 4), (15, 4), (16, 4.2), (17, 6), (18, 6), (19, 6), (20, 7.4), (21, 9),
         (22, 9)]
NOTES = [
    ((2, 9), "START", "Start here and walk right."),
    ((4, 9), "EMBER 1", "An easy ember on the ground."),
    ((6.5, 9), "SPIKES", "The first spikes. Jump over."),
    ((10, 6), "EMBER 2", "Jump up onto the platform."),
    ((14, 4), "MOTH + EMBER 3", "Hardest part. Wait for the moth."),
    ((13, 9), "SPIKE PITS", "Fall here and you lose a life."),
    ((18, 6), "EMBER 4", "Watch the moth on the floor."),
    ((22, 8), "EXIT", "Take ember 5, then the door."),
]


# ---------------------------------------------------------------- jump check
def standable(x, y):
    """Pip can stand in cell (x, y) if it is empty and has solid ground below it."""
    return L.cell(x, y) in ".PeMD" and L.cell(x, y + 1) in "#="


def can_jump(a, b):
    (ax, ay), (bx, by) = a, b
    up = ay - by
    return up <= L.JUMP_UP_TILES and abs(bx - ax) <= L.JUMP_ACROSS_TILES + 1


def reachable_from_start():
    cells = [(x, y) for y in range(L.H) for x in range(L.W) if standable(x, y)]
    start = L.find('P')[0]
    seen, todo = {start}, [start]
    while todo:
        a = todo.pop()
        for b in cells:
            if b not in seen and can_jump(a, b):
                seen.add(b)
                todo.append(b)
    return seen


def jump_check():
    seen = reachable_from_start()
    door = L.find('D')[0]
    door_floor = (door[0], door[1] + 1)
    results = {
        "embers in level": len(L.find('e')),
        "spike groups": 3,
        "moths": len(L.find('M')),
        "all embers reachable": all(e in seen for e in L.find('e')),
        "door reachable": door_floor in seen,
        "embers standing on solid ground": all(standable(*e) for e in L.find('e')),
    }
    # check each jump on the planned route (only the landing points)
    stops = [(2, 9), (4, 9), (5, 9), (8, 9), (9, 6), (11, 6), (13, 4), (15, 4), (17, 6),
             (19, 6), (21, 9), (22, 9)]
    jumps = []
    for a, b in zip(stops, stops[1:]):
        gap = max(0, abs(b[0] - a[0]) - 1)
        jumps.append({"from": a, "to": b, "up": a[1] - b[1], "gap": gap,
                      "ok": can_jump(a, b) and standable(*b)})
    results["route jumps ok"] = all(j["ok"] for j in jumps)
    results["route jumps"] = jumps
    return results


# ---------------------------------------------------------------- drawing
def tc(x, y):
    return (int(x * 16 + 8), int(y * 16 + 8))


def dashed(d, pts, col, w):
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        dist = math.hypot(bx - ax, by - ay)
        n = max(1, int(dist / 6))
        for i in range(n):
            if i % 2 == 0:
                t0, t1 = i / n, (i + 1) / n
                d.line([ax + (bx - ax) * t0, ay + (by - ay) * t0,
                        ax + (bx - ax) * t1, ay + (by - ay) * t1], fill=col, width=w)


def badge(img, n, cx, cy):
    d = ImageDraw.Draw(img)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=art.rgba('K'))
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=art.rgba('Y'))
    m = font.text_mask(str(n))
    img.paste(Image.new("RGBA", m.size, art.rgba('K')), (cx - m.width // 2, cy - 3), m)


def annotated():
    top, lvl_h = 22, 192
    legend_y = top + lvl_h + 6
    img = Image.new("RGBA", (384, legend_y + 128), art.rgba('N'))
    art.draw_text(img, "LEVEL MAP - THE LITTLE CANDLE", 6, 6, color='Y')
    art.draw_text(img, "24 X 12 TILES", 378, 6, color='L', anchor='r', shadow=False)
    img.alpha_composite(L.render(show_start=True), (0, top))
    lay = Image.new("RGBA", (384, lvl_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    # moth paths
    for (row, x0, x1) in L.MOTH_PATHS:
        y = row * 16 + 8
        d.line([x0 * 16 + 4, y + 7, x1 * 16 + 12, y + 7], fill=art.rgba('F'), width=1)
        for x in (x0 * 16 + 4, x1 * 16 + 12):
            d.line([x, y + 5, x, y + 9], fill=art.rgba('F'))
    # route
    pts = [tc(x, y) for x, y in ROUTE]
    dashed(d, pts, art.rgba('K'), 4)
    dashed(d, pts, art.rgba('Y'), 2)
    ex, ey = pts[-1]
    d.polygon([(ex - 4, ey - 4), (ex + 3, ey), (ex - 4, ey + 4)], fill=art.rgba('Y'))
    img.alpha_composite(lay, (0, top))
    ember = art.from_map(art.EMBER_A, 16, 16)          # draw embers again on top of the route
    for (x, y) in L.find('e'):
        img.alpha_composite(ember, (x * 16, top + y * 16))
    for i, ((x, y), _, _) in enumerate(NOTES):
        cx, cy = tc(x, y)
        badge(img, i + 1, cx, top + cy - 13)
    # notes
    for i, (_, title, text) in enumerate(NOTES):
        col, row = i // 4, i % 4
        x, y = 6 + col * 190, legend_y + row * 22
        badge(img, i + 1, x + 5, y + 5)
        art.draw_text(img, title, x + 14, y, color='Y', shadow=False)
        art.draw_text(img, text.upper(), x + 14, y + 10, color='C', shadow=False)
    # key
    ky = legend_y + 92
    d2 = ImageDraw.Draw(img)
    d2.line([6, ky + 3, 22, ky + 3], fill=art.rgba('Y'), width=2)
    art.draw_text(img, "PLAYER ROUTE", 26, ky, color='C', shadow=False)
    d2.line([110, ky + 3, 126, ky + 3], fill=art.rgba('F'))
    art.draw_text(img, "MOTH FLIES HERE", 130, ky, color='C', shadow=False)
    icons = [(art.candle_frames()["candle_idle"][0], "START"), (art.from_map(art.EMBER_A, 16, 16), "EMBER"),
             (art.from_map(art.MOTH_UP, 16, 16), "MOTH"), (art.from_map(art.SPIKES, 16, 16), "SPIKES"),
             (art.from_map(art.PLATFORM, 16, 16), "PLATFORM")]
    for i, (ic, name) in enumerate(icons):
        x = 6 + i * 62
        img.alpha_composite(ic, (x, ky + 14))
        art.draw_text(img, name, x + 18, ky + 20, color='C', shadow=False)
    door = art.from_map(art.door_rows(False)).resize((8, 16), Image.NEAREST)
    img.alpha_composite(door, (330, ky + 14))
    art.draw_text(img, "EXIT", 342, ky + 20, color='C', shadow=False)
    return img


def grid_map():
    lvl = art.scale(L.render(show_start=True), 3)
    d = ImageDraw.Draw(lvl, "RGBA")
    for x in range(L.W + 1):
        d.line([x * 48, 0, x * 48, lvl.height], fill=(255, 255, 255, 60))
    for y in range(L.H + 1):
        d.line([0, y * 48, lvl.width, y * 48], fill=(255, 255, 255, 60))
    out = Image.new("RGBA", (lvl.width + 40, lvl.height + 40), art.rgba('K'))
    out.alpha_composite(lvl, (40, 40))
    for x in range(L.W):
        art.draw_text(out, str(x), 40 + x * 48 + 24, 14, color='C', sc=2, anchor='c', shadow=False)
    for y in range(L.H):
        art.draw_text(out, str(y), 20, 40 + y * 48 + 17, color='C', sc=2, anchor='c', shadow=False)
    return out


def main():
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    art.scale(L.render(show_start=True), 3).save(os.path.join(OUT, "level_map_x3.png"))
    art.scale(annotated(), 3).save(os.path.join(OUT, "level_map_annotated_x3.png"))
    grid_map().save(os.path.join(OUT, "level_map_grid.png"))
    # data files
    with open(os.path.join(OUT, "data", "level.txt"), "w") as f:
        f.write(L.__doc__.split("One letter = one tile:")[1].strip("\n") + "\n\n")
        f.write("\n".join(L.ROWS) + "\n")
    grid = [[TILE_INDEX[L.tile_name(x, y)] if L.tile_name(x, y) else -1 for x in range(L.W)]
            for y in range(L.H)]
    with open(os.path.join(OUT, "data", "level_tiles.csv"), "w") as f:
        f.write("\n".join(",".join(str(v) for v in row) for row in grid) + "\n")
    names = {'P': 'start', 'e': 'ember', 'M': 'moth', 'D': 'exit_door'}
    objs = []
    for ch, name in names.items():
        for (x, y) in L.find(ch):
            objs.append({"id": len(objs) + 1, "name": name, "type": name, "x": x * 16, "y": y * 16,
                         "width": 16, "height": 32 if ch == 'D' else 16, "rotation": 0,
                         "visible": True})
    tmj = {
        "type": "map", "version": "1.10", "tiledversion": "1.10.2", "orientation": "orthogonal",
        "renderorder": "right-down", "width": L.W, "height": L.H, "tilewidth": 16,
        "tileheight": 16, "infinite": False, "nextlayerid": 3, "nextobjectid": len(objs) + 1,
        "tilesets": [{"firstgid": 1, "name": "wicklight_tiles",
                      "image": "../../02_Pixel_Art_Assets/tiles/tileset.png",
                      "imagewidth": 64, "imageheight": 16, "tilewidth": 16, "tileheight": 16,
                      "columns": 4, "tilecount": 4, "margin": 0, "spacing": 0}],
        "layers": [
            {"type": "tilelayer", "id": 1, "name": "Tiles", "width": L.W, "height": L.H,
             "x": 0, "y": 0, "opacity": 1, "visible": True,
             "data": [v + 1 if v >= 0 else 0 for row in grid for v in row]},
            {"type": "objectgroup", "id": 2, "name": "Objects", "opacity": 1, "visible": True,
             "x": 0, "y": 0, "draworder": "topdown", "objects": objs}],
    }
    with open(os.path.join(OUT, "data", "level.tmj"), "w") as f:
        json.dump(tmj, f, indent=1)
    res = jump_check()
    with open(os.path.join(OUT, "data", "jump_check_result.json"), "w") as f:
        json.dump(res, f, indent=1)
    return res


if __name__ == "__main__":
    r = main()
    print({k: v for k, v in r.items() if k != "route jumps"})
