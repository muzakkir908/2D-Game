"""Saves all the pixel art into 02_Pixel_Art_Assets/.

PNG files (one per frame), sprite sheet strips, one combined sprite sheet,
the tileset, the cave background, the palette, UI pieces and .piskel files.
"""
import base64
import io
import json
import os
from PIL import Image, ImageDraw
import art
import font

ROOT = os.path.join(os.path.dirname(__file__), "..", "02_Pixel_Art_Assets")


def p(*parts):
    path = os.path.join(ROOT, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def animations():
    """All animated things: name -> (folder, frames, frames per second)."""
    c = art.candle_frames()
    return {
        "candle_idle": ("player", c["candle_idle"], 3),
        "candle_walk": ("player", c["candle_walk"], 8),
        "candle_jump": ("player", c["candle_jump"], 1),
        "ember": ("ember", [art.from_map(art.EMBER_A, 16, 16), art.from_map(art.EMBER_B, 16, 16)], 4),
        "moth": ("moth", [art.from_map(art.MOTH_UP, 16, 16), art.from_map(art.MOTH_DOWN, 16, 16)], 6),
        "door": ("door", [art.from_map(art.door_rows(False)), art.from_map(art.door_rows(True))], 1),
    }


def strip(frames):
    w, h = frames[0].size
    im = Image.new("RGBA", (w * len(frames), h), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        im.alpha_composite(f, (i * w, 0))
    return im


def png_b64(img):
    b = io.BytesIO()
    img.save(b, "PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()


def piskel_file(name, frames, fps):
    """A Piskel project file (.piskel). All frames are on one layer."""
    w, h = frames[0].size
    layer = {"name": "Layer 1", "opacity": 1, "frameCount": len(frames),
             "chunks": [{"layout": [[i] for i in range(len(frames))],
                         "base64PNG": png_b64(strip(frames))}]}
    return {"modelVersion": 2,
            "piskel": {"name": name, "description": "WICKLIGHT - The Little Candle", "fps": fps,
                       "height": h, "width": w, "layers": [json.dumps(layer)],
                       "hiddenFrames": []}}


def export_palette():
    keys = list(art.PALETTE)
    sw = Image.new("RGBA", (len(keys) * 8, 8))
    d = ImageDraw.Draw(sw)
    for i, k in enumerate(keys):
        d.rectangle([i * 8, 0, i * 8 + 7, 7], fill=art.rgba(k))
    sw.save(p("palette", "palette.png"))
    card = Image.new("RGBA", (4 * 116 + 8, 4 * 40 + 24), art.rgba('N'))
    art.draw_text(card, "WICKLIGHT PALETTE - 16 COLOURS", 6, 6, color='Y')
    cd = ImageDraw.Draw(card)
    for i, k in enumerate(keys):
        x, y = 6 + (i % 4) * 116, 22 + (i // 4) * 40
        cd.rectangle([x - 1, y - 1, x + 22, y + 22], fill=art.rgba('K'))
        cd.rectangle([x, y, x + 21, y + 21], fill=art.rgba(k))
        r, g, b = art.RGB[k]
        art.draw_text(card, art.PALETTE[k][0].upper(), x + 26, y + 2, color='C', shadow=False)
        art.draw_text(card, "#%02X%02X%02X" % (r, g, b), x + 26, y + 12, color='L', shadow=False)
    art.scale(card, 3).save(p("palette", "palette_card_x3.png"))
    with open(p("palette", "wicklight.gpl"), "w") as f:
        f.write("GIMP Palette\nName: WICKLIGHT\nColumns: 4\n#\n")
        for k in keys:
            r, g, b = art.RGB[k]
            f.write(f"{r:3d} {g:3d} {b:3d}\t{art.PALETTE[k][0]}\n")
    with open(p("palette", "wicklight.hex"), "w") as f:
        for k in keys:
            f.write("%02x%02x%02x\n" % art.RGB[k])


def export_ui():
    for lbl in ("PLAY", "SETTINGS", "EXIT", "REPLAY", "RETRY", "MAIN MENU"):
        for sel in (False, True):
            art.button(lbl, selected=sel).save(
                p("ui", "buttons", f"button_{lbl.lower().replace(' ', '_')}_{'selected' if sel else 'normal'}.png"))
    art.panel(48, 48).save(p("ui", "panel.png"))
    for name, rows in [("heart_full", art.HEART), ("heart_empty", art.HEART_EMPTY),
                       ("ember_icon", art.ICON_EMBER), ("ember_icon_empty", art.ICON_EMBER_EMPTY),
                       ("clock_icon", art.ICON_CLOCK)]:
        art.from_map(rows).save(p("ui", "icons", name + ".png"))
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:.,!?-+/'x%()<>&=| "
    im = Image.new("RGBA", (16 * 8, 4 * 10), (0, 0, 0, 0))
    for i, ch in enumerate(chars):
        m = font.text_mask(ch)
        im.paste(Image.new("RGBA", m.size, art.rgba('W')), ((i % 16) * 8 + 1, (i // 16) * 10 + 1), m)
    im.save(p("ui", "font_sheet.png"))
    with open(p("ui", "font_sheet_letters.txt"), "w") as f:
        f.write("Each letter is in an 8 x 10 box, 16 boxes per row, in this order:\n" + chars + "\n")


def overview(anims, tiles):
    """One sheet that shows every asset with its name (shown 4x bigger)."""
    im = Image.new("RGBA", (360, 150), art.rgba('N'))
    art.draw_text(im, "WICKLIGHT - ASSET PACK", 180, 6, color='Y', anchor='c')
    x, y = 8, 22
    for name, (_, frames, _) in anims.items():
        fw, fh = frames[0].size
        need = max(len(frames) * (fw + 2), font.text_width(name.upper().replace('_', ' '))) + 10
        if x + need > 356:
            x, y = 8, y + 44
        d = ImageDraw.Draw(im)
        for i, f in enumerate(frames):
            d.rectangle([x + i * (fw + 2) - 1, y - 1, x + i * (fw + 2) + fw, y + fh], fill=art.rgba('B'))
            im.alpha_composite(f, (x + i * (fw + 2), y))
        art.draw_text(im, name.upper().replace('_', ' '), x, y + (fh if fh < 32 else 32) + 3,
                      color='C', shadow=False)
        x += need
    y += 64
    art.draw_text(im, "TILES", 8, y - 10, color='Y', shadow=False)
    for i, (name, t) in enumerate(tiles):
        im.alpha_composite(t, (8 + i * 88, y))
        art.draw_text(im, name.upper().replace('_', ' '), 26 + i * 88, y + 5, color='C', shadow=False)
    art.scale(im.crop((0, 0, 360, y + 22)), 4).save(p("preview", "asset_overview_x4.png"))


def candle_sheet(anims):
    """Candle frames at 8x size with a pixel grid."""
    frames = [(n.replace("candle_", "") + " " + str(i), f)
              for n in ("candle_idle", "candle_walk", "candle_jump") for i, f in enumerate(anims[n][1])]
    S = 8
    im = Image.new("RGBA", (16 + len(frames) * (16 * S + 12), 16 * S + 60), art.rgba('N'))
    art.draw_text(im, "THE LITTLE CANDLE - 16 X 16 PIXELS", 12, 8, color='Y', sc=2)
    d = ImageDraw.Draw(im)
    for i, (label, f) in enumerate(frames):
        x, y = 12 + i * (16 * S + 12), 30
        d.rectangle([x, y, x + 16 * S - 1, y + 16 * S - 1], fill=art.rgba('B'))
        im.alpha_composite(art.scale(f, S), (x, y))
        for g in range(1, 16):
            d.line([x + g * S, y, x + g * S, y + 16 * S - 1], fill=(255, 255, 255, 25))
            d.line([x, y + g * S, x + 16 * S - 1, y + g * S], fill=(255, 255, 255, 25))
        art.draw_text(im, label.upper(), x, y + 16 * S + 8, color='C', sc=2, shadow=False)
    im.save(p("preview", "candle_sheet_x8.png"))


def main():
    anims = animations()
    meta = {"frame_size_note": "All frames are 16x16, except the door (16x32).", "animations": {}}
    for name, (folder, frames, fps) in anims.items():
        for i, f in enumerate(frames):
            fname = ["door_closed", "door_open"][i] if name == "door" else f"{name}_{i}"
            f.save(p("sprites", folder, fname + ".png"))
        file = f"{name}_strip{len(frames)}.png"
        strip(frames).save(p("spritesheets", file))
        with open(p("piskel", f"{name}.piskel"), "w") as fh:
            json.dump(piskel_file(name, frames, fps), fh)
        meta["animations"][name] = {"file": file, "frame_width": frames[0].width,
                                    "frame_height": frames[0].height, "frames": len(frames), "fps": fps}
    # combined sheet: one row per animation, 16 px cells (door uses two rows)
    rows = [(n, a[1]) for n, a in anims.items()]
    sheet = Image.new("RGBA", (16 * 4, 16 * (len(rows) + 1)), (0, 0, 0, 0))
    y = 0
    layout = {}
    for name, frames in rows:
        for i, f in enumerate(frames):
            sheet.alpha_composite(f, (i * 16, y))
        layout[name] = {"y": y, "frames": len(frames), "frame_width": frames[0].width,
                        "frame_height": frames[0].height}
        y += frames[0].height
    sheet.save(p("spritesheets", "wicklight_spritesheet.png"))
    meta["combined_sheet"] = {"file": "wicklight_spritesheet.png", "rows": layout}
    with open(p("spritesheets", "spritesheets.json"), "w") as fh:
        json.dump(meta, fh, indent=2)

    tiles = [(n, art.from_map(m, 16, 16)) for n, m, _ in art.TILES]
    ts = Image.new("RGBA", (16 * len(tiles), 16), (0, 0, 0, 0))
    for i, (n, t) in enumerate(tiles):
        t.save(p("tiles", f"{i}_{n}.png"))
        ts.alpha_composite(t, (i * 16, 0))
    ts.save(p("tiles", "tileset.png"))
    art.background().save(p("background", "cave_background.png"))
    export_palette()
    export_ui()
    overview(anims, tiles)
    candle_sheet(anims)


if __name__ == "__main__":
    main()
