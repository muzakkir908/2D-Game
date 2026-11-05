"""Makes the UI screens. They are drawn at 384x216 and saved 5x bigger (1920x1080)."""
import os
import numpy as np
from PIL import Image, ImageDraw
import wl
import level as L

OUT = os.path.join(os.path.dirname(__file__), "..", "04_UI_and_Prototype")
SW, SH = 384, 216
SCALE = 5
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0


def lighting(img, lights, base=175, steps=4, cold=False):
    """Pixel-art lighting: darkens the screen and adds light circles. lights = [(x, y, radius, warm)]."""
    h, w = img.height, img.width
    yy, xx = np.mgrid[0:h, 0:w]
    lightv = np.zeros((h, w))
    warm = np.zeros((h, w))
    for (lx, ly, r, is_warm) in lights:
        f = np.clip(1 - np.hypot(xx - lx, yy - ly) / r, 0, 1)
        lightv = np.maximum(lightv, f)
        if is_warm:
            warm = np.maximum(warm, f)
    dither = np.tile(BAYER, (h // 4 + 1, w // 4 + 1))[:h, :w]
    q = np.floor(lightv * steps + dither * 0.9) / steps
    q = np.clip(q, 0, 1)
    alpha = (base * (1 - q)).astype(np.uint8)
    tint = wl.RGB['p'] if cold else wl.RGB['K']
    dark = np.zeros((h, w, 4), np.uint8)
    dark[..., :3] = tint
    dark[..., 3] = alpha
    out = img.copy()
    out.alpha_composite(Image.fromarray(dark, "RGBA"))
    wq = np.floor(warm * 3 + dither * 0.9) / 3
    glow = np.zeros((h, w, 4), np.uint8)
    glow[..., :3] = wl.RGB['A']
    glow[..., 3] = (np.clip(wq, 0, 1) * 34).astype(np.uint8)
    out.alpha_composite(Image.fromarray(glow, "RGBA"))
    return out


def frost_grade(img):
    """Makes the picture cold and blue for the Game Over screen."""
    a = np.asarray(img.convert("RGB")).astype(float)
    lum = a @ np.array([0.3, 0.55, 0.15])
    tint = np.array(wl.RGB['I'], float) / 255
    res = (lum[..., None] * tint * 0.8 + a * 0.15)
    return Image.fromarray(np.clip(res, 0, 255).astype(np.uint8)).convert("RGBA")


def veil(img, key='N', a=150):
    img.alpha_composite(Image.new("RGBA", img.size, wl.rgba(key, a)))


def icon(rows):
    return wl.from_map(rows)


# --------------------------------------------------------------------- HUD
def hud(img, hearts=2, wax=0.62, time="1:42", score=1240, embers=12, shards=1, glow=3,
        unbanked=90, section=2):
    d = ImageDraw.Draw(img)
    # top-left: hearts + wax meter
    p = wl.panel(92, 34)
    img.alpha_composite(p, (4, 4))
    for i in range(3):
        img.alpha_composite(icon(wl.HEART if i < hearts else wl.HEART_EMPTY), (10 + i * 9, 10))
    wl.draw_text(img, "LIVES", 40, 10, color='H', shadow=False, outline=None)
    img.alpha_composite(icon(wl.ICON_CLOCK), (10, 24))
    bx, by, bw = 18, 24, 50
    d.rectangle([bx, by, bx + bw, by + 5], fill=wl.rgba('K'))
    fillw = int((bw - 2) * wax)
    d.rectangle([bx + 1, by + 1, bx + 1 + fillw, by + 4], fill=wl.rgba('C'))
    d.line([bx + 1, by + 1, bx + 1 + fillw, by + 1], fill=wl.rgba('W'))
    d.line([bx + 1, by + 4, bx + 1 + fillw, by + 4], fill=wl.rgba('S'))
    d.point((bx + 1 + fillw, by - 1), fill=wl.rgba('A'))  # tiny flame on wax bar
    d.point((bx + 1 + fillw, by - 2), fill=wl.rgba('Y'))
    wl.draw_text(img, time, 72, 23, color='C')

    # top-centre: objective
    obj = "RING THE GREAT BELL"
    ow = wl.text_width(obj) + 40
    p = wl.panel(ow, 20)
    img.alpha_composite(p, (SW // 2 - ow // 2, 4))
    small_bell = wl.bell().resize((12, 12), Image.NEAREST)
    img.alpha_composite(small_bell, (SW // 2 - ow // 2 + 6, 8))
    wl.draw_text(img, obj, SW // 2 + 8, 8, color='Y', anchor='c')
    # section progress pips
    for i in range(4):
        cx = SW // 2 - 18 + i * 12
        col = 'A' if i < section - 1 else ('Y' if i == section - 1 else 'D')
        d.rectangle([cx, 27, cx + 8, 29], fill=wl.rgba('K'))
        d.rectangle([cx + 1, 27, cx + 7, 28], fill=wl.rgba(col))

    # top-right: score, embers, shards
    p = wl.panel(96, 34)
    img.alpha_composite(p, (SW - 100, 4))
    wl.draw_text(img, "SCORE", SW - 94, 9, color='H', shadow=False, outline=None)
    wl.draw_text(img, f"{score:06d}", SW - 9, 9, color='W', anchor='r')
    img.alpha_composite(icon(wl.ICON_EMBER), (SW - 94, 22))
    wl.draw_text(img, f"{embers}/{L.count('e')}", SW - 86, 22, color='A')
    for i in range(3):
        img.alpha_composite(icon(wl.ICON_SHARD if i < shards else wl.ICON_SHARD_EMPTY),
                            (SW - 42 + i * 11, 22))

    # bottom-left: GLOW meter (the risk/reward heart of the game)
    p = wl.panel(118, 30)
    img.alpha_composite(p, (4, SH - 34))
    wl.draw_text(img, "GLOW", 10, SH - 28, color='A')
    for i in range(5):
        x = 38 + i * 11
        lit = i < glow
        flame = ["..K..", ".KAK.", "KAYOK", "KOWOK", ".KRK."] if lit else \
                ["..K..", ".KDK.", "KDMDK", "KDDDK", ".KKK."]
        img.alpha_composite(wl.from_map(flame), (x, SH - 29))
    wl.draw_text(img, f"x{glow}", 96, SH - 28, color='Y')
    wl.draw_text(img, f"AT RISK {unbanked}", 10, SH - 18, color='R')
    wl.draw_text(img, "BANK IT!", 112, SH - 18, color='H', shadow=False, outline=None, anchor='r')

    # bottom-right: control hints
    hint = "< > MOVE   SPACE JUMP   ESC PAUSE"
    wl.draw_text(img, hint, SW - 6, SH - 12, color='H', anchor='r', shadow=False)


# --------------------------------------------------------------------- screens
def with_rows(mod_rows, fn):
    old = L.ROWS
    L.ROWS = mod_rows
    try:
        return fn()
    finally:
        L.ROWS = old


def remove_entities(cells):
    rows = [list(r) for r in L.ROWS]
    for x, y in cells:
        rows[y][x] = ' '
    return ["".join(r) for r in rows]


def gameplay_scene(frame=0):
    """Section 2 of the level: Pip on the high path at glow x3, with the moth coming close."""
    collected = [(31, 7), (34, 4)] + \
                [(x, y) for (c, x, y) in L.entities() if c == 'e' and x < 24]
    rows = remove_entities(collected)
    pip_x, pip_y = 36 * 16 + 2, 4 * 16
    run = wl.pip_anim('run')[frame % 4]

    def r():
        return L.render(24, 48, frame=frame, lit_sconces=(22,), player=(run, pip_x, pip_y),
                        moth_offsets={(38, 3): (-6, 6 + (frame % 2))})
    scene = with_rows(rows, r).crop((0, 8, SW, 8 + SH))
    px, py = pip_x - 24 * 16 + 8, pip_y - 8 + 6
    lights = [(px, py, 76, True)]
    for (c, x, y) in L.entities():
        if 24 <= x < 48 and (x, y) not in collected:
            cx, cy = (x - 24) * 16 + 8, y * 16 + 8 - 8
            if c == 'e': lights.append((cx, cy, 18, True))
            if c == 'b': lights.append((cx, cy, 22, True))
            if c == 'd': lights.append((cx, cy, 14, False))
            if c == 'M': lights.append((cx - 6, cy + 6, 16, False))
    for wx in L.WINDOWS:
        if 24 <= wx < 48:
            lights.append(((wx - 24) * 16 + 8, 3 * 16, 30, False))
            lights.append(((wx - 24) * 16 + 40, 9 * 16, 34, False))
    scene = lighting(scene, lights, base=165)
    # moth alert bubble
    mx, my = (38 - 24) * 16 - 6 + 8 + 14, 3 * 16 + 6 - 8 - 2
    d = ImageDraw.Draw(scene)
    d.rectangle([mx - 4, my - 6, mx + 4, my + 4], fill=wl.rgba('K'))
    d.rectangle([mx - 3, my - 5, mx + 3, my + 3], fill=wl.rgba('F'))
    d.line([mx, my - 4, mx, my], fill=wl.rgba('R'))
    d.point((mx, my + 2), fill=wl.rgba('R'))
    d.point((mx - 1, my + 5), fill=wl.rgba('K'))
    # aggro ring (glow-scaled detection radius visual cue)
    r = 3 * 16 + glow_radius(3)
    for a in range(0, 360, 9):
        import math
        x = px + r * math.cos(math.radians(a)); y = py + r * math.sin(math.radians(a))
        if 0 <= x < SW and 0 <= y < SH and (a // 9) % 2 == 0:
            scene.putpixel((int(x), int(y)), wl.rgba('A', 150))
    # ember pickup popup
    wl.draw_text(scene, "+40", px - 40, py - 4, color='Y')
    return scene


def glow_radius(glow):
    return glow * 8


def screen_gameplay(frame=0):
    img = gameplay_scene(frame)
    hud(img, hearts=2, wax=0.57, time="1:42", score=600, embers=10, shards=0, glow=3, unbanked=60)
    return img


def menu_background(frame=0):
    img = Image.new("RGBA", (SW, SH), wl.rgba('N'))
    bg = wl.tile_stone_bg()
    for y in range(0, SH, 16):
        for x in range(0, SW, 16):
            img.alpha_composite(bg, (x, y))
    veil(img, 'N', 110)
    # tall cathedral windows
    for wx in (40, 136, 232, 328):
        win = Image.new("RGBA", (16, 64), (0, 0, 0, 0))
        win.alpha_composite(wl.tile_window_top(), (0, 0))
        for k in range(1, 4):
            win.alpha_composite(wl.tile_window_bottom().crop((0, 0, 16, 12)), (0, k * 12 + 4))
        win.alpha_composite(wl.tile_window_bottom(), (0, 48))
        img.alpha_composite(wl.scale(win, 1), (wx, 22))
    shafts = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shafts)
    for wx in (40, 136, 232, 328):
        sd.polygon([(wx + 3, 40), (wx + 13, 40), (wx + 70, 200), (wx + 40, 200)],
                   fill=wl.rgba('F', 20))
    img.alpha_composite(shafts)
    # giant bell silhouette (right)
    big = wl.scale(wl.bell(False), 3)
    big_dark = wl.recolor(big, {'z': 'Z', 'Y': 'z', 'Z': 'b', 'n': 'b', 'l': 'n'})
    img.alpha_composite(big_dark, (302, -30))
    # chain from bell
    ch = wl.tile_chain()
    # floor ledge + water
    ledge_y = 160
    for x in range(0, 112, 16):
        img.alpha_composite(wl.tile_stone_top(), (x, ledge_y))
        img.alpha_composite(wl.tile_stone(), (x, ledge_y + 16))
        img.alpha_composite(wl.tile_stone(), (x, ledge_y + 32))
    for x in range(112, SW, 16):
        img.alpha_composite(wl.tile_water(frame % 2), (x, 180))
        img.alpha_composite(wl.tile_water(0, False), (x, 196))
        img.alpha_composite(wl.tile_water(0, False), (x, 212))
    for x in range(300, SW, 16):
        img.alpha_composite(wl.tile_stone_top(), (x, 172))
        img.alpha_composite(wl.tile_stone(), (x, 188))
        img.alpha_composite(wl.tile_stone(), (x, 204))
    img.alpha_composite(wl.sconce_frames()[1 + frame % 2], (88, ledge_y - 16))
    pip = wl.pip_anim('idle')[frame % 2]
    img.alpha_composite(pip, (52, ledge_y - 16))
    # floating embers (particles)
    for (x, y) in [(70, 120), (150, 140), (200, 90), (34, 100), (320, 150), (110, 70)]:
        img.alpha_composite(wl.ember_frames()[(x + frame) % 4], (x, y + (frame % 2)))
    mo = wl.moth_frames()[frame % 2]
    img.alpha_composite(mo, (248, 132))
    img.alpha_composite(wl.icicle_frames()[0], (180, 0))
    # bell reflection shimmer in water
    d = ImageDraw.Draw(img)
    for i, x in enumerate(range(270, 340, 6)):
        d.line([x, 186 + (i % 3) * 4, x + 3, 186 + (i % 3) * 4], fill=wl.rgba('z', 120))
    lights = [(60, ledge_y - 8, 80, True), (96, ledge_y - 12, 46, True)]
    lights += [(x + 8, y + 8, 16, True) for (x, y) in [(70, 120), (150, 140), (200, 90),
                                                      (34, 100), (320, 150), (110, 70)]]
    lights += [(wx + 8, 50, 40, False) for wx in (40, 136, 232, 328)]
    lights += [(300, 50, 60, False)]
    return lighting(img, lights, base=150)


def logo(img, cx, y):
    title = "WICKLIGHT"
    w = wl.draw_text(img, title, cx, y, sc=4, grad=('Y', 'O', 'W'), anchor='c')
    # Pip's flame dots the I
    x0 = cx - w // 2
    i_off = wl.text_width("W", 4) + 4
    fl = wl.from_map(wl.FLAME['idle0'][:7])
    img.alpha_composite(fl, (x0 + i_off + 6 - 8 + 2, y - 8))
    return w


def screen_menu(frame=0):
    img = menu_background(frame)
    logo(img, SW // 2, 22)
    sub = "-  THE DROWNED BELFRY  -"
    wl.draw_text(img, sub, SW // 2, 58, color='F', anchor='c')
    for i, lbl in enumerate(("PLAY", "SETTINGS", "EXIT")):
        b = wl.button(lbl, w=104, selected=(i == 0))
        img.alpha_composite(b, (SW // 2 - 52, 84 + i * 24))
    # selection cursor: tiny flame
    cur = wl.from_map(["..K..", ".KAK.", "KAYOK", "KOWOK", ".KRK."])
    img.alpha_composite(cur, (SW // 2 - 64, 89))
    img.alpha_composite(cur, (SW // 2 + 58, 89))
    wl.draw_text(img, "BEST 001980", 8, SH - 12, color='A')
    wl.draw_text(img, "A  NO RISK? NO REWARD!  GAME  -  V0.1", SW - 8, SH - 12, color='H',
                 anchor='r', shadow=False)
    return img


def screen_victory(frame=0):
    rows = remove_entities([(x, y) for (c, x, y) in L.entities() if c in 'eb' and x >= 72])
    pip = wl.pip_anim('jump')[0]
    sc = with_rows(rows, lambda: L.render(72, 96, frame=frame, lit_sconces=(22, 50, 73),
                                          player=(pip, 90 * 16, 4 * 16 - 4)))
    sc = sc.crop((0, 8, SW, 8 + SH))
    bell_r = wl.bell(True)
    sc.alpha_composite(bell_r, ((92 - 72) * 16, 4 * 16 - 8))
    sc = lighting(sc, [((92 - 72) * 16 + 16, 4 * 16 + 8, 140, True), (20, 160, 40, True)], base=120)
    veil(sc, 'K', 120)
    img = sc
    pw, ph = 236, 176
    px, py = SW // 2 - pw // 2, 20
    img.alpha_composite(wl.panel(pw, ph), (px, py))
    wl.draw_text(img, "THE BELL RINGS!", SW // 2, py + 10, sc=2, grad=('Y', 'z', 'W'), anchor='c')
    wl.draw_text(img, "LEVEL 1  THE DROWNED BELFRY  COMPLETE", SW // 2, py + 30, color='F',
                 anchor='c', shadow=False)
    d = ImageDraw.Draw(img)
    d.line([px + 10, py + 41, px + pw - 10, py + 41], fill=wl.rgba('D'))
    stats = [
        ("EMBERS BANKED", "21/24", "+1,470"),
        ("BELL SHARDS", "2/3", "+500"),
        ("WAX REMAINING", "0:48", "+240"),
        ("HITS TAKEN", "1", "+0"),
        ("TIME", "2:10", ""),
    ]
    for i, (k, v, pts) in enumerate(stats):
        yy = py + 47 + i * 11
        wl.draw_text(img, k, px + 14, yy, color='H', shadow=False)
        wl.draw_text(img, v, px + 150, yy, color='W', anchor='r', shadow=False)
        wl.draw_text(img, pts, px + pw - 14, yy, color='A', anchor='r', shadow=False)
    for i in range(3):
        img.alpha_composite(icon(wl.ICON_SHARD if i < 2 else wl.ICON_SHARD_EMPTY),
                            (px + 102 + i * 9, py + 58))
    yy = py + 104
    d.line([px + 10, yy - 3, px + pw - 10, yy - 3], fill=wl.rgba('D'))
    wl.draw_text(img, "FINAL SCORE", px + 14, yy + 3, color='Y')
    wl.draw_text(img, "002210", px + pw - 14, yy, sc=2, grad=('W', 'Y'), anchor='r')
    wl.draw_text(img, "RANK", px + 14, yy + 18, color='H', shadow=False)
    wl.draw_text(img, "BLAZE", px + 44, yy + 18, color='O')
    for i in range(5):
        lit = i < 4
        fl = ["..K..", ".KAK.", "KAYOK", "KOWOK", ".KRK."] if lit else \
             ["..K..", ".KDK.", "KDMDK", "KDDDK", ".KKK."]
        img.alpha_composite(wl.from_map(fl), (px + 80 + i * 8, yy + 18))
    wl.draw_text(img, "NEW BEST!", px + pw - 14, yy + 18, color='G', anchor='r')
    wl.draw_text(img, "MISSED: BELL SHARD 3 - BELL CLIMB", SW // 2, yy + 32, color='H', anchor='c', shadow=False)
    img.alpha_composite(wl.button("REPLAY", w=100, selected=True), (px + 12, py + ph - 26))
    img.alpha_composite(wl.button("MAIN MENU", w=100), (px + pw - 112, py + ph - 26))
    return img


def screen_gameover(frame=0):
    pip = wl.pip_anim('hurt')[0]
    sc = L.render(48, 72, frame=frame, lit_sconces=(22, 50), player=(pip, 63 * 16, 8 * 16 - 2),
                  moth_offsets={(67, 5): (-30, 22)})
    sc = sc.crop((0, 8, SW, 8 + SH))
    sc = frost_grade(sc)
    sc = lighting(sc, [((63 - 48) * 16 + 8, 8 * 16 - 6, 40, False)], base=170, cold=True)
    veil(sc, 'K', 110)
    img = sc
    # smoke wisps rising from Pip
    d = ImageDraw.Draw(img)
    for i, (dx, dy) in enumerate([(0, -10), (2, -14), (-1, -18), (1, -22), (3, -26)]):
        img.putpixel(((63 - 48) * 16 + 8 + dx, 8 * 16 - 8 + dy), wl.rgba('H', 200 - i * 30))
    pw, ph = 236, 176
    px, py = SW // 2 - pw // 2, 20
    img.alpha_composite(wl.panel(pw, ph, 'frost'), (px, py))
    wl.draw_text(img, "YOUR FLAME", SW // 2, py + 9, sc=2, grad=('F', 'I', 'W'), anchor='c')
    wl.draw_text(img, "WENT OUT", SW // 2, py + 27, sc=2, grad=('F', 'I', 'W'), anchor='c')
    wl.draw_text(img, "CAUSE: FROST MOTH  -  NO LIVES LEFT", SW // 2, py + 46, color='H',
                 anchor='c', shadow=False)
    # progress bar toward the bell
    bx, by, bw = px + 16, py + 70, pw - 32
    wl.draw_text(img, "PROGRESS TO THE BELL", bx, by - 9, color='F', shadow=False)
    wl.draw_text(img, "62%", bx + bw, by - 9, color='W', anchor='r', shadow=False)
    d.rectangle([bx, by, bx + bw, by + 7], fill=wl.rgba('K'))
    d.rectangle([bx + 1, by + 1, bx + 1 + int((bw - 2) * 0.62), by + 6], fill=wl.rgba('I'))
    d.line([bx + 1, by + 1, bx + int((bw - 2) * 0.62), by + 1], fill=wl.rgba('F'))
    for i in range(1, 4):
        x = bx + int(bw * i / 4)
        d.line([x, by - 1, x, by + 8], fill=wl.rgba('N'))
    small_bell = wl.bell().resize((10, 10), Image.NEAREST)
    img.alpha_composite(small_bell, (bx + bw - 4, by + 9))
    marker = wl.pip_anim('hurt')[0].crop((4, 0, 12, 16)).resize((4, 8), Image.NEAREST)
    img.alpha_composite(marker, (bx + int((bw - 2) * 0.62) - 2, by + 9))
    rows = [("SCORE (BANKED)", "001140"), ("EMBERS LOST", "6"), ("BELL SHARDS", "1/3"),
            ("REACHED", "SECTION 3")]
    for i, (k, v) in enumerate(rows):
        yy = py + 92 + i * 11
        wl.draw_text(img, k, px + 16, yy, color='H', shadow=False)
        wl.draw_text(img, v, px + pw - 16, yy, color='W' if i else 'F', anchor='r', shadow=False)
    wl.draw_text(img, "TIP: LIGHT A SCONCE TO BANK YOUR GLOW", SW // 2, py + 139, color='A',
                 anchor='c', shadow=False)
    img.alpha_composite(wl.button("RETRY", w=100, selected=True), (px + 12, py + ph - 24))
    img.alpha_composite(wl.button("MAIN MENU", w=100), (px + pw - 112, py + ph - 24))
    return img


def screen_settings(frame=0):
    img = menu_background(frame)
    veil(img, 'K', 120)
    pw, ph = 220, 172
    px, py = SW // 2 - pw // 2, 22
    img.alpha_composite(wl.panel(pw, ph), (px, py))
    wl.draw_text(img, "SETTINGS", SW // 2, py + 9, sc=2, grad=('Y', 'O'), anchor='c')
    d = ImageDraw.Draw(img)
    opts = [("MUSIC", 0.7), ("SOUND FX", 0.85), ("SCREEN SHAKE", 0.4)]
    for i, (k, v) in enumerate(opts):
        yy = py + 34 + i * 16
        wl.draw_text(img, k, px + 14, yy, color='C' if i else 'Y')
        bx = px + 110
        for s in range(10):
            on = s < int(v * 10)
            d.rectangle([bx + s * 9, yy, bx + s * 9 + 6, yy + 6], fill=wl.rgba('K'))
            d.rectangle([bx + s * 9 + 1, yy + 1, bx + s * 9 + 5, yy + 5],
                        fill=wl.rgba('A' if on else 'D'))
    toggles = [("FULLSCREEN", "ON"), ("PIXEL PERFECT", "ON"), ("ASSIST: SLOW WAX", "OFF")]
    for i, (k, v) in enumerate(toggles):
        yy = py + 84 + i * 13
        wl.draw_text(img, k, px + 14, yy, color='C')
        wl.draw_text(img, "< " + v + " >", px + pw - 14, yy, color='G' if v == 'ON' else 'R',
                     anchor='r')
    wl.draw_text(img, "CONTROLS: A/D OR < > MOVE   SPACE JUMP", SW // 2, py + 128, color='H',
                 anchor='c', shadow=False)
    img.alpha_composite(wl.button("BACK", w=80, selected=True), (SW // 2 - 40, py + ph - 26))
    return img


SCREENS = [("01_main_menu", screen_menu), ("02_gameplay", screen_gameplay),
           ("03_victory", screen_victory), ("04_game_over", screen_gameover),
           ("05_settings_bonus", screen_settings)]


def flow_diagram():
    import math
    th = {n: f(0) for n, f in SCREENS[:4]}
    tw, thh = 192, 108
    W, H = 800, 430
    im = Image.new("RGBA", (W, H), wl.rgba('N'))
    wl.draw_text(im, "SCREEN FLOW  /  PROTOTYPE NAVIGATION", W // 2, 6, sc=2, grad=('Y', 'O'),
                 anchor='c')
    pos = {"01_main_menu": (24, 160), "02_gameplay": (304, 160),
           "03_victory": (584, 52), "04_game_over": (584, 268)}
    labels = {"01_main_menu": "1  MAIN MENU", "02_gameplay": "2  GAMEPLAY",
              "03_victory": "3  VICTORY", "04_game_over": "4  GAME OVER"}
    d = ImageDraw.Draw(im)
    for n, (x, y) in pos.items():
        t = th[n].resize((tw, thh), Image.LANCZOS)
        d.rectangle([x - 2, y - 2, x + tw + 1, y + thh + 1], fill=wl.rgba('K'))
        d.rectangle([x - 1, y - 1, x + tw, y + thh], fill=wl.rgba('L'))
        im.alpha_composite(t, (x, y))
        wl.draw_text(im, labels[n], x + tw // 2, y + thh + 5, color='Y', anchor='c')

    def arrow(pts, label, col='A', lpos=None):
        d.line(pts, fill=wl.rgba('K'), width=4, joint="curve")
        d.line(pts, fill=wl.rgba(col), width=2, joint="curve")
        a, b = pts[-2], pts[-1]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        p1 = (b[0] - 8 * math.cos(ang - 0.5), b[1] - 8 * math.sin(ang - 0.5))
        p2 = (b[0] - 8 * math.cos(ang + 0.5), b[1] - 8 * math.sin(ang + 0.5))
        d.polygon([b, p1, p2], fill=wl.rgba(col), outline=wl.rgba('K'))
        if label:
            lx, ly = lpos
            wl.draw_text(im, label, lx, ly, color=col, anchor='c')
    mmx, mmy = pos["01_main_menu"]; gpx, gpy = pos["02_gameplay"]
    vx, vy = pos["03_victory"]; gox, goy = pos["04_game_over"]
    arrow([(mmx + tw + 6, mmy + 40), (gpx - 6, gpy + 40)], "PLAY", 'A', ((mmx + tw + gpx) // 2, mmy + 28))
    arrow([(gpx - 6, gpy + 70), (mmx + tw + 6, mmy + 70)], "ESC > QUIT", 'H', ((mmx + tw + gpx) // 2, mmy + 76))
    arrow([(gpx + tw + 6, gpy + 22), (vx - 6, vy + 70)], "RING BELL", 'Y', (vx - 40, vy + 52))
    arrow([(vx - 6, vy + 92), (gpx + tw + 6, gpy + 40)], "REPLAY", 'A', (gpx + tw + 50, gpy + 54))
    arrow([(gpx + tw + 6, gpy + 86), (gox - 6, goy + 38)], "0 LIVES OR 0 WAX", 'I', (gpx + tw + 42, goy + 70))
    arrow([(gox - 6, goy + 16), (gpx + tw + 6, gpy + 68)], "RETRY", 'A', (gox - 24, goy - 24))
    arrow([(vx + tw // 2, vy - 6), (vx + tw // 2, 36), (mmx + tw // 2, 36), (mmx + tw // 2, mmy - 6)],
          "MAIN MENU", 'H', (W // 2 - 60, 40))
    arrow([(gox + tw // 2, goy + thh + 18), (gox + tw // 2, H - 14), (mmx + tw // 2, H - 14),
           (mmx + tw // 2, mmy + thh + 18)], "MAIN MENU", 'H', (W // 2 - 60, H - 26))
    wl.draw_text(im, "SETTINGS: MAIN MENU > SETTINGS > BACK", mmx + tw // 2 + 8, mmy + thh + 24, color='H',
                 shadow=False)
    wl.scale(im, 2).save(os.path.join(OUT, "screen_flow_diagram.png"))


def main():
    os.makedirs(os.path.join(OUT, "screens"), exist_ok=True)
    pimg = os.path.join(OUT, "prototype", "img")
    os.makedirs(pimg, exist_ok=True)
    for name, fn in SCREENS:
        img = fn(0)
        wl.scale(img, SCALE).save(os.path.join(OUT, "screens", f"{name}_1920x1080.png"))
        frames = [fn(f) for f in range(4)]
        for i, fr in enumerate(frames):
            fr.save(os.path.join(pimg, f"{name}_f{i}.png"))
    for lbl, w in (("PLAY", 104), ("SETTINGS", 104), ("EXIT", 104), ("BACK", 80),
                   ("REPLAY", 100), ("RETRY", 100), ("MAIN MENU", 100)):
        wl.button(lbl, w=w, selected=True).save(
            os.path.join(pimg, f"btn_{lbl.lower().replace(' ', '_')}_hover.png"))
    flow_diagram()


if __name__ == "__main__":
    main()
