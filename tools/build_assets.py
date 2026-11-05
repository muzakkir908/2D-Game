"""Exports the WICKLIGHT pixel-art asset pack into 02_Pixel_Art_Assets/."""
import json
import os
from PIL import Image, ImageDraw
import wl

ROOT = os.path.join(os.path.dirname(__file__), "..", "02_Pixel_Art_Assets")


def p(*a):
    path = os.path.join(ROOT, *a)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


# ---------------------------------------------------------------- tileset
TILESET = [  # index -> (name, image, solid-type)
    ("stone_top", wl.tile_stone_top(), "solid"),
    ("stone", wl.tile_stone(), "solid"),
    ("stone_bg", wl.tile_stone_bg(), "background"),
    ("plank", wl.tile_plank(), "one_way"),
    ("crumble", wl.tile_crumble(0), "crumble"),
    ("crumble_breaking", wl.tile_crumble(1), "crumble"),
    ("spikes", wl.tile_spikes(), "hazard"),
    ("pillar", wl.tile_pillar(), "background"),
    ("water_surface_0", wl.tile_water(0), "hazard_water"),
    ("water_surface_1", wl.tile_water(1), "hazard_water"),
    ("water_fill", wl.tile_water(0, False), "hazard_water"),
    ("chain", wl.tile_chain(), "decor"),
    ("window_top", wl.tile_window_top(), "background"),
    ("window_bottom", wl.tile_window_bottom(), "background"),
    ("icicle_mount", wl.icicle_frames()[0], "hazard_spawn"),
    ("sconce_unlit", wl.sconce_frames()[0], "checkpoint"),
]
TILE_INDEX = {name: i for i, (name, _, _) in enumerate(TILESET)}
TS_COLS = 8


def tileset_image():
    rows = (len(TILESET) + TS_COLS - 1) // TS_COLS
    im = Image.new("RGBA", (TS_COLS * 16, rows * 16), (0, 0, 0, 0))
    for i, (_, t, _) in enumerate(TILESET):
        im.alpha_composite(t, ((i % TS_COLS) * 16, (i // TS_COLS) * 16))
    return im


# ---------------------------------------------------------------- sprites
def sprite_groups():
    return {
        "player": {f"pip_{a}": wl.pip_anim(a) for a in wl.PIP_ANIMS},
        "collectibles": {
            "ember": wl.ember_frames(),
            "wax_drop": wl.wax_frames(),
            "bell_shard": wl.shard_frames(),
        },
        "hazards": {
            "frost_moth": wl.moth_frames(),
            "icicle": wl.icicle_frames(),
        },
        "objects": {
            "sconce_unlit": wl.sconce_frames()[:1],
            "sconce_lit": wl.sconce_frames()[1:],
            "great_bell_idle": [wl.bell(False)],
            "great_bell_ringing": [wl.bell(True), wl.bell(False)],
        },
    }


FPS = {"pip_idle": 3, "pip_run": 10, "pip_jump": 1, "pip_fall": 1, "pip_hurt": 1,
       "ember": 8, "wax_drop": 3, "bell_shard": 6, "frost_moth": 8, "icicle": 2,
       "sconce_unlit": 1, "sconce_lit": 6, "great_bell_idle": 1, "great_bell_ringing": 8}


def strip(frames):
    w, h = frames[0].size
    im = Image.new("RGBA", (w * len(frames), h), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        im.alpha_composite(f, (i * w, 0))
    return im


def export_palette():
    keys = list(wl.PALETTE)
    sw = Image.new("RGBA", (len(keys) * 8, 8))
    d = ImageDraw.Draw(sw)
    for i, k in enumerate(keys):
        d.rectangle([i * 8, 0, i * 8 + 7, 7], fill=wl.rgba(k))
    sw.save(p("palette", "wicklight_palette_1x.png"))
    # big labelled swatch card
    card = Image.new("RGBA", (7 * 60 + 8, 4 * 44 + 30), wl.rgba('N'))
    wl.draw_text(card, "WICKLIGHT MASTER PALETTE - 28 COLOURS", 6, 6, grad=('Y', 'A'))
    for i, k in enumerate(keys):
        x, y = 6 + (i % 7) * 60, 22 + (i // 7) * 44
        cd = ImageDraw.Draw(card)
        cd.rectangle([x - 1, y - 1, x + 52, y + 26], fill=wl.rgba('K'))
        cd.rectangle([x, y, x + 51, y + 25], fill=wl.rgba(k))
        r, g, b = wl.RGB[k]
        wl.draw_text(card, "%02X%02X%02X" % (r, g, b), x, y + 30, color='C', shadow=False)
    wl.scale(card, 3).save(p("palette", "wicklight_palette_card.png"))
    with open(p("palette", "wicklight.gpl"), "w") as f:
        f.write("GIMP Palette\nName: WICKLIGHT\nColumns: 7\n#\n")
        for k in keys:
            r, g, b = wl.RGB[k]
            f.write(f"{r:3d} {g:3d} {b:3d}\t{wl.PALETTE[k][0]}\n")
    with open(p("palette", "wicklight.hex"), "w") as f:
        for k in keys:
            f.write("%02x%02x%02x\n" % wl.RGB[k])


def export_font():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:.,!?-+/'x%()<>& "
    im = Image.new("RGBA", (16 * 8, 4 * 10), (0, 0, 0, 0))
    for i, ch in enumerate(chars):
        m = wl.text_mask(ch)
        im.paste(Image.new("RGBA", m.size, wl.rgba('W')), ((i % 16) * 8 + 1, (i // 16) * 10 + 1), m)
    im.save(p("ui", "font_belfry5x7_sheet.png"))
    with open(p("ui", "font_belfry5x7_order.txt"), "w") as f:
        f.write("Cell size 8x10, 16 per row, glyph at +1,+1. Order:\n" + chars + "\n")


def export_ui():
    for lbl in ("PLAY", "SETTINGS", "EXIT", "REPLAY", "RETRY", "MAIN MENU"):
        for sel in (False, True):
            wl.button(lbl, selected=sel).save(
                p("ui", "buttons", f"btn_{lbl.lower().replace(' ', '_')}_{'hover' if sel else 'idle'}.png"))
    wl.panel(48, 48).save(p("ui", "panel_stone_9slice_48.png"))
    wl.panel(48, 48, 'frost').save(p("ui", "panel_frost_9slice_48.png"))
    for name, rows in [("heart_full", wl.HEART), ("heart_empty", wl.HEART_EMPTY),
                       ("icon_ember", wl.ICON_EMBER), ("icon_shard", wl.ICON_SHARD),
                       ("icon_shard_empty", wl.ICON_SHARD_EMPTY), ("icon_clock", wl.ICON_CLOCK)]:
        wl.from_map(rows).save(p("ui", "icons", name + ".png"))


def overview():
    """Labelled presentation sheet of every asset (x4)."""
    groups = sprite_groups()
    W = 400
    im = Image.new("RGBA", (W, 330), wl.rgba('N'))
    d = ImageDraw.Draw(im)
    wl.draw_text(im, "WICKLIGHT - PIXEL ART ASSET PACK", W // 2, 6, sc=1, grad=('Y', 'O'), anchor='c')
    y = 22
    for gname, g in groups.items():
        wl.draw_text(im, gname.upper(), 8, y, color='A')
        y += 11
        x = 8
        for name, frames in g.items():
            fw = frames[0].width
            need = len(frames) * (fw + 2) + 4
            lw = wl.text_width(name.upper().replace('_', ' ')) + 4
            if x + max(need, lw) > W - 4:
                x = 8; y += frames[0].height + 16
            for i, f in enumerate(frames):
                d.rectangle([x + i * (fw + 2) - 1, y - 1, x + i * (fw + 2) + fw, y + f.height],
                            fill=wl.rgba('D'))
                im.alpha_composite(f, (x + i * (fw + 2), y))
            wl.draw_text(im, name.upper().replace('_', ' '), x, y + frames[0].height + 3,
                         color='H', shadow=False, outline=None)
            x += max(need, lw) + 6
        y += 34 if gname != "objects" else 46
    wl.draw_text(im, "TILESET (16X16 GRID)", 8, y, color='A')
    y += 11
    ts = tileset_image()
    for i, (name, t, kind) in enumerate(TILESET):
        x = 8 + (i % 8) * 48
        yy = y + (i // 8) * 30
        d.rectangle([x - 1, yy - 1, x + 16, yy + 16], fill=wl.rgba('D'))
        im.alpha_composite(t, (x, yy))
        wl.draw_text(im, str(i), x + 19, yy + 4, color='C', shadow=False, outline=None)
    im = im.crop((0, 0, W, y + 64))
    wl.scale(im, 4).save(p("preview", "asset_pack_overview_x4.png"))


def character_sheet():
    """Pip presentation sheet: every frame at x8 with pixel grid + size callouts."""
    S = 8
    anims = list(wl.PIP_ANIMS)
    frames = [(n + ' ' + str(j), f) for n in anims for j, f in enumerate(wl.pip_anim(n))]
    cols = len(frames)
    W = 24 + cols * (16 * S + 16)
    im = Image.new("RGBA", (W, 16 * S + 150), wl.rgba('N'))
    wl.draw_text(im, "PIP - THE LAST WICK  |  PLAYER CHARACTER SHEET", 24, 14, sc=3, grad=('Y', 'O'))
    wl.draw_text(im, "16X16 PX  -  HITBOX 8X13 (X4..11, Y3..15)  -  OUTLINE SOOT #0D0B1A  -  FACES RIGHT, FLIP FOR LEFT",
                 24, 46, sc=2, color='H')
    d = ImageDraw.Draw(im)
    for i, (n, f) in enumerate(frames):
        x, y = 24 + i * (16 * S + 16), 76
        d.rectangle([x - 2, y - 2, x + 16 * S + 1, y + 16 * S + 1], fill=wl.rgba('K'))
        d.rectangle([x, y, x + 16 * S - 1, y + 16 * S - 1], fill=wl.rgba('D'))
        big = wl.scale(f, S)
        im.alpha_composite(big, (x, y))
        for g in range(1, 16):
            d.line([x + g * S, y, x + g * S, y + 16 * S - 1], fill=(255, 255, 255, 18))
            d.line([x, y + g * S, x + 16 * S - 1, y + g * S], fill=(255, 255, 255, 18))
        d.rectangle([x + 4 * S, y + 3 * S, x + 12 * S - 1, y + 16 * S - 1], outline=wl.rgba('R'))
        wl.draw_text(im, n.upper(), x, y + 16 * S + 10,
                     sc=2, color='C')
    im.save(p("preview", "pip_character_sheet.png"))


def main():
    character_sheet()
    meta = {"tile_size": 16, "sheets": {}}
    for group, sprites in sprite_groups().items():
        for name, frames in sprites.items():
            for i, f in enumerate(frames):
                f.save(p("sprites", group, f"{name}_{i}.png"))
            s = strip(frames)
            s.save(p("spritesheets", f"{name}_strip{len(frames)}.png"))
            meta["sheets"][name] = {
                "file": f"{name}_strip{len(frames)}.png", "frame_w": frames[0].width,
                "frame_h": frames[0].height, "frames": len(frames), "fps": FPS.get(name, 6),
                "loop": name not in ("pip_hurt",)}
    # combined master sprite sheet (all 16x16 sprites in rows)
    rows = []
    for group, sprites in sprite_groups().items():
        for name, frames in sprites.items():
            if frames[0].size == (16, 16):
                rows.append((name, frames))
    sheet = Image.new("RGBA", (16 * 4, 16 * len(rows)), (0, 0, 0, 0))
    atlas = {}
    for r, (name, frames) in enumerate(rows):
        for i, f in enumerate(frames):
            sheet.alpha_composite(f, (i * 16, r * 16))
        atlas[name] = {"row": r, "frames": len(frames), "y": r * 16}
    sheet.save(p("spritesheets", "wicklight_master_spritesheet.png"))
    wl.scale(sheet, 4).save(p("spritesheets", "wicklight_master_spritesheet_x4_preview.png"))
    meta["master_sheet"] = {"file": "wicklight_master_spritesheet.png", "cell": 16, "rows": atlas}
    with open(p("spritesheets", "spritesheets.json"), "w") as f:
        json.dump(meta, f, indent=2)

    ts = tileset_image()
    ts.save(p("tileset", "wicklight_tileset.png"))
    wl.scale(ts, 4).save(p("tileset", "wicklight_tileset_x4_preview.png"))
    for i, (name, t, kind) in enumerate(TILESET):
        t.save(p("tileset", "tiles", f"{i:02d}_{name}.png"))
    with open(p("tileset", "tileset.json"), "w") as f:
        json.dump({"image": "wicklight_tileset.png", "tile_size": 16, "columns": TS_COLS,
                   "tiles": [{"index": i, "name": n, "type": k} for i, (n, _, k) in enumerate(TILESET)]},
                  f, indent=2)
    export_palette()
    export_font()
    export_ui()
    overview()


if __name__ == "__main__":
    main()
